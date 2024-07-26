import cv2
from ultralytics import YOLO
import os
from control import tools
from control.run_ocr import OcrReader
import numpy as np
import pandas as pd
import settings
from module.generic import CustomBaseClass
from huggingface_hub import hf_hub_download


# class definition:



class DetectorMosaic(CustomBaseClass):

    tag = '모자이크'
    
    def __init__(self, multiMode = False) -> None:
        super().__init__(multiMode=False)
        # GPU 사용하는 YOLO 모델 불러오기
        self.thr = 1    # 욜로에서는 임계값, 이벤트에서는 영상 차이
        model_base = os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt')
        model_nbp = os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')
        model_face = os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')
        # AI 모델 생성
        self.model = YOLO(model_base)
        self.model_nbp = YOLO(model_nbp)
        self.model_face = YOLO(model_face)

        
    def change_model(self, text):
        ''' 모델을 변경하는 함수 '''
        print('현재 생성된 객체를 제거 하고 초기화 함  \n구현예정')
        return 
    

    ##############
    ## 슬롯함수 ##
    ##############
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(self, frame, thr):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img, thr

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        detections = self.model.track(frame, persist=True)[0]
        text = ''
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            _cap_number = 0
            _xmin, _ymin, _xmax, _ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            xmin, ymin, xmax, ymax = tools.to_original_shape(frame.shape, frame.shape, _xmin, _ymin, _xmax, _ymax) # 원본
            try:
                _track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if _label_number not in [0,2,3,5,7,9]:
                continue
            # 임계값 이하는 생략 하라는 코드
            if _confidence < thr/100:
                continue
            detected_img = frame[ymin:ymax, xmin:xmax]  # <== 오토바이 이미지
            if not _label_number == 0:
                img = self.detect_nbp_mosaic(detected_img)
            if _label_number == 0:
                img = self.detect_face_mosaic(detected_img) 
            # 모자이크 처리 원본에 삽입
            if img is not None:
                frame[ymin:ymax, xmin:xmax] = img
        return frame, text
    
        
    def detect_move(self, roi_img, region_status, thr):
        '''
        모자이크 모드에서는 사용하지 않음                    
        '''
        return roi_img, True, thr


    def detect_nbp_mosaic(self, bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        mosaic_img = None
        detection = self.model_nbp(bike_img)[0]
        # 번호판 검출
        for data_nbp in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_nbp[0]), int(data_nbp[1]), int(data_nbp[2]), int(data_nbp[3])
            try:
                confidence_nbp, label = float(data_nbp[4]), int(data_nbp[5])
            except IndexError:
                continue
            if label != 1:
                continue
            mosaic_img = tools.mosaic(bike_img, xmin, ymin, xmax, ymax, ratio=0.01)
        return mosaic_img
    

    def detect_face_mosaic(self, face_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        mosaic_img = None
        detection = self.model_face(face_img)[0]
        # 번호판 검출
        for data_face in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_face[0]), int(data_face[1]), int(data_face[2]), int(data_face[3])
            try:
                confidence_, label = float(data_face[4]), int(data_face[5])
            except IndexError:
                continue
            # if label != 1:
            #     continue
            mosaic_img = tools.mosaic(face_img, xmin, ymin, xmax, ymax, ratio=0.01)
        return mosaic_img

    def reorderPts(self, pts):
        idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
        pts = pts[idx]  # x좌표로 정렬
        if pts[0, 1] > pts[1, 1]:
            pts[[0, 1]] = pts[[1, 0]]
        if pts[2, 1] < pts[3, 1]:
            pts[[2, 3]] = pts[[3, 2]]
        return pts



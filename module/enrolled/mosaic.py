import cv2
from ultralytics import YOLO
import os
from control import tools
from control.run_ocr import OcrReader
import numpy as np
import pandas as pd
import settings
from module.modelLoader import ModelClass
from module.sharedData import DT
from huggingface_hub import hf_hub_download


 
# class definition:
class DetectorMosaic():

    tag = '모자이크_얼굴_번호판만'
    slider_dict = {
        '민감도':1,
        '모자이크':5,
        }
        # GPU 사용하는 YOLO 모델 불러오기
    models = {
        'model': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt')),
        'model_nbp':  YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 DT.models 로 전달함
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']
    btn_names = ['시작', '끝', '분석', '추가(프레임)', '추가(전체)', '작업시작']
    
    def setup(): 
        # 슬라이더 설정
        DT.clear()
        DT.setSliderValue(DetectorMosaic.tag, DetectorMosaic.slider_dict)
        DT.setDf(columns = DetectorMosaic.columns)
 

    ##############
    ## 슬롯함수 ##
    ##############
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img, thr

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        text = ''
        try:
            detections = DetectorMosaic.models['model'].track(frame, persist=True)[0]
        except Exception as e:
            print(e)
            # 욜로 트래커 초기화
            DetectorMosaic.models['model'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt'))
            detections = DetectorMosaic.models['model'].track(frame, persist=True)[0]
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            _cap_number = 0
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            # xmin, ymin, xmax, ymax = tools.to_original_shape(frame.shape, frame.shape, _xmin, _ymin, _xmax, _ymax) # 원본
            try:
                _track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if _label_number not in [0,2,3,5,7,9]:
                continue
            # 임계값 이하는 생략 하라는 코드
            yolo_thr = DT.sliderDict[DetectorMosaic.tag]['민감도']
            if _confidence < yolo_thr/100:
                continue
            detected_img = frame[ymin:ymax, xmin:xmax]  # <== 오토바이 이미지
            if not _label_number == 0:
                img = DetectorMosaic.detect_nbp_mosaic(detected_img)
            if _label_number == 0:
                # 사람 모자이크 
                # img = tools.mosaic(detected_img, 0, 0, detected_img.shape[1], detected_img.shape[0], ratio=0.01)
                img = DetectorMosaic.detect_face_mosaic(detected_img)  # 얼굴만 모자이크
            # 모자이크 처리 원크본에 삽입
            if img is not None:
                frame[ymin:ymax, xmin:xmax] = img
        return frame, text
    
        
    def detect_move(roi_img):
        '''
        모자이크 모드에서는 사용하지 않음                    
        '''
        return roi_img, True


    def detect_nbp_mosaic(bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        mosaic_img = None
        detection = DetectorMosaic.models['model_nbp'](bike_img)[0]
        ratio = DT.sliderDict[DetectorMosaic.tag]['모자이크']/600
        # 번호판 검출
        for data_nbp in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_nbp[0]), int(data_nbp[1]), int(data_nbp[2]), int(data_nbp[3])
            try:
                confidence_nbp, label = float(data_nbp[4]), int(data_nbp[5])
            except IndexError:
                continue
            if label != 1:
                continue
            mosaic_img = tools.mosaic(bike_img, xmin, ymin, xmax, ymax, ratio=ratio)
        return mosaic_img
    

    def detect_face_mosaic(face_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        mosaic_img = None
        ratio = DT.sliderDict[DetectorMosaic.tag]['모자이크']/600
        detection = DetectorMosaic.models['model_face'](face_img)[0]
        # 번호판 검출
        for data_face in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_face[0]), int(data_face[1]), int(data_face[2]), int(data_face[3])
            try:
                confidence_, label = float(data_face[4]), int(data_face[5])
            except IndexError:
                continue
            # if label != 1:
            #     continue
            mosaic_img = tools.mosaic(face_img, xmin, ymin, xmax, ymax, ratio=ratio)
        return mosaic_img

    def reorderPts(pts):
        idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
        pts = pts[idx]  # x좌표로 정렬
        if pts[0, 1] > pts[1, 1]:
            pts[[0, 1]] = pts[[1, 0]]
        if pts[2, 1] < pts[3, 1]:
            pts[[2, 3]] = pts[[3, 2]]
        return pts


    #####################
    ## 커스텀 버튼 함수 ##
    #####################

    def btn1():
        print('btn1')

    def btn2():
        print('btn2')

    def btn3():
        print('btn3')

    def btn4():
        print('btn4')

    def btn5():
        print('btn5')

    def btn6():
        print('btn6')

    btns = [btn1, btn2, btn3, btn4, btn5, btn6]
    


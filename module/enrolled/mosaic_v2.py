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



# ToDo
# 1. 분석 시작점, 끝점 버튼과 라벨 추가
#   - 시작점 cap.get(cv2.CAP_PROP_POS_FRAMES) 으로 프레임 설정후 레코딩 시작
#   - 끝점 반복 조건문(if cap_num == 끝점)으로 레코딩 종료
# 2. 프레임별 모자이크 추가 버튼 및 기능
#   - 모자이크 추가 버튼 클릭시, 프레임별로 모자이크 추가 df = {'cap_num': cap_num, 'a': a, 'b': b}
# 3. 판다스로 데이터 저장


class DetectorMosaic_v2:

    tag = '모자이크'
    arg_dict = {
        '민감도':1,
        '가림정도':10,
        }
    models = {
        'model': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8s.pt')),
        'model_nbp':  YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 DT.models 로 전달함
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']
    

    def setup():
        # 슬라이더 설정
        DT.clear()
        DT.setValue(DetectorMosaic_v2.tag, DetectorMosaic_v2.arg_dict)
        DT.setDf(columns = DetectorMosaic_v2.columns)


    #######################
    ## 슬롯함수 오버라이드 ##
    ######################## 
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num):
        '''화
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        text = ''
        try:
            detections = DetectorMosaic_v2.models['model'].track(frame, persist=True)[0]
        except Exception as e:
            print(e)
            # 욜로 트래커 초기화
            DetectorMosaic_v2.models['model'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt'))
            detections = DetectorMosaic_v2.models['model'].track(frame, persist=True)[0]
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            _cap_number = 0
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            
            try:
                track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if _label_number not in [0,2,3,5,7,9]:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = DT.getValue(DetectorMosaic_v2.tag, '민감도')
            if _confidence < thr/100:
                continue
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
            cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
            # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가
            if DT.play_status:
                # xmin, ymin, xmax, ymax의 값은 roi_img의 상대좌표인데, 이를 전체 이미지에서의 상대좌표로 변환(전체 이미지 shape은 DT.img.shape)
                xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
                # df, temp_df 정리
                DT.df_temp = pd.concat([DT.df_temp, pd.DataFrame([[track_id, cap_num, xmin, ymin, xmax, ymax]], columns=DT.df.columns)], ignore_index=True)
                result_df = DT.df_temp.loc[DT.df_temp.groupby('객체ID')['프레임번호'].idxmin()]
                DT.mosaic_df(result_df)
        return frame, text

        #     # 검출된 객체 모자이크 정보 df 저장
        #     detected_img = frame[ymin:ymax, xmin:xmax]  
        #     ratio = DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600
        #     img = tools.mosaic(detected_img, xmin, ymin, xmax, ymax, ratio=ratio, full=True)

        #     # 모자이크 처리 원본에 삽입
        #     if img is not None:
        #         frame[ymin:ymax, xmin:xmax] = img
        # return frame, text
    
    def drop(index, inplace=True):
        DT.applyDrop(index, inplace=True)   


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
        detection = DetectorMosaic_v2.models['model_nbp'](bike_img)[0]
        ratio = DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600
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
        detection = DetectorMosaic_v2.models['model_face'](face_img)[0]
        ratio = DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600
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


    def detlete_tableview_row():
        pass
import cv2
import os
import numpy as np
import pandas as pd
from ultralytics import YOLO
from control import tools
from control.run_ocr import OcrReader
from module.modelLoader import ModelClass
from module import generic 
# from module.generic import CustomBaseClass
from module.sharedData import DT
import settings


# class definition:



class DetectorBike():

    tag = '이륜차_번호판_감지'
    slider_dict = {
        '감지_민감도':1,
        }
    models = {
        'base': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8s.pt')),
        'model_nbp': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'reader': OcrReader(),
    }
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']
    btn_names = ['btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5', 'btn_6']
    
    img_path = os.path.join(settings.BASE_DIR, 'rsc/init.jpg')
    df = pd.DataFrame({'si':[], 'giho':[], 'num':[]})
    track_ids = {}
    
    def setup(): 
        # 슬라이더 설정
        DT.clear()
        DT.setSliderValue(DetectorBike.tag, DetectorBike.slider_dict)
        DT.setDf(columns = DetectorBike.columns)
    
 
    ##############
    ## 슬롯함수 ##
    ##############
    
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        # 이미지에 디텍션값을 넣으면 roi가 되는 함수를 만들어야 됨
        # 함수명은 detct_make_roiimg
        text = ''
        try:
            detections = DetectorBike.models['base'].track(frame, persist=True)[0]
        except:
            DetectorBike.models['base'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8n.pt'))
            detections = DetectorBike.models['base'].track(frame, persist=True)[0]
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            xmin, ymin, xmax, ymax  = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            try:
                track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 오토바이만 검출하도록 함
            if _label_number != 3:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = DT.sliderDict[DetectorBike.tag]['감지_민감도'] 
            if _confidence < thr/100:
                continue
            # 프레임의 절대좌표 => 상대좌표 => 오리지날 이미지의 절대좌표
            xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
            xmin, ymin, xmax, ymax = tools.rel_to_abs(DT.img.shape, xmin, ymin, xmax, ymax)
            bike_img = DT.img[ymin:ymax, xmin:xmax]
            # 번호판 이미지 검출
            nbp_img = DetectorBike.detect_nbp_img(bike_img)
            # 휘어진 번호판 이미지 처리
            try:
                nbp_img = DetectorBike.nbp_transform(nbp_img)
            except:
                return frame, None
            # ocr 처리
            if nbp_img is not None:
                si, giho, num = DetectorBike.models['reader'].read(nbp_img)
                _df = pd.DataFrame({'si':[si], 'giho':[giho], 'num':[num]})
                DetectorBike.df = pd.concat([DetectorBike.df, _df], ignore_index=True)
                frame[0:nbp_img.shape[0], 0:nbp_img.shape[1]] = nbp_img
        try:
            s = DetectorBike.df['si'].value_counts().idxmax()
            g = DetectorBike.df['giho'].value_counts().idxmax()
            n = DetectorBike.df['num'].value_counts().idxmax()
            text = f'{s} {g} {n}'  # 누적 인식
        except:
            pass
        return frame, text
        


    def detect_nbp_img(bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        roi_img = None
        detection = DetectorBike.models['model_nbp'](bike_img)[0]
        # 번호판 검출
        for data_nbp in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_nbp[0]), int(data_nbp[1]), int(data_nbp[2]), int(data_nbp[3])
            try:
                confidence_nbp, label = float(data_nbp[4]), int(data_nbp[5])
            except IndexError:
                continue
            if label != 1:
                continue
            roi_img = bike_img[ymin:ymax, xmin:xmax]
            return roi_img
    

    def nbp_transform(frame):
        img = frame.copy()
        # 출력 영상 설정
        dw, dh = 300, 150
        srcQuad = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32)
        dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)
        dst = np.zeros((dh, dw), np.uint8)
        frame = cv2.GaussianBlur(frame, (3,3), 7)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 외곽선 검출 및 명함 검출
        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for pts in contours:
            # 너무 작은 객체는 제외
            if cv2.contourArea(pts) < 10:
                continue
            # 외곽선 근사화
            approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.05, True)
            # 컨벡스가 아니면 제외
            if not cv2.isContourConvex(approx) or len(approx) != 4:
                continue
            # cv2.polylines(frame, [approx], True, (0, 255, 0), 2, cv2.LINE_AA)
            srcQuad = DetectorBike.reorderPts(approx.reshape(4, 2).astype(np.float32))
            pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
            dst = cv2.warpPerspective(img, pers, (dw, dh), flags=cv2.INTER_CUBIC)
        return dst
    

    def reorderPts(pts):
        idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
        pts = pts[idx]  # x좌표로 정렬
        if pts[0, 1] > pts[1, 1]:
            pts[[0, 1]] = pts[[1, 0]]
        if pts[2, 1] < pts[3, 1]:
            pts[[2, 3]] = pts[[3, 2]]
        return pts


    def detect_move(roi_img):
        '''
        바이크 탐지에서는 사용하지 않음   
        return 값의 3번째는 True로 주어야 메인윈도우메니저의 무브 디텍트에서 안잡힘                 
        '''
        return roi_img, True


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
    
    
    

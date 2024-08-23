import cv2
import os
import numpy as np
import pandas as pd
from ultralytics import YOLO
from control import tools
from control.run_ocr import OcrReader
from views import generic 
# from module.generic import CustomBaseClass
from views.sharedData import DT
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from rsc.ui.bike_ui import Ui_Bike



class Bike(Ui_Bike, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 시그널 슬롯 연결
        self.pushButton_4.clicked.connect(self.btn4)
        self.pushButton_5.clicked.connect(self.btn5)
        self.pushButton_6.clicked.connect(self.btn6)
        self.pushButton_1.clicked.connect(self.btn1)
        self.pushButton_2.clicked.connect(self.btn2)
        self.pushButton_3.clicked.connect(self.btn3)
        
    def btn4(self):
        print('slot_pushButton_4')

    def btn5(self):
        print('slot_pushButton_5')

    def btn6(self):
        print('slot_pushButton_6')

    def btn1(self):
        print('slot_pushButton_1')

    def btn2(self):
        print('slot_pushButton_2')
        
    def btn3(self):
        print('slot_pushButton_3')

    def program_exit(self):
        print('Ui_Bike 프로그램 종료')

    def applyImageProcessing(self, img):
        '''bike 모드에서는 아직 미확정'''
        print('bike 이미지 처리')
        return img



class DetectorBike(QObject):

    tag = 'bike'
    slider_dict = {
        '감지_민감도':1,
        }
    models = {
        'base': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8n.pt')),
        'model_nbp': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'reader': OcrReader(),
    }
    btn_names = ['btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5', 'btn_6']
    
    # 시그널
    reset = Signal()
    signal_1 = Signal(int)
    signal_2 = Signal(int)
    signal_3 = Signal()
    signal_4 = Signal()
    signal_5 = Signal()
    signal_6 = Signal()

    # 변수
    img_path = os.path.join(DT.BASE_DIR, 'rsc/init.jpg')
    df = pd.DataFrame({'si':[], 'giho':[], 'num':[]})
    track_ids = {}
 
    ##############
    ## 슬롯함수 ##
    ##############
    
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num, realsize_bool):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        text = ''
        try:
            detections = DetectorBike.models['base'].track(frame, persist=True, device=DT.device)[0]
        except:
            DetectorBike.models['base'] = YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8n.pt'))
            detections = DetectorBike.models['base'].track(frame, persist=True, device=DT.device)[0]
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            xmin, ymin, xmax, ymax  = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            try:
                track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 오토바이(3), 신호등(9)만 검출하도록 함
            if label not in [3, 9]:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = DT.sliderDict[DetectorBike.tag]['감지_민감도'] 
            if confidence < thr/100:
                continue

            xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
            if DT.play_status:
                DT.detection_add(DT.cap_num, track_id, label, xmin, ymin, xmax, ymax, confidence)
            xmin, ymin, xmax, ymax = tools.rel_to_abs(DT.img.shape, xmin, ymin, xmax, ymax)
            # 번호판 이미지 검출
            # 프레임의 절대좌표 => 상대좌표 => 오리지날 이미지의 절대좌표
            if label == 9:
                # 신호등 처리
                signal_light_img = DT.img[ymin:ymax, xmin:xmax]
                # frame의 6/10 위치에 신호등 이미지 삽입
                x = int(frame.shape[0]/10*6)
                frame[x:x+signal_light_img.shape[0], 0:signal_light_img.shape[1]] = signal_light_img
            if label == 3:
                # 오토바이 처리
                bike_img = DT.img[ymin:ymax, xmin:xmax]
                nbp_img = DetectorBike.detect_nbp_img(bike_img)
                # 휘어진 번호판 이미지 처리
                try:
                    nbp_img = DetectorBike.nbp_transform(nbp_img)
                except:
                    return frame, None
                # ocr
                if nbp_img is not None:
                    si, giho, num = DetectorBike.models['reader'].read(nbp_img)
                    text = f'{si} {giho} {num}'
                    _df = pd.DataFrame({'si':[si], 'giho':[giho], 'num':[num]})
                    DetectorBike.df = pd.concat([DetectorBike.df, _df], ignore_index=True)
                    frame[0:nbp_img.shape[0], 0:nbp_img.shape[1]] = nbp_img
        try:
            DT.bike_si = DetectorBike.df['si'].value_counts().idxmax()
            DT.bike_giho = DetectorBike.df['giho'].value_counts().idxmax()
            DT.bike_num = int(DetectorBike.df['num'].value_counts().idxmax())

        except:
            pass
        return frame, ''
        


    def detect_nbp_img(bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        if bike_img is None or bike_img.shape[0] == 0 or bike_img.shape[1] == 0:
            print(bike_img.shape)
            return
        roi_img = None
        detection = DetectorBike.models['model_nbp'](bike_img, device=DT.device)[0]
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

    def plot_df_to_img(img, cap_num):
        img = img.copy()
        df = DT.df
        cap_num = int(cap_num)
        df = df[df['frame']== cap_num]
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
            img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            img = cv2.putText(img, f'{row["ID"]}', (xmin, ymin-5), cv2.FONT_ITALIC, 1, (255,255,255), 2)
        return img

    def detect_move(roi_img):
        '''
        바이크 탐지에서는 사용하지 않음   
        return 값의 3번째는 True로 주어야 메인윈도우메니저의 무브 디텍트에서 안잡힘                 
        '''
        return roi_img, True
    
    def make_plot_df():
        DT.df_plot = DT.df.copy()

    @classmethod
    def reset_df(cls):
        cls.df = pd.DataFrame({'si':[], 'giho':[], 'num':[]})


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
    
    
    

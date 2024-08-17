import cv2
from ultralytics import YOLO
import os
from control import tools
from control.run_ocr import OcrReader
import numpy as np
import pandas as pd
from module.modelLoader import ModelClass
from module.sharedData import DT
from PySide6.QtCore import Signal   
from PySide6.QtCore import QObject
import time


# ToDo
# 1. 분석 시작점, 끝점 버튼과 라벨 추가
#   - 시작점 cap.get(cv2.CAP_PROP_POS_FRAMES) 으로 프레임 설정후 레코딩 시작
#   - 끝점 반복 조건문(if cap_num == 끝점)으로 레코딩 종료
# 2. 프레임별 모자이크 추가 버튼 및 기능
#   - 모자이크 추가 버튼 클릭시, 프레임별로 모자이크 추가 df = {'cap_num': cap_num, 'a': a, 'b': b}
# 3. 판다스로 데이터 저장


class DetectorMosaic_v2(QObject):

    tag = '모자이크'
    slider_dict = {
        '민감도':1,
        '가림정도':10,
        }
    models = {
        'model': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8m.pt')),
        'model_nbp':  YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 DT.models 로 전달함
    # 커스텀 버튼 설정
    btn_names = ['시작', '끝', '분석', '프레임 추가', '전체 추가', '모자이크']

    # 시그널
    reset = Signal()
    signal_1 = Signal(int)
    signal_2 = Signal(int)
    signal_3 = Signal()
    signal_4 = Signal()
    signal_5 = Signal()
    signal_6 = Signal()

 
    def __init__(self):
        super().__init__()
        self.make_btn_list()


    def setup():
        '''
        모델이 초기화 될 때 실행되는 함수
        '''
        # 슬라이더 설정
        DT.clear()
        DT.setSliderValue(DetectorMosaic_v2.tag, DetectorMosaic_v2.slider_dict)
        DT.dfReset()
    #######################
    ## 슬롯함수 오버라이드 ##
    ######################## 
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num, realsize_bool):
        '''
        모자이크에서는 플레이로 사용하고
        모자이크 처리 함수는 별도(self.mosaic_frame_list)로 사용함
        ''' 
        text = ''
        return frame, text

 

    def drop(index, inplace=True):
        DT.applyDrop(index, inplace=True)   


    def detect_move(roi_img):
        '''
        모자이크 모드에서는 사용하지 않음                    
        '''
        return roi_img, True
    
    def plot_df_to_img(img, cap_num):
        img = img.copy()
        df = DT.df
        cap_num = int(cap_num)
        df = df[df['frame']== cap_num]
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
            img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600)
            img = cv2.putText(img, f'{row["ID"]}', (xmin, ymin-5), cv2.FONT_ITALIC, 1, (255,255,255), 2)
        return img
    
    def plot_df_to_mosaic(img, cap_num):
        img = img.copy()
        df = DT.df
        cap_num = int(cap_num)
        df = df[df['frame']== cap_num]
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
            img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600)
        return img


    def detect_nbp_mosaic(bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        mosaic_img = None
        detection = DetectorMosaic_v2.models['model_nbp'](bike_img, device=DT.device)[0]
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
        detection = DetectorMosaic_v2.models['model_face'](face_img, device=DT.device)[0]
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

    def analyze(self, start, end):
        '''프레임 리스트를 넣어주면 모자이크 처리하는 함수'''
        # 캡셋을 해서 시작점 설정
        cap_num = start
        self.cap = cv2.VideoCapture(DT.fileName)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, cap_num)
        DT.detection_list.clear()
        while cap_num < end+1:
            ret, frame = self.cap.read()
            cap_num = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            print(cap_num)
            # cap_num = cap.get(프레임) 
            try:
                detections = DetectorMosaic_v2.models['model'].track(frame, persist=True, device=DT.device)[0]
            except Exception as e:
                print(e)
                # 욜로 트래커 초기화
                DetectorMosaic_v2.models['model'] = YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8x.pt'))
                detections = DetectorMosaic_v2.models['model'].track(frame, persist=True, device=DT.device)[0]
            # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
            
            for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                    continue
                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
                track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
                # 검출대상 설정
                # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
                if label not in [0,2,3,5,7,9]:
                    continue
                # 임계값 이하는 생략 하라는 코드
                thr = DT.getValue(DetectorMosaic_v2.tag, '민감도')
                if confidence < thr/100:
                    continue
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
                cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
                # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가
                # xmin, ymin, xmax, ymax의 값은 roi_img의 상대좌표인데, 이를 전체 이미지에서의 상대좌표로 변환(전체 이미지 shape은 DT.img.shape)
                xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
                # df, temp_df 정리
                DT.detection_add(cap_num-1, track_id, label, xmin, ymin, xmax, ymax, confidence)
        DT.df = pd.DataFrame(DT.detection_list, columns=DT.columns)
        DT.detection_list.clear()
        DT.df_plot = pd.DataFrame({'frame': DT.df['frame']})
        r = range(DT.start_point, DT.end_point+1)
        df = pd.DataFrame({'frame': r})
        DT.df_plot = pd.concat([DT.df_plot, df], axis=0).drop_duplicates()
        self.signal_3.emit()

    def getCustomeID(self):
        '''
        DT.df 에서 label이 custom인 것 중 id max값 +1 을 id값으로 리턴하는 함수
        '''
        return 1
    
    def getTotalID(self):
        '''
        DT.df 에서 label이 total인 것 중 id max값 +1 을 id값으로 리턴하는 함수
        '''
        return 3
    #####################
    ## 커스텀 버튼 함수 ##
    #####################

    def btn1(self):
        DT.start_point = DT.cap_num
        self.signal_1.emit(DT.start_point)
        print('시작: ', DT.start_point)


    def btn2(self):
        DT.end_point = DT.cap_num
        self.signal_2.emit(DT.end_point)
        print('끝: ', DT.end_point)

    def btn3(self):
        '''분석'''
        start = DT.start_point if DT.start_point else 0
        end = DT.end_point if DT.end_point else DT.total_frames
        start_time = time.time()
        self.analyze(start, end)
        end_time = time.time()
        print((end-start)/(end_time-start_time))
        print('''
분석 버튼을 눌렀을 때
DT.start_point와 DT.end_point 값이 존재 => 해당 구간을 df에 저장
값이 없으면 0 부터 total_frame 까지 df에 저장
              ''')

    def btn4(self):
        print('btn4: roi값 프레임에 추가 => df에 저장')
        ID = self.getCustomeID()
        x1, y1, x2, y2 = DT.roi
        df = pd.DataFrame({'frame': DT.cap_num, 'ID': ID, 'label': 'custom', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
        DT.df = pd.concat([DT.df, df], ignore_index=True)
        print(DT.df)
        

    def btn5(self):
        print('btn5: 전체 프레임에 roi값 모자이크 추가 => df에 저장')
        start = DT.start_point if DT.start_point else 0
        end = DT.end_point if DT.end_point else DT.total_frames
        ID = self.getTotalID()
        x1, y1, x2, y2 = DT.roi
        for frame in range(start, end+1):
            df = pd.DataFrame({'frame': frame, 'ID': ID, 'label': 'total', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
            DT.df = pd.concat([DT.df, df], ignore_index=True)
        print(DT.df)

    def btn6(self):
        '''
        모자이크 처리
        '''
        self.flag_btn6 = True
        worker = WorkerMosaic(DT.fileName, 
                        DT.df,
                        DT.start_point, 
                        DT.end_point, 
                        DT.total_frames, 
                        DT.fps, 
                        DT.width, 
                        DT.height,
                        DT.getValue(DetectorMosaic_v2.tag, '가림정도')/600)
        worker.start()
        worker.join()
        result = worker.queue.get()
        print(result)

    # 버튼 리스트
    def make_btn_list(self):
        self.btns = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6]




from multiprocessing import Process, Queue

class WorkerMosaic(Process):
    def __init__(self, fileName, df, start_point, end_point, total_frames, fps, width, height, ratio):
        super().__init__()
        self.queue = Queue()
        self.fileName = fileName
        self.df = df
        self.start_point = start_point
        self.end_point = end_point
        self.total_frames = total_frames
        self.fps = fps
        self.width = width
        self.height = height
        self.ratio = ratio

    def run(self):
        start = self.start_point if self.start_point else 0
        end = self.end_point if self.end_point else self.total_frames
        cap = cv2.VideoCapture(self.fileName)
        fileName = os.path.basename(self.fileName)
        outdir  = os.path.dirname(self.fileName)
        output_path = os.path.join(outdir, 'output')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        outfile = os.path.join(output_path, f'{fileName}')
        self.video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        for frame in range(start, end+1):
            text = f'{frame}'
            self.queue.put(text)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, img = cap.read()
            img = self.plot_df_to_mosaic(img, frame)
            self.video.write(img)             
        self.video.release()
        tools.openpath(output_path)

    def plot_df_to_mosaic(self, img, cap_num):
        img = img.copy()
        df = self.df
        cap_num = int(cap_num)
        df = df[df['frame']== cap_num]
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
            img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=self.ratio)
        return img
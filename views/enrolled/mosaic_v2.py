import cv2
from ultralytics import YOLO
import os
from control import tools
from control.run_ocr import OcrReader
import numpy as np
import pandas as pd
from views.sharedData import DT
from PySide6.QtCore import Signal, QObject, QTimer 
from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QAbstractItemView
import time
from multiprocessing import Process, Queue
from rsc.ui.mosaic_ui import Ui_mosaic 

 

class Mosaic(Ui_mosaic, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableView_mosaic_ID.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_mosaic_frame.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_mosaic_ID.clicked.connect(lambda: self.selected_table('ID'))
        self.tableView_mosaic_frame.clicked.connect(lambda: self.selected_table('frame'))
        
        # 시그널 슬롯 연결
        self.pushButton_4.clicked.connect(self.btn4)
        self.pushButton_5.clicked.connect(self.btn5)
        self.pushButton_6.clicked.connect(self.btn6)
        self.pushButton_1.clicked.connect(self.btn1)
        self.pushButton_2.clicked.connect(self.btn2)
        self.pushButton_3.clicked.connect(self.btn3)
        self.slider_mosaic.valueChanged.connect(self.slot_mosaic_valueChanged)
        
        
    def btn4(self):
        DT.start_point = DT.cap_num
        self.pushButton_4.setText(f'시작: {DT.start_point}')

    def btn5(self):
        DT.end_point = DT.cap_num
        self.pushButton_5.setText(f'끝: {DT.end_point}')

    def btn6(self):
        '''숫자6 입력시 분석 실행되는 함수'''
        self.progressBar_mosaic.setValue(0)
        self.start = DT.start_point if DT.start_point else 0
        self.end = DT.end_point if DT.end_point else DT.total_frames
        # 캡셋을 해서 시작점 설정
        cap_num = self.start
        DT.cap = cv2.VideoCapture(DT.fileName)
        DT.cap.set(cv2.CAP_PROP_POS_FRAMES, cap_num)
        DT.detection_list.clear()
        while cap_num < self.end+1:
            ret, frame = DT.cap.read()
            cap_num = DT.cap.get(cv2.CAP_PROP_POS_FRAMES)
            DT.mosaic_current_frame = cap_num
            # cap_num = cap.get(프레임) 
            try:
                print('btn6', DT.device)
                detections = self.detector.track(frame, persist=True, device=DT.device)[0]
            except Exception as e:
                print(e)
                # 욜로 트래커 초기화
                self.detector = YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8x.pt'))
                detections = self.detector.track(frame, persist=True, device=DT.device)[0]
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
                if confidence < 1/100:
                    continue
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
                cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
                # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가
                # xmin, ymin, xmax, ymax의 값은 roi_img의 상대좌표인데, 이를 전체 이미지에서의 상대좌표로 변환(전체 이미지 shape은 DT.img.shape)
                xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
                # df, temp_df 정리
                DT.detection_add(cap_num-1, track_id, label, xmin, ymin, xmax, ymax, confidence)
            progress_var = int((cap_num / (self.end+1)) * 100)
            self.progressBar_mosaic.setValue(progress_var)
        DT.df = pd.DataFrame(DT.detection_list, columns=DT.columns)
        DT.detection_list.clear()
        self.df_frame = pd.DataFrame({'frame': DT.df['frame']})
        r = range(DT.start_point, DT.end_point+1)
        df = pd.DataFrame({'frame': r})
        self.df_frame = pd.concat([self.df_frame, df], axis=0).drop_duplicates()
        self.progressBar_mosaic.setValue(100)
        self.df_to_tableView_mosaic_frame()
        self.df_to_tableView_mosaic_ID()
        # ID 리스트 뷰와
        # frame 리스트 뷰 출력


    def btn1(self):
        print('btn4: roi값 프레임에 추가 => df에 저장')
        ID = 3
        x1, y1, x2, y2 = DT.roi
        df = pd.DataFrame({'frame': DT.cap_num, 'ID': ID, 'label': '부분', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
        DT.df = pd.concat([DT.df, df], ignore_index=True)
        self.df_to_tableView_mosaic_frame()
        self.df_to_tableView_mosaic_ID()
        print(DT.df)
        

    def btn2(self):
        print('btn5: 전체 프레임에 roi값 모자이크 추가 => df에 저장')
        start = DT.start_point if DT.start_point else 0
        end = DT.end_point if DT.end_point else DT.total_frames
        ID = 7
        x1, y1, x2, y2 = DT.roi
        for frame in range(start, end+1):
            df = pd.DataFrame({'frame': frame, 'ID': ID, 'label': '전체', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
            DT.df = pd.concat([DT.df, df], ignore_index=True)
        self.df_to_tableView_mosaic_frame()
        self.df_to_tableView_mosaic_ID()
        print(DT.df)
        
    def btn3(self):
        '''
        모자이크 처리
        '''
        self.progressBar_mosaic.setValue(0)
        if DT.df is None:
            print('df가 없습니다.')
            return
        queue = Queue()
        start_point = int(DT.df['frame'].min())
        end_point = int(DT.df['frame'].max())
        self.worker_mosaic_video = WorkerMosaic(
            queue,
            DT.fileName, 
            DT.df,
            start_point, 
            end_point, 
            DT.total_frames, 
            DT.fps, 
            DT.width, 
            DT.height,
            self.slider_mosaic.value()/600)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(1)
        self.worker_mosaic_video.start()
        # self.worker_mosaic_video.join()

    def updateProgressBar(self):
        var = self.worker_mosaic_video.queue.get()
        self.progressBar_mosaic.setValue(var)
        self.update()
        print(f'var: {var}')
        if var >= 100:
            self.progressBar_mosaic.setValue(100)
            self.timer.stop()
 

    def applyImageProcessing(self, img=None):
        if img is None:
            img = DT.img.copy()
        print('모자이크 이미지 처리')
        print(DT.df)
        df = DT.df[DT.df['frame']==DT.cap_num]
        # 모자이크 처리
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)
            img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=self.slider_mosaic.value()/600)
            img = cv2.putText(img, f'{row["ID"]}', (xmin, ymin-5), cv2.FONT_ITALIC, 3, (0,255,0))
        return img

    def slot_mosaic_valueChanged(self):
        self.label.setText(f'{self.slider_mosaic.value()}')


    def df_to_tableView_mosaic_frame(self):
        # 모델 초기화를 데터 추가 전에 수행
        self.qmodel_mosaic_frame = QtGui.QStandardItemModel()  # 초기 행과 열의 수를 설정하지 않음
        columns = self.df_frame.columns
        self.qmodel_mosaic_frame.setColumnCount(len(columns))
        self.qmodel_mosaic_frame.setHorizontalHeaderLabels(columns)
        for row in range(len(self.df_frame)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in self.df_frame.iloc[row]]
            self.qmodel_mosaic_frame.appendRow(value_objs)
        self.tableView_mosaic_frame.setModel(self.qmodel_mosaic_frame)

    def df_to_tableView_mosaic_ID(self):
        self.df_id = DT.df[['ID','label']].copy()
        self.df_id = self.df_id.drop_duplicates()

        # 모델 초기화를 데터 추가 전에 수행
        self.qmodel_mosaic_ID = QtGui.QStandardItemModel()
        columns = self.df_id.columns
        self.qmodel_mosaic_ID.setColumnCount(len(columns))
        self.qmodel_mosaic_ID.setHorizontalHeaderLabels(columns)
        for row in range(len(self.df_id)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in self.df_id.iloc[row]]
            self.qmodel_mosaic_ID.appendRow(value_objs)
        self.tableView_mosaic_ID.setModel(self.qmodel_mosaic_ID)
        self.update()

    def delete_key(self):
        # 2가지 테이블중 어떤 테이블이 선택되었는지 확인
        if self.table == 'ID':
            print('id')
            index = self.tableView_mosaic_ID.currentIndex()
            row = index.row()
            id = self.df_id.iloc[row]['ID']
            DT.df = DT.df[DT.df['ID'] != id]
            self.df_to_tableView_mosaic_ID()
        elif self.table == 'frame':
            index = self.tableView_mosaic_frame.currentIndex()
            row = index.row()
            frame = self.df_frame.iloc[row]['frame']
            DT.df = DT.df[DT.df['frame'] != frame]
            self.df_frame = DT.df[['frame']].drop_duplicates()
            self.df_to_tableView_mosaic_frame()

    def selected_table(self, table_name):
        if table_name == 'ID':
            self.table = 'ID'
        elif table_name == 'frame':
            self.table = 'frame'
        else:
            print('테이블이 선택되지 않음')
        self.update()


    def program_exit(self):
        print('Ui_Bike 프로그램 종료')


class WorkerMosaic(Process):

    def __init__(self, queue, fileName, df, start_point, end_point, total_frames, fps, width, height, ratio):
        Process.__init__(self)   
        self.fileName = fileName
        self.df = df
        self.start_point = start_point
        self.end_point = end_point
        self.total_frames = total_frames
        self.fps = fps
        self.width = width
        self.height = height
        self.ratio = ratio
        self.queue = queue
        
    def run(self):
        self.queue.put(0)
        start = self.start_point  
        end = self.end_point  
        cap = cv2.VideoCapture(self.fileName)
        fileName = os.path.basename(self.fileName)
        outdir  = os.path.dirname(self.fileName)
        output_path = os.path.join(outdir, 'output')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        outfile = os.path.join(output_path, f'{fileName}')
        self.video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        for frame in range(start, end+1):
            processed_frame = frame - start
            progress_var = int((processed_frame / (end) * 100 ) )+1
            self.queue.put(progress_var)
            print(f'progress_var: {progress_var}')
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            _, img = cap.read()
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




class DetectorMosaic_v2(QObject):

    tag = 'mosaic'
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
 
 
    def __init__(self):
        super().__init__()


    def setup():
        '''
        모델이 초기화 될 때 실행되는 함수
        '''
        # 슬라이더 설정
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




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
from PySide6.QtWidgets import QWidget, QAbstractItemView, QApplication
import time
from multiprocessing import Process, Queue
from rsc.ui.mosaic_ui import Ui_mosaic 
from control.tools import getTime
 

class Mosaic(Ui_mosaic, QWidget):

    signal_frame_move = Signal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableView_mosaic_ID.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_mosaic_ID.clicked.connect(lambda: self.selected_table('ID'))
        
        # 시그널 슬롯 연결
        self.pushButton_4.clicked.connect(self.btn4)
        self.pushButton_5.clicked.connect(self.btn5)
        self.pushButton_6.clicked.connect(self.btn6)
        self.pushButton_1.clicked.connect(self.btn1)  # 프레임 추가
        self.pushButton_2.clicked.connect(self.btn2)  # 프레임 전체 추가
        self.pushButton_3.clicked.connect(self.btn3)  # 모자이크 처리
        self.slider_mosaic.valueChanged.connect(self.slot_mosaic_valueChanged)
        self.btn_move_start.clicked.connect(self.slot_btn_move_start)
        self.btn_move_end.clicked.connect(self.slot_btn_move_end)
        
        
    def btn4(self):
        DT.start_point = DT.cap_num
        self.pushButton_4.setText(f'시작: {DT.start_point}')

    def btn5(self):
        DT.end_point = DT.cap_num
        self.pushButton_5.setText(f'끝: {DT.end_point}')

    @getTime
    def btn6(self):
        '''숫자6 입력시 분석 실행되는 함수'''
        obj = {0: '사람', 2: '승용차', 3: '오토바이', 5: '버스', 7: '트랙'}
        self.progressBar_mosaic.setValue(0)
        self.start = DT.start_point if DT.start_point else 0
        self.end = DT.end_point if DT.end_point else DT.total_frames
        # 캡셋을 해서 시작점 설정
        cap_num = self.start
        DT.cap = cv2.VideoCapture(DT.fileName)
        DT.cap.set(cv2.CAP_PROP_POS_FRAMES, cap_num)
        DT.detection_list.clear()
        while cap_num < self.end:
            ret, frame = DT.cap.read()
            if not ret:
                fail+=1
                continue
            cap_num = DT.cap.get(cv2.CAP_PROP_POS_FRAMES)
            DT.mosaic_current_frame = cap_num
            # cap_num = cap.get(프레임) 
            try:
                detections = self.detector.track(frame, persist=True, device=DT.device)[0]
            except Exception as e:
                print(e)
                # 욜로 트래커 초기화
                self.detector = YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8x.pt'))
                detections = self.detector.track(frame, persist=True, device=DT.device)[0]
            for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                    continue
                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
                track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
                # 검출대상 설정
                # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
                
                if label not in [0,2,3,5,7]:
                    continue
                if confidence < 1/100:
                    continue
                xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
                # df, temp_df 정리
                DT.detection_add(cap_num-1, track_id, obj[label], xmin, ymin, xmax, ymax, confidence)
            progress_var = int(cap_num / self.end * 100) +1
            self.progressBar_mosaic.setValue(progress_var)
            QApplication.processEvents()
        DT.df = pd.DataFrame(DT.detection_list, columns=DT.columns)
        DT.detection_list.clear()
        self.progressBar_mosaic.setValue(100)
        self.df_to_tableView_mosaic_ID()
        # ID 리스트 뷰와
        # frame 리스트 뷰 출력


    def btn1(self):
        n = DT.df[DT.df['label'] == '부분']['ID'].max()
        ID = 0 if pd.isnull(n) else n + 1
        x1, y1, x2, y2 = DT.roi
        df = pd.DataFrame({'frame': DT.cap_num, 'ID': ID, 'label': '부분', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
        DT.df = pd.concat([DT.df, df], ignore_index=True)
        self.df_to_tableView_mosaic_ID()
        

    def btn2(self):
        start = DT.start_point if DT.start_point else 0
        end = DT.end_point if DT.end_point else DT.total_frames
        n = DT.df[DT.df['label'] == '전체']['ID'].max()
        ID = 0 if pd.isnull(n) else n + 1
        x1, y1, x2, y2 = DT.roi
        for frame in range(start, end+1):
            df = pd.DataFrame({'frame': frame, 'ID': ID, 'label': '전체', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thr': 1}, index=[0])
            DT.df = pd.concat([DT.df, df], ignore_index=True)
        self.df_to_tableView_mosaic_ID()
        
    def btn3(self):
        '''
        모자이크 처리
        '''
        self.progressBar_mosaic.setValue(0)
        if DT.df is None:
            print('df가 없습니다.')
            return
        start_point = int(DT.df['frame'].min())
        end_point = int(DT.df['frame'].max())
        self.fileName = DT.fileName
        self.total_frames = DT.total_frames
        cap = cv2.VideoCapture(self.fileName)
        fileName = os.path.basename(self.fileName)
        outdir  = os.path.dirname(self.fileName)
        output_path = os.path.join(outdir, 'output')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        outfile = os.path.join(output_path, f'{fileName}')
        self.video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), DT.fps, (DT.width, DT.height))
        for frame in range(start_point, end_point+1):
            processed_frame = frame - start_point
            progress_var = int((processed_frame / (end_point) * 100 ) )+1
            self.progressBar_mosaic.setValue(progress_var)
            QApplication.processEvents()
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            _, img = cap.read()
            img = self.plot_df_to_mosaic(img, frame)
            self.video.write(img)             
        self.video.release()
        self.progressBar_mosaic.setValue(100)
        tools.openpath(output_path)

    def plot_df_to_mosaic(self, img, cap_num):
        img = img.copy()
        df = DT.df
        cap_num = int(cap_num)
        df = df[df['frame']== cap_num]
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
            img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=self.slider_mosaic.value()/600)
        return img
 


    def slot_btn_move_start(self):
        self.signal_frame_move.emit(DT.start_point)

    def slot_btn_move_end(self):
        self.signal_frame_move.emit(DT.end_point)

    def updateProgressBar(self):
        var = self.worker_mosaic_video.queue.get()
        self.progressBar_mosaic.setValue(var)
        self.update()
        QApplication.processEvents()
        if var >= 100:
            self.progressBar_mosaic.setValue(100)
            self.timer.stop()
 

    def applyImageProcessing(self, img=None):
        if img is None:
            img = DT.img.copy()
        df = DT.df[DT.df['frame']==DT.cap_num]
        # 모자이크 처리
        for index, row in df.iterrows():
            xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']
            xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)
            _id = int(row["ID"])
            color = DT.color_map[_id%18]
            if self.checkBox_mosaic.isChecked():
                img = tools.mosaic(img, xmin, ymin, xmax, ymax, ratio=self.slider_mosaic.value()/600)
            else:
                img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 5)
                img = cv2.putText(img, f'{_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 3, color, 5)
        return img

    def slot_mosaic_valueChanged(self):
        self.label.setText(f'{self.slider_mosaic.value()}')

 
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
            index = self.tableView_mosaic_ID.currentIndex()
            row = index.row()
            id = self.df_id.iloc[row]['ID']
            DT.df = DT.df[DT.df['ID'] != id]
            self.df_to_tableView_mosaic_ID()


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


 
 
        




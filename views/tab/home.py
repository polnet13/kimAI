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
from PySide6.QtWidgets import QWidget, QFileDialog, QAbstractItemView
from rsc.ui.home_ui import Ui_Form
from multiprocessing import Process, Queue
import time

 

class Home(Ui_Form, QWidget):

    playerOpenSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 시그널 슬롯 연결
        self.btn_open_file.clicked.connect(self.open_files)
        # self.pushButton_4.clicked.connect(self.btn4)
        # self.pushButton_5.clicked.connect(self.btn5)
        # self.pushButton_6.clicked.connect(self.btn6)
        # self.pushButton_1.clicked.connect(self.btn1)
        # self.pushButton_2.clicked.connect(self.btn2)
        # self.pushButton_3.clicked.connect(self.btn3)
        
    def open_files(self):
        '''
        파일 입력 받아서 맨 처음 파일을 오픈
        리스트는 테이블뷰에 출력
        테이블 선택시 해당 파일 오픈
        '''
        self.flag_files = True
        fileNames, _ = QFileDialog.getOpenFileNames(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        DT.fileNames = fileNames
        if len(DT.fileNames) == 0:
            self.flag_files = False
            return
        self.df_to_tableView()
        # fileNames의 파일들의 용량을 확인하고 용량이 큰 순서대로 정렬
        DT.fileName = DT.fileNames[0]
        self.playerOpenSignal.emit()
        print('테이블 선택시 해당 파일 오픈 하는 것으로 수정 예정')

    def btn4(self):
        pass

    def btn5(self):
        pass

    def btn6(self):
        '''숫자6 입력시 분석 실행되는 함수'''
        pass


    def btn1(self):
        pass

    def btn2(self):
        pass
        
    def btn3(self):
        pass

     
    def program_exit(self):
        print('Ui_Bike 프로그램 종료')

    def applyImageProcessing(self, img):
        print('모자이크 이미지 처리')
        return img



    def df_to_tableView(self):
        # df 정리
        filenames = [ os.path.basename(row) for row in DT.fileNames ]
        self.dirname = os.path.dirname(DT.fileNames[0])
        self.df = pd.DataFrame({'file': filenames})
        columns = self.df.columns
        # tableView 정의
        # 모델 초기화를 데터 추가 전에 수행
        qmodel_ = QtGui.QStandardItemModel()
        qmodel_.setColumnCount(len(columns))
        qmodel_.setHorizontalHeaderLabels(columns)
        for row in range(len(self.df)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in self.df.iloc[row]]
            qmodel_.appendRow(value_objs)
        self.tableView.setModel(qmodel_)
        self.update()
        
        # 테이블뷰 클릭 시 값을 가져오도록 수정
        self.tableView.clicked.connect(self.get_selected_value)
        
    def get_selected_value(self, index):
        '''테이블 클릭시 행동'''
        row = index.row()
        val = self.df.iloc[row, 0]
        DT.fileName = os.path.join(self.dirname, val)
        self.playerOpenSignal.emit()
        # row, col 에 해당하는 값 출력


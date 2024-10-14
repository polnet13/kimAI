import cv2
from ultralytics import YOLO
import torch
import os
from control import tools
from control.run_ocr import OcrReader
import numpy as np
import pandas as pd
from views.sharedData import DT
from PySide6.QtCore import Signal, QObject, QTimer 
from PySide6 import QtGui
from PySide6.QtWidgets import QWidget
import time
from multiprocessing import Process, Queue
from rsc.ui.settings_ui import Ui_Settings

 

class Settings(Ui_Settings, QWidget):
    def __init__(self, options):
        super().__init__()
        self.setupUi(self)
        
        DT.setOption(options)
        if (DT.check_cuda == True or DT.check_cuda != 0) and torch.cuda.is_available():
            DT.device = 'cuda'
            print('cuda 사용')
        else:
            DT.device = 'cpu'
            print('cpu 사용')
        self.checkBox_cuda.setChecked(DT.check_cuda)
        print(options)
        # options 의 키값을 변수로 밸류를 변수의 값으로 DT에 저장
        # 시그널 슬롯 연결
        # self.pushButton_4.clicked.connect(self.btn4)
        # self.pushButton_5.clicked.connect(self.btn5)
        # self.pushButton_6.clicked.connect(self.btn6)
        # self.pushButton_1.clicked.connect(self.btn1)
        # self.pushButton_2.clicked.connect(self.btn2)
        # self.pushButton_3.clicked.connect(self.btn3)
        self.checkBox_cuda.stateChanged.connect(self.setCuda)
        
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

    def setCuda(self, value):
        if value and torch.cuda.is_available():
            DT.device = 'cuda'
            print(f'{DT.device} 사용')
        elif value == False:
            DT.device = 'cpu'
            print(f'{DT.device} 사용')
        DT.saveOption(check_cuda=value)

    def program_exit(self):
        print('Ui_Bike 프로그램 종료')

    def applyImageProcessing(self, img):
        print('모자이크 이미지 처리')
        return img


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
from PySide6.QtWidgets import QWidget
import time
from multiprocessing import Process, Queue
from rsc.ui.home_ui import Ui_Form

 

class Home(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 시그널 슬롯 연결
        # self.pushButton_4.clicked.connect(self.btn4)
        # self.pushButton_5.clicked.connect(self.btn5)
        # self.pushButton_6.clicked.connect(self.btn6)
        # self.pushButton_1.clicked.connect(self.btn1)
        # self.pushButton_2.clicked.connect(self.btn2)
        # self.pushButton_3.clicked.connect(self.btn3)
        
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


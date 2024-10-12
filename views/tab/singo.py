import subprocess
import sys
from ultralytics import YOLO
import cv2
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout
from PySide6.QtWidgets import QWidget, QScrollArea, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QCursor
# 시그널 임포트
from PySide6.QtCore import Signal
# 외부 모듈
import os, json
import cv2
from multiprocessing import Process, Queue
from control import tools
from views.sharedData import DT
from rsc.ui.singo_ui import Ui_Form
from control.tools import getTime
from control.singo_external import *




class Chuldong(Ui_Form, QWidget):

    playerOpenSignal = Signal()

    '''ui와 시그널 연결'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_point_1.clicked.connect(self.listen_start)
        self.btn_point_2.clicked.connect(self.listen_start)
        self.label_point1.setText(f'{DT.btn_point_1[0]}, {DT.btn_point_1[1]}')
        self.label_point2.setText(f'{DT.btn_point_2[0]}, {DT.btn_point_2[1]}')
        self.is_listening = False
        # 시그널 슬롯 연결
        self.ra_rank_1.clicked.connect(self.rank_select)
        self.ra_rank_2.clicked.connect(self.rank_select)
        self.ra_rank_3.clicked.connect(self.rank_select)
        self.ra_rank_4.clicked.connect(self.rank_select)
        self.ra_rank_5.clicked.connect(self.rank_select)
        self.ra_team_1.clicked.connect(self.team_select)
        self.ra_team_2.clicked.connect(self.team_select)
        self.ra_team_3.clicked.connect(self.team_select)
        self.ra_team_4.clicked.connect(self.team_select)
        self.set_rank(DT.rank)
        self.set_team(DT.team)

    def getInstance(self):
        '''시작시 한 번에 불러오면 대기시간이 올래 걸리므로 좌메뉴 클릭시 인스턴스 생성'''
        return 

    def listen_start(self):
        self.installEventFilter(self)
        self.sender_btn = self.sender()  # sender()로 이벤트를 보낸 위젯을 구분하는 원리는????????

    def eventFilter(self, watched, event):
        if watched == self and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                pos = QCursor.pos()
                if self.sender_btn == self.btn_point_1:
                    self.label_point1.setText(f'{pos.x()}, {pos.y()}')
                    DT.saveOption(btn_point_1=(pos.x(), pos.y()))
                elif self.sender_btn == self.btn_point_2:
                    self.label_point2.setText(f'{pos.x()}, {pos.y()}')
                    DT.saveOption(btn_point_2=(pos.x(), pos.y()))
                self.removeEventFilter(self)
        return super().eventFilter(watched, event)

    def team_select(self):
        '''팀 선택'''
        if self.ra_team_1.isChecked():
            self.team = '1팀'
        elif self.ra_team_2.isChecked():
            self.team = '2팀'
        elif self.ra_team_3.isChecked():
            self.team = '3팀'
        elif self.ra_team_4.isChecked():
            self.team = '4팀'
        print(f'팀 선택: {self.team}')
        DT.team = self.team
        DT.saveOption(team=self.team)    

    def rank_select(self, btn):
        '''랭크 선택'''
        if self.ra_rank_1.isChecked():
            self.rank = '순경'
        elif self.ra_rank_2.isChecked():
            self.rank = '경장'
        elif self.ra_rank_3.isChecked():
            self.rank = '경사'
        elif self.ra_rank_4.isChecked():
            self.rank = '경위'
        elif self.ra_rank_5.isChecked():
            self.rank = '경감'
        print(f'랭크 선택: {self.rank}')
        DT.rank = self.rank
        DT.saveOption(rank=self.rank)

    def set_rank(self, rank):
        '''랭크 설정'''
        if rank == '순경':
            self.ra_rank_1.setChecked(True)
        elif rank == '경장':
            self.ra_rank_2.setChecked(True)
        elif rank == '경사':
            self.ra_rank_3.setChecked(True)
        elif rank == '경위':
            self.ra_rank_4.setChecked(True)
        elif rank == '경감':
            self.ra_rank_5.setChecked(True)

    def set_team(self, team):
        '''팀 설정'''
        if team == '1팀':
            self.ra_team_1.setChecked(True)
        elif team == '2팀':
            self.ra_team_2.setChecked(True)
        elif team == '3팀':
            self.ra_team_3.setChecked(True)
        elif team == '4팀':
            self.ra_team_4.setChecked(True)

    def program_exit(self):
        '''멀티 CCTV 프로그램 종료'''
        print('멀티 CCTV 종료')

    ####################     
    # 멀티프로세싱 함수 #
    ####################

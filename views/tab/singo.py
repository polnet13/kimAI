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
import os, sys
import pandas as pd
#from ui_mainwindow import UI_MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

import time, datetime
import pyautogui
import keyboard
import pyperclip




class Chuldong(Ui_Form, QWidget):

    signalSingo = Signal(int)
    # 1: DT.df_main 생성
    # 2: DT.df_main 선택행 삭제


    '''ui와 시그널 연결'''
    def __init__(self):
        super().__init__()
        self.df1 = None     # 사건검색리스트 파일 -> df
        self.df2 = None     # 출동수당 파일 -> df
        self.result = None
        self.setupUi(self)
        self.btn_point_1.clicked.connect(self.listen_start)
        self.btn_point_2.clicked.connect(self.listen_start)
        self.label_point1.setText(f'{DT.btn_point_1[0]}, {DT.btn_point_1[1]}')
        self.label_point2.setText(f'{DT.btn_point_2[0]}, {DT.btn_point_2[1]}')
        self.is_listening = False
        # 시그널 슬롯 연결
        self.btn_make_df.clicked.connect(self.make_df)
        self.btn_del.clicked.connect(self.delete_row)
        self.btn_hwp.clicked.connect(self.make_hwp)
        # 시그널 라디오버튼
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
        '''마우스 클릭 이벤트 리스너 시작'''
        self.installEventFilter(self)
        self.sender_btn = self.sender()  # sender()로 이벤트를 보낸 위젯을 구분하는 원리는????????

    def eventFilter(self, watched, event):
        '''마우스 클릭 이벤트 리스너'''
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
            self.team = 1
        elif self.ra_team_2.isChecked():
            self.team = 2
        elif self.ra_team_3.isChecked():
            self.team = 3
        elif self.ra_team_4.isChecked():
            self.team = 4
        print(f'팀 선택: {self.team}')
        DT.team = self.team
        DT.saveOption(team=self.team)    

    def rank_select(self, btn):
        '''랭크 선택'''
        if self.ra_rank_1.isChecked():
            self.rank = 0
        elif self.ra_rank_2.isChecked():
            self.rank = 1
        elif self.ra_rank_3.isChecked():
            self.rank = 2
        elif self.ra_rank_4.isChecked():
            self.rank = 3
        elif self.ra_rank_5.isChecked():
            self.rank = 4
        print(f'랭크 선택: {self.rank}')
        DT.rank = self.rank
        DT.saveOption(rank=self.rank)

    def set_rank(self, rank):
        '''랭크 설정'''
        rank = [self.ra_rank_1, self.ra_rank_2, self.ra_rank_3, self.ra_rank_4, self.ra_rank_5][rank]
        rank.setChecked(True)

    def set_team(self, team):
        '''팀 설정'''
        team = [ self.ra_team_1, self.ra_team_2, self.ra_team_3, self.ra_team_4][team-1]
        team.setChecked(True)

    ## 사건검색리스트 엑셀 파일 등록
    def file_up_112(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '사건검색리스트 엑셀파일', os.getcwd(), 'All files (*)')
        if file_path:
            try:
                df = pd.read_excel(
                    file_path,
                    sheet_name='List', 
                    usecols='A:AJ',
                    header=0,
                    )
                self.df1 = df
            except Exception as e:
                print(e)
                QMessageBox.critical(self, "Error", str(e))
                return


    ## 엑셀등록(이미 등록된 리스트) => df2 생성
    def file_up_enrolled(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '출동수당 등록 엑셀파일', os.getcwd(), 'All files (*)')
        if file_path: 
            try:
                df = pd.read_excel(
                    file_path, 
                    sheet_name='sheet_1', 
                    usecols='A:J',
                    header=1,
                    )
                file_name = os.path.basename(file_path)
                print(file_name)
                self.df2 = df
            except Exception as e:
                print(e)
                QMessageBox.critical(self, "Error", str(e))
                return

    
    ## 엑셀 파일 정리
    def make_df(self):
        '''엑셀 파일 정리 해서 DT.df_main 생성'''
        try:
            name = self.lineEdit.text()  # 라인에딧으로 입력 받은 이름을 name 변수에 저장
            df1 = self.df1   
            df2 = self.df2
            # df1: 112접수시간 datetime 형식으로 변경하여 '신고time' 변수에 저장
            print('df1: 112접수시간 datetime 형식으로 변경')
            df1['접수시간'] = pd.to_datetime(df1['접수시간'], format='%H:%M:%S')
            # df1에서 남길 열 정리
            print('df1에서 남길 열 정리')
            df1 = df1[['접수번호','신고내용','종결내용','종결보고자','사건번호','접수시간','코드','종결']]  # 지령시간은 외부코드에서 +5분하기 위해 사용
            # 종결 코드 동일건 제외
            print('동일건 제외')
            if self.checkBox_dongil.isChecked():
                df1 = df1[ df1['종결']!='동일']
            # FTX 제외 
            print('FTX 제외 구현')
            if self.checkBox_ftx.isChecked():
                df1 = df1[ df1['종결']!='FTX']
            #조건1: 코드0,1 이름 필터링 
            print('조건1: 코드0,1 이름 필터링 ')
            df1_1 = df1[df1['코드'].isin(['C0','C1']) & df1['종결보고자'].str.contains(name)]
            df1_1.reset_index(inplace=True, drop=True)
            
            #조건2: 코드2 중에서 21:50 - 06:00
            print('조건2: 코드2 중에서 21:50 - 06:00 ')
            df1_2 = df1[ (df1['코드']=='C2') & (df1['종결보고자'].str.contains(name))]
            print('조건2: 코드2 중에서 21:50 - 06:00 중에서 종결보고자 포함된 것 필터링')
            df1_2 = df1_2[ (df1_2['접수시간'] >= pd.to_datetime('21:50', format='%H:%M').time())|(df1_2['접수시간'] <= pd.to_datetime('06:00', format='%H:%M').time())]
            print('조건2: 코드2 중에서 21:50 - 06:00 : 접수시간이 21:50보다 크거나 같음 or 접수시간이 06:00보다 작은것')
            df1_2.reset_index(drop=True, inplace=True)
            
            #조건1, 조건2 결합
            print('조건1, 조건2 결합')
            result = pd.concat([df1_1, df1_2])
            
            # df2: 이미 등록된 출동수당 리스트로 만들기
            print('df2: 이미 등록된 출동수당 리스트로 만들기')
            df2_list = df2['접수 번호'].tolist()
            
            # 출동수당 정리한거에서 이미 등록된 출동수당
            print('출동수당 정리한거에서 이미 등록된 출동수당')
            DT.df_main = result.drop(result[result['접수번호'].isin(df2_list)].index)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", str(e))
        self.signalSingo.emit(1)
    
    
    ## 외부 코드 실행
    def auto_register(self):
        try:
            print(self.result)
            print('-------auto_register 실행---------')
            # 외부 코드 실행
            print('외부코드 실행 시작')
            if self.result is None:
                print(f'self.result 값이 없음')
            else:
                self.ex_code(self.result)
                print('외부코드 실행 끝')
                
        except Exception as e:
            print(e)
 

    ## tableView 생성
    def make_table_view(self, df):
        table_view = self.ui.tableView
        # standard item model 생성
        model = QStandardItemModel()
        # 컬럼 헤더 생성
        model.setHorizontalHeaderLabels(df.columns)
        # 데이터를 모델로 치환
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, column]))
                model.setItem(row, column, item)
        # tableView 에 모델 집어 넣기
        table_view.setModel(model)


    ## 선택된 행을 삭제합니다.
    def delete_row(self):
        self.signalSingo.emit(2)
        


    def make_hwp(self):
        print('make_hwp 실행코드 만들어주세요')
    

    def ex_code(df):
        print(df)
        print('df 컬럼정보')
        print(df.columns)
        # df.columns = ['접수번호','신고내용','종결내용','종결보고자','사건번호','지령시간','지령time','코드','종결']
        time.sleep(1)
        # 도착시간 계산
        poi = pyautogui.position()
        print(poi)
        df['도착시간'] = df['지령시간'].apply(tools.plus5min)
        df['도착date'] = df['도착시간'].dt.strftime('%Y-%m-%d')
        df['도착time'] = df['도착시간'].dt.strftime('%H:%M')
        receipt_num_list = df['접수번호'].tolist()
        arrival_time_date = df['도착date'].tolist()
        arrival_time_list = df['도착time'].tolist()
        print(receipt_num_list, arrival_time_date, arrival_time_list)
        # 임의동록 버튼 좌표 생성
        try:
            img_path = r'module\target.jpg'
            location = pyautogui.locateOnScreen(img_path, confidence= 0.9)
            location = pyautogui.center(location)
            print(f'임의등록 버튼: {location}')
        except TypeError:
            location = (1660, 320)
            pyautogui.alert(f'위치값 인식을 위해 ctrl + 0(숫자) 입력해서 익스플로러창 100%로 맞춰주삼 {location}')
        except Exception as e:
            print(e)
        # 접수번호 입력란 좌표 초기화
        receipt_num_xy = None
        # 증빙구분 좌표 초기화
        jb_xy = None
        for receipt_num, arrival_date, arrival_time in zip(receipt_num_list, arrival_time_date, arrival_time_list):
            print(receipt_num, arrival_date, arrival_time)
            try:
                # 임의등록버튼 클릭
                print('임의등록 버튼 클릭!!')
                pyautogui.moveTo(location, duration=0.2)
                pyautogui.click()
                time.sleep(1)
                # 접수번호 좌표 있을 경우 좌표생성 패스
                if receipt_num_xy:
                    pass
                # 접수번호 좌표 없을 경우 좌표 생성
                else:
                    try:
                        img_path = r'module\1.jpg'
                        receipt_num_xy = pyautogui.locateOnScreen(img_path, confidence= 0.80)
                        print(f'센터값1: {receipt_num_xy}')
                        receipt_num_xy = pyautogui.center(receipt_num_xy)
                        print(f'센터값2: {receipt_num_xy}')
                    except TypeError:
                        pyautogui.alert('접수번호 이미지를 인식하지 몬함 800*350')
                        receipt_num_xy = (800, 350)
                    except Exception as e:
                        print(e)
                pyautogui.moveTo(receipt_num_xy, duration=0.2)
                pyautogui.click()
                pyautogui.typewrite(f'{receipt_num}', interval = 0.01)
                # 이미 등록된 경우 패스하기
                img_path4 = r'module\4.jpg'  # 이미 등록된
                img_path6 = r'module\6.jpg'  # 등록 가능한
                result4 = False
                result6 = False
                while True:
                    result4 = pyautogui.locateOnScreen(img_path4, confidence= 0.9)
                    if result4:
                        # 이미 등록된
                        result = 'stop'
                        break
                    result6 = pyautogui.locateOnScreen(img_path6, confidence= 0.9)
                    if result6:
                        # 등록 가능한
                        result = 'go'
                        break
                    time.sleep(0.1)
                if result == 'stop':
                    # 이미 등록된 경우 패스 하는 코드임
                    tools.tap_n(14)
                    pyautogui.press('enter')
                    time.sleep(0.1)
                    pyautogui.press('enter')
                    time.sleep(0.1)
                    continue
                # 도착일 입력: 탭6번 후 입력
                tools.tap_n(6)
                pyautogui.typewrite(f'{arrival_date}', interval = 0.02)
                # 도착시간 입력
                pyautogui.press('tab')
                pyautogui.typewrite(f'{arrival_time}', interval = 0.02)
                # 사유 작성
                tools.tap_n(2)
                pyperclip.copy('출동수당 누락으로 입력 함')
                pyautogui.hotkey('ctrl', 'v')
                # pyautogui.typewrite('출동수당 누락으로 입력 함', interval = 0.06)
                time.sleep(0.1)
                # 증빙구분선택 좌표 있을 경우 좌표생성 패스
                if jb_xy:
                    pass
                # 증빙구분선택 좌표 없을 경우 좌표 생성
                else:
                    try:
                        img_path = r'module\3.jpg'
                        jb_xy = pyautogui.locateOnScreen(img_path, confidence= 0.98)
                        print(f'센터값1: {jb_xy}')
                        jb_xy = pyautogui.center(jb_xy)
                        print(f'센터값2: {jb_xy}')
                    except TypeError:
                        pyautogui.alert('증빙구분(3) 이미지를 인식하지 몬함')
                    except Exception as e:
                        print(e)
                # 증빙구분 클릭
                pyautogui.moveTo(jb_xy, duration=0.2)
                pyautogui.click()
                time.sleep(0.2)
                # 입력버튼 좌표 있을 경우 좌표생성 패스
                tools.tap_n(3)
                pyautogui.press('enter')
                time.sleep(0.7)
                enter_1 = False
                enter_2 = False
                while True:
                    enter_1 = pyautogui.locateOnScreen(r'module\enter_1.jpg', confidence= 0.9)
                    if enter_1:
                        print('임의등록을 하겠습니까? => 버튼 확인함')
                        break
                    time.sleep(0.2)
                pyautogui.press('enter')
                while True:
                    enter_2 = pyautogui.locateOnScreen(r'module\enter_2.jpg', confidence= 0.9)
                    if enter_2:
                        print('저장되었습니다. => 버튼 확인함')
                        break
                    time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)                
            except Exception as e:
                print(e)
                print('위의 오류로 루프 종료함')
                break
                
        pyautogui.alert('끝')
        

    def program_exit(self):
        '''멀티 CCTV 프로그램 종료'''
        print('멀티 CCTV 종료')

    ####################     
    # 멀티프로세싱 함수 #
    ####################

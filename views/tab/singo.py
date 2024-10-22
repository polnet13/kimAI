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
from control.hangle import Hwp




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
        self.close_signal = False
        self.setupUi(self)
        self.btn_point_1.clicked.connect(self.listen_start)
        self.btn_point_2.clicked.connect(self.listen_start)
        self.label_point_1.setText(f'{DT.btn_point_1[0]}, {DT.btn_point_1[1]}')
        self.label_point_2.setText(f'{DT.btn_point_2[0]}, {DT.btn_point_2[1]}')
        self.is_listening = False
        self.btn_macro.clicked.connect(self.auto_register)
        # 시그널 슬롯 연결
        self.btn_files.clicked.connect(self.file_open)
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
                    self.label_point_1.setText(f'{pos.x()}, {pos.y()}')
                    DT.saveOption(btn_point_1=(pos.x(), pos.y()))
                elif self.sender_btn == self.btn_point_2:
                    self.label_point_2.setText(f'{pos.x()}, {pos.y()}')
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
    def file_open(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, '출동수당 파일 등록', os.getcwd(), 'All files (*)')
        if not file_paths:
            return
        for file_path in file_paths:
            self.sagun(file_path)
            self.enrolled(file_path)

    def sagun(self, file_path):
        try:
            df = pd.read_excel(
                file_path,
                sheet_name='List', 
                usecols='A:AJ',
                header=0,
                )
            self.df1 = df
            self.label_112.setStyleSheet('color: #90EE90; font-weight: bold;')
        except Exception as e:
            print(e)
            return


    def enrolled(self, file_path):
        try:
            self.df2 = pd.read_excel(
                file_path, 
                sheet_name='sheet_1', 
                usecols='A:J',
                header=1,
                )
            self.label_enrol.setStyleSheet('color: #90EE90; font-weight: bold;')
        except Exception as e:
            print(e)
            return

    
    ## 엑셀 파일 정리
    def make_df(self):
        '''엑셀 파일 정리 해서 DT.df_main 생성'''
        try:
            name = self.lineEdit.text()  # 라인에딧으로 입력 받은 이름을 name 변수에 저장
            df1 = self.df1   
            df2 = self.df2
            df1['접수시간'] = pd.to_datetime(df1['접수시간'], format='%H:%M:%S')
            df1 = df1[['접수번호','접수일자', '접수시간', '신고내용','종결내용','종결보고자','사건번호','코드','종결','종결시사건코드','도착시간']]  # 지령시간은 외부코드에서 +5분하기 위해 사용
            if self.checkBox_dongil.isChecked():
                df1 = df1[ df1['종결']!='동일']
            if self.checkBox_ftx.isChecked():
                df1 = df1[ df1['종결']!='FTX']
            #조건1: 코드0,1 이름 필터링 
            df1_1 = df1[df1['코드'].isin(['C0','C1']) & df1['종결보고자'].str.contains(name)]
            df1_1.reset_index(inplace=True, drop=True)
            #조건2: 코드2 중에서 21:50 - 06:00
            df1_2 = df1[ (df1['코드']=='C2') & (df1['종결보고자'].str.contains(name))]
            # df1_2 = df1_2[ (df1_2['접수시간'] >= pd.to_datetime('21:50', format='%H:%M').time())|(df1_2['접수시간'] <= pd.to_datetime('06:00', format='%H:%M').time())]
            df1_2 = df1_2[ (df1_2['접수시간'].dt.time >= pd.to_datetime('21:50', format='%H:%M').time()) |
               (df1_2['접수시간'].dt.time <= pd.to_datetime('06:00', format='%H:%M').time()) ]
            df1_2.reset_index(drop=True, inplace=True)
            #조건1, 조건2 결합
            result = pd.concat([df1_1, df1_2])
            result['112신고 접수일시'] = result['접수일자'] + '\n' + result['접수시간'].dt.strftime('%H:%M')
            # df2: 이미 등록된 출동수당 리스트로 만들기
            result = result.drop(['접수일자','접수시간'], axis=1)
            result = result[['112신고 접수일시','신고내용','종결내용','종결보고자','사건번호','코드','종결','종결시사건코드','접수번호','도착시간']] 
            df2_list = df2['접수 번호'].tolist()

            
            DT.df_main = result.drop(result[result['접수번호'].isin(df2_list)].index).reset_index(drop=True)
            print(DT.df_main)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "파일 오류", '엑셀 파일 2개를 업로드하세요')
        self.signalSingo.emit(1)
    

    ## 선택된 행을 삭제합니다.
    def delete_row(self):
        self.signalSingo.emit(2)

    def delete_key(self):
        self.delete_row()
        


    def make_hwp(self):
        date = datetime.datetime.now().strftime('%y. %m. %d')
        weekday = ['월','화','수','목','금','토','일'][datetime.datetime.now().weekday()]
        team = ['1팀','2팀','3팀','4팀'][DT.team-1]
        rank = ['순경','경장','경사','경위','경감'][DT.rank]
        name = self.lineEdit.text()
        dic = dict(date=date, weekday=weekday, team=team, rank=rank, name=name)
        path = os.path.join(DT.BASE_DIR, 'rsc', 'hwp', 'templete.hwp')
        df = DT.df_main
        df['연번'] = range(1, df.shape[0]+1)
        # df['112신고 접수일시'] = df['접수일자'] + '\n' + df['접수시간'].dt.strftime('%H:%M')
        df['e1'] = ''
        df['e2'] = ''
        df['e3'] = ''
        df['e4'] = ''
        df['e5'] = ''
        df['e6'] = ''
        df = df[['연번','사건번호','112신고 접수일시','종결시사건코드','e1','e2','e3','e4','종결보고자','신고내용','e5','e6']]
        self.hwp = Hwp(path)
        self.hwp.display(True)
        self.hwp.dic_to_field(dic)
        self.hwp.make_table(df.shape[0], df.shape[1])
        self.hwp.insert_df(df)
        # hwp 파일을 읽음
        # 필드 입력
        # 루프 돌면서 df -> 표에 삽입
        # 다른이름으로 저장
    
    
    ## 외부 코드 실행
    def auto_register(self):
        print('-------auto_register 실행---------')
        # 외부 코드 실행
        print('외부코드 실행 시작')
        if DT.df_main is None:
            print(f'DT.df_main 값이 없음')
        else:
            self.macro_code()
            print('매크로 코드 실행 끝')

            
 

    def macro_code(self):
        df = DT.df_main
        # df.columns = ['접수번호','신고내용','종결내용','종결보고자','사건번호','지령시간','지령time','코드','종결']
        time.sleep(1)
        # 임의등록 버튼 클릭

        # 접수번호 클릭
        # 입력
        # 등록
        df_transpose = df.T
        print(df_transpose.head())

        # df['도착시간'] = df['접수시간'].apply(tools.plus5min)
        df['도착시간'] = pd.to_datetime(df['도착시간'], format='%Y-%m-%d %H:%M:%S')
        df['도착date'] = df['도착시간'].dt.strftime('%Y-%m-%d')
        df['도착time'] = df['도착시간'].dt.strftime('%H:%M')
        receipt_num_list = df['접수번호'].tolist()
        arrival_time_date = df['도착date'].tolist()
        arrival_time_list = df['도착time'].tolist()
        # 임의동록(register) 버튼 좌표 생성
        register = DT.btn_point_1  # 임의등록 좌표
        # 증빙구분 좌표 초기화
        jb_xy = None
        for receipt_num, arrival_date, arrival_time in zip(receipt_num_list, arrival_time_date, arrival_time_list):
            # 임의등록 버튼 클릭
            print('임의등록 버튼 클릭!!')
            if self.close_signal:
                break
            pyautogui.moveTo(register, duration=0.2)
            pyautogui.click()
            time.sleep(1)
            # 접수번호 입력란 좌표 초기화
            try:
                img_path = os.path.join(DT.BASE_DIR, 'rsc', 'singo', '1.jpg')
                receipt_num_xy = pyautogui.locateOnScreen(img_path, confidence= 0.80)
                receipt_num_xy = pyautogui.center(receipt_num_xy)
                print(f'센터값2: {receipt_num_xy}')
            except Exception as e:
                pyautogui.alert('접수번호 이미지를 인식하지 몬함 800*350')
                receipt_num_xy = DT.btn_point_2  # 접수번호
                print(e)
            pyautogui.moveTo(receipt_num_xy, duration=0.2)
            pyautogui.click()
            pyautogui.typewrite(f'{receipt_num}', interval = 0.01)
            # 이미 등록된 경우 패스하기
            img_registered = os.path.join(DT.BASE_DIR, 'rsc', 'singo', '4.jpg')  # 이미 등록된  
            img_unregistered = os.path.join(DT.BASE_DIR, 'rsc', 'singo', '6.jpg')  # 등록 가능한  
            resultOfRegistered = False
            n=0
            gostop = None
            while True:
                print(n, '등록된 이미지인지 확인하는 중')
                n += 1
                try:
                    resultOfRegistered = pyautogui.locateOnScreen(img_registered, confidence=0.6)
                except:
                    pass
                if resultOfRegistered:
                    gostop = 'stop'
                    break
                try:
                    resultOfRegistered = pyautogui.locateOnScreen(img_unregistered, confidence= 0.6)
                except:
                    pass
                if resultOfRegistered:
                    break
                time.sleep(0.5)
            if gostop == 'stop':
                # 이미 등록된 경우 패스 하는 코드임
                tools.tap_n(14)
                pyautogui.press('enter')
                time.sleep(0.3)
                pyautogui.press('enter')
                time.sleep(0.3)
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
                    img_path = os.path.join(DT.BASE_DIR, 'rsc', 'singo', '3.jpg')  
                    jb_xy = pyautogui.locateOnScreen(img_path, confidence= 0.98)
                    jb_xy = pyautogui.center(jb_xy)
                    print(f'증빙구분 좌표 값: {jb_xy}')
                except Exception as e:
                    pyautogui.alert('증빙구분(3) 이미지를 인식하지 몬함')
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
            n=0
            while True:
                if self.close_signal:
                    break
                print(n, '임의등록 확인창 찾는 중')
                n += 1
                enter_1 = pyautogui.locateOnScreen(os.path.join(DT.BASE_DIR, 'rsc', 'singo', 'enter_1.jpg'), confidence= 0.5)   
                if enter_1:
                    print('임의등록을 하겠습니까? => 버튼 확인함')
                    break
                time.sleep(0.3)
            pyautogui.press('enter')
            n=0
            while True:
                if self.close_signal:
                    break
                print(n, '저장되었습니다 확인창 찾는 중')
                n += 1
                enter_2 = pyautogui.locateOnScreen(os.path.join(DT.BASE_DIR, 'rsc', 'singo', 'enter_2.jpg'), confidence= 0.5)
                if enter_2:
                    print('저장되었습니다. => 버튼 확인함')
                    break
                time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(0.2)                    
        pyautogui.alert('끝')
        

    def program_exit(self):
        self.close_signal = True
        print('멀티 CCTV 종료')

    def btn1(self):
        '''버튼 클릭'''
        print('버튼1 클릭')

    def btn2(self):
        '''버튼 클릭'''
        print('버튼2 클릭')
    
    def btn3(self):
        '''버튼 클릭'''
        print('버튼3 클릭')

    def btn4(self):
        '''버튼 클릭'''
        print('버튼4 클릭')

    def btn5(self):
        '''버튼 클릭'''
        print('버튼5 클릭')

    def btn6(self):
        '''버튼 클릭'''
        print('버튼6 클릭')

    


    ####################     
    # 멀티프로세싱 함수 #
    ####################

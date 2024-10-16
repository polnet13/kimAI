import subprocess
import sys
import json
from PySide6.QtWidgets import QMainWindow, QFileDialog  
from PySide6.QtCore import QTimer, Qt 
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6 import QtGui
from PySide6.QtGui import QKeySequence, QShortcut  
from PySide6.QtCore import Qt
from rsc.ui.untitled_ui import Ui_MainWindow
# 외부 모듈
import os, time
import cv2
import torch
import pandas as pd
# 사용자
from control import tools
from views import generic
from views.sharedData import DT
from views.tab.cctv_multi import CCTV 
from views.tab.mosaic_v2 import Mosaic 
from views.tab.settings import Settings
from views.tab.bike import Bike 
from views.tab.home import Home 
from views.tab.singo import Chuldong 





class mainWindow(QMainWindow, Ui_MainWindow):  

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1179,612)
        
        # 로드 탭
        self.tab_home = Home()
        self.stackedWidget.addWidget(self.tab_home)
        json_path = os.path.join(DT.BASE_DIR, 'rsc', 'json', 'options.json')
        with open(json_path, "r") as f:
            options = json.load(f)
        self.tab_settings = Settings(options)
        self.stackedWidget.addWidget(self.tab_settings)
        self.tab_mosaic = Mosaic() 
        self.stackedWidget.addWidget(self.tab_mosaic)   
        self.tab_bike = Bike() 
        self.stackedWidget.addWidget(self.tab_bike)
        self.tab_cctv = CCTV() 
        self.stackedWidget.addWidget(self.tab_cctv)
        self.tab_singo = Chuldong() 
        self.stackedWidget.addWidget(self.tab_singo)
        # 초기 탭 설정
        index_home = self.stackedWidget.indexOf(self.tab_home)
        self.stackedWidget.setCurrentIndex(index_home)
        self.detector = self.tab_home
        # 멀티 프로세싱 관련 변수
        self.statusBar().showMessage(f'스레드: {self.thread}')
        # 메시지 박스 표시 플래그
        self.message_box_shown = False  
        # qslider 설정
        # 플레이창
        self.label.setStyleSheet("background-color: black")
        # 리스트뷰 
        # 멀티프로세싱
        self.workers = None
        self.btn_flag_multi_start = False
        self.flag_dongzip_btn = False
        # 플레이어 객체 생성
        self.player = generic.PlayerClass()
        # 삭제 예정
        #################
        ## 시그널 연결 ##
        ################
        self.btn_fileopen.clicked.connect(self.slot_btn_fileopen)
        self.btn_page_print.clicked.connect(self.slot_btn_print)
        self.btn_play.clicked.connect(self.slot_btn_play)
        self.btn_region_reset.clicked.connect(self.slot_btn_region_reset)
        # 탭 시그널 정의
        self.tab_cctv.playerOpenSignal.connect(self.player_fileopen)
        self.tab_home.playerOpenSignal.connect(self.player_fileopen)
        self.tab_mosaic.signal_frame_move.connect(self.mosaic_move_clicked)
        self.tab_singo.signalSingo.connect(self.control_singo_signal)
        # 버튼 좌 메뉴 
        self.btn_cctv.clicked.connect(self.buttonClick)
        self.btn_mosaic.clicked.connect(self.buttonClick)
        self.btn_settings.clicked.connect(self.buttonClick)
        self.btn_home.clicked.connect(self.buttonClick)
        self.btn_bike.clicked.connect(self.buttonClick)
        self.btn_112.clicked.connect(self.buttonClick)
        self.slider_delay.valueChanged.connect(self.slot_delay_valueChanged)
        self.playSlider.valueChanged.connect(self.play_slider_moved)  # 재생구간
 

        #################
        ## 단축키 함수 ##
        ################
        # A키 눌렀을 때 설정
        self.s_key = QShortcut(QKeySequence(Qt.Key_A), self)
        self.s_key.activated.connect(self.slot_btn_minusOneFrame) 
        # S키 눌렀을 때 설정
        self.s_key = QShortcut(QKeySequence(Qt.Key_S), self)
        self.s_key.activated.connect(self.slot_btn_play) 
        # D키 눌렀을 때 설정
        self.s_key = QShortcut(QKeySequence(Qt.Key_D), self)
        self.s_key.activated.connect(self.slot_btn_plusOneFrame)    
        # O키 눌렀을 때 설정
        self.d_key = QShortcut(QKeySequence(Qt.Key_O), self)
        self.d_key.activated.connect(self.slot_btn_fileopen)   
        # # 오른쪽 화살표 눌렀을 때 설정
        self.right_key = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.right_key.activated.connect(self.slot_right_key)       
        # # 왼쪽 화살표 눌렀을 때 설정
        self.left_key = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.left_key.activated.connect(self.slot_left_key)  
        # esc키 눌렀을 때 설정
        self.esc_key = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.esc_key.activated.connect(self.program_exit)   
        # delete키 눌렀을 때 설정
        self.delete_key = QShortcut(QKeySequence(Qt.Key_Delete), self)
        self.delete_key.activated.connect(self.slot_delete_key) 
        # 디텍터 버튼 숫자 단축키 456|123
        self.key_4 = QShortcut(QKeySequence(Qt.Key_4), self)
        self.key_4.activated.connect(self.btn4)
        self.key_5 = QShortcut(QKeySequence(Qt.Key_5), self)
        self.key_5.activated.connect(self.btn5)
        self.key_6 = QShortcut(QKeySequence(Qt.Key_6), self)
        self.key_6.activated.connect(self.btn6)
        self.key_1 = QShortcut(QKeySequence(Qt.Key_1), self)
        self.key_1.activated.connect(self.btn1)
        self.key_2 = QShortcut(QKeySequence(Qt.Key_2), self)
        self.key_2.activated.connect(self.btn2)
        self.key_3 = QShortcut(QKeySequence(Qt.Key_3), self)
        self.key_3.activated.connect(self.btn3)
        

    def btn1(self):
        self.detector.btn1()
 
    def btn2(self):
        self.detector.btn2()
   
    def btn3(self):
        self.detector.btn3()

    def btn4(self):
        self.detector.btn4()

    def btn5(self):
        self.detector.btn5()

    def btn6(self):
        self.detector.btn6()

    def buttonClick(self):
        '''좌 메뉴 버튼 클릭시 실행되는 함수 정의'''
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        # SHOW HOME PAGE
        if btnName == "btn_home":
            DT.index = self.stackedWidget.indexOf(self.tab_home)
            self.detector = self.tab_home
            self.change_stack(0)
        if btnName == "btn_cctv":
            DT.index = self.stackedWidget.indexOf(self.tab_cctv)
            self.detector = self.tab_cctv
            self.change_stack(0)
        if btnName == "btn_mosaic":
            DT.index = self.stackedWidget.indexOf(self.tab_mosaic)
            self.detector = self.tab_mosaic
            self.change_stack(0)
        if btnName == "btn_bike":
            DT.index = self.stackedWidget.indexOf(self.tab_bike)
            self.detector = self.tab_bike
            self.change_stack(0)
        if btnName == "btn_112":
            DT.index = self.stackedWidget.indexOf(self.tab_singo)
            self.detector = self.tab_singo
            self.change_stack(1)
        if btnName == "btn_settings":
            DT.index = self.stackedWidget.indexOf(self.tab_settings)
            self.detector = self.tab_settings
            self.change_stack(0)
        self.stackedWidget.setCurrentIndex(DT.index)

    ##############
    ## 슬롯함수 ##
    ##############
    def slot_right_key(self):
        fps = self.player.cap.get(cv2.CAP_PROP_FPS)
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)
        _curent_frame += 5*fps
        if _curent_frame > DT.total_frames:
            _curent_frame = DT.total_frames
        self.playSlider.setValue(_curent_frame)


    def slot_left_key(self):
        fps = self.player.cap.get(cv2.CAP_PROP_FPS)
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)
        _curent_frame -= 5*fps
        if _curent_frame < 0:
            _curent_frame = 0
        self.playSlider.setValue(_curent_frame)

        

    def slot_delay_valueChanged(self, value):
        self.time_delay = value
        self.label_delay_time.setText(f'{value} ms')

    def slot_btn_df_reset(self):
        '''탐지내역 초기화'''
        DT.reset()
        DT.setMoveSliderScale()
        print(DT.realsizeChecked)

    def slot_btn_print(self):
        # 현재 df.img 를 main.py의 부모 폴더에 저장
        if DT.img is None:
            return
        _fileName = os.path.join(DT.BASE_DIR, 'output', f'{DT.fileName}({DT.cap_num}).png')
        cv2.imwrite(_fileName, DT.img)
        # 저장 경로 열기
        if sys.platform.startswith('win'):
            os.startfile(_fileName)
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', _fileName])

    def slot_btn_fileopen(self):
        _fileName, _ = QFileDialog.getOpenFileName(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        if _fileName == '':
            return
        DT.fileName = _fileName
        self.player_fileopen()
        tools.plot_df_to_obj_img(DT.img, 0, DT.df)
        
    def slot_btn_minusOneFrame(self):
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)-2
        self.playSlider.setValue(_curent_frame)
        
    def slot_btn_plusOneFrame(self):
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.playSlider.setValue(_curent_frame)


    def slot_btn_play(self):
        '''
        qimage 객체로 변경해서 출력하는 것의 속도 측정
        '''
        _play_status = not DT.play_status
        DT.setPlayStatus(_play_status)
        DT.setMoveSliderScale()
        self.playSlider.setEnabled(not _play_status)
        self.slider_delay.setEnabled(not _play_status)
        if DT.play_status:
            # 타임이벤트 생성
            self.timer = QTimer()
            # self.timer.timeout.connect(self.play)
            self.timer.timeout.connect(self.play)
            self.timer.start(self.slider_delay.value())
        if DT.play_status == False:
            self.timer.stop()
            DT.detection_list_to_df()
            self.update()

    def mosaic_move_clicked(self, value):
        DT.cap_num = value
        self.playSlider.setValue(value)


    # 이벤트 감지       
    def play(self):
        '''
        핵심: slot_btn_play()에서 호출이 반복되어 프레임을 처리하고 화면에 출력
        '''
        if DT.fileName is None:
            DT.play_status = False
            return
        self.statusBar().showMessage(os.path.basename(DT.fileName))
        # 프레임을 읽어옴
        self.start_time = time.time()
        self.player.cap_read()
        # 정지 버튼이 눌렸을 때
        if DT.play_status == False:
            self.timer.stop()
            self.process_time_print()
            return 
        # 마지막 프레임일 때
        if DT.cap_num == DT.total_frames:
            DT.play_status = False
            self.timer.stop()
            DT.setCapNum(0)
        # 슬라이더 업데이트: 슬라이더 업데이트는 캡넘버만 수정하도록
        self.playSlider.setValue(DT.cap_num)
        # 이미지가 없을 때
        if DT.img is None:
            self.process_time_print()
            return
        # 분석용 이미지 선택
        img = DT.img
        DT.setOriginalShape(img.shape[:2])
        self.process_time_print()
        img = self.detector.applyImageProcessing(img) 
        self.display_img(img)

    def process_time_print(self):
        end_time = time.time()  
        time_diff = end_time - self.start_time
        if time_diff != 0:
            fps = int(1 / time_diff)
        else:
            fps = 0  # 또는 다른 적절한 방법으로 처리
        self.statusBar().showMessage(
            f'{DT.width}*{DT.height}     roi: {DT.roi[0]:.2f} {DT.roi[1]:.2f} {DT.roi[2]:.2f} {DT.roi[3]:.2f}     fps: {int(fps)}'
            )
    





    def player_fileopen(self):
        '''
        DT의 현재 파일을 불러와서 GUI에 반영하고
        디스플레이 함수 호출
        '''
        # 이미지 처리
        self.player.open(DT.fileName)
        DT.setMoveSliderScale()
        self.reset_roi()
        self.statusBar().showMessage(f'해상도: {DT.width}*{DT.height}   fps : {DT.fps}')
        # 영상의 전체 프레임수를 가지고 옴
        self.playSlider.setMaximum(DT.total_frames -1)
        self.playSlider.setValue(0)
        DT.setRoiPoint()
        self.update()
        self.display_img()

        

    def slot_btn_reset(self):
        '''관심영역 초기화'''
        print(DT.roi_point)
        if DT.img is None:
            return
        else:
            self.reset_roi()
            self.display_img()
        print(DT.roi_point)

    def reset_roi(self):
        '''
        이미지의 해상도에 꽉차는 roi를 설정함
        '''
        DT.setRegionStatus(False)
        DT.setRoi((0, 0, 1, 1))
        DT.setRoiPoint()
        self.label_roi_update()
        self.statusBar().showMessage(f'roi0: {DT.roi_point[0]}   roi1: {DT.roi_point[1]}')
        
    
    #####################
    ## 단축키 실행 함수 ##
    #####################
    def reverse_status_change(self):
        self.reverse_status = not self.reverse_status
 
    def slot_delete_key(self):
        '''delete_tableview_row'''
        self.detector.delete_key()
 
    def change_stack(self, index):
        '''
        0: 플레이어
        1: 테이블
        '''
        self.stackedWidget_play.setCurrentIndex(index)
        
    ##################    
    # 플레이 슬라이더 #
    ##################
    def play_slider_moved(self, value):
        '''
        stop 상태에서만 슬러이더 움직일 수 있음
        '''
        # 공통 코드 
        if DT.play_status == False:
            self.player.cap.set(cv2.CAP_PROP_POS_FRAMES, value)
            DT.cap_num = value
            self.player.cap_read()
            self.detector.applyImageProcessing(DT.img)
            self.display_img()
    

    def program_exit(self):
        '''워커와 GUI 종료'''
        if self.detector is not None:
            self.detector.program_exit()
        self.close()        


    ############
    ## 마우스 ##
    ############
    # 마우스 왼쪽 버튼이 눌렸을 때의 동작
    def mousePressEvent(self, event):
        '''
        실제 좌표(a,b)를 받아서 디스플레이 이미지의 좌표로 변환
        '''

        if DT.play_status:
            return
        if DT.img is None:
            return
        x, y = event.pos().x(), event.pos().y()
        print(x, y)
        # a, b값이 play창 밖이면 무시하도록(720*480 기준)
        if x < 70 or x > 790 or y < 10 or y > 490:
            return
        x, y = tools.shape_to_adjust(x, y)  # gui 오차 보정
        if event.button() == Qt.LeftButton:
            DT.setRoi((x, y, DT.roi[2], DT.roi[3]))
          
    def mouseMoveEvent(self, event):
        img = None
        if DT.play_status:
            return
        x, y = event.pos().x(), event.pos().y()
        # a, b값이 play창 밖이면 무시하도록
        if x < 70 or x > 790 or y < 10 or y > 490 or DT.img is None:
            return
        if DT.img is None:
            return
        x, y = tools.shape_to_adjust(x, y)
        img = DT.img.copy()
        DT.setRoi((DT.roi[0], DT.roi[1], x, y))
        x1, y1, x2, y2 = DT.roi[0], DT.roi[1], DT.roi[2], DT.roi[3]
        x1, y1, x2, y2 = tools.sort_roi(x1, y1, x2, y2)
        DT.setRoi((x1, y1, x2, y2))
        # 영상비율 자동 조절되도록 수정 필요
        self.display_img(img)
        self.label_roi_update()
  
    # 마우스 왼쪽 버튼이 떼졌을 때의 동작
    def mouseReleaseEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        x, y = tools.shape_to_adjust(x, y)
        if DT.img is None:
            return
        # a, b값이 play창 밖이면 무시하도록
        if x < 70 or x > 790 or y < 10 or y > 490:
            return
        if DT.play_status:
            return
        # a, b값을 gui좌표에서 백분율로 변환
        img = DT.img
        _, _, x, y = tools.abs_to_rel(img.shape, DT.roi[0], DT.roi[1], x, y, )
        # 마우스 왼쪽 버튼이 떼지고 재생중이 아닐 때
        if (event.button() == Qt.LeftButton):
            DT.region_status = True
            self.drawing = False  #???? 뭐지??
            DT.setRoi((DT.roi[0], DT.roi[1], x, y))
        x1, y1, x2, y2 = DT.roi[0], DT.roi[1], DT.roi[2], DT.roi[3]
        x1, y1, x2, y2 = tools.sort_roi(x1, y1, x2, y2)
        DT.setRoi((x1, y1, x2, y2))
        DT.setRoiPoint()
        DT.setMoveSliderScale()
        self.slot_btn_df_reset()
        self.display_img(img)
        self.label_roi_update()
    
    ##################
    ## GUI 업데이트 ##
    ##################
    def label_roi_update(self):
        '''
        디스플레이창에 roi 좌표를 출력하고
        roi 갱신으로 욜로모델도 갱신함(트래킹시 이미지 사이즈 변경되면 욜로 오류발생 방지)
        '''
        x1, y1, x2, y2 = DT.roi
        self.statusBar().showMessage(
            f'{DT.width}*{DT.height}     roi: {DT.roi[0]:.2f} {DT.roi[1]:.2f} {DT.roi[2]:.2f} {DT.roi[3]:.2f}'
            )
        self.update()
        
    def display_img(self, img=None):
        '''
        최종적으로 roi를 표시한 이미지를 출력하는 함수
        img를 입력 받으면 입력받은 이미지를 출력하고, 입력받지 않으면 self.img를 출력
        '''
        if img is None:
            plot_img = DT.img.copy()
        else:
            plot_img = img.copy()
        # ROI 좌표가 모두 있는지 확인
        roi = DT.roi_point[0]
        if roi[0] is None or roi[2] is None or roi[1] is None or roi[3] is None:
            pass
        else:
            cv2.rectangle(plot_img, (roi[0], roi[1]),(roi[2], roi[3]), DT.roi_color, 2)
        # 욜로 감지된 경우(구현 예정)
        # plot 이미지의 x축이 680 넘어가면 비율대로 x를 680 맞춤
        if plot_img.shape[1] > 680:
            plot_img = tools.resize_img(plot_img, 680)
        self.label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(plot_img.data, plot_img.shape[1], plot_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()))
        self.label.setScaledContents(True)
        self.label_cap_num.setText(f'{DT.cap_num} / {DT.total_frames}')
        frameTimer = time.strftime('%H:%M:%S', time.gmtime(DT.cap_num/DT.fps))
        self.playTimer.setText(f'{frameTimer}')
        self.label.update()
        
    ##########
    ## 기타 ##
    ##########            
    def slot_btn_region_reset(self):
        if DT.img is None:
            return
        else:
            self.reset_roi()
            self.display_img()
 

    def slot_btn_pageprint(self):
        pass
        
    
    # def signal_6(self, value):
    #     self.progressChanged(int(value))
        
    
    ##################
    # 테이블뷰 컨트롤 #
    ##################
    def control_singo_signal(self, value):
        '''tab_singo 시그널을 받아서 분기해주는 함수'''
        if value == 1:
            self.df_to_tableview()
        elif value == 2:
            self.delete_tableview_row()

    def df_to_tableview(self):
        '''DT.df_main 을 테이블뷰에 출력'''
        if DT.df_main is None:
            import pandas as pd
            DT.df_main = pd.DataFrame({
                '접수번호':[1222222,1224542,1222222,44444444,55555555],
                '신고내용':['테스트','test','동해물과','344','555'],
                '종결내용':[2,2,333,344,555],
                '종결보고자':['유비 관우 장비','보라 나은 한석','유비 유모비 라엘','나은 경미 상미','원철 영철 김훈'],
                '사건번호':[22262,33332,33443,34554,556665],
                '접수시간':[2,2,333,344,555],
                '코드':[0,1,2,3,4],
                '종결':[2,2,333,344,555]
                })
        df = DT.df_main
        columns = df.columns
        qmodel_ = QtGui.QStandardItemModel()
        qmodel_.setColumnCount(len(columns))
        qmodel_.setHorizontalHeaderLabels(columns)
        for row in range(len(df)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in df.iloc[row]]
            qmodel_.appendRow(value_objs)
        self.tableView.setModel(qmodel_)
        self.update()

    def delete_tableview_row(self):
        '''
        tab_singo 시그널을 받고 테이블뷰에서 선택된 행 삭제
        - DT_df_main 에서 삭제 하고 테이블뷰에 반영하는 코드임
        '''
        index = self.tableView.currentIndex().row()
        DT.df_main = DT.df_main.drop(index).reset_index(drop=True)
        self.df_to_tableview()

        
 
   




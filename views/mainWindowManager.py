import subprocess
import sys
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QGridLayout, QHBoxLayout, QComboBox
from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout, QSlider, QTableView, QHeaderView
from PySide6.QtWidgets import QWidget, QScrollArea, QMessageBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6 import QtGui
from PySide6.QtGui import QKeySequence, QShortcut  
from PySide6.QtCore import Qt
from rsc.ui.untitled_ui import Ui_MainWindow
# 외부 모듈
import os, time
import cv2
from multiprocessing import Process, Queue
# 사용자
from control import tools
from views import enrolled, generic
from views.sharedData import DT
from views.enrolled.cctv_multi import CCTV, MultiCCTV
from views.enrolled.bike import Bike, DetectorBike
from views.enrolled.mosaic_v2 import Mosaic, DetectorMosaic_v2  
import pandas as pd





class mainWindow(QMainWindow, Ui_MainWindow):  

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # 로드 탭
        self.tab_mosaic = Mosaic() 
        self.stackedWidget.addWidget(self.tab_mosaic)   
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_mosaic))
        self.tab_bike = Bike() 
        self.stackedWidget.addWidget(self.tab_bike)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_bike))
        self.tab_cctv = CCTV() 
        self.stackedWidget.addWidget(self.tab_cctv)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_cctv))
        self.tab_cctv.playerOpenSignal.connect(self.player_fileopen)
        self.detector = self.tab_cctv


        # 멀티 프로세싱 관련 변수
        
        self.statusBar().showMessage(f'스레드: {self.thread}')
        # 메시지 박스 표시 플래그
        self.message_box_shown = False  
        # qslider 설정
        self.playSlider.valueChanged.connect(self.play_slider_moved)  # 재생구간
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
        # 버튼 좌 메뉴 
        self.btn_home.clicked.connect(self.buttonClick)
        self.btn_cctv.clicked.connect(self.buttonClick)
        self.btn_bike.clicked.connect(self.buttonClick)
        self.btn_mosaic.clicked.connect(self.buttonClick)
        self.btn_temp1.clicked.connect(self.buttonClick)
        self.btn_settings.clicked.connect(self.buttonClick)
 

        #################
        ## 단축키 함수 ##
        ################
        # 아래 화살표를 눌렀을 때 설정
        self.down_key = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.down_key.activated.connect(self.tableview_df_down)
        # 위 화살표를 눌렀을 때 설정
        self.up_key = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.up_key.activated.connect(self.tableview_df_up)
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
        # 오른쪽 화살표 눌렀을 때 설정
        self.right_key = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.right_key.activated.connect(self.plus_gap)       
        # 왼쪽 화살표 눌렀을 때 설정
        self.left_key = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.left_key.activated.connect(self.minus_gap)  
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
            self.stackedWidget.setCurrentWidget(self.stack_home)
            self.detector = None
        if btnName == "btn_cctv":
            self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_cctv))
            self.detector = self.tab_cctv
        if btnName == "btn_mosaic":
            self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_mosaic))
            self.detector = self.tab_mosaic
        if btnName == "btn_bike":
            self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.tab_bike))
            self.detector = self.tab_bike
        if btnName == "btn_temp1":
            self.stackedWidget.setCurrentWidget(self.stack_temp)
            self.detector = None
        if btnName == "btn_settings":
            self.stackedWidget.setCurrentWidget(self.stack_settings)
            self.detector = None    

    ##############
    ## 슬롯함수 ##
    ##############
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
        tools.plot_df_to_obj_img(DT.img, 0)
        
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
        delay = DT.time_delay
        _play_status = not DT.play_status
        DT.setPlayStatus(_play_status)
        DT.setMoveSliderScale()
        self.playSlider.setEnabled(not _play_status)
        if DT.play_status:
            # 타임이벤트 생성
            self.timer = QTimer()
            # self.timer.timeout.connect(self.play)
            self.timer.timeout.connect(self.play)
            self.timer.start(delay)
        if DT.play_status == False:
            self.timer.stop()
            DT.detection_list_to_df()
            self.update()


    # 이벤트 감지       
    def play(self):
        '''
        핵심: slot_btn_play()에서 호출이 반복되어 프레임을 처리하고 화면에 출력
        '''
        if DT.fileName is None:
            DT.play_status = False
            return
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
        x1, y1, x2, y2 = DT.roi_point[0]
        frameTimer = time.strftime('%H:%M:%S', time.gmtime(DT.cap_num/DT.fps))
        self.playTimer.setText(f'{frameTimer}')
        self.label_cap_num.setText(f'프레임 번호 : {DT.cap_num}')
        #
        if DT.selected_mode == 'bike':
            # 초기화
            self.text_si.clear()
            self.text_giho.clear()
            self.text_num.clear()
            self.text_si.setText(DT.bike_si)
            self.text_giho.setText(DT.bike_giho)
            self.text_num.setText(str(DT.bike_num))
        self.process_time_print()
        img = self.detector.playplot(img)
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
        self.statusBar().showMessage(f'파일 경로: {DT.fileName}')
        # 영상의 전체 프레임수를 가지고 옴
        self.label_xy_.setText(f'해상도: {DT.width}*{DT.height}')
        self.playSlider.setMaximum(DT.total_frames -1)
        self.label_fps_.setText(f'fps : {DT.fps}')
        DT.setRoiPoint()
        self.update()
        self.display_img()
        

    def slot_btn_reset(self):
        '''관심영역 초기화'''
        print(DT.roi_point)
        if DT.img is None:
            self.label_roi.setText(f'관심영역: {DT.region_status}') 
            self.update()
        else:
            self.reset_roi()
            self.display_img()
        print(DT.roi_point)

    def reset_roi(self):
        '''
        이미지의 해상도에 꽉차는 roi를 설정함
        '''
        print(DT.roi_point)
        DT.setRegionStatus(False)
        DT.setRoi((0, 0, 1, 1))
        DT.setRoiPoint()
        self.label_roi_update()
        print(DT.roi_point)
        
    
    #####################
    ## 단축키 실행 함수 ##
    #####################
    def reverse_status_change(self):
        self.reverse_status = not self.reverse_status
    # 점프 프레임값 +3    
    def plus_gap(self):
        self.jump_frameSlider.setValue(self.jump_frameSlider.value() + 3)
    # 점프 프레임값 -3    
    def minus_gap(self):
        self.jump_frameSlider.setValue(self.jump_frameSlider.value() - 3)
    # 테이블뷰 선택된 행 삭제
    def slot_delete_key(self):
        '''delete_tableview_row'''
        self.detector.slot_delete_key()

    # 리스트뷰 항목 클릭시 해당 프레임으로 이동
    def on_item_clicked(self, index):
        # 해당 위치의 항목을 가져옴
        row = index.row()
        # 항목의 텍스트를 가져옴
        n = self.qmodel_mosaic_frame.item(row, 0).text()
        n = float(n)
        # slider 위치를 n 값으로 이동
        self.playSlider.setValue(n) 
        self.player.cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        self.player.cap_read()
        img = DT.img
        # cap_num 에 맞춰 바운딩 박스 그림
        if DT.play_status is False:
            cap_num = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES) -1
            img = tools.plot_df_to_obj_img(img, cap_num)        
            self.display_img(img)

    def tableview_df_down(self):
        # 테이블뷰에서 아래행으로 이동
        if self.tableView_mosaic_frame.hasFocus():
            row = self.tableView_mosaic_frame.currentIndex().row()
            row += 1
            self.tableView_mosaic_frame.selectRow(row)
        # 항목의 텍스트를 가져옴
        if self.qmodel_mosaic_frame.item(row, 0) is None:
            return
        n = self.qmodel_mosaic_frame.item(row, 0).text()
        n = float(n)
        # slider 위치를 n 값으로 이동
        self.playSlider.setValue(n) 
        self.player.cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        self.player.cap_read()
        img = DT.img
        # cap_num 에 맞춰 바운딩 박스 그림
        if DT.play_status is False:
            cap_num = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES) -1
            img = DT.detector.plot_df_to_img(img, cap_num)        
            self.display_img(img)

    def tableview_df_up(self):
        if self.tableView_mosaic_frame.hasFocus():
            row = self.tableView_mosaic_frame.currentIndex().row()
            row -= 1
            self.tableView_mosaic_frame.selectRow(row)
        if self.qmodel_mosaic_frame.item(row, 0) is None:
            return
        # 항목의 텍스트를 가져옴
        n = self.qmodel_mosaic_frame.item(row, 0).text()
        n = float(n)
        # slider 위치를 n 값으로 이동
        self.playSlider.setValue(n) 
        self.player.cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        self.player.cap_read()
        img = DT.img
        # cap_num 에 맞춰 바운딩 박스 그림
        if DT.play_status is False:
            cap_num = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES) -1
            img = DT.detector.plot_df_to_img(img, cap_num)       
            self.display_img(img)
        
        
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
            self.player.cap_read()
            self.display_img()
        
    def jump_frameSlider_moved(self, value):
        self.label_frame_gap.setText(str(value)) # label7 = self.jump_frameSlider 값
    
    def Slider_bright_moved(self, value):
        self.label_bright.setText(str(value))

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
        self.label_cap_num.setText(f'프레임 번호 : {DT.cap_num}')
        self.label.update()
        
    ##########
    ## 기타 ##
    ##########            
    def slot_btn_region_reset(self):
        if DT.img is None:
            self.label_roi.setText(f'관심영역: {DT.region_status}') 
            self.update()
        else:
            self.reset_roi()
            self.display_img()
 

    def slot_btn_pageprint(self):
        pass
        
    
    ############
    # 모자이크 #
    ############
    def signal_start_point(self, value):
        # 시작 버튼명을 f'시작({value})'로 변경
        self.btn_mosaic_start.setText(f'시작({value})')

    def signal_end_point(self, value):
        # 종료 버튼명을 f'시작({value})'로 변경
        if value+1 < DT.start_point:
            return
        self.btn_mosaic_end.setText(f'종료({value})')

    def frame_list_to_listview(self):
        '''frame_list를 리스트뷰에 출력'''
        frame_list = DT.df_plot
        self.listView_mosaic.clear()
        for frame in frame_list:
            self.listView_mosaic.addItem(str(frame))
        self.update()

    def update_label(self, value, selected_menu_text, label1, label2, arg):
        label1.setText(str(value))  # 버튼명
        DT.sliderDict[selected_menu_text][arg] = value
        if arg == '지연':
            DT.time_delay = value
        print(value)

    
    def signal_6(self, value):
        self.progressChanged(int(value))
        
    
    #########################
    # 테이블뷰 선택된 행 삭제 #
    #########################
    def delete_tableview_row(self):
        index = self.tableview_df.currentIndex().row()
        # 디텍터 마다 테이블 삭제시 작동하는 함수를 다르게 하기 위해서 detector에 위임함
        DT.df.drop(index).reset_index(drop=True)
        # 테이블뷰 다시 출력
        self.df_to_tableview()
        self.tableview_df.update()
        
 
    # df => 리스트뷰
    
 
    def mosaic_analyze_percent(self):
        start = DT.start_point
        end = DT.end_point
        curent_frame = DT.mosaic_current_frame
        if start <= curent_frame <= end:
            percent = (curent_frame - start) / (end - start) * 100
            self.progressBar_mosaic.setValue(percent)
        else:
            self.progressBar_mosaic.setValue(100)
        self.update()
    





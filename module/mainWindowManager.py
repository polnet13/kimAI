import subprocess
import sys
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QScrollArea, QMessageBox


# 웹 바로가기
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6 import QtGui
# 단축키
from PySide6.QtGui import QKeySequence, QShortcut  
from PySide6.QtCore import Qt
# 외부 모듈
import os, time
import cv2
from multiprocessing import Process, Queue
# 사용자
from control import tools
from module import enrolled, generic
from rsc.ui.untitled_ui import Ui_MainWindow
from PySide6.QtUiTools import QUiLoader   
import settings
from module.sharedData import DT
from module.modelLoader import ModelClass
from module import cctv_multi



class Worker(Process):
    '''
    멀티 작업 클래스
    '''
    def __init__(self):
        super().__init__()
        self.queue = None
        self.obj = None

    def run(self):
        self.obj.queue = self.queue
        self.obj.multi_process()


class mainWindow(QMainWindow, Ui_MainWindow):  
    '''
    UI 컨트롤 관련 클래스
    영상부 해상도 680*480
    '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 멀티 프로세싱 관련 변수
        self.num_cores = os.cpu_count()
        self.statusBar().showMessage(f'코어 수: {self.num_cores}')
        # 메시지 박스 표시 플래그
        self.message_box_shown = False  
        self.checkbox_yolo.setChecked(True)
        # qslider 설정
        self.playSlider.valueChanged.connect(self.play_slider_moved)  # 재생구간
        # 플레이창
        self.label.setStyleSheet("background-color: black")
        # 리스트뷰 
        self.tableView.clicked.connect(self.on_item_clicked)
        # # CCTV 분석기 초기화
        # self.img = cv2.imread(DT.fileName)
        # 멀티프로세싱
        self.workers = None
        self.flag_start_btn = False
        self.flag_dongzip_btn = False
        # 플레이어 객체 생성
        self.player = generic.PlayerClass()
        # 모델 드롭다운 메뉴
        detectors = tools.get_classes(enrolled)
        for detector in detectors:
            DT.setSliderValue(detector.tag, detector.slider_dict)
            DT.enrollDetectors(detector.tag, detector)
        self.modelclass = ModelClass()
        self.frame_option.addLayout(self.modelclass.layout, 11)

 
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
        self.delete_key.activated.connect(self.delete_listview_row) 


    ##############
    ## 슬롯함수 ##
    ##############
    def slot_btn_fileopen(self):
        _fileName, _ = QFileDialog.getOpenFileName(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        DT.setFileName(_fileName)
        DT.selected_mode = self.modelclass.combo_box.currentText()
        columns = DT.detector_dict[DT.selected_mode].columns
        DT.setDf(columns)
        self.player_fileopen()
        self.df_to_tableview()
        tools.plot_df_to_obj_img(DT.img, 0)
        

    def slot_btn_minusOneFrame(self):
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)-2
        self.playSlider.setValue(_curent_frame)
        

    def slot_btn_plusOneFrame(self):
        _curent_frame = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.playSlider.setValue(_curent_frame)


    def slot_btn_open_complete(self):
        path = os.path.join(settings.BASE_DIR, 'output')
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', path])



    def slot_btn_play(self):
        '''
        qimage 객체로 변경해서 출력하는 것의 속도 측정
        '''
        _play_status = not DT.play_status
        DT.setPlayStatus(_play_status)
        self.playSlider.setEnabled(not _play_status)
        if DT.play_status:
            # 타임이벤트 생성
            self.timer = QTimer()
            # self.timer.timeout.connect(self.play)
            self.timer.timeout.connect(self.play)
            self.timer.start(1)
        else:
            self.timer.stop()


    # 이벤트 감지       
    def play(self):
        '''
        핵심: slot_btn_play()에서 호출이 반복되어 프레임을 처리하고 화면에 출력
        '''
        # 프레임을 읽어옴
        self.player.cap_read()
        # 정지 버튼이 눌렸을 때
        if DT.play_status == False:
            self.timer.stop()
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
            return
        # 재생시간 업데이트
        frameTimer = time.strftime('%H:%M:%S', time.gmtime(DT.cap_num/DT.fps))
        self.playTimer.setText(f'{frameTimer}')
        #######################################################################
        # 분석용 이미지로 처리
        if self.check_realsize.isChecked():
            img = DT.img
            x1, y1, x2, y2 = DT.roi_point[0]
            print(x1, y1, x2, y2)
        else:
            img = tools.resize_img(DT.img, 680)
            x1, y1, x2, y2 = DT.roi_point[1]
        roi_img = img[y1:y2, x1:x2]
        roi_img, move_detect_bool = DT.detector.detect_move(roi_img)
        # 움직임이 없는 경우 원본 이미지 출력
        if move_detect_bool == False:
            self.display_img(img, (0,0,255))
            return
        #######################################################################
        # ROI 부분만 욜로 디텍션
        #######################################################################
        if self.checkbox_yolo.isChecked():
            # 이후 추가 디텍션은 원본이미지로 수행함
            roi_img, text  = DT.detector.detect_yolo_track(roi_img, DT.cap_num)
            # roi_img 사용 : cctv, multicctv
            # roi 무시: bike, 모자이크함
            if text:
                self.textBrowser.append(text)
                self.textBrowser.setFocus()
            if not DT.df.empty:
                self.df_to_tableview() 
        #################################################################################
        # self.img에 roi_img를 붙여서 출력
        img[y1:y2, x1:x2] = roi_img
        self.label_cap_num.setText(f'프레임 번호 : {DT.cap_num}')
        #
        self.display_img(img, (0,255,0))


    def slot_btn_multi_open(self):
        '''
        동집 버튼을 누르면
        큐(실질적인 동영상 압축 작업)와 프로그래스바를 생성하고,
        '''
        # 탭 위젯 2번째 탭으로 이동
        self.tabWidget.setCurrentIndex(1)
        self.textBrowser.clear()
        
        if self.flag_dongzip_btn is True:
            return
        self.flag_dongzip_btn = True
        fileNames, _ = QFileDialog.getOpenFileNames(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        DT.setFileNames(fileNames)
        if len(DT.fileNames) == 0:
            self.flag_dongzip_btn = False
            self.textBrowser.append('동영상 파일이 선택되지 않았습니다.')
            return
        # fileNames의 파일들의 용량을 확인하고 용량이 큰 순서대로 정렬
        DT.fileNames = tools.sort_files_by_size(DT.fileNames)
        _fileName = DT.fileNames[0]
        DT.setFileName(_fileName)
        self.player_fileopen()
        self.make_queue_and_progress_bars(DT.fileNames)


    def player_fileopen(self):
        '''
        DT의 현재 파일을 불러와서 GUI에 반영하고
        디스플레이 함수 호출
        '''
        # 이미지 처리
        self.player.open(DT.fileName)
        self.reset_roi()
        self.statusBar().showMessage(f'파일 경로: {DT.fileName}')
        # 영상의 전체 프레임수를 가지고 옴
        self.label_xy.setText(f'해상도: {DT.width}*{DT.height}')
        self.playSlider.setMaximum(DT.total_frames -1)
        self.label_fps.setText(f'fps : {DT.fps}')
        DT.setRoiPoint(DT.img.shape)
        self.update()
        self.display_img()
        


        
    def start_multi(self):
        '''
        백그라운드 워커을 실행하고,
        프로그레스바를 업데이트하는 타이머를 실행
        '''
        if self.flag_start_btn is True:
            return
        # 메뉴 넘버 따오는 함수 추가예정
        self.objects = [cctv_multi.MultiCCTV(file) for file in DT.fileNames]
        self.object_queue_to_worker()
        self.run_workers()
        self.flag_start_btn= True
        self.startBtn.setText('동영상 압축 중...')
        self.completed_count = 0
        # 백그라운드 워커(실질적인 영상 압축 코드)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  




 
    def slot_btn_reset(self):
        if DT.img is None:
            self.label_roi.setText(f'관심영역: {DT.region_status}') 
            self.update()
        else:
            self.reset_roi()
            self.display_img()


    def reset_roi(self):
        '''
        이미지의 해상도에 꽉차는 roi를 설정함
        '''
        DT.setRegionStatus(False)
        DT.setRoi((0, 0, 1, 1))
        yx = (DT.height, DT.width)
        DT.setRoiPoint(yx)
        self.label_roi_update()
        
    
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
    def delete_listview_row(self):
        index = self.tableView.currentIndex().row()
        print(f'테이블 index: {index}')
        # 디텍터 마다 테이블 삭제시 작동하는 함수를 다르게 하기 위해서 detector에 위임함
        DT.detector.drop(index, inplace=True)
        # 테이블뷰 다시 출력
        self.df_to_tableview()
        self.update()
        
    # 리스트뷰 항목 클릭시 해당 프레임으로 이동
    def on_item_clicked(self, index):
        # 해당 위치의 항목을 가져옴
        row = index.row()
        # 항목의 텍스트를 가져옴
        n = self.qmodel.item(row, 1).text()
        n = float(n)
        # slider 위치를 n 값으로 이동
        self.playSlider.setValue(n) 
        self.player.cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        img = self.player.cap.read()[1]
        # cap_num 에 맞춰 바운딩 박스 그림
        if DT.play_status is False:
            cap_num = self.player.cap.get(cv2.CAP_PROP_POS_FRAMES) -1
            img = tools.plot_df_to_obj_img(img, cap_num)
        
        self.display_img(img)
        print(f'row: {row}, n: {n}')
        
        
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
            DT.setCapNum(value)
            self.player.cap_read()
            self.display_img()
        

        
            
    def jump_frameSlider_moved(self, value):
        self.label_frame_gap.setText(str(value)) # label7 = self.jump_frameSlider 값
        
    def thr_slider_move_moved(self, value):
        self.move_thr = value
        self.label_thr_move.setText(str(value)) # label4 = self.thrSlider 값


    def Slider_bright_moved(self, value):
        self.label_bright.setText(str(value))
    

    # df => 리스트뷰
    def df_to_tableview(self):
        # 모델 초기화를 데터 추가 전에 수행
        self.qmodel = QtGui.QStandardItemModel()  # 초기 행과 열의 수를 설정하지 않음
        columns = DT.df.columns
        self.qmodel.setColumnCount(len(columns))
        self.qmodel.setHorizontalHeaderLabels(columns)
        for row in range(len(DT.df)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in DT.df.iloc[row]]
            self.qmodel.appendRow(value_objs)
        self.tableView.setModel(self.qmodel)



    def program_exit(self):
        '''워커와 GUI 종료'''
        self.terminate_workers()
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
        # a, b값이 play창 밖이면 무시하도록
        if x < 40 or x > 760 or y < 40 or y > 520:
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
        if x < 40 or x > 760 or y < 40 or y > 520 or DT.img is None:
            return
        if DT.img is None:
            return
        x, y = tools.shape_to_adjust(x, y)
        if self.check_realsize.isChecked():
            img = DT.img.copy()
        else:
            img = tools.resize_img(DT.img, 680)
        DT.setRoi((DT.roi[0], DT.roi[1], x, y))
        x1, y1, x2, y2 = DT.roi[0], DT.roi[1], DT.roi[2], DT.roi[3]
        x1, y1, x2, y2 = tools.sort_roi(x1, y1, x2, y2)
        DT.setRoi((x1, y1, x2, y2))
        DT.setRoiPoint(img.shape)
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
        if x < 40 or x > 760 or y < 40 or y > 520:
            return
        if DT.play_status:
            return
        # a, b값을 gui좌표에서 백분율로 변환
        if self.check_realsize.isChecked():
            img = DT.img
        else:
            img = tools.resize_img(DT.img, 680)
        _, _, x, y = tools.abs_to_rel(img.shape, DT.roi[0], DT.roi[1], x, y, )
        # 마우스 왼쪽 버튼이 떼지고 재생중이 아닐 때
        if (event.button() == Qt.LeftButton):
            DT.region_status = True
            self.drawing = False  #???? 뭐지??
            DT.setRoi((DT.roi[0], DT.roi[1], x, y))

        x1, y1, x2, y2 = DT.roi[0], DT.roi[1], DT.roi[2], DT.roi[3]
        x1, y1, x2, y2 = tools.sort_roi(x1, y1, x2, y2)
        DT.setRoi((x1, y1, x2, y2))
        DT.setRoiPoint(img.shape)
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
        self.label_roi.setText(f'관심영역(x1,y1,x2,y2): {x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}') 
        self.update()
        
    def display_img(self, img=None, color=(0, 0, 255)):
        '''
        최종적으로 roi를 표시한 이미지를 출력하는 함수
        img를 입력 받으면 입력받은 이미지를 출력하고, 입력받지 않으면 self.img를 출력
        '''

        if img is None:
            plot_img = DT.img.copy()
        else:
            plot_img = img.copy()
        # ROI 좌표가 모두 있는지 확인
        if DT.roi_point[1][0] is None or DT.roi_point[1][2] is None or DT.roi_point[1][1] is None or DT.roi_point[1][3] is None:
            pass
        else:
            cv2.rectangle(plot_img, (DT.roi_point[1][0], DT.roi_point[1][1]),(DT.roi_point[1][2], DT.roi_point[1][3]), color, 2)
        # 욜로 감지된 경우(구현 예정)
        # plot 이미지의 x축이 680 넘어가면 비율대로 x를 680 맞춤
        if plot_img.shape[1] > 680:
            plot_img = tools.resize_img(plot_img, 680)
        self.label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(plot_img.data, plot_img.shape[1], plot_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()))
        self.label.setScaledContents(True)
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

    def slot_btn_multi_reset(self):
        DT.fileNames = []
        self.flag_dongzip_btn = False
        self.flag_start_btn = False
        self.clear_status_bars()
        self.terminate_workers()
        self.update()


    def slot_btn_pageprint(self):
        pass
        
    ####################     
    # 멀티프로세싱 함수 #
    ####################
    def make_queue_and_progress_bars(self, fileNames):
        print('make_queue_and_progress_bars')
        '''큐(통신)와 프로그레스 바, 워커 생성 '''
        # 상태바 제거
        self.clear_status_bars()
        # 스크롤 가능한 프로그레스 바 위젯 생성
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.vLayout_dongzip_statusbar.addWidget(scroll_area)
        self.len_filenames = len(fileNames)
        self.startBtn = QPushButton(f'작업 시작')
        scroll_layout.addWidget(self.startBtn)

        cap = cv2.VideoCapture(fileNames[0])
        self.img_shape = cap.read()[1].shape
        self.startBtn.clicked.connect(self.start_multi)
        # 큐, 프로그래스 바, 워커 생성
        self.progress_bars = []
        self.queues = []
        self.workers = []
        for i in range(self.len_filenames):
            # 큐 생성
            queue = Queue()
            self.queues.append(queue)
            # 프로그래스바 생성
            progress_bar = QProgressBar()
            self.progress_bars.append(progress_bar)
            scroll_layout.addWidget(progress_bar)
            # 워커 생성
            worker = Worker()
            self.workers.append(worker)


        
    def object_queue_to_worker(self):
        '''객체와 큐 연결 '''
        for i in range(len(self.workers)):
            self.workers[i].queue = self.queues[i]
            self.workers[i].obj = self.objects[i]
        
    
    def terminate_workers(self):
        '''모든 워커를 종료'''
        if self.workers is not None:
            for worker in self.workers:
                if worker.is_alive():
                    worker.terminate()

 

    def clear_status_bars(self):
        '''상태바를 모두 제거'''
        for i in reversed(range(self.vLayout_dongzip_statusbar.count())):  
            widget = self.vLayout_dongzip_statusbar.itemAt(i).widget()
            if widget is not None:  # 위젯이 있는 경우
                widget.deleteLater()  # 위젯 제거


    def run_workers(self):
        '''워커 시작: 멀티프로세스 열일 시작'''
        self.active_workers = 0
        for _ in range(min(int(self.num_cores) - 1, len(DT.fileNames))):  # 코어 수 - 2개의 작업을 시작
            self.workers[self.active_workers].x1 = DT.roi[0]
            self.workers[self.active_workers].x2 = DT.roi[2]
            self.workers[self.active_workers].y1 = DT.roi[1]
            self.workers[self.active_workers].y2 = DT.roi[3]
            self.workers[self.active_workers].start()
            self.active_workers += 1


    def update_progress(self):
        '''진행 상태 업데이트'''
        for i in range(self.active_workers):
            while not self.queues[i].empty():
                msg = self.queues[i].get()
                if msg[0] == 'done':
                    # 워커 종료시
                    file = os.path.basename(msg[4])
                    one_page_summary = (f'{file}\n{round(msg[1]/msg[3],1)}초 => {round(msg[2]/msg[3],1)}초\n관심영역에 움직임이 감지된 {round(msg[2]/msg[1]*100,1)}% 만 남김\n')
                    self.textBrowser.append(one_page_summary)
                    self.flag_dongzip_btn = False
                    self.progress_bars[i].setValue(100)
                    self.completed_count += 1
                    self.statusBar().showMessage(f'상태바: 완료 {self.completed_count}/{self.len_filenames}')
                    if self.active_workers < self.len_filenames:  # 추가 작업이 있는 경우
                        self.workers[self.active_workers].start()  # 새 작업 시작
                        self.active_workers += 1
                else:
                    self.progress_bars[i].setValue(msg[0])
        # 모든 작업이 완료되었는지 확인하고 메시지 박스가 아직 표시되지 않았다면 표시
        if self.completed_count == self.len_filenames and not self.message_box_shown:
            if self.completed_count == 0:
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("모든 작업이 완료되었습니다!")
            msg.setWindowTitle("작업 완료")
            self.startBtn.setText('작업 완료!')
            msg.exec_()
            self.message_box_shown = True  # 메시지 박스 표시 플래그 업데이트        self.update()
            self.slot_btn_multi_reset()

            
    def button_clicked(self):
        print("Button clicked")
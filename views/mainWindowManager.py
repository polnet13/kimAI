from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QScrollArea, QMessageBox
# 웹 바로가기
from PySide6.QtGui import QDesktopServices 
from PySide6.QtCore import QUrl, QTimer, Qt, QThread
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6 import QtGui
# 단축키
from PySide6.QtGui import QKeySequence, QShortcut  
from PySide6.QtCore import Qt
# 외부 모듈
import os, time, random
import cv2
from multiprocessing import Process, Queue
# 사용자
from control import tools
from module import enrolled
from rsc.ui.untitled_ui import Ui_MainWindow
import settings



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



class mainWindow(QMainWindow, Ui_MainWindow): # Ui_MainWindow == rec.ui.MainWindow   
    '''
    UI 컨트롤 관련 클래스
    '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 멀티 프로세싱 관련 변수
        self.num_cores = os.cpu_count()
        self.statusBar().showMessage(f'코어 수: {self.num_cores}')
        # 메시지 박스 표시 플래그
        self.message_box_shown = False  
        # 모델 드롭다운 메뉴
        detectors = tools.get_classes(enrolled)
        for detector in detectors:
            self.dropdown_models.addItem(detector.tag)
        # 기본 값을 "이륜차 번호판 감지"으로 설정(배포시 제거)
        index = self.dropdown_models.findText("이륜차 번호판 감지")
        self.dropdown_models.setCurrentIndex(index)
        self.checkbox_yolo.setChecked(True)
        # 움직임 감지 임계값
        self.move_thr = 5
        # yolo 모델 선택 및 경로
        self.selected_model = self.dropdown_models.currentText()
        self.model_path = os.path.join(settings.BASE_DIR, 'rsc/models', self.selected_model)
        self.yolo_thr = 30
        # 드롭다운 값이 변경되었을 때 함수 실행
        self.selected_mode = self.dropdown_models.currentText()
        self.dropdown_models.currentIndexChanged.connect(self.slot_dropdown_model_changed)

        # qslider 설정
        self.playSlider.valueChanged.connect(self.play_slider_moved)  # 재생구간
        self.thrSlider_move.valueChanged.connect(self.thr_slider_move_moved) # 움직임 감도
        self.thrSlider_yolo.valueChanged.connect(self.thr_slider_yolo_moved) # 욜로 감도
        self.thrSlider_move.setValue(5)
        self.thrSlider_yolo.setValue(30)
        self.label_thr_move.setText(str(5)) # label5 = 움직임 감도
        self.label_4.setText(str(30)) # label4 = 욜로 감도
        self.jump_frameSlider.valueChanged.connect(self.jump_frameSlider_moved) # 초당프레임 분석
        self.jump_frameSlider.setValue(1)
        self.Slider_bright.valueChanged.connect(self.Slider_bright_moved)  # 재생구간
        # 플레이창
        self.label.setStyleSheet("background-color: black")
        # 리스트뷰 
        self.tableView.clicked.connect(self.on_item_clicked)
        # # CCTV 분석기 초기화
        self.init_img_path = os.path.join(settings.BASE_DIR, 'rsc/init.jpg')
        self.fileName = self.init_img_path
        self.img = cv2.imread(self.init_img_path)
        # 영상관련 정보 
        self.width = 0
        self.height = 0
        self.fps = 0
        self.total_frames = 0  
        # roi: 영상의 해상도 값으로 설정
        self.x1 = self.x2 = self.y1 = self.y2  = 0
        self.region_status = False
        # play/pause 스위치
        self.play_status = False
        self.recording = False
        # 멀티프로세싱
        self.workers = None
        self.flag_start_btn = False
        self.flag_dongzip_btn = False
        
        
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

    def detector_init(self):
        # CCTV 분석기 초기화

        if self.selected_model == '이륜차 번호판 감지':
            self.detector = enrolled.DetectorBike()
        else:
            self.detector = enrolled.DetectorCCTV() 
        self.detector_fileopen()


    def slot_btn_fileopen(self):
        '''
        파일 입력 받고 
        현재 선택된 모델 초기화
        '''
        self.fileName, _ = QFileDialog.getOpenFileName(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        self.selected_model = self.dropdown_models.currentText()
        self.detector_init()
        

    def slot_btn_minusOneFrame(self):
        self.curent_frame = self.detector.cap.get(cv2.CAP_PROP_POS_FRAMES)-2
        self.playSlider.setValue(self.curent_frame)
        

    def slot_btn_plusOneFrame(self):
        self.curent_frame = self.detector.cap.get(cv2.CAP_PROP_POS_FRAMES)+1
        self.playSlider.setValue(self.curent_frame)


    def slot_btn_open_complete(self):
        path = os.path.join(settings.BASE_DIR, 'output')
        os.startfile(path)


    def detector_fileopen(self):
        # 이미지 처리
        self.img, self.width, self.height = self.detector.fileopen(self.fileName)
        self.reset_roi(self.img)
        self.statusBar().showMessage(f'파일 경로: {self.fileName}')
        # 영상의 전체 프레임수를 가지고 옴
        self.total_frames = self.detector.total_frames
        self.label_xy.setText(f'해상도: {self.width}*{self.height}')
        self.playSlider.setMaximum(self.detector.total_frames -1)
        self.label_fps.setText(f'fps : {self.detector.fps}')
        self.fps = self.detector.fps
        self.update()
        self.display_img()
        
    def slot_btn_play(self):
        '''
        qimage 객체로 변경해서 출력하는 것의 속도 측정
        '''
        self.play_status = not self.play_status

        print(self.selected_model)

        if self.play_status:
            # 타임이벤트 생성
            self.timer = QTimer()
            self.timer.timeout.connect(self.play)
            self.timer.start(1)
        else:
            self.timer.stop()
        # self.detector.play()


    # 이벤트 감지       
    def play(self):
        '''
        cap_read() 함수는 cv2.VideoCapture 객체를 통해 프레임을 읽어오고,
        jump_frame 만큼 프레임을 건너뛰어서 읽어온다.
        '''
        self.jump_frame = self.jump_frameSlider.value()
        # 프레임을 읽어옴
        img, self.curent_frame, self.play_status = self.detector.cap_read(self.jump_frame, self.play_status)
        # 정지 버튼이 눌렸을 때
        if self.play_status == False:
            self.timer.stop()
            return 
        # 이미지가 없을 때
        if img is None:
            return
        # 슬라이더 업데이트
        self.playSlider.setValue(self.curent_frame)
        # 재생시간 업데이트
        frame_time = time.strftime('%H:%M:%S', time.gmtime(self.curent_frame/self.detector.fps))
        self.playTimer.setText(f'{frame_time}')
        # 마지막 프레임일 때
        if self.curent_frame == self.total_frames:
            self.timer.stop()
            self.play_status = False


    def slot_btn_multi_open(self):
        # slot_btn_multi_open로 변경 예정
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
        self.fileNames, _ = QFileDialog.getOpenFileNames(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        if len(self.fileNames) == 0:
            self.flag_dongzip_btn = False
            self.textBrowser.append('동영상 파일이 선택되지 않았습니다.')
            return
        # fileNames의 파일들의 용량을 확인하고 용량이 큰 순서대로 정렬
        self.fileNames = tools.sort_files_by_size(self.fileNames)
        self.fileName = self.fileNames[0]
        self.detector_init()
        print('self.detector_init()')
        self.make_queue_and_progress_bars(self.fileNames)


        
    def start_multi(self):
        '''
        백그라운드 워커을 실행하고,
        프로그레스바를 업데이트하는 타이머를 실행
        '''
        if self.flag_start_btn is True:
            return
        # 메뉴 넘버 따오는 함수 추가예정
        menu_number = 0
        self.make_objects(menu_number)
        self.object_queue_to_worker()
        self.run_workers()
        self.flag_start_btn= True
        self.startBtn.setText('동영상 압축 중...')
        self.completed_count = 0
        # 백그라운드 워커(실질적인 영상 압축 코드)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  


    def sort_roi(self):
        '''
        roi 좌표를 정렬하는 함수
        '''
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1

 
    def slot_btn_reset(self):
        if self.img is None:
            self.label_roi.setText(f'관심영역: {self.region_status}') 
            self.update()
        else:
            self.reset_roi(self.img)
            self.display_img()

    def reset_roi(self, img):
        '''
        이미지의 해상도에 꽉차는 roi를 설정함
        '''
        self.region_status = False
        if img is None:
            return
        self.x1 = self.y1 = 0
        self.x2 = self.img.shape[1]
        self.y2 = self.img.shape[0]
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
    # 리스트뷰에서 선택된 행 삭제
    def delete_listview_row(self):
        index = self.tableView.currentIndex().row()
        self.qmodel.removeRow(index)
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
        self.detector.cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        self.img = self.detector.cap.read()[1]
        self.display_img()
        print(f'row: {row}, n: {n}')
        
        
    ##################    
    # 플레이 슬라이더 #
    ##################
    def play_slider_moved(self, value):
        '''
        슬라이더가 움직일 때 이미지 처리하는 '핵심' 함수
        '''
        # 공통 코드 
        self.detector.cap.set(cv2.CAP_PROP_POS_FRAMES, value)
        self.img, self.curent_frame, self.play_status = self.detector.cap_read(
            self.jump_frame, self.play_status)
        roi_img = tools.get_roi_img(
            self.img, 
            self.x1, self.y1, self.x2, self.y2
            )
        # ROI 부분만 움직임 감지
        roi_img, detect_move_bool, contours = self.detector.detect_move(
            roi_img, self.region_status, self.move_thr
            )
        # 움직임이 없는 경우 원본 이미지 출력
        if detect_move_bool == False:
            self.display_img(self.img, (0,0,255))
            return
        # ROI 부분만 욜로 디텍션
        if self.checkbox_yolo.isChecked():
            roi_img, text  = self.detector.detect_yolo_track(roi_img, self.yolo_thr)
            if text:
                self.textBrowser.append(text)
                self.textBrowser.setFocus()
            # 이것 때문에 오류 발생
            # bike:  track_ids[n] = [_cap_number, ocr_text] 
            # cctv:  track_ids[n] = cap 
            if self.detector.track_ids:
                self.dict_to_listview() 
        # self.img에 roi_img를 붙여서 출력
        plot_img = self.img.copy()
        plot_img[self.y1:self.y2, self.x1:self.x2] = roi_img
        self.display_img(plot_img, (0,255,0))
        
            
    def jump_frameSlider_moved(self, value):
        self.label_frame_gap.setText(str(value)) # label7 = self.jump_frameSlider 값
        
    def thr_slider_move_moved(self, value):
        self.move_thr = value
        self.label_thr_move.setText(str(value)) # label4 = self.thrSlider 값

    def thr_slider_yolo_moved(self, value):
        self.yolo_thr = value
        self.label_thr_yolo.setText(str(value)) # label4 = self.thrSlider 값

    def Slider_bright_moved(self, value):
        self.label_bright.setText(str(value))
    
      
    # 딕셔너리 리스트뷰에 출력
    def dict_to_listview(self):
        # bike:  track_ids[n] = [_cap_number, ocr_text] 
        # cctv:  track_ids[n] = cap 
        # 모델 초기화를 데이터 추가 전에 수행
        self.qmodel = QtGui.QStandardItemModel()  # 초기 행과 열의 수를 설정하지 않음
        print(f'self.detector.track_ids = {self.detector.track_ids}')
        for key, values in self.detector.track_ids.items():
            print(f'key: {key}, value: {values}')
            value_objs = []
            key_item = QtGui.QStandardItem(str(key))
            value_objs = [QtGui.QStandardItem(str(value)) for value in values]
            value_objs.insert(0, key_item)
            self.qmodel.appendRow(value_objs)

            # add_textview = [row for row in value]
            # add_textview.insert(0, key)
            # add_textview = [str(i) for i in add_textview]
            # add_textview_str = ' | '.join(add_textview)
            # self.textBrowser.append(add_textview_str)
        self.tableView.setModel(self.qmodel)


    def program_exit(self):
        '''워커와 GUI 종료'''
        self.terminate_workers()
        self.close()        

    # 마우스 좌표가 30 보다 작으면 30으로 설정하고 영상 가로 사이즈+30 보다 크면 영상가로 사이즈+30으로 설정
    def is_in_label_x(self, x):   
        '''
        영상 비율 관련 수정필요
        ''' 
        return max(0, min(x, self.width))
        
    def is_in_label_y(self, y):   
        '''
        영상 비율 관련 수정필요
        ''' 
        return max(0, min(y, self.height))

    ############
    ## 마우스 ##
    ############

    # 마우스 왼쪽 버튼이 눌렸을 때의 동작
    def mousePressEvent(self, event):
        '''
        실제 좌표(a,b)를 받아서 디스플레이 이미지의 좌표로 변환
        '''
        a, b = event.pos().x(), event.pos().y()
        if self.img is None:
            return
        # a, b값이 play창 밖이면 무시하도록
        if a < 40 or a > 760 or b < 40 or b > 520:
            return
        if self.play_status:
            return
        # a, b값을 gui좌표에서 백분율로 변환
        a, b = tools.guiToResolution(a, b, self.img)
        if event.button() == Qt.LeftButton:
            self.x1, self.y1 = a, b

        
    # 마우스 왼쪽 버튼을 누르고 드래그 할 때의 동작
    def mouseMoveEvent(self, event):
        a, b = event.pos().x(), event.pos().y()
        if self.img is None:
            return
        # a, b값이 play창 밖이면 무시하도록
        if a < 40 or a > 760 or b < 40 or b > 520 or self.img is None:
            return
        # a, b값을 gui좌표에서 백분율로 변환
        a, b = tools.guiToResolution(a, b, self.img)
        img = self.img.copy()
        if self.play_status:
            return
        self.x2, self.y2 = a,b
        # 영상비율 자동 조절되도록 수정 필요
        self.display_img(img)

        
    # 마우스 왼쪽 버튼이 떼졌을 때의 동작
    def mouseReleaseEvent(self, event):
        a, b = event.pos().x(), event.pos().y()
        if self.img is None:
            return
        img = self.img.copy()
        # a, b값이 play창 밖이면 무시하도록
        if a < 40 or a > 760 or b < 40 or b > 520:
            return
        if self.play_status:
            return
        # a, b값을 gui좌표에서 백분율로 변환
        a, b = tools.guiToResolution(a, b, img)
        # 마우스 왼쪽 버튼이 떼지고 재생중이 아닐 때
        if (event.button() == Qt.LeftButton):
            self.region_status = True
            self.drawing = False
            self.x2, self.y2 = a, b
            self.display_img(img)
        self.sort_roi()
        self.label_roi_update()
    
    ##################
    ## GUI 업데이트 ##
    ##################

    def label_roi_update(self):
        '''
        디스플레이창에 roi 좌표를 출력하고
        roi 갱신으로 욜로모델도 갱신함(트래킹시 이미지 사이즈 변경되면 욜로 오류발생 방지)
        '''
        self.label_roi.setText(f'관심영역: ({int(self.x1)}, {int(self.y1)}), ({int(self.x2)}, {int(self.y2)})') 
        self.update()
        
    def display_img(self, img=None, color=(0, 0, 255)):
        '''
        최종적으로 roi를 표시한 이미지를 출력하는 함수
        '''
        if img is None:
            plot_img = self.img.copy()
        else:
            plot_img = img.copy()
        # ROI 좌표가 모두 있는지 확인
        if self.x1 is None or self.x2 is None or self.y1 is None or self.y2 is None:
            pass
        else:
            cv2.rectangle(plot_img, (self.x1, self.y1),(self.x2, self.y2),color, 2)
        # 욜로 감지된 경우(구현 예정)
        self.label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(plot_img.data, plot_img.shape[1], plot_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()))
        self.label.setScaledContents(True)
        self.label.update()
        
    ##########
    ## 기타 ##
    ##########            
        
    # 드롭다운 메뉴가 변경되었을 때 Yolo 모델을 변경 
    def slot_dropdown_model_changed(self):
        text = self.dropdown_models.currentText() 
        if not self.selected_mode == text:
            self.selected_mode = text
        if self.selected_mode == '이륜차 번호판 감지':
            self.checkbox_yolo.setChecked(True)
            self.detector = enrolled.DetectorBike()
        elif self.selected_mode == 'CCTV 분석':
            self.checkbox_yolo.setChecked(False)
            self.detector = enrolled.DetectorCCTV()
        else:
            self.detector = enrolled.DetectorCCTV()
        if self.fileName:
            self.detector.fileopen(self.fileName)
        self.update()
        self.display_img()

        
    def slot_btn_init_detection(self):
        self.detector.track_ids = {}
        self.dict_to_listview()
    
    def slot_btn_region_reset(self):
        if self.img is None:
            self.label_roi.setText(f'관심영역: {self.region_status}') 
            self.update()
        else:
            self.reset_roi(self.img)
            self.display_img()

    def slot_btn_multi_reset(self):
        self.fileNames = []
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


    # 객체 생성은 여기서 전부 해야 함
    def make_objects(self, menu_number=0):
        '''
        멀티 작업 객체 생성
        0: CCTV 분석
        1: 오토바이 분석
        '''
        if menu_number == 0:
            self.objects = [enrolled.MultiCCTV(
                file, self.x1, self.y1, self.x2, self.y2
            ) for i, file in enumerate(self.fileNames)]
        if menu_number == 1:
            pass


    def clear_status_bars(self):
        '''상태바를 모두 제거'''
        for i in reversed(range(self.vLayout_dongzip_statusbar.count())):  
            widget = self.vLayout_dongzip_statusbar.itemAt(i).widget()
            if widget is not None:  # 위젯이 있는 경우
                widget.deleteLater()  # 위젯 제거


    def run_workers(self):
        '''워커 시작: 멀티프로세스 열일 시작'''
        self.active_workers = 0
        for _ in range(min(int(self.num_cores) - 1, len(self.fileNames))):  # 코어 수 - 2개의 작업을 시작
            self.workers[self.active_workers].x1 = self.x1
            self.workers[self.active_workers].x2 = self.x2
            self.workers[self.active_workers].y1 = self.y1
            self.workers[self.active_workers].y2 = self.y2
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

import time
import subprocess
import sys
from ultralytics import YOLO
import cv2
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout
from PySide6.QtWidgets import QWidget, QScrollArea, QMessageBox
from PySide6.QtCore import QTimer
# QSound 임포트

# 시그널 임포트
from PySide6.QtCore import Signal
# 외부 모듈
import os, json
import cv2
from multiprocessing import Process, Queue
from control import tools
from views.sharedData import DT
from rsc.ui.cctv_ui import Ui_CCTV
from control.tools import getTime



class CCTV(Ui_CCTV, QWidget):

    playerOpenSignal = Signal()

    '''ui와 시그널 연결'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 시그널 슬롯 연결
        self.btn_multi_open.clicked.connect(self.btn_multi_open_func)
        self.btn_multi_reset.clicked.connect(self.slot_btn_multi_reset)
        self.btn_multi_complete_open.clicked.connect(self.slot_btn_open_complete)
        self.slider_move_thr.valueChanged.connect(self.slot_slider_move_thr)
        self.slider_jump.valueChanged.connect(self.slot_slider_jump)
        self.flag_dongzip_btn = False
        self.flag_multiprocess = False
        self.roi_frame_1 = None
        self.roi_frame_2 = None
        self.roi_frame_3 = None
        self.kernel_size = None

        # 큐, 프로그래스 바, 워커 생성
        self.workers = []
        self.thread = os.cpu_count()
        

    def getInstance(self):
        '''시작시 한 번에 불러오면 대기시간이 올래 걸리므로 좌메뉴 클릭시 인스턴스 생성'''
        a = MultiCCTV()
        return 

    def slot_slider_move_thr(self):
        '''슬라이더 값 변경'''
        self.label_thr.setText(f'{self.slider_move_thr.value()}')
        DT.setMoveSliderScale()

    def slot_slider_jump(self):
        '''점프 슬라이더 값 변경'''
        self.label_jump.setText(f'{self.slider_jump.value()}')
        DT.jump = self.slider_jump.value()
        DT.saveOption(jump=DT.jump)


    def slot_btn_open_complete(self):
        path = DT.OUT_DIR
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', path])

    def btn_multi_open_func(self):
        '''파일 여러개 불러오기'''
        if self.flag_dongzip_btn is True:
            return
        self.flag_dongzip_btn = True
        fileNames, _ = QFileDialog.getOpenFileNames(self, '파일 선택', '~/', 'Video Files (*.mp4 *.avi *.mkv *.mov *.*)')
        DT.fileNames = fileNames
        if len(DT.fileNames) == 0:
            self.flag_dongzip_btn = False
            return
        # fileNames의 파일들의 용량을 확인하고 용량이 큰 순서대로 정렬
        DT.fileNames = tools.sort_files_by_size(DT.fileNames)
        DT.fileName = DT.fileNames[0]
        DT.OUT_DIR = os.path.join(os.path.dirname(DT.fileName), 'output')
        self.playerOpenSignal.emit()
        self.make_queue_and_progress_bars(DT.fileNames)  # 모든 파일 큐와 프로그래스바 생성


    def slot_btn_multi_reset(self):
        DT.fileNames = []
        self.flag_dongzip_btn = False
        self.btn_flag_multi_start = False
        self.flag_multiprocess = False
        self.terminate_workers()
        self.clear_status_bars()
        self.update()


    def make_queue_and_progress_bars(self, fileNames):
        # 상태바 제거
        self.flag_start_multi = False
        self.clear_status_bars()
        # 스크롤 가능한 프로그레스 바 위젯 생성
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.vLayout_dongzip_statusbar.addWidget(scroll_area)
        self.startBtn = QPushButton(f'작업 시작')
        scroll_layout.addWidget(self.startBtn)

        cap = cv2.VideoCapture(fileNames[0])
        ret, frame = cap.read()
        # 첫프레임 오류난 파일 처리
        if ret is False:
            ret, frame = cap.read() 
        if ret is True:
            self.img_shape = frame.shape

        self.startBtn.clicked.connect(self.start_multi)
        
        self.len_filenames = len(fileNames)
        self.queues = []
        self.progress_bars = [] 
        self.workers = []
        for filename in fileNames:
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
            # 파일 네임 리스트 생성



    def program_exit(self):
        '''멀티 CCTV 프로그램 종료'''
        print('멀티 CCTV 종료')
        self.terminate_workers()


    def applyImageProcessing(self, img):
        '''cctv 모드에서는 roi이미지를 움직임 감지 하여 전체 이미지에 합성'''
        if DT.cap_num%DT.jump != 0:
            return img
        x1, y1, x2, y2 = DT.roi_point[0]
        # cv2 이벤트 감지
        self.difframe = None
        self.roi_color = (0, 0, 255)
        # 움직임 감지
        self.thr_move_slider = self.slider_move_thr.value()
        roi_img = img[y1:y2, x1:x2]
        # ROI 부분만 움직임 감지
        roi_img, detect_move_bool, contours = self.detect_move(roi_img)     
        # 움직임이 없는 경우 루프 건너뜀
        if detect_move_bool == False:
            return img
        # # ROI 부분만 욜로 디텍션
        # 컨투어 표시
        roi_img = tools.draw_contours(roi_img, contours)        
        # ROI 이미지를 원본이미지에 합성
        img = tools.merge_roi_img(img, roi_img, x1, y1)
        # 녹화 옵션
        cv2.rectangle(img, (x1, y1),(x2, y2),(111,111,111), 1)
        return img

    ####################     
    # 멀티프로세싱 함수 #
    ####################

    def object_queue_to_worker(self):
        '''객체와 큐 연결 '''
        for i in range(len(self.workers)):
            print(f'i:: {i}')
            print(f'self.workers: {len(self.workers)}')
            self.workers[i].queue = self.queues[i]
            self.workers[i].obj = self.objects[i]
            self.workers[i].filename = DT.fileNames[i]
        
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
        for _ in range(min(int(self.thread) - 1, len(DT.fileNames))):  # 코어 수 - 2개의 작업을 시작
            roi = DT.roi
            roi = tools.rel_to_abs(self.img_shape, roi[0], roi[1], roi[2], roi[3])
            self.workers[self.active_workers].x1 = roi[0]
            self.workers[self.active_workers].x2 = roi[2]
            self.workers[self.active_workers].y1 = roi[1]
            self.workers[self.active_workers].y2 = roi[3]
            self.workers[self.active_workers].start()
            self.active_workers += 1

    def start_multi(self):
        '''
        작업 시작 버튼을 누르면 실행되는 함수
        백그라운드 워커을 실행하고,
        프로그레스바를 업데이트하는 타이머를 실행
        '''
        self.st = time.time()
        if self.flag_multiprocess:
            return
        # 메뉴 넘버 따오는 함수 추가예정
        self.objects = [
            MultiCCTV(
                file, 
                scale_move_thr = DT.scale_move_thr,
                thr_move_slider = self.slider_move_thr.value(),
                jump=DT.jump
                ) for file in DT.fileNames
                ]
        self.object_queue_to_worker()
        self.run_workers()
        self.completed_count = 0
        # 백그라운드 워커(실질적인 영상 압축 코드)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  
        # self.startBtn 버튼 제거
        self.startBtn.deleteLater()




    def update_progress(self):
        '''진행 상태 업데이트'''

        self.completed_count = 0
        for i in range(self.active_workers):
            while not self.queues[i].empty():
                msg = self.queues[i].get()
                if msg[0] == 'done':
                    # 워커 종료시
                    # ['done', total_frames, frame_cnt, self.fps, self.file_name, round(et-st), self.jump]
                    file = os.path.basename(msg[4])
                    before_time = round(msg[1]/msg[3],1)
                    after_time = round(msg[2]/msg[3],1)
                    detect_time = round(msg[2]/msg[1]*100,1)
                    print('작업 완료')
                    one_page_summary = (f'{file}\n{before_time}초 => {after_time}초\n관심영역에 움직임이 감지된 {detect_time}% 남김, {msg[5]}소요, jump: ({msg[6]})\n\n')
                    with open(os.path.join(DT.OUT_DIR, 'summary.txt'), 'a') as f:
                        f.write(one_page_summary)
                    self.flag_dongzip_btn = False
                    self.progress_bars[i].setValue(100)
                    self.completed_count += 1

                    if self.active_workers < self.len_filenames:  # 추가 작업이 있는 경우
                        self.workers[self.active_workers].start()  # 새 작업 시작
                        self.active_workers += 1
                else:
                    try:
                        self.progress_bars[i].setValue(msg[0])
                    except:
                        return
        # 모든 작업이 완료되었는지 확인하고 메시지 박스가 아직 표시되지 않았다면 표시
        if self.completed_count == self.len_filenames:
            print(self.completed_count)
            if self.completed_count == 0:
                return
            # 멀티 작업 종료시 작업
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("모든 작업이 완료되었습니다!")
            msg.setWindowTitle("작업 완료")
            msg.exec_()
            self.slot_btn_multi_reset()
            self.et = time.time()
            print(f'소요시간: {self.et - self.st}')
    
    def detect_move(self, roi_img):
        '''
        WorkerCCTV.detect_move()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, 움직임 Bool, contours
        '''
        plot_img = roi_img.copy()
        gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        if roi_img is None or roi_img.size == 0:
            return roi_img, False, 0
        gray_img = cv2.GaussianBlur(gray_img, DT.kernel_size, 0)
        # 밝기 처리한 이미지를 리턴하므로 원본 이미지를 복사하여 사용
        contours = 0
        # ROI를 설정합니다.
        self.setRoiFrame123(gray_img)
        # frame1, frame2, frame3이 하나라도 None이면 원본+밝기 이미지 출력
        if self.roi_frame_1 is None or self.roi_frame_2 is None or self.roi_frame_3 is None:
            DT.roi_color = (0, 0, 255)
            # plot_img의 테두리를 self.roiColor로 설정
            cv2.rectangle(plot_img, (0, 0), (plot_img.shape[1], plot_img.shape[0]), DT.roi_color, 1)
            return plot_img, False, contours
        # 움직임 감지
        diff_cnt, diff_img = self.get_diff_img()
        thr = DT.scale_move_thr * self.slider_move_thr.value() # * brightness
        if diff_cnt < thr:
            DT.roi_color = (0, 0, 255)
            cv2.rectangle(plot_img, (0, 0), (plot_img.shape[1], plot_img.shape[0]), DT.roi_color, 1)
            return plot_img, False, contours
        DT.roi_color = (0, 255, 0)
        # 영상에서 1인 부분이 thr 이상이면 움직임이 있다고 판단 영상출력을 하는데 움직임이 있는 부분은 빨간색으로 테두리를 표시
        contours, _ = cv2.findContours(diff_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return plot_img, True, contours
    

    def get_diff_img(self):
        '''
        return diff_cnt(영상간 차이값), diff(이미지)
        활용 if diff_cnt > self.thr:
        
        연속된 3개의 프레임에서 1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        ''' 
        # 1,2 프레임, 2,3 프레임 영상들의 차를 구함
        if self.roi_frame_1.shape == self.roi_frame_2.shape and self.roi_frame_2.shape == self.roi_frame_3.shape:   
            diff_ab = cv2.absdiff(self.roi_frame_1, self.roi_frame_2)
            diff_bc = cv2.absdiff(self.roi_frame_2, self.roi_frame_3)
        else:
            return 0, None

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        # 수정필요: self.thr 슬라이더로 받기
        _, diff_ab_t = cv2.threshold(diff_ab, 1, 255, cv2.THRESH_BINARY)
        _, diff_bc_t = cv2.threshold(diff_bc, 1, 255, cv2.THRESH_BINARY)

        # 두 영상 차의 공통된 부분을 1로 만들어줌
        diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
        # 영상에서 1이 된 부분을 적당히 확장해줌(morpholgy)
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
        # 영상에서 1인 부분의 갯수를 셈
        diff_cnt = cv2.countNonZero(diff)
        return diff_cnt, diff

    def setRoiFrame123(self, gray_img):
        self.roi_frame_1 = self.roi_frame_2 
        self.roi_frame_2 = self.roi_frame_3 
        self.roi_frame_3 = gray_img




            


   
class MultiCCTV:
    
    models = {
        'model': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8x.pt')),
        'model_nbp':  YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 self.models 로 전달함
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']

    def __init__(self, fileName, scale_move_thr=1, thr_move_slider=50, jump =1):
 
        super().__init__()
        self.track = False
        self.queue = None
        # 경로 설정
        self.filePath = fileName
        self.output_base = os.path.join(os.path.dirname(fileName), 'output')
        baseName = os.path.basename(fileName)   
        self.file_name, _ = os.path.splitext(baseName)
        # 아웃풋 경로 생성
        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base)
        # ROI 설정
        x1, y1, x2, y2 = DT.roi
        self.x1, self.y1, self.x2, self.y2 = tools.rel_to_abs(DT.img.shape, x1, y1, x2, y2)
        height, width = DT.img.shape[:2]
        kernel_size = (width // 20, height // 20)  # 예: 이미지 크기의 1/70
        self.kernel_size = (kernel_size[0] | 1, kernel_size[1] | 1) # 커널 크기는 홀수여야 함
        # cv2 이벤트 감지
        self.roi_frame_1 = None
        self.roi_frame_2 = None
        self.roi_frame_3 = None
        self.difframe = None
        self.roi_color = (0, 0, 255)
        self.jump = jump
        # 움직임 감지
        self.thr_move_slider_multi = thr_move_slider


    def multi_process(self):
        '''영상압축 함수'''
        # 비디오 파일 열기
        st = time.time()
        self.cap = cv2.VideoCapture(self.filePath)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 전체 프레임 가져오기
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.percentage = 0
        false = 0
        self.newFrameNum = 0
        outvideo = os.path.join(self.output_base, f'{self.file_name}.mp4')
        # 비디오 생성
        self.video = cv2.VideoWriter(outvideo, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        frame_cnt = 0
        # 루프 돌기
        while True: # 동영상이 올바로 열렸는지
            ret, self.img = self.cap.read() 
            curent_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES) 
            if curent_frame%self.jump != 0:
                if curent_frame >= total_frames:
                    break
                continue
            # 상태바 업데이트를 위해 작업 진행률을 계산
            self.percentage_1 = self.percentage
            self.percentage_2 = round(curent_frame/total_frames*100)
            if self.percentage_1 != self.percentage_2:
                self.percentage = self.percentage_2
            self.queue.put([self.percentage-2])
            # 프레임 처리
            if not ret:
                false += 1
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, curent_frame+1)
                if curent_frame >= total_frames:
                    break
            else:
                false=0
                roi_img = self.img[self.y1:self.y2, self.x1:self.x2]
                # roi 이미지 가우시안 블러 처리
                final_img = roi_img.copy()
                # ROI 부분만 움직임 감지
                roi_img, detect_move_bool, contours = self.detect_move(roi_img)     
                # 움직임이 없는 경우 루프 건너뜀
                if detect_move_bool == False:
                    continue
                # 움직임 표시
                final_img = tools.draw_contours(final_img, contours)        
                # ROI 이미지를 원본이미지에 합성
                img = tools.merge_roi_img(self.img, final_img, self.x1, self.y1)
                # 녹화 옵션
                cv2.rectangle(img, (self.x1, self.y1),(self.x2, self.y2),(0,255,0), 1)
                self.video.write(img) 
                frame_cnt += 1
            if false > 2:
                break
        # total_frames/fps
        et = time.time()
        message = ['done', total_frames, frame_cnt, self.fps, self.file_name, round(et-st), self.jump]
        self.queue.put(message)
        self.cap.release()
        self.video.release()
        

    def yolo_detection(self, roi_img, frame_number):
        '''
        이 함수는 roi_img를 받아서 yolo 디텍션을 수행함(이미지 처리X)
        - 키: new 프레임번호 생성해서 딕셔너리 
        - 밸류: 탐지된 객체의 집합 [(), (), ()] 구조를 만들어서 self.obj_dict에 저장
        '''
        frame_number = frame_number
        values = []
        tracking_id = None
        try:
            detections = self.detector.track(roi_img, persist=True, device=DT.device)[0]
        except Exception as e:
            # 욜로 트래커 초기화
            self.detector = YOLO(os.path.join(DT.BASE_DIR, 'rsc/models/yolov8x.pt'))
            detections = self.detector.track(roi_img, persist=True, device=DT.device)[0]
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            tracking_id, thr, label = int(data[4]), float(data[5]), int(data[6])
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            x1, y1, x2, y2 = tools.abs_to_rel(roi_img.shape, xmin, ymin, xmax, ymax)
            if tracking_id in self.obj_dict.keys():
                continue
            if self.check_people and label in [0]:
                values.append((frame_number, label, x1, y1, x2, y2, thr))
            if self.check_car and label in [2, 3, 5, 7]:
                values.append((frame_number, label, x1, y1, x2, y2, thr))
        if tracking_id:
            self.obj_dict[tracking_id] = values        


    def detect_move(self, roi_img):
        '''
        WorkerCCTV.detect_move()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, 움직임 Bool, contours
        '''
        plot_img = roi_img.copy()
        gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        if roi_img is None or roi_img.size == 0:
            return roi_img, False, 0
        gray_img = cv2.GaussianBlur(gray_img, self.kernel_size, 0)
        # 밝기 처리한 이미지를 리턴하므로 원본 이미지를 복사하여 사용
        contours = 0
        # ROI를 설정합니다.
        self.setRoiFrame123(gray_img)
        # frame1, frame2, frame3이 하나라도 None이면 원본+밝기 이미지 출력
        if self.roi_frame_1 is None or self.roi_frame_2 is None or self.roi_frame_3 is None:
            DT.roi_color = (0, 0, 255)
            # plot_img의 테두리를 self.roiColor로 설정
            cv2.rectangle(plot_img, (0, 0), (plot_img.shape[1], plot_img.shape[0]), DT.roi_color, 1)
            return plot_img, False, contours
        # 움직임 감지
        diff_cnt, diff_img = self.get_diff_img()
        thr = DT.scale_move_thr * self.thr_move_slider_multi # * brightness
        if diff_cnt < thr:
            DT.roi_color = (0, 0, 255)
            cv2.rectangle(plot_img, (0, 0), (plot_img.shape[1], plot_img.shape[0]), DT.roi_color, 1)
            return plot_img, False, contours
        DT.roi_color = (0, 255, 0)
        # 영상에서 1인 부분이 thr 이상이면 움직임이 있다고 판단 영상출력을 하는데 움직임이 있는 부분은 빨간색으로 테두리를 표시
        contours, _ = cv2.findContours(diff_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return plot_img, True, contours
    

    def get_diff_img(self):
        '''
        return diff_cnt(영상간 차이값), diff(이미지)
        활용 if diff_cnt > self.thr:
        
        연속된 3개의 프레임에서 1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        ''' 
        # 1,2 프레임, 2,3 프레임 영상들의 차를 구함
        if self.roi_frame_1.shape == self.roi_frame_2.shape and self.roi_frame_2.shape == self.roi_frame_3.shape:   
            diff_ab = cv2.absdiff(self.roi_frame_1, self.roi_frame_2)
            diff_bc = cv2.absdiff(self.roi_frame_2, self.roi_frame_3)
        else:
            return 0, None

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        # 수정필요: self.thr 슬라이더로 받기
        _, diff_ab_t = cv2.threshold(diff_ab, 1, 255, cv2.THRESH_BINARY)
        _, diff_bc_t = cv2.threshold(diff_bc, 1, 255, cv2.THRESH_BINARY)

        # 두 영상 차의 공통된 부분을 1로 만들어줌
        diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
        # 영상에서 1이 된 부분을 적당히 확장해줌(morpholgy)
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
        # 영상에서 1인 부분의 갯수를 셈
        diff_cnt = cv2.countNonZero(diff)
        return diff_cnt, diff

    def setRoiFrame123(self, gray_img):
        self.roi_frame_1 = self.roi_frame_2 
        self.roi_frame_2 = self.roi_frame_3 
        self.roi_frame_3 = gray_img




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

        
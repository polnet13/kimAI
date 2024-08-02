import os
import cv2
import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO


from control import tools
import settings




class CustomBaseClass():
    '''
    커스텀 모듈의 기본기능을 정의한 클래스

    [ input ] 
    path(프로젝트 경로), model_path(모델 경로), multiMode(멀티프로세스 사용여부)
    
    [ output ]
    None

    [ 속성 ]

    [ 매서드 ]
    __init__(path, model_path, multiMode)
    __str__()
    fileopen(파일경로)
    cap_read(jump_frame, play_status)
    detect_yolo_track(frame, thr)
    '''
    tag = 'CustomBaseClass'

    def __init__(self, multiMode = False) -> None:
        self.tag = CustomBaseClass.tag
        self.track = True
        # GPU 사용 
        # self.gpu = torch.cuda.is_available()
        # 이미지 초기화
        self.img_path = os.path.join(settings.BASE_DIR, 'rsc/init.jpg')
        self.img = cv2.imread(self.img_path)
        # 탐지 영역 설정 활성화 상태
        self.region_status = False
        # GPU 사용하는 YOLO 모델 불러오기
        self.thr = 5      # 욜로에서는 임계값, 이벤트에서는 영상 차이
        self.labels = None
        self.track_ids = {}
        # cv2 관련
        self.cap = None
        self.fps = None
        self.total_frames = 0    # 진행률을 확인하기 위한 총 프레임수
        self.curent_frame = 0    # 현재 프레임
        # cv2 이벤트 감지
        self.roi_color = (0, 0, 255)

 
 
    def __str__(self) -> str:
        return CustomBaseClass.tag      
            
    ##############
    ## 슬롯함수 ##
    ##############
    def fileopen(self, fileName):
        if fileName:
            self.fileName = fileName
            self.cap = cv2.VideoCapture(fileName)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # track_ids 초기화
            self.track_ids = {}
            # 프레임 관련 정보 초기화
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  
            print(self.total_frames)
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            _, frame = self.cap.read() 
            self.img = frame
            if self.model is not None:
                detection = self.model(frame)[0]
                # 라벨을 초기화 하는 함수 작성        
                self.labels = [ v for _ , v in detection.names.items() ]
            return (frame, self.width, self.height )
        
    def cap_read(self, jump_frame, play_status):
        '''
        cap_read() 함수는 cv2.VideoCapture 객체를 통해 프레임을 읽어오고,
        이미지, 프레임(float), 플레이 상태(불리언)를 반환함
        '''
        ret, self.img = self.cap.read() 
        if ret:
            # 현재 프레임 번호가 self.jump_frame 의 배수일 때만 이미지 처리
            self.curent_frame = int( self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if self.curent_frame % jump_frame != 0:
                return self.img, self.curent_frame, play_status
            return self.img, self.curent_frame, play_status
        else:
            self.curent_frame = 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
            play_status = False
            return self.img, self.curent_frame, play_status
        



    def get_diff_img(self):
        '''
        return diff_cnt(영상간 차이값), diff(이미지)
        활용 if diff_cnt > self.thr:
        
        연속된 3개의 프레임에서 1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        ''' 
        # 1,2 프레임, 2,3 프레임 영상들의 차를 구함
        diff_ab = cv2.absdiff(self.roi_frame_1, self.roi_frame_2)
        diff_bc = cv2.absdiff(self.roi_frame_2, self.roi_frame_3)

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        _, diff_ab_t = cv2.threshold(diff_ab, self.thr, 255, cv2.THRESH_BINARY)
        _, diff_bc_t = cv2.threshold(diff_bc, self.thr, 255, cv2.THRESH_BINARY)

        # 두 영상 차의 공통된 부분을 1로 만들어줌
        diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
        # 영상에서 1이 된 부분을 적당히 확장해줌(morpholgy)
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
        # 영상에서 1인 부분의 갯수를 셈
        diff_cnt = cv2.countNonZero(diff)
        return diff_cnt, diff
    

    def getTrack(self):
        return self.track


class CustomMultiClass():
    '''
    Worker의 start() 함수가 실행되면 동집의 실질적인 작업 수행
    '''
    def __init__(self, fileName, x1, y1, x2, y2):
        self.queue = None
        # 경로 설정
        self.base = os.path.dirname(fileName)
        self.fileName = os.path.basename(fileName)
        self.output_path = os.path.dirname(os.path.dirname(__file__))
        self.output_path = os.path.join(self.output_path, 'output')
        # 아웃풋 경로 생성
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        # cv2 이벤트 감지
        self.roi_frame_1 = None
        self.roi_frame_2 = None
        self.roi_frame_3 = None
        self.difframe = None
        self.move_thr = 30
        self.diff_max = 11       # 영상 차이 픽셀의 개수(이것 이상이면 움직임이 있다고 결정)
        self.roi_color = (0, 0, 255)
        self.thr = 5


    def multi_process(self):
        '''동집 실질적인 작업 함수'''
        file = os.path.join(self.base, self.fileName)
        self.cap = cv2.VideoCapture(file)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 전체 프레임 가져오기
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.percentage = 0
        false = 0
        outfile = os.path.join(self.output_path, f'{self.fileName}.mp4')
        # 비디오 생성
        self.video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        frame_cnt = 0
        # 루프 돌기
        while True: # 동영상이 올바로 열렸는지
            ret, self.img = self.cap.read() 
            curent_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES) 
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
                roi_img = tools.get_roi_img(
                    self.img, 
                    self.x1, self.y1, self.x2, self.y2)
                # ROI 부분만 움직임 감지
                roi_img, detect_move_bool, contours = self.detect_move(
                    roi_img, self.move_thr)
                # 움직임이 없는 경우 루프 건너뜀
                if detect_move_bool == False:
                    continue
                # # ROI 부분만 욜로 디텍션
                # 컨투어 표시
                tools.draw_contours(roi_img, contours)        
                # ROI 이미지를 원본이미지에 합성
                img = tools.merge_roi_img(self.img, roi_img, self.x1, self.y1)
                # 녹화 옵션
                cv2.rectangle(img, (self.x1, self.y1),(self.x2, self.y2),(0,255,0), 1)
                self.video.write(img) 
                frame_cnt += 1
            if false > 2:
                break
        # total_frames/fps
        message = ['done', total_frames, frame_cnt, self.fps, file]
        self.queue.put(message)
        self.cap.release()
        self.video.release()


    def detect_move(self, roi_img, thr=30):
        '''
        WorkerCCTV.detect_move()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, 움직임 Bool, contours
        '''
        plot_img = roi_img.copy()
        gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        # ROI를 설정합니다.
        self.roi_frame_1 = self.roi_frame_2 
        self.roi_frame_2 = self.roi_frame_3 
        self.roi_frame_3 = gray_img
        # frame1, frame2, frame3이 하나라도 None이면 원본+밝기 이미지 출력
        if self.roi_frame_1 is None or self.roi_frame_2 is None or self.roi_frame_3 is None:
            self.roi_color = (0, 0, 255)
            return plot_img, False, False
        # 움직임 감지
        diff_cnt, diff_img = self.get_diff_img()
    
        # 움직임이 임계값 이하인 경우 원본 출력
        if diff_cnt < thr:
            return plot_img, False, False
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
        diff_ab = cv2.absdiff(self.roi_frame_1, self.roi_frame_2)
        diff_bc = cv2.absdiff(self.roi_frame_2, self.roi_frame_3)

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        _, diff_ab_t = cv2.threshold(diff_ab, self.thr, 255, cv2.THRESH_BINARY)
        _, diff_bc_t = cv2.threshold(diff_bc, self.thr, 255, cv2.THRESH_BINARY)

        # 두 영상 차의 공통된 부분을 1로 만들어줌
        diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
        # 영상에서 1이 된 부분을 적당히 확장해줌(morpholgy)
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
        # 영상에서 1인 부분의 갯수를 셈
        diff_cnt = cv2.countNonZero(diff)
        return diff_cnt, diff
    
    def set_roi(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        

class PlayerClass:
    
    def __init__(self) -> None:
        # cv2 관련
        self.cap = None
        self.fps = None
        self.total_frames = 0    # 진행률을 확인하기 위한 총 프레임수
        self.curent_frame = 0    # 현재 프레임
        # 모델 
        self.model = None

    def fileopen(self, fileName):
        '''반드시 정의 해야 함'''
        if fileName:
            self.fileName = fileName
            self.cap = cv2.VideoCapture(fileName)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))          
            # 프레임 관련 정보 초기화
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            _, frame = self.cap.read() 
            self.img = frame
            if self.model is not None:
                detection = self.model(frame)[0]
                # 라벨을 초기화 하는 함수 작성        
                self.labels = [ v for _ , v in detection.names.items() ]
            return (frame, self.width, self.height)
        
    def cap_read(self, jump_frame, play_status):
        '''
        반드시 정의해야 함
        cap_read() 함수는 cv2.VideoCapture 객체를 통해 프레임을 읽어오고,
        이미지, 프레임(float), 플레이 상태(불리언)를 반환함
        '''
        ret, self.img = self.cap.read() 
        if ret:
            # 현재 프레임 번호가 self.jump_frame 의 배수일 때만 이미지 처리
            self.curent_frame = int( self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if self.curent_frame % jump_frame != 0:
                return self.img, self.curent_frame, play_status
            return self.img, self.curent_frame, play_status
        else:
            self.curent_frame = 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
            play_status = False
            return self.img, self.curent_frame, play_status
                

class ArgsDict:
                     
    arg_dict = {}  # 슬라이더 변수 저장
    detector_dict = {}  # 디텍터 클래스 저장 ex) {DetectorMosaic.tag: DetectorMosaic, ...}
    selected_mode = None  # 현재 드롭다운에서 선택된 모드
    detector = None   # 현재 선택된 디텍터 (모델로더의 드롭다운 변경시 초기화)
    roi_frame_1 = None   # 움직임 감지를 위한 프레임 저장
    roi_frame_2 = None
    roi_frame_3 = None
    roi_color = (0, 0, 255)   # 움직임 감지 ROI 색상
    track_ids = {}  # 추적된 객체의 id값
    

    @classmethod
    def setDetector(cls, tag):
        cls.detector = cls.detector_dict[tag]
        return
    
    @classmethod
    def setValue(cls, tag, _arg_dict):
        cls.arg_dict[tag] = _arg_dict

    @classmethod
    def enrollDetectors(cls, tag, _model_dict):
        cls.detector_dict[tag] = _model_dict

    @classmethod
    def getValue(cls, tag, arg):
        '''
        str: 'tag', '모자이크'
        key: '모자이크'
        '''
        return cls.arg_dict[tag][arg]

    @classmethod
    def clear(cls):
        cls.arg_dict = {}

    @classmethod
    def all(cls):
        print(cls.arg_dict)
        return cls.arg_dict
    
    @classmethod
    def getDetector(cls):
        return cls.detector_dict[cls.selected_mode]

    @classmethod
    def setRoiFrame(cls, gray_img):
        cls.roi_frame_1 = cls.roi_frame_2 
        cls.roi_frame_2 = cls.roi_frame_3 
        cls.roi_frame_3 = gray_img

    @classmethod
    def getRoiFrame(cls):
        return cls.roi_frame_1, cls.roi_frame_2, cls.roi_frame_3

    @classmethod
    def setRoiColor(cls, color):
        cls.roi_color = color
    
    @classmethod
    def getRoiColor(cls):
        return cls.roi_color
    
    @classmethod
    def setTrackIds(cls, track_id, cap_num):
        cls.track_ids[track_id] = [cap_num]


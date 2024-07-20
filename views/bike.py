import torch
import cv2
from ultralytics import YOLO
import os, random, time
from multiprocessing import Process
from views.control import tools
import easyocr
import numpy as np
from .run_ocr import OcrReader
import pandas as pd

class DetectorBike():
    '''
    cv2, YOLO를 이용한 이미지 처리
    '''
    def __init__(self, path, multiMode = False) -> None:
        print('이륜차 탐지 모드 실행')
        # 이미지 초기화
        self.base = path
        self.img_path = os.path.join(path, 'rsc/init.jpg')
        # C:\Users\prude\OneDrive\Documents\kimAI\rsc\init.jpg
        self.model_bike_path = os.path.join(path, 'rsc/models/yolov8n.pt')
        self.model_nbp_path = os.path.join(path, 'rsc/models/motobike_e300_b8_s640.pt')
        # 데이터 프레임
        self.df = pd.DataFrame({'si':[], 'giho':[], 'num':[]})
        # 이미지 읽기
        self.img = cv2.imread(self.img_path)
        # 탐지 영역 설정 활성화 상태
        self.region_status = False
        # GPU 사용하는 YOLO 모델 불러오기
        self.thr_bike = 0.6     # 욜로에서는 임계값, 이벤트에서는 영상 차이
        self.thr_nbp = 0.3
        self.labels = None
        self.track_ids = {}
        # cv2 관련
        self.cap = None
        self.fps = None
        self.total_frames = 0    # 진행률을 확인하기 위한 총 프레임수
        self.curent_frame = 0    # 현재 프레임
        # 모델 초기화
        # AI 모델 생성
        self.model = YOLO(self.model_bike_path)
        self.model_nbp = YOLO(self.model_nbp_path)
        self.reader = OcrReader()
        try:
            bike_img = cv2.imread(self.img_path)
            detection = self.model(bike_img)[0]
            print(detection.names.items())
            self.labels = [ v for _ , v in detection.names.items() ]
        except:
            print("모델 초기화 중 디텍션 오류 발생")
        # 라벨을 초기화 하는 함수 작성        


        
    def change_model(self, text):
        ''' 모델을 변경하는 함수 '''
        print('현재 생성된 객체를 제거 하고 초기화 함  \n구현예정')
        return 
    

    ##############
    ## 슬롯함수 ##
    ##############
    def fileopen(self, fileName):
        '''반드시 정의 해야 함'''
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
            print(self.df['si'].value_counts()[:3])
            print(self.df['giho'].value_counts()[:3])
            print(self.df['num'].value_counts()[:3])
            self.curent_frame = 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
            play_status = False
            return self.img, self.curent_frame, play_status
    
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(self, frame, thr):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img, thr

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        detections = self.model.track(frame, persist=True)[0]
        text = None
        font_scale = int(frame.shape[0]/30)
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            _cap_number = 0
            _xmin, _ymin, _xmax, _ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            xmin, ymin, xmax, ymax = tools.to_original_shape(frame.shape, frame.shape, _xmin, _ymin, _xmax, _ymax) # 원본
            try:
                _track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 오토바이만 검출하도록 함
            if _label_number != 3:
                continue
            # 임계값 이하는 생략 하라는 코드
            if _confidence < thr/100:
                continue
            bike_img = frame[ymin:ymax, xmin:xmax]
            # 번호판 이미지 검출
            nbp_img = self.detect_nbp_img(bike_img)
            # 휘어진 번호판 이미지 처리
            try:
                nbp_img = self.nbp_transform(nbp_img)
            except:
                return frame, None
            # ocr 처리
            if nbp_img is not None:
                si, giho, num = self.reader.read(nbp_img)
                _df = pd.DataFrame({'si':[si], 'giho':[giho], 'num':[num]})
                self.df = pd.concat([self.df, _df], ignore_index=True)
                frame[0:nbp_img.shape[0], 0:nbp_img.shape[1]] = nbp_img
        try:
            s = self.df['si'].value_counts().idxmax()
            g = self.df['giho'].value_counts().idxmax()
            n = self.df['num'].value_counts().idxmax()
            text = f'{s} {g} {n}'  # 누적 인식
        except:
            pass
        return frame, text
        
    def detect_move(self, roi_img, region_status, thr):
        '''
        바이크 탐지에서는 사용하지 않음                    
        '''
        return roi_img, True, thr




    def detect_nbp_img(self, bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        roi_img = None
        detection = self.model_nbp(bike_img)[0]
        # 번호판 검출
        for data_nbp in detection.boxes.data.tolist():
            xmin, ymin, xmax, ymax = int(data_nbp[0]), int(data_nbp[1]), int(data_nbp[2]), int(data_nbp[3])
            try:
                confidence_nbp, label = float(data_nbp[4]), int(data_nbp[5])
            except IndexError:
                continue
            if label != 1:
                continue
            roi_img = bike_img[ymin:ymax, xmin:xmax]
        return roi_img

    def reorderPts(self, pts):
        idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
        pts = pts[idx]  # x좌표로 정렬
        if pts[0, 1] > pts[1, 1]:
            pts[[0, 1]] = pts[[1, 0]]
        if pts[2, 1] < pts[3, 1]:
            pts[[2, 3]] = pts[[3, 2]]
        return pts

    def nbp_transform(self, frame):
        img = frame.copy()
        # 출력 영상 설정
        dw, dh = 300, 150
        srcQuad = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32)
        dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)
        dst = np.zeros((dh, dw), np.uint8)
        frame = cv2.GaussianBlur(frame, (3,3), 7)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 외곽선 검출 및 명함 검출
        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for pts in contours:
            # 너무 작은 객체는 제외
            if cv2.contourArea(pts) < 10:
                continue
            # 외곽선 근사화
            approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.05, True)
            # 컨벡스가 아니면 제외
            if not cv2.isContourConvex(approx) or len(approx) != 4:
                continue
            # cv2.polylines(frame, [approx], True, (0, 255, 0), 2, cv2.LINE_AA)
            srcQuad = self.reorderPts(approx.reshape(4, 2).astype(np.float32))
            pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
            dst = cv2.warpPerspective(img, pers, (dw, dh), flags=cv2.INTER_CUBIC)
        return dst

class DataPD():
    
    def __init__(self):
            # 자료 정리
        data = {
            "track_ID": [],
            "cap": [],
            "bike_thr": [],
            "ocr_si_thr": [],
            "ocr_giho_thr": [],
            "ocr_number_thr": [],
            "ocr_si": [],
            "ocr_giho": [],
            "ocr_number": []
        }
        self.df = pd.DataFrame(data)  # 트랙ID, cap넘버, bike_thr, ocr_si_thr, ocr_giho_thr, ocr_number_thr, ocr_si, ocr_giho, ocr_number


class MultiBike():
    '''
    Process 모듈을 상속 받아서
    detect_bike() 오토바이를 탐지 하여 tracking 하는 함수
    detect_nbp() tracking 된 오토바이의 번호판을 탐지하는 함수
    ocr_nbp() 번호판 이미지를 OCR하여 번호판을 추출하는 함수
    nbp_tracking_sort() 가장 확률이 높은 순으로 3개 선택하는 함수
    '''

    def __init__(self, fileName):
        self.queue = None
        # 경로 설정
        self.base = os.path.dirname(fileName)
        self.fileName = os.path.basename(fileName)
        self.output_path = os.path.dirname(os.path.dirname(__file__))
        self.output_path = os.path.join(self.output_path, 'output')
        # 아웃풋 경로 생성
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
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
        self.percentage = 0
        false = 0
        # 아웃풋 경로 생성
        if not os.path.exists(os.path.join(self.base, 'output')):
            os.makedirs(os.path.join(self.base, 'output'))
        outfile = os.path.join(self.base, 'output', f'{self.fileName}.mp4')
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
                roi_img, detect_bike_bool, contours = self.detect_bike(
                    roi_img, self.move_thr)
                # 움직임이 없는 경우 루프 건너뜀
                if detect_bike_bool == False:
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
        message = ['done', total_frames, frame_cnt, file]
        self.queue.put(message)
        self.cap.release()
        self.video.release()


    def detect_bike(self, img):
        '''
        WorkerCCTV.detect_bike()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, 움직임 Bool, contours
        '''
        # 디텍트 바이크
        # 번호판 roi 
        print('detect_bike()')

    def detect_nbp(self, img):
        '''
        이미지를 받아서 번호판을 디텍트하는 함수
        return plot_img, 번호판 좌표
        '''
        # 디텍트 넘버플레이트
        # 번호판 roi
        print('detect_nbp()')

    def ocr_nbp(self, img):
        '''
        번호판 이미지를 받아서 OCR을 수행하는 함수
        return OCR 결과
        [('경기', 0.7),('하남',0.7),('가',0.7),('1234',0.7)]
        '''
        # OCR
        print('ocr_nbp()')

    def nbp_tracking_sort(self, nbp_ocr_list):
        '''
        OCR 결과를 받아서 정렬하는 함수
        return 정렬된 OCR 결과
        [('경기', 0.7),('하남',0.7),('가',0.7)]
        '''
        # 정렬
        print('nbp_tracking_sort()')
        # return nbp_list
        pass
    
    

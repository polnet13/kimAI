import cv2
import os
import numpy as np
import pandas as pd
from ultralytics import YOLO
from control import tools
from control.run_ocr import OcrReader
from module.modelLoader import ModelClass
from module import generic 
# from module.generic import CustomBaseClass
from module.sharedData import DT
import settings


# class definition:



class DetectorBike():

    tag = '이륜차_번호판_감지'
    arg_dict = {
        '감지_민감도':1,
        }
    models = {
        'base': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt')),
        'model_nbp': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'reader': OcrReader(),
    }
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']
    
    img_path = os.path.join(settings.BASE_DIR, 'rsc/init.jpg')
    df = pd.DataFrame({'si':[], 'giho':[], 'num':[]})
    track_ids = {}
    
    def setup():
        print('setup()')
    # def __init__(self) -> None:
    #     super().__init__()
    #     # 슬라이더 설정
    #     DT.clear()
    #     DT.setValue(DetectorBike.tag, DetectorBike.arg_dict)
    #     self.tag = DetectorBike.tag

    #     # 모델 초기화
    #     try:
    #         bike_img = cv2.imread(DetectorBike.img_path)
    #         detector = DetectorBike.models['base']
    #         detection = detector(bike_img)[0]
    #         print(detection.names.items())
    #         self.labels = [ v for _ , v in detection.names.items() ]
    #     except:
    #         print("모델 초기화 중 디텍션 오류 발생")
    #     # 라벨을 초기화 하는 함수 작성        
 

    ##############
    ## 슬롯함수 ##
    ##############
    
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num):
        '''
        이 함수에서 실질적인 탐지 작업을 수행함
        input: origin_img

        output
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        # 이미지에 디텍션값을 넣으면 roi가 되는 함수를 만들어야 됨
        # 함수명은 detct_make_roiimg
        text = ''
        try:
            detections = DetectorBike.models['base'].track(frame, persist=True)[0]
        except:
            DetectorBike.models['base'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8n.pt'))
            detections = DetectorBike.models['base'].track(frame, persist=True)[0]
        print('탐지 중')
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            xmin, ymin, xmax, ymax  = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            try:
                track_id, _confidence, _label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 오토바이만 검출하도록 함
            if _label_number != 3:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = DT.arg_dict[DetectorBike.tag]['감지_민감도'] 
            if _confidence < thr/100:
                continue
            # 프레임의 절대좌표 => 상대좌표 => 오리지날 이미지의 절대좌표
            xmin, ymin, xmax, ymax = tools.abs_to_rel(frame.shape, xmin, ymin, xmax, ymax)
            xmin, ymin, xmax, ymax = tools.rel_to_abs(DT.img.shape, xmin, ymin, xmax, ymax)
            bike_img = DT.img[ymin:ymax, xmin:xmax]
            # 번호판 이미지 검출
            nbp_img = DetectorBike.detect_nbp_img(bike_img)
            # 휘어진 번호판 이미지 처리
            try:
                nbp_img = DetectorBike.nbp_transform(nbp_img)
            except:
                return frame, None
            # ocr 처리
            if nbp_img is not None:
                si, giho, num = DetectorBike.models['reader'].read(nbp_img)
                _df = pd.DataFrame({'si':[si], 'giho':[giho], 'num':[num]})
                DetectorBike.df = pd.concat([DetectorBike.df, _df], ignore_index=True)
                frame[0:nbp_img.shape[0], 0:nbp_img.shape[1]] = nbp_img
        try:
            s = DetectorBike.df['si'].value_counts().idxmax()
            g = DetectorBike.df['giho'].value_counts().idxmax()
            n = DetectorBike.df['num'].value_counts().idxmax()
            text = f'{s} {g} {n}'  # 누적 인식
        except:
            pass
        return frame, text
        


    def detect_nbp_img(bike_img):
        '''
        return 
        성공: 번호판 이미지
        실패: None
        ''' 
        roi_img = None
        detection = DetectorBike.models['model_nbp'](bike_img)[0]
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
    

    def nbp_transform(frame):
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
            srcQuad = DetectorBike.reorderPts(approx.reshape(4, 2).astype(np.float32))
            pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
            dst = cv2.warpPerspective(img, pers, (dw, dh), flags=cv2.INTER_CUBIC)
        return dst
    

    def reorderPts(pts):
        idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
        pts = pts[idx]  # x좌표로 정렬
        if pts[0, 1] > pts[1, 1]:
            pts[[0, 1]] = pts[[1, 0]]
        if pts[2, 1] < pts[3, 1]:
            pts[[2, 3]] = pts[[3, 2]]
        return pts


    def detect_move(roi_img):
        '''
        바이크 탐지에서는 사용하지 않음   
        return 값의 3번째는 True로 주어야 메인윈도우메니저의 무브 디텍트에서 안잡힘                 
        '''
        return roi_img, True



class MultiBike():
    '''
    Process 모듈을 상속 받아서
    detect_bike() 오토바이를 탐지 하여 tracking 하는 함수
    detect_nbp() tracking 된 오토바이의 번호판을 탐지하는 함수
    ocr_nbp() 번호판 이미지를 OCR하여 번호판을 추출하는 함수
    nbp_tracking_sort() 가장 확률이 높은 순으로 3개 선택하는 함수
    '''
    tag = '이륜차 탐지(멀티)'

    def __init__(self, fileName):
        print(self.tag)
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
    
    

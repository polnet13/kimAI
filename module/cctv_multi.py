import torch
import cv2
from ultralytics import YOLO
import os
from control import tools
from module.modelLoader import ModelClass
from module.sharedData import DT
import settings



class MultiCCTV:
    
    tag = 'CCTV_멀티작업'
    slider_dict = {
        '움직임_픽셀차이': 5,
        '감지_민감도': 1,
        '띄엄띄엄_보기':1,
        '밝기':0
        }
    models = {
        'model': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt')),
        'model_nbp':  YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 DT.models 로 전달함
    columns = ['객체ID', '프레임번호', 'x1', 'y1', 'x2', 'y2']

    # MultiCCTV.arg




    def __init__(self, fileName):
        # x1, y1, x2, y2 는 상대적 좌표임

        # 슬라이더 설정
        DT.setSliderValue(MultiCCTV.tag, MultiCCTV.slider_dict)
        # self.arg = ModelClass(MultiCCTV.arg_dict)
        super().__init__()
        self.track = False
        self.queue = None
        # 경로 설정
        self.base = os.path.dirname(fileName)
        self.fileName = os.path.basename(fileName)
        self.output_path = os.path.dirname(os.path.dirname(__file__))
        self.output_path = os.path.join(self.output_path, 'output')
        # 아웃풋 경로 생성
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        # 비디오 파일의 이미지 쉐입을 가져옴
        x1, y1, x2, y2 = DT.roi
        self.x1, self.y1, self.x2, self.y2 = tools.rel_to_abs(DT.img.shape, x1, y1, x2, y2)
        # cv2 이벤트 감지
        self.roi_frame_1 = None
        self.roi_frame_2 = None
        self.roi_frame_3 = None
        self.difframe = None
        self.move_thr = 30
        self.roi_color = (0, 0, 255)
        self.thr = 20
        self.diff_max = 20


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
                roi_img = self.img[self.y1:self.y2, self.x1:self.x2]
                # ROI 부분만 움직임 감지
                thr = 20
                roi_img, detect_move_bool, contours = self.detect_move(
                    roi_img, thr)
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
        # 수정필요: self.thr 슬라이더로 받기
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
        
import cv2
from ultralytics import YOLO
import os
from module.sharedData import DT
import settings
import pandas as pd
from control import tools
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
import numpy as np



class DetectorCCTV(QObject):

    tag = 'CCTV_플레이어'
    slider_dict = {
        '움직임_픽셀차이': 50,
        '감지_민감도': 1,
        '띄엄띄엄_보기':1,
        '밝기':0
        }
    models = {
        'model': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8n.pt')),
        'model_nbp':  YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 DT.models 로 전달함
    btn_names = ['btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5']

    # 시그널
    reset = Signal()
    signal_start = Signal(int)
    signal_end = Signal(int)

    def setup():
        # 슬라이더 설정
        DT.clear()
        DT.setSliderValue(DetectorCCTV.tag, DetectorCCTV.slider_dict)
        DT.dfReset()

    
    #######################
    ## 슬롯함수 오버라이드 ##
    ######################## 
    # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num, realsize_bool):
        '''
        input: 원본해상도 이미지
        output: 원본해상도 욜로 이미지,
        검출된 객체에 대한 bbox와 텍스트를 생성하여 이미지에 출력
        개인정보 가리기와 bbox 생성을 선택할 수 있음
        
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 

        if realsize_bool:
            roi_x = DT.roi_point[0][0]
            roi_y = DT.roi_point[0][1]
            shape = DT.original_shape
        else:
            roi_x = DT.roi_point[1][0]
            roi_y = DT.roi_point[1][1]
            shape = DT.resized_shape
        text = ''
        try:
            detections = DetectorCCTV.models['model'].track(frame, persist=True)[0]
        except Exception as e:
            DetectorCCTV.models['model'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8n.pt')).to('cpu')
            detections = DetectorCCTV.models['model'].track(frame, persist=True)[0]
    
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                continue
            track_id, xmin, ymin, xmax, ymax = None, None, None, None, None
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if int(data[6]) != 0:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = DT.getValue(DetectorCCTV.tag, '감지_민감도')
            if confidence < thr/100:
                continue
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
            cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
            # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가
            if DT.play_status:
                # xmin, ymin, xmax, ymax의 값은 roi_img의 상대좌표인데, 이를 전체 이미지에서의 상대좌표로 변환(전체 이미지 shape은 DT.img.shape)
                xmin = roi_x + xmin
                ymin = roi_y + ymin
                xmax = roi_x + xmax
                ymax = roi_y + ymax
                xmin, ymin, xmax, ymax = tools.abs_to_rel(shape, xmin, ymin, xmax, ymax)
                DT.detection_add(DT.cap_num, track_id, label, xmin, ymin, xmax, ymax, confidence)
        return frame, text
    
    def make_plot_df():
        DT.df_plot = DT.df.copy()

    def drop(index, inplace=True):
        DT.applyDrop(index, inplace=True)


    def detect_move(roi_img):
        '''
        DetectorCCTV.detect_move()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, region_status
        '''
        # bright = self.Slider_bright.value()
        bright = DT.getValue(DetectorCCTV.tag, '밝기')
        roi_img = cv2.add(roi_img, bright)   
        # 밝기 처리한 이미지를 리턴하므로 원본 이미지를 복사하여 사용
        plot_img = roi_img.copy()
        gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        # ROI를 설정합니다.
        DT.setRoiFrame(gray_img)
        # frame1, frame2, frame3이 하나라도 None이면 원본+밝기 이미지 출력
        if DT.roi_frame_1 is None or DT.roi_frame_2 is None or DT.roi_frame_3 is None:
            DT.setRoiColor((0, 0, 255))
            return plot_img, False
        # 움직임 감지
        diff_cnt, diff_img = DetectorCCTV.get_diff_img()
        # 움직임이 임계값 이하인 경우 원본 출력
        mean_brightness = np.mean(roi_img)
        brightness = 1
        if mean_brightness > 80:
            brightness= 2
        thr = DT.getValue(DetectorCCTV.tag, '움직임_픽셀차이')
        thr = thr * DT.move_slider_scale * brightness
        if diff_cnt < thr:
            return plot_img, False
        DT.setRoiColor((0, 255, 0))      
        # 영상에서 1인 부분이 thr 이상이면 움직임이 있다고 판단 영상출력을 하는데 움직임이 있는 부분은 빨간색으로 테두리를 표시
        contours, _ = cv2.findContours(diff_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return plot_img, True
    

    def get_diff_img():
        '''
        return diff_cnt(영상간 차이값), diff(이미지)
        활용 if diff_cnt > self.thr:
        
        연속된 3개의 프레임에서 1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        ''' 
        roi_frame_1, roi_frame_2, roi_frame_3 = DT.getRoiFrame()
        # 1,2 프레임, 2,3 프레임 영상들의 차를 구함
        diff_ab = cv2.absdiff(roi_frame_1, roi_frame_2)
        diff_bc = cv2.absdiff(roi_frame_2, roi_frame_3)

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        thr = DT.getValue(DetectorCCTV.tag, '감지_민감도')
        _, diff_ab_t = cv2.threshold(diff_ab, thr, 255, cv2.THRESH_BINARY)
        _, diff_bc_t = cv2.threshold(diff_bc, thr, 255, cv2.THRESH_BINARY)

        # 두 영상 차의 공통된 부분을 1로 만들어줌
        diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
        # 영상에서 1이 된 부분을 적당히 확장해줌(morpholgy)
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
        # 영상에서 1인 부분의 갯수를 셈
        diff_cnt = cv2.countNonZero(diff)
        return diff_cnt, diff
    

    #####################
    ## 커스텀 버튼 함수 ##
    #####################

    def btn1():
        print('btn1')

    def btn2():
        print('btn2')

    def btn3():
        print('btn3')

    def btn4():
        print('btn4')

    def btn5():
        print('btn5')

    def btn6():
        print('btn6')

    btns = [btn1, btn2, btn3, btn4, btn5, btn6]
    




    


  
import cv2
from ultralytics import YOLO
import os
from module.generic import ArgsDict
import settings


class DetectorCCTV:

    tag = 'CCTV_플레이어'
    arg_dict = {
        '움직임_픽셀차이': 5,
        '감지_민감도': 1,
        '띄엄띄엄_보기':1,
        '밝기':0
        }
    models = {
        'model': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt')),
        'model_nbp':  YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/motobike_e300_b8_s640.pt')),
        'model_face': YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/model_face.pt')),
    } # 어디서 읽어서 ArgsDict.models 로 전달함
    


    def __init__(self) -> None:
        super().__init__()
        # 슬라이더 설정
        ArgsDict.clear()
        ArgsDict.setValue(DetectorCCTV.tag, DetectorCCTV.arg_dict)
        # self.arg = ModelClass()
        self.tag = DetectorCCTV.tag
        self.track = False
        # 움직임 감지
        self.diff_max = ArgsDict.getValue(self.tag, '움직임_픽셀차이')
    
    #######################
    ## 슬롯함수 오버라이드 ##
    ######################## 
    def detect_move(roi_img, region_status):
        '''
        DetectorCCTV.detect_move()
        이미지 3개를 받아서 흑백으로 변환(빠른 연산을 위해서)
        1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        return plot_img, region_status
        '''
        # bright = self.Slider_bright.value()
        bright = ArgsDict.getValue(DetectorCCTV.tag, '밝기')
        roi_img = cv2.add(roi_img, bright)   
        # 밝기 처리한 이미지를 리턴하므로 원본 이미지를 복사하여 사용
        plot_img = roi_img.copy()
        gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        # ROI를 설정합니다.
        ArgsDict.setRoiFrame(gray_img)
        # frame1, frame2, frame3이 하나라도 None이면 원본+밝기 이미지 출력
        if ArgsDict.roi_frame_1 is None or ArgsDict.roi_frame_2 is None or ArgsDict.roi_frame_3 is None:
            ArgsDict.setRoiColor((0, 0, 255))
            return plot_img, region_status, False
        # 움직임 감지
        diff_cnt, diff_img = DetectorCCTV.get_diff_img()
        # 움직임이 임계값 이하인 경우 원본 출력
        thr = ArgsDict.getValue(DetectorCCTV.tag, '움직임_픽셀차이')
        if diff_cnt < thr:
            return plot_img, region_status, False
        ArgsDict.setRoiColor((0, 255, 0))      
        # 영상에서 1인 부분이 thr 이상이면 움직임이 있다고 판단 영상출력을 하는데 움직임이 있는 부분은 빨간색으로 테두리를 표시
        contours, _ = cv2.findContours(diff_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return plot_img, region_status, True
    

    def get_diff_img():
        '''
        return diff_cnt(영상간 차이값), diff(이미지)
        활용 if diff_cnt > self.thr:
        
        연속된 3개의 프레임에서 1,2프레임과 2,3프레임의 차이를 구하고,
        두 차이 이미지를 비교하여 움직임이 있는 부분을 찾아내는 함수
        ''' 
        roi_frame_1, roi_frame_2, roi_frame_3 = ArgsDict.getRoiFrame()
        # 1,2 프레임, 2,3 프레임 영상들의 차를 구함
        diff_ab = cv2.absdiff(roi_frame_1, roi_frame_2)
        diff_bc = cv2.absdiff(roi_frame_2, roi_frame_3)

        # 영상들의 차가 threshold 이상이면 값을 255(백색)으로 만들어줌
        thr = ArgsDict.getValue(DetectorCCTV.tag, '감지_민감도')
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
    

        # yolo 이미지 디텍션 함수
    def detect_yolo_track(frame, cap_num):
        '''
        input: 원본해상도 이미지
        output: 원본해상도 욜로 이미지,
        검출된 객체에 대한 bbox와 텍스트를 생성하여 이미지에 출력
        개인정보 가리기와 bbox 생성을 선택할 수 있음
        
        frame: 원본 해상도의 욜로 처리된 이미지
        img: cv2 이미지(바운딩 박스 처리된 이미지)
        track_id: 추적된 객체의 id값
        ''' 
        text = ''
        try:
            detections = DetectorCCTV.models['model'].track(frame, persist=True)[0]
        except Exception as e:
            print(e)
            # 욜로 트래커 초기화
            DetectorCCTV.models['model'] = YOLO(os.path.join(settings.BASE_DIR, 'rsc/models/yolov8x.pt'))
            detections = DetectorCCTV.models['model'].track(frame, persist=True)[0]
    
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            try:
                track_id, confidence, label_number = int(data[4]), float(data[5]), int(data[6])
            except IndexError:
                continue
            # 사람만 검출하도록 함(추후 수정 필요)\
            if label_number != 0:
                continue
            # 임계값 이하는 생략 하라는 코드
            thr = ArgsDict.getValue(DetectorCCTV.tag, '감지_민감도')
            if confidence < thr/100:
                continue
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 2)
            cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
            # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가
            if track_id not in ArgsDict.track_ids:
                ArgsDict.setTrackIds(track_id, cap_num)
        return frame, text
 

    @classmethod
    def getTrackid(cls, track_id):
        return cls.track_ids[track_id] 

  
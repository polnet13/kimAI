import os
from control import tools
import pandas as pd


class DT:
    '''
    DT: 앱에서 공유할 Data 와 입출력 매서드를 정의한 클래스

    DT.sliderDict: {'태그':{'민감도':3}, ...} 찾을 때: DT.sliderDict['태그']['민감도']
    ''' 
    device = 'cuda'   # 'cuda' or 'cpu'
    # BASE_DIR
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUT_DIR = os.path.join(BASE_DIR, 'output')
    # OCR 커스텀
    model_name = 'best_norm_ED'
    model_alchitecture = 'None-VGG-BiLSTM-CTC-Seed1111'
    OCR_MODEL = os.path.join(BASE_DIR, 'rsc', 'saved_models', model_alchitecture)
    # 변수
    sliderDict = {}  # 슬라이더 변수 저장: 
    valDict = {}  # 슬라이더 제외 변수 저장
    detector_dict = {}  # 디텍터 클래스 저장 ex) {DetectorMosaic.tag: DetectorMosaic, ...}
    selected_mode = None  # 현재 드롭다운에서 선택된 모드
    detector = None   # 현재 선택된 디텍터 (모델로더의 드롭다운 변경시 초기화)
    roi = (0,0,1,1) # (x1, y1, x2, y2) 상대적좌표(백분율)
    # roi_point: plot_img 함수에서 매번 값을 계산하면 오버헤드 발생해서 미리 따는거임
    roi_point = [(0,0,0,0), (0,0,0,0)] # [ orignal_roi, resized_roi ] 
    original_shape = (0,0)
    resized_shape = (0,0)
    roi_frame_1 = None   # 움직임 감지를 위한 프레임 저장
    roi_frame_2 = None
    roi_frame_3 = None
    # 움직임
    thr_move_slider_multi = 50
    scale_move_thr = 1
    roi_color = (0, 0, 255)   # 움직임 감지 ROI 색상
    # 트래킹
    track_ids = {}  # 추적된 객체의 id값
    detection_list = []  # df 로 만들면 항상 리셋 시켜야 됨
    columns=['frame', 'ID', 'label', 'x1', 'y1', 'x2', 'y2', 'thr']
    # 데이터 프레임
    df = pd.DataFrame(columns=columns)  # 전체 저장
    df_temp = pd.DataFrame(columns=columns)  # df에 추가하기 전에 임시로 저장
    df_plot = pd.DataFrame(columns=columns)  # 출력전에 정리해서 저장
    # 플레이어 관련
    img = None  # 오리지날 이미지임 / 보관하고 있다가 출력할 때 또는 부분에서 이미지 디텍션할 때
    play_status = False
    region_status = False
    cap_num = 0
    total_frames = 0
    fpst = 0
    width = 0
    height = 0
    check_realsize = False
    time_delay = 0
    # 시작, 종료점
    start_point = None
    end_point = None
    # 메인 윈도우 관련
    fileNames = None
    fileName = None
    # 멀티 관련
    queue = None
    flag_multiCCTV = False
    


    @classmethod
    def setMoveSliderScale(cls):
        '''
        roi 변화에 따른 슬라이더 스케일 조정

        영상이 바뀌거나 => player_fileopen
        디텍터가 바뀌거나 => cls.setDetector
        checkbox_realsize가 바뀔때 => mainwindwo.slot_btn_df_reset
        roi가 바뀔때 => mainwindow.mouseReleaseEvent
        멀티 open 했을 때 => mainwindow.slot_btn_multi_open
        '''
        if cls.check_realsize:
            resolution = DT.roi_point[0]
        else:
            resolution = DT.roi_point[1]
        w = resolution[2]-resolution[0]
        h = resolution[3]-resolution[1]
        m = min(w, h)
        pic_count = m**2  # roi의 최소변 제곱
        magic_num = 15260
        cls.scale_move_thr = pic_count/magic_num
        print(f'슬라이더 스케일: {DT.scale_move_thr}')



    @classmethod
    def setRealsize(cls, bool):
        cls.check_realsize = bool

    @classmethod
    def detection_add(cls, cap_num, track_id, label, x1, y1, x2, y2, thr):
        # 이전버전 roiTemp_add와 동일한 기능
        '''캡 정보를 리스트로 저장만 하다가 플레이 상태가 아닐 때 df로 변환'''
        x1 = round(x1, 2)
        y1 = round(y1, 2)
        x2 = round(x2, 2)
        y2 = round(y2, 2)
        thr = round(thr, 2)
        cls.detection_list.append((cap_num, track_id, label, x1, y1, x2, y2, thr))

    @classmethod
    def detection_list_to_df(cls):
        cls.df_temp = pd.DataFrame(cls.detection_list, columns=cls.columns)
        cls.df_temp = cls.df_temp.dropna(axis=1, how='all')
        cls.detection_list.clear()
        cls.df = pd.concat([cls.df, cls.df_temp], ignore_index=True)
    
    
    @classmethod
    def roiTemp_clear(cls):
        pass
        # cls.detection_list.clear()


    @classmethod
    def setFlagmulticctv(cls, bool):
        cls.flag_multiCCTV = bool


    @classmethod
    def setSelectedMode(cls, selected_menu_text):
        cls.selected_mode = selected_menu_text
        cls.detector = cls.detector_dict[cls.selected_mode]

    @classmethod
    def reset(cls):
        '''
        디텍터 초기화 코드
        '''
        cls.df = None
        cls.df = pd.DataFrame(columns=cls.columns) 
        cls.detector = cls.detector_dict[cls.selected_mode]
        DT.dfReset()
        DT.setSliderValue(DT.detector_dict[DT.selected_mode].tag, 
                          DT.detector_dict[DT.selected_mode].slider_dict)
        # cls.detector 객체에 df 속성이 있는 지 확인하는 코드
        if hasattr(cls.detector, 'df'):
            cls.detector.reset_df()
        

    @classmethod
    def setRoiPoint(cls):
        '''
        roi_point = (900, 400)
        원본이미지와 GUI 화면용 이미지의 ROI 좌표를 생성
        '''
        xmin, ymin, xmax, ymax = cls.roi
        cls.roi_point[0] = (tools.rel_to_abs(DT.img.shape, xmin, ymin, xmax, ymax))
        cls.roi_point[1] = (tools.rel_to_abs(DT.resized_shape, xmin, ymin, xmax, ymax))
        cls.setMoveSliderScale()


    @classmethod
    def setResizedShape(cls, shape):
        cls.resized_shape = shape

    @classmethod
    def setOriginalShape(cls, shape):
        cls.original_shape = shape

    @classmethod
    def setImg(cls, img):
        cls.img = img
        
    @classmethod
    def setFps(cls, fps):
        cls.fps = fps

    @classmethod
    def setRegionStatus(cls, bool):
        cls.region_status = bool

    @classmethod
    def setTotalFrames(cls, total_frames):
        cls.total_frames = total_frames


    @classmethod
    def setWidth(cls, width):
        cls.width = width

    @classmethod
    def setHeight(cls, height):
        cls.height = height

    @classmethod
    def setCapNum(cls, cap_num):
        cls.cap_num = cap_num   

    @classmethod
    def setPlayStatus(cls, status):
        cls.play_status = status

    @classmethod
    def setRoi(cls, tuple):
        '''백분율 튜플 (x1, y1, x2, y2)'''
        cls.roi = tuple
        if DT.img.all() != None:
            DT.setRoiPoint()
        DT.setMoveSliderScale()

    @classmethod
    def setDetector(cls, tag):
        cls.detector = cls.detector_dict[tag]
        cls.setMoveSliderScale()
        return
    
    @classmethod
    def addValue(cls, _tag_name, _valDict):
        '''삭제 ㅇ예정'''
        cls.valDict[_tag_name] = _valDict

    @classmethod
    def setSliderValue(cls, _tag_name, _sliderDict):
        cls.sliderDict[_tag_name] = _sliderDict

    @classmethod
    def enrollDetectors(cls, tag, _model_dict):
        cls.detector_dict[tag] = _model_dict

    @classmethod
    def getValue(cls, tag, key):
        '''
        str: 'tag', '모자이크'
        key: '민감도'
        '''
        return cls.sliderDict[tag][key]


    @classmethod
    def all(cls):
        print(cls.sliderDict)
        return cls.sliderDict
    
    @classmethod
    def getDetector(cls):
        return cls.detector_dict[cls.selected_mode]

    @classmethod
    def setRoiFrame(cls, gray_img):
        '''
        cls.roi_frame_1 = cls.roi_frame_2 
        cls.roi_frame_2 = cls.roi_frame_3 
        cls.roi_frame_3 = gray_img
        '''
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


    @classmethod
    def dfReset(cls):
        '''
        df컨트롤
        '''
        cls.df = pd.DataFrame(columns=DT.columns)
        cls.df_plot = pd.DataFrame(columns=DT.columns)

    @classmethod
    def mosaic_df(cls, obj_id):
        '''
        mosaic_df(): 객체 아이디를 넘기면 
        # DT.temp_df에서 해당 객체 ID를 가진 행을 삭제
        # DT.df는 temp_df로 다시 생성하는 함수
        # 해당 객체ID를 가진 행을 삭제
        '''
        df = cls.df_plot
        cls.df = df


    @classmethod
    def applyDrop(cls, index, inplace=True):
        '''
        drop the row by index
        '''
        cls.df = cls.df.drop(index).reset_index(drop=True)


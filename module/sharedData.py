import os
from control import tools
import settings


class DT:
    '''
    DT: 앱에서 공유할 Data 와 입출력 매서드를 정의한 클래스

    DT.arg_dict: {'태그':{'민감도':3}, ...} 찾을 때: DT.arg_dict['태그']['민감도']
    ''' 

    arg_dict = {}  # 슬라이더 변수 저장: 
    detector_dict = {}  # 디텍터 클래스 저장 ex) {DetectorMosaic.tag: DetectorMosaic, ...}
    selected_mode = None  # 현재 드롭다운에서 선택된 모드
    detector = None   # 현재 선택된 디텍터 (모델로더의 드롭다운 변경시 초기화)
    roi_frame_1 = None   # 움직임 감지를 위한 프레임 저장
    roi_frame_2 = None
    roi_frame_3 = None
    roi_color = (0, 0, 255)   # 움직임 감지 ROI 색상
    track_ids = {}  # 추적된 객체의 id값
    # 플레이어 관련
    img = None  # 오리지날 이미지임 / 보관하고 있다가 출력할 때 또는 부분에서 이미지 디텍션할 때
    play_status = False
    region_status = False
    cap_num = 0
    total_frames = 0
    fpst = 0
    # 메인 윈도우 관련
    fileNames = None
    fileName = os.path.join(settings.BASE_DIR, 'rsc/init.jpg')
    width = 0
    height = 0
    roi = (0,0,1,1) # (x1, y1, x2, y2) 상대적좌표(백분율)
    roi_point = [(0,0,0,0), (0,0,0,0)] # [원본이미지 좌표, 비디오(x: 680) 좌표] / roi 조정때, 
 

    @classmethod
    def setRoiPoint(cls, img_shape):
        '''
        원본이미지와 GUI 화면용 이미지의 ROI 좌표를 생성
        '''
        xmin, ymin, xmax, ymax = cls.roi
        cls.roi_point[0] = (tools.shape_to_absPoint(DT.img.shape, xmin, ymin, xmax, ymax))
        cls.roi_point[1] = (tools.shape_to_absPoint(img_shape, xmin, ymin, xmax, ymax))

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

    @classmethod
    def setFileNames(cls, fileNames):
        cls.fileNames = fileNames

    @classmethod
    def setFileName(cls, fileName):
        cls.fileName = fileName

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
        key: '민감도'
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


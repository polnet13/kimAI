import os
import cv2
import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO


from control import tools
import settings




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
    # 메인 윈도우 관련
    fileNames = None
    roi = (0,0,0,0) # x1, y1, x2, y2

    

    @classmethod
    def setRoi(cls, tuple):
        '''(x1, y1, x2, y2)'''
        cls.roi = tuple


    @classmethod
    def setFileNames(cls, fileNames):
        cls.fileNames = fileNames

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


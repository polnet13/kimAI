import os
import cv2
import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO


from control import tools
from views.sharedData import DT




class PlayerClass:
    
    def __init__(self) -> None:
        self.model = None
        self.cap = None

    def open(self, fileName):
        '''반드시 정의 해야 함'''
        if fileName:
            self.fileName = fileName
            self.cap = cv2.VideoCapture(fileName)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            _height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
            # 프레임 관련 정보 초기화
            _total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  
            _fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            _, original_img = self.cap.read() 
            _img = tools.resize_img(original_img, 680)
            DT.setOriginalShape(original_img.shape[:2])
            DT.setResizedShape(_img.shape[:2])
            print('original_shape:', original_img.shape[:2])
            print('resized_shape:', _img.shape[:2])
            DT.setWidth(_width)
            DT.setHeight(_height)        
            DT.setTotalFrames(_total_frames)
            DT.setFps(_fps)
            DT.setImg(original_img)
            return 
        
    def cap_read(self):
        '''
        반드시 정의해야 함
        DT.img에 이미지를 저장하고, DT.play_status에 플레이 상태를 저장함
        cap_read() 함수는 cv2.VideoCapture 객체를 통해 프레임을 읽어오고,
        이미지, 프레임(float), 플레이 상태(불리언)를 반환함
        '''
        ret, original_img = self.cap.read() 
        DT.setImg(original_img)
        if ret:
            _curent_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            DT.setCapNum(_curent_frame-1)
        else:
            DT.setPlayStatus(False)
            DT.setCapNum(0)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


    ## 실제 프레임하고 안맞음 311-069: 240정도 14300 |  60프레임당 1정도 엇나감
                

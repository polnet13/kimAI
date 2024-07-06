

import cv2
from ultralytics import YOLO


class Detector:
    def __init__(self, model_path):
        self.a = model_path       
        # GPU 사용하는 YOLO 모델 불러오기
        self.model = YOLO(self.a)
        self.thr = 5
        self.labels = None
        self.track_ids = {}
        self.init_model()
    
        # 모델을 초기화 하는 함수
    def init_model(self):
        if not self.file_label:
            self.img = cv2.imread(r'my_project\qt_django_yolo\rsc\init.jpg')
            detection = self.model(self.img)[0]
            # 라벨을 초기화 하는 함수 작성        
            self.labels = [ v for _ , v in detection.names.items() ]
            print('init_model 매서드 실행')

    
    def detect_image(self):
        pass
    
        
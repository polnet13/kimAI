import cv2
from ultralytics import YOLO
import os



# 연속으로 인퍼런스 
def inference_continuous(cap, model, device):
    cap = cap
    
    ret = True

    while ret:
        ret, frame = cap.read()
        if not ret:
            break   
        cap_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(cap_num)
        # cap_num = cap.get(프레임) 
        detections = model.track(frame, persist=True, device=device)[0]
    
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if label not in [0,2,3,5,7,9]:
                continue
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
            cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
            # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가


# 연속으로 인퍼런스 
def inference_dict(cap, modelList, n, device):
    cap = cap
    
    ret = True

    while ret:
        ret, frame = cap.read()
        if not ret:
            break   
        cap_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(cap_num)
        # cap_num = cap.get(프레임) 
        detections = modelList[n].track(frame, persist=True, device=device)[0]
    
        # yolo result 객체의 boxes 속성에는 xmin, ymin, xmax, ymax, confidence_score, class_id 값이 담겨 있음
        for data in detections.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            if len(data) < 7:  # data 리스트의 길이가 7보다 작은 경우 해당 데이터를 건너뛰도록 합니다. 이를 통해 인덱스 오류를 방지
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3]) # 리사이즈
            track_id, confidence, label = int(data[4]), float(data[5]), int(data[6])
            # 검출대상 설정
            # (0, 'person'), (2, 'car'), (3, 'motorcycle'), (5, 'bus'), (7, 'truck'), (9, 'traffic light')
            if label not in [0,2,3,5,7,9]:
                continue
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (200,100,200), 1)
            cv2.putText(frame, f'{track_id}', (xmin, ymin-5), cv2.FONT_ITALIC, 0.5, (255,255,255), 1)
            # 추적한 id값이 새로운 id 이고 태그 옵션이 켜져 있으면 값을 딕셔너리에 추가


# 모델을 선택해서 인퍼런스 


# 실행

path = r'C:\Users\prude\OneDrive\Pictures\20240724_174847.mp4'
modeln = YOLO(r'C:\Users\prude\kimAI\rsc\models\yolov8n.pt')
models = YOLO(r'C:\Users\prude\kimAI\rsc\models\yolov8s.pt')
modelm = YOLO(r'C:\Users\prude\kimAI\rsc\models\yolov8m.pt')
modell = YOLO(r'C:\Users\prude\kimAI\rsc\models\yolov8l.pt')
modelx = YOLO(r'C:\Users\prude\kimAI\rsc\models\yolov8x.pt')

modelDict = {'n':modeln, 's':models, 'm':modelm, 'l':modell, 'x':modelx}

cap = cv2.VideoCapture(path)
import time
time_list=[]
key_list=[]


modelList = [modeln, models, modelm, modell, modelx]
start = time.time()
inference_continuous(cap, models, device='cuda')
end = time.time()
t = end-start
print(t)


del inference_continuous
del cap

 



# 계속 인퍼런스
# for k, model in modelList.items():
# inference_dict(cap, modelList, n, device):
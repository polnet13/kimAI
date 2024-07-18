from ultralytics import YOLO
import cv2
import os, time
 



model1 = YOLO(r'C:\Users\prude\OneDrive\Documents\kimAI\rsc\models\yolov8n.pt')
model2 = YOLO(r'C:\Users\prude\OneDrive\Documents\kimAI\rsc\models\yolov10n.pt')


file_path = r'C:\Users\prude\OneDrive\Pictures\bike2.mp4'
cap = cv2.VideoCapture(file_path)


def test_speed(model, cap):
    cnt = 0
    CONFIDENCE_THRESHOLD = 0.5
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detection = model(frame)[0]
        for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            cnt+=1
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = int(data[5])
            if label != 3:
                continue
            # 임계값 이하는 생략 하라는 코드
            confidence = float(data[4]) 
            if confidence < CONFIDENCE_THRESHOLD:
                continue
            n = cap.get(cv2.CAP_PROP_POS_FRAMES)
            print(n)

    endtime = time.time()
    totalFrame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # fps
    fps = totalFrame / (endtime - start_time)
    fps = int(fps)
    print(f'fps : {fps}')
    print(totalFrame)
    print(endtime - start_time)
    print(cnt)



test_speed(model2, cap)
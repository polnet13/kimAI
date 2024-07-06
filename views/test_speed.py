from ultralytics import YOLO
import cv2
import os, time
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.



start_time = time.time()
file_path = r'C:\Users\prude\OneDrive\Pictures\bike2.mp4'
model_path = r'C:\Users\prude\OneDrive\Documents\kimAI\rsc\models\yolov8n.pt'

model = YOLO(model_path)
cap = cv2.VideoCapture(file_path)

CONFIDENCE_THRESHOLD = 0.5


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # frame = cv2.resize(frame, (640, 480)) 
    # 이미지를 흑백으로 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 흑백 이미지를 3채널 BGR 이미지로 변환
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    detection = model(frame)[0]
    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]

        # 임계값 이하는 생략 하라는 코드
        confidence = float(data[4]) 
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])
        if label != 3:
            continue


        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

endtime = time.time()
totalFrame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# fps
fps = totalFrame / (endtime - start_time)
fps = int(fps)
print(f'fps : {fps}')
print(totalFrame)
print(endtime - start_time)
print(model_path)


import cv2

# 모자이크 처리 
def blind_img(img, xmin, ymin, xmax, ymax):
    '''
    xmin, ymin, xmax, ymax 좌표에 해당하는 이미지 모자이크 처리
    '''
    face = img[ymin:ymax, xmin:xmax]
    face = cv2.resize(face, (0, 0), fx=0.08, fy=0.08)
    face = cv2.resize(face, (xmax-xmin, ymax-ymin), interpolation=cv2.INTER_NEAREST)
    img[ymin:ymax, xmin:xmax] = face
    return img 

# 바운딩 박스 그리기
def draw_boxes(img, xmin, ymin, xmax, ymax):
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
    return img

# 탐지된 객체에 대한 정보를 이미지에 추가
def draw_detections(img, xmin, ymin, xmax, ymax, label, score):
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
    cv2.putText(img, f'{label} {score:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return img

# 해당영역에서 탐지 되었는지 확인
def check_detection(xmin, ymin, xmax, ymax, detection_list):
    for detection in detection_list:
        if detection[0] > xmin and detection[1] > ymin and detection[2] < xmax and detection[3] < ymax:
            return True
    return False


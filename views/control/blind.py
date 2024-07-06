import cv2

# xmin, ymin, xmax, ymax 좌표에 해당하는 이미지를 가리는 함수
def blind_img(img, xmin, ymin, xmax, ymax):
    face = img[ymin:ymax, xmin:xmax]
    face = cv2.resize(face, (0, 0), fx=0.08, fy=0.08)
    face = cv2.resize(face, (xmax-xmin, ymax-ymin), interpolation=cv2.INTER_NEAREST)
    img[ymin:ymax, xmin:xmax] = face
    return img 


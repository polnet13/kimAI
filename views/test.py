from paddleocr import PaddleOCR    
import cv2
import os 
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='korean') # need to run only once to download and load model into memory
img_path = r'C:\Users\prude\SynologyDrive\vscode\데이터셋_img\bike\bike_numberplate\05836.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)


result = result[0]
if os.path.isfile(img_path):
    print('file exist')
else:
    print('file not exist')
# 이미지 읽어 들이기
img = cv2.imread(img_path)
print(img.shape)
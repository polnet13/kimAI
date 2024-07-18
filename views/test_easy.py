import glob, random, cv2
import easyocr 


 

# 이미지를 OCR을 이용해서 번호판을 찾는 함수
def easy_ocr(img):
    reader_custom = easyocr.Reader(lang_list=['ko'], 
                                   user_network_directory=r'C:\Users\prude\OneDrive\Documents\kimAI\rsc\user_network',
                                   recog_network='best_accuracy',
                                   gpu=False
                                   )
    result_custom = reader_custom.readtext(img, detail=0)
    print(f'result_custom: {result_custom}')
    # reader_default = easyocr.Reader(lang_list=['ko'], gpu=False)
    # OCR을 이용해서 번호판 찾기
    # result_default = reader_default.readtext(img, detail=0)
    # print(f'result_default: {result_default}')

 
file_path = r'C:\Users\prude\SynologyDrive\Dataset\bike_nbp\*.jpg'
file_path = r'C:\Users\prude\SynologyDrive\Dataset\test_nbp\*.jpg'
# r'C:\Users\prude\SynologyDrive\vscode\dataset_img\bike\moto_v1' 경로의 파일을 모두 불러오기
img_files = glob.glob(file_path)
file_path = random.choice(img_files)


img = cv2.imread(file_path)
print(f'file_path = r"{file_path}"')
print(file_path)
easy_ocr(img)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
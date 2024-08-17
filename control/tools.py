import cv2
import os, time, sys
import inspect
from module.sharedData import DT
from control import tools   
import subprocess


def sort_roi(x1, y1, x2, y2):
    '''
    마우스 드래그시 roi를 정렬하는 함수
    x1, y1, x2, y2
    '''
    if x1 > x2:
            x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def resize_img(plot_img, x_res):
    '''
    이미지를 640으로 리사이즈
    '''
    height, width = plot_img.shape[:2]
    if width > x_res:
        ratio = x_res / width
        plot_img = cv2.resize(plot_img, (x_res, int(height * ratio)))
    return plot_img


def to_video_point_y(y, height):
    '''
    '''
    return y * 100 / height

def to_gui_point_x(x, width):
    '''
    '''
    return x * width / 100

def to_gui_point_y(y, height):
    '''
    '''
    return y * height / 100

def merge_roi_img(img, roi_img, x1, y1):
    '''원본 이미지에 roi이미지를 합성'''
    out_img = img.copy()
    out_img[y1:y1+roi_img.shape[0], x1:x1+roi_img.shape[1]] = roi_img
    return out_img

def draw_contours(img, contours):
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return img


def sort_files_by_size(filesPath):
    return sorted(filesPath, key=lambda x: os.path.getsize(x), reverse=True)


def shape_to_adjust(x, y):
    '''
    gui 좌표값 오차 보정 함수
    gui(720, 480)의 좌표 값을 입력된 이미지의 해상도에 맞춰 비디오의 좌표로 변환
    '''
    x = max(0, min(x-40, 720)) / 720  
    y = max(0, min(y-40, 720)) / 480  
    return x, y

def rel_to_abs(img_shape, xmin, ymin, xmax, ymax):
    '''
    이미지 쉐입과 상대적 좌표 => 절대적 좌표로 변환
    img_shape = img.shape
    '''
    # 욜로 디텍션 결과로 얻은 xmin, ymin, xmax, ymax의 상대적 좌표 값을 이미지의 사이즈에 맞게 변환
    h, w = img_shape[:2]
    xmin = int(xmin * w)
    ymin = int(ymin * h)
    xmax = int(xmax * w)
    ymax = int(ymax * h)
    return xmin, ymin, xmax, ymax

def abs_to_rel(img_shape, xmin, ymin, xmax, ymax):
    '''
    이미지 쉐입과 절대적 좌표 => 상대적 좌표로 변환
    '''
    h, w = img_shape[:2]
    xmin = xmin / w
    ymin = ymin / h
    xmax = xmax / w
    ymax = ymax / h
    return xmin, ymin, xmax, ymax

def plot_df_to_obj_img(img, cap_num):
    '''
    입력: img, cap_num
    처리: DT.df 정보를 이용하여 이미지에 바운딩 박스를 그림
    출력: img
    '''
    img = img.copy()
    df = DT.df
    cap_num = int(cap_num)
    df = df[df['frame']== cap_num]
    for index, row in df.iterrows():
        xmin, ymin, xmax, ymax = row['x1'], row['y1'], row['x2'], row['y2']  # roi에서의 상대적 좌표
        xmin, ymin, xmax, ymax = tools.rel_to_abs(img.shape, xmin, ymin, xmax, ymax)  # roi에서 전체 이미지로 좌표 변환
        img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 5)
        img = cv2.putText(img, f'{row["ID"]}', (xmin, ymin-5), cv2.FONT_ITALIC, 1, (255,255,255), 2)
    return img



def makeText(text, filepath):
    today = time.time()
    path = os.path.join(filepath, f'요약_{today}.txt')
    for row in text:
        with open(path, 'a') as f:
            f.write(row + '\n')

def roiImg_to_oigin(roi_img_shape, xmin, ymin, xmax, ymax):
    '''
    목표: 입력좌표는 roi에서의 상대적 좌표임 이것을 전체 이미지에서의 상대적 좌표로 변환
    [입력]
    roi_min_point: (xmin, ymin)
    roi_img.shape: (w, h)
    xmin, ymin, xmax, ymax: 상대적 좌표

    [출력]
    original_xmin, original_ymin, original_xmax, original_ymax
    '''
    xmin, ymin, xmax, ymax = rel_to_abs(roi_img_shape, xmin, ymin, xmax, ymax)
    original_xmin = DT.roi_point[0][0] + xmin
    original_ymin = DT.roi_point[0][1] + ymin
    original_xmax = DT.roi_point[0][0] + xmax
    original_ymax = DT.roi_point[0][1] + ymax
    return original_xmin, original_ymin, original_xmax, original_ymax

# 이미지를 입력 받으면 모자이크 처리된 이미지를 반환
def mosaic(img, xmin, ymin, xmax, ymax, ratio=0.01, full=False):
    '''
    이미지와 xmin, ymin, xmax, ymax값을 입력 받아서 xmin, ymin, xmax, ymax 좌표에 모자이크 처리
    '''
    # 모자이크 처리할 영역 추출
    if full is True:
        roi = img
        ymin, ymax, xmin, xmax = 0, img.shape[0], 0, img.shape[1]
    else:
        roi = img[ymin:ymax, xmin:xmax]
    
    # 모자이크 처리
    h, w = roi.shape[:2]
    small_w = max(1, int(w * ratio))
    small_h = max(1, int(h * ratio))
    small_roi = cv2.resize(roi, (small_w, small_h), interpolation=cv2.INTER_NEAREST)
    
    # 원래 크기로 확대
    mosaic_roi = cv2.resize(small_roi, (w, h), interpolation=cv2.INTER_NEAREST)
    
    # 모자이크 처리된 이미지를 원본 이미지에 삽입
    img[ymin:ymax, xmin:xmax] = mosaic_roi
    
    return img





def get_classes(module):
    """특정 모듈 객체에서 정의된 모든 클래스를 반환 

    Args:
    module: 대상 모듈 객체

    Returns:
    클래스 객체 목록
    """
    classes = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            classes.append(obj)

    return classes

def openpath(path):
    '''경로를 열어주는 함수'''
    if sys.platform.startswith('win'):
        os.startfile(path)
    elif sys.platform.startswith('linux'):
        subprocess.run(['xdg-open', path])
import cv2
import os, time


def guiToResolution(x, y, img):
    '''
    gui(720, 480)의 좌표 값을 해상도에 맞춰 변환
    '''
    height, width = img.shape[:2]
    x = max(0, min(x-40, 720)) / 720 * width
    y = max(0, min(y-40, 720)) / 480 * height
    return int(x), int(y)

def to_video_point_y(y, height):
    return y * 100 / height

def to_gui_point_x(x, width):
    return x * width / 100

def to_gui_point_y(y, height):
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

def get_roi_img(img, x1, y1, x2, y2):
    return img[y1:y2, x1:x2]

def sort_files_by_size(filesPath):
    return sorted(filesPath, key=lambda x: os.path.getsize(x), reverse=True)


def makeText(text, filepath):
    today = time.time()
    path = os.path.join(filepath, f'요약_{today}.txt')
    for row in text:
        with open(path, 'a') as f:
            f.write(row + '\n')

def to_original_shape(original_shape, _frame_shape, xmin, ymin, xmax, ymax):
    '''
    입력: original_shape, _frame_shape, xmin, ymin, xmax, yma
    출력: original_xmin, original_ymin, original_xmax, original_ymax
    '''
    # 원본 이미지의 너비와 높이
    original_width = original_shape[1]
    original_height = original_shape[0]

    # 조정된 이미지의 너비와 높이
    resized_width = _frame_shape[1]
    resized_height = _frame_shape[0]  # 이전 단계에서 계산한 높이

    # 너비와 높이의 비율 계산
    width_ratio = original_width / resized_width
    height_ratio = original_height / resized_height

    # 검출된 좌표를 원본 이미지의 좌표로 변환
    original_xmin = int(xmin * width_ratio)
    original_ymin = int(ymin * height_ratio)
    original_xmax = int(xmax * width_ratio)
    original_ymax = int(ymax * height_ratio)
    return original_xmin, original_ymin, original_xmax, original_ymax
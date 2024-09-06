


import cv2, time



file = r'C:\Users\prude\OneDrive\Pictures\외곽-5_CLIP-20240831T200543-20240901T143043_CH01\외곽-5_CLIP-20240831T200543-20240901T143043_CH01_3.mp4'


# 375881 에서 멈춘 이유 찾기
cap = cv2.VideoCapture(file)
no_frame = 0
error = 0


start = 0
# 토탈 프레임
end = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.set(cv2.CAP_PROP_POS_FRAMES, start)

for i in range(start, end):
    ret, frame = cap.read()
    if ret:
        no_frame = 0
    else:
        no_frame += 1
        error += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, i+1)
        print('노 프레임: ', i)
    if no_frame == 10:
        print('노 프레임 10개 이상')
        break
    cap_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
    print(cap_num, i, ret, type(frame), error, end)




def get_video_codec(video_path):
    """
    주어진 영상 파일의 코덱 정보를 반환합니다.

    Args:
        video_path (str): 영상 파일 경로

    Returns:
        str: 영상 코덱 정보 (예: 'H264', 'MPEG-4', 'DivX' 등)
    """
    # 영상 파일 열기
    cap = cv2.VideoCapture(video_path)
    # FOURCC 코드 가져오기
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    # FOURCC 코드를 문자열로 변환
    codec_str = ''.join([chr((int(fourcc) >> i) & 0xFF) for i in range(4 * 8 - 8, -8, -8)])
    # 캡처 해제
    cap.release()
    return codec_str

# 코덱 정보 가져오기
codec = get_video_codec(file)
print("영상 코덱:", codec)
 
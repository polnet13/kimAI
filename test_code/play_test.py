


import cv2, time, os



file = r'C:\Users\prudent13\Pictures\외곽-5_CLIP-20240831T200543-20240901T143043_CH01_3.mp4'


# 375881 에서 멈춘 이유 찾기
cap = None
cap = cv2.VideoCapture(file)
no_frame = 0
error = 0


start = 0
# 토탈 프레임
end = cap.get(cv2.CAP_PROP_FRAME_COUNT)
'''영상압축 함수'''
# 비디오 파일 열기
st = time.time()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 전체 프레임 가져오기
print('total_frames:', end)
fps = int(cap.get(cv2.CAP_PROP_FPS))
percentage = 0
newFrameNum = 0
# 비디오 생성
fail = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, start)
while True:
    ret, img = cap.read()
    curent_frame = cap.get(cv2.CAP_PROP_POS_FRAMES) 
    if fail > 5:
        print('실패 5회 이상으로 종료')
        print(fail, curent_frame, '/', end)
        break
    if curent_frame < 0:
        print('마이너스 프레임으로 종료')
        break
    # 프레임 처리
    if not ret:
        fail += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, curent_frame+1)
        print(fail, curent_frame, '/', end)
        if curent_frame >= end:
            print('끝 프레임 초과로 종료')
            break
    else:
        fail=0
        print(fail, curent_frame, '/', end)
    
# total_frames/fps
et = time.time()
cap.release()
print(et-st)

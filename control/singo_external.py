import pyautogui
import keyboard
import datetime, time
import pandas as pd


# 검색 이미지 경로: C:\Users\prude\kimAI\rsc\ico\target.jpg

# '접수번호','지령일','지령시간'
# while True:
#     if keyboard.is_pressed('F4'):
#         posi = pyautogui.position()
#         print(posi)
#         time.sleep(0.4)
#         break

def plus5min(row):
    return row + datetime.timedelta(minutes=5)

def ex_code(df):
    
    # 도착시간 계산
    print('df에서 도착시간 계산하기')
    df['도착시간'] = df['지령시간'].apply(plus5min)
    df['도착time'] = df['도착시간'].dt.strftime('%H:%M')
    receipt_num_list = df['접수번호'].tolist()
    arrival_time_list = df['도착time'].tolist()
    print(receipt_num_list, arrival_time_list)
    
    # 버튼 좌표 생성
    try:
        img_path = r'module\target.jpg'
        location = pyautogui.locateOnScreen(img_path, confidence= 0.98)
        print(f'센터값1: {location}')
        location = pyautogui.center(location)
        print(f'센터값2: {location}')
    except TypeError:
        print('이미지를 인식하지 몬함 <br>로케이션 값 지정해주삼')
    except Exception as e:
        print(e)
        

    for receipt_num, arrival_time in zip(receipt_num_list, arrival_time_list):
        print(receipt_num, arrival_time)
        
        try:
            pyautogui.moveTo(location, duration=0.2)
            pyautogui.click()
            print(f'접수번호 입력: {receipt_num}')
            time.sleep(0.2)
            print(f'도착시간 입력: {arrival_time}')
            time.sleep(0.2)
            print('사유 작성')
            time.sleep(0.2)
            print('증빙구분 선택')
            time.sleep(0.2)
            print('입력 버튼 클릭')
            time.sleep(3)
            print('--'*30)
            
        except Exception as e:
            print('오류정보')
            print(e)
    


# 마우스 우측하단이동시 작동을 중지 하도록 하는 기능 끄기
# pyautogui.FAILSAFE = False

# pyautogui.moveTo(300, 300, duration=0.4)  		# 좌표로 몇 초동안 이동
# pyautogui.dragTo(x, y, duration=Nseconds) 		# 마우스를 x,y좌표로 N초동안 드래그 

# pyautogui.hotkey('ctrl', 'c') 				# 복사
# pyautogui.hotkey('ctrl', 'v') 				# 붙여넣기

# pyautogui.position() 						# 현재 위치 
# pyautogui.click()  						# 클릭
# pyautogui.typewrite('Hello!', interval = 0.25)  	# 문자열 입력
# pyautogui.press('enter')					# 엔터
# pyautogui.press('tab')					# 탭

 
# img_path = r'module\target.jpg'
# location = pyautogui.locateOnScreen(image_path)
# location = pyautogui.center(location)
# pyautogui.click(location)

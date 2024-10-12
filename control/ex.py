import pyautogui
import keyboard
import datetime, time
import pandas as pd
import pyperclip


def plus5min(row):
    print(f'함수: plus5min({row})')
    if isinstance(row, str):
        row = datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S')
    return row + datetime.timedelta(minutes=5)

def tap_n(n):
    for _ in range(n):
        pyautogui.press('tab')
        time.sleep(0.03)


def ex_code(df):
    print(df)
    print('df 컬럼정보')
    print(df.columns)

    # df.columns = ['접수번호','신고내용','종결내용','종결보고자','사건번호','지령시간','지령time','코드','종결']
    time.sleep(1)
    # 도착시간 계산
    poi = pyautogui.position()
    print(poi)
    df['도착시간'] = df['지령시간'].apply(plus5min)
    df['도착date'] = df['도착시간'].dt.strftime('%Y-%m-%d')
    df['도착time'] = df['도착시간'].dt.strftime('%H:%M')
    receipt_num_list = df['접수번호'].tolist()
    arrival_time_date = df['도착date'].tolist()
    arrival_time_list = df['도착time'].tolist()
    print(receipt_num_list, arrival_time_date, arrival_time_list)
    
    # 임의동록 버튼 좌표 생성
    try:
        img_path = r'module\target.jpg'
        location = pyautogui.locateOnScreen(img_path, confidence= 0.9)
        location = pyautogui.center(location)
        print(f'임의등록 버튼: {location}')
    except TypeError:
        location = (1660, 320)
        pyautogui.alert(f'위치값 인식을 위해 ctrl + 0(숫자) 입력해서 익스플로러창 100%로 맞춰주삼 {location}')
    except Exception as e:
        print(e)

    # 접수번호 입력란 좌표 초기화
    receipt_num_xy = None

    # 증빙구분 좌표 초기화
    jb_xy = None

    # 등록여부 체크 초기화
    enrolled = None

    for receipt_num, arrival_date, arrival_time in zip(receipt_num_list, arrival_time_date, arrival_time_list):
        print(receipt_num, arrival_date, arrival_time)
        
        try:
            # 임의등록버튼 클릭
            print('임의등록 버튼 클릭!!')
            pyautogui.moveTo(location, duration=0.2)
            pyautogui.click()
            time.sleep(1)

            # 접수번호 좌표 있을 경우 좌표생성 패스
            if receipt_num_xy:
                pass
            # 접수번호 좌표 없을 경우 좌표 생성
            else:
                try:
                    img_path = r'module\1.jpg'
                    receipt_num_xy = pyautogui.locateOnScreen(img_path, confidence= 0.80)
                    print(f'센터값1: {receipt_num_xy}')
                    receipt_num_xy = pyautogui.center(receipt_num_xy)
                    print(f'센터값2: {receipt_num_xy}')
                except TypeError:
                    pyautogui.alert('접수번호 이미지를 인식하지 몬함 800*350')
                    receipt_num_xy = (800, 350)
                except Exception as e:
                    print(e)
            pyautogui.moveTo(receipt_num_xy, duration=0.2)
            pyautogui.click()
            pyautogui.typewrite(f'{receipt_num}', interval = 0.01)

            # 이미 등록된 경우 패스하기


            img_path4 = r'module\4.jpg'  # 이미 등록된
            img_path6 = r'module\6.jpg'  # 등록 가능한
            result4 = False
            result6 = False

            while True:
                result4 = pyautogui.locateOnScreen(img_path4, confidence= 0.9)
                if result4:
                    # 이미 등록된
                    result = 'stop'
                    break
                result6 = pyautogui.locateOnScreen(img_path6, confidence= 0.9)
                if result6:
                    # 등록 가능한
                    result = 'go'
                    break
                time.sleep(0.1)

            if result == 'stop':
                # 이미 등록된 경우 패스 하는 코드임
                tap_n(14)
                pyautogui.press('enter')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.1)
                continue
            # 도착일 입력: 탭6번 후 입력
            tap_n(6)
            pyautogui.typewrite(f'{arrival_date}', interval = 0.02)
            # 도착시간 입력
            pyautogui.press('tab')
            pyautogui.typewrite(f'{arrival_time}', interval = 0.02)
            # 사유 작성
            tap_n(2)
            pyperclip.copy('출동수당 누락으로 입력 함')
            pyautogui.hotkey('ctrl', 'v')
            # pyautogui.typewrite('출동수당 누락으로 입력 함', interval = 0.06)
            time.sleep(0.1)


            # 증빙구분선택 좌표 있을 경우 좌표생성 패스
            if jb_xy:
                pass
            # 증빙구분선택 좌표 없을 경우 좌표 생성
            else:
                try:
                    img_path = r'module\3.jpg'
                    jb_xy = pyautogui.locateOnScreen(img_path, confidence= 0.98)
                    print(f'센터값1: {jb_xy}')
                    jb_xy = pyautogui.center(jb_xy)
                    print(f'센터값2: {jb_xy}')
                except TypeError:
                    pyautogui.alert('증빙구분(3) 이미지를 인식하지 몬함')
                except Exception as e:
                    print(e)
            # 증빙구분 클릭
            pyautogui.moveTo(jb_xy, duration=0.2)
            pyautogui.click()
            time.sleep(0.2)


            # 입력버튼 좌표 있을 경우 좌표생성 패스
            tap_n(3)
            pyautogui.press('enter')
            time.sleep(0.7)
            enter_1 = False
            enter_2 = False

            while True:
                enter_1 = pyautogui.locateOnScreen(r'module\enter_1.jpg', confidence= 0.9)
                if enter_1:
                    print('임의등록을 하겠습니까? => 버튼 확인함')
                    break
                time.sleep(0.2)

            pyautogui.press('enter')
            while True:
                enter_2 = pyautogui.locateOnScreen(r'module\enter_2.jpg', confidence= 0.9)
                if enter_2:
                    print('저장되었습니다. => 버튼 확인함')
                    break
                time.sleep(0.2)

            pyautogui.press('enter')
            time.sleep(0.2)
            
        except Exception as e:
            print(e)
            print('위의 오류로 루프 종료함')
            break
            
    pyautogui.alert('끝')


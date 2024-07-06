import yt_dlp
import pyautogui
import time

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
from views.control import auto
 
 
def get_video(url, path):
    '''
    url: 다운받을 유튜브 url
    path: 다운 받을 경로
    '''
    os.chdir(os.path.join(path))
    # 작업경로를 다운로드 out폴더로 변경함
    ydl_opts = {
        "writesubtitles": True,
        "subtitlesformat": "vtt",
        "subtitleslangs": ["en", "ko"],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(dir(ydl))
        
def getWebSubtitle(url='https://downsub.com/'):
    # 브라우저 바로 닫힘 방지
    options = Options()
    options.add_experimental_option("detach", True)

    # 드라이버 경로 설정(없으면 드라이버 설치 하는 코드 임)
    service = Service(executable_path= ChromeDriverManager().install())
    # 드라이버 로드
    driver = webdriver.Chrome(service=service, options=options)
    # url 접속
    web = driver.get(url)
    # 자동화
    pyautogui.FAILSAFE = False
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.6)
    pyautogui.typewrite('korea')
    pyautogui.hotkey('enter')
    pyautogui.moveRel(-200,0)

################################################################
## selenium
################################################################
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 크롬 컨트롤
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


################################################################
## request, bs4
################################################################
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup 

def getTitle(url: str) -> BeautifulSoup:
    '''
    url = 'http://~~
    return bs4 객체 없으면  None
    '''
    # urlopen 에러 처리
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
    except HTTPError as e:
        print(e)
        return None
    # 뷰티풀 숩 에러처리
    try:
        bs = BeautifulSoup(html, 'html.parser')
        title = bs
        print(title)
    except AttributeError as e:
        print(e)
        return None
    return title

if __name__ == '__main__':
    url = 'https://downsub.com/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D3iqRhbXBVRE%26t%3D123s'
    # url = 'https://polnet13.duckdns.org'
    # bs4 테스트
    # getTitle(url)
    

    
    
    


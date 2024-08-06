import os
import cv2
from easyocr.easyocr import *
from fuzzywuzzy import fuzz
from collections import Counter
import settings
# GPU 설정
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


# 텍스트 리스트
text_list = []
서울 = '강남 강동 강북 강서 관악 광진 구로 금천 노원 도봉 동대문 동작 마포 서대문 서초 성동 성북 송파 양천 영등포 용산 은평 종로 중 중랑'
부산 = '강서 금정 기장 남 동 동래 부산진 북 사상 사하 서 수영 연제 영도 중 해운대'
대구 = '남 달서 달성 동 북 서 수성 중'
인천 = '강화 계양 남 남동 미추홀 동 부평 북 서 연수 옹진 중'
울산 = '남 동 북 울주 중'
광주 = '광산 남 동 북 서'
대전 = '대덕 동 서 유성 중'
경기 = '가평 강화 고양 과천 광명 광주 구리 군포 김포 남양주 동두천 부천 성남 송탄 수원 시흥 안산 안성 안양 양주 양평 여주 연천 오산 옹진 용인 의왕 의정부 이천 파주 평택 평택시 포천 하남 화성'
강원 = '강릉 고성 동해 명주 삼척 삼척군 삼척시 속초 양구 양양 영월 원성 원성군 원주 원주군 원주시 인제 정선 철원 춘성 춘성군 춘천 춘천군 춘천시 태백 평창 홍천 화천 횡성'
충북 = '공주 공주군 괴산 단양 대천 보령 보은 영동 옥천 음성 제원 제천 제천군 증원 증평 진천 청원 청원군 청주 충주'
충남 = '계룡 공주 공주시 금산 논산 당진 대덕 대전 대천시 보령시 보령 부여 서산 서산군 서산시 서천 아산 아산군 아산시 연기 예산 온양 천안 천안군 천안시 천원 천원군 청양 태안 홍성'
전북 = '고창 군산 김제 김제시 남원 남원시 무주 부안 순창 옥구 완주 이리 익산 임실 장수 전주 정읍 정주 진안'
전남 = '강진 고흥 곡성 광양 광주 구례 금성 나주 나주시 담양 동광양 목포 무안 보성 순천 승주 승천 신안 여수 여수시 여천 여천군 여천시 영광 영암 완도 장성 장흥 진도 진도군 천원군 함평 해남 화순'
경북 = '경산 경산군 경주 경주군 경주시 고령 구미 군위 금릉 김천 문경 문경군 봉화 상주 상주군 상주시 선산 성주 안동 안동군 안동시 영덕 영양 영일 영주 영천 영천군 영천시 영풍 예천 울릉 울진군 울진 의성 청도 청송 칠곡 포항'
경남 = '거제 거창 고성 김해 김해시 남해 밀양 밀양시 마산 사천 산청 삼천포 양산 울산 울주 의령 의창 의창군 장승포 진양 진주 진해 창녕 창원 창원군 창원시 충무 통영 하동 함안 함양 합천'
제주 = '남제주 북제주 서귀포 제주'
val_name = ['서울', '부산', '대구', '인천', '울산', '광주', '대전', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
for row in val_name:
    globals()[row] = [ row+i for i in globals()[row].split(' ')]
text_list = 서울 + 부산 + 대구 + 인천 + 울산 + 광주 + 대전 + 경기 + 강원 + 충북 + 충남 + 전북 + 전남 + 경북 + 경남 + 제주
giho = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '거', '너', '더', '러', '머', '버', '서', '어', '저', '처', '커', '터', '퍼', '허']
allowlist_si = '택완아무읍연중탄속안횡풍금단홀귀수등두음마척계작기온인칠송북보하덕가태담함악종영선전군나서흥일철례산평사거실화월합옹청밀익의백김임로은추유항삼원포달주랑령초구창노과대운천승괴통상룡양논해춘충봉부울관미신시녕암목순리이도정고동오곡강광진파옥제장용남왕경증위성홍릉공래문명당예여'
allowlist_giho = '자가하다아러타너차파버바나어서라사거카더커처마터저머허퍼'
allowlist_num = '0123456789'

class OcrReader:
   
    def __init__(self, model_name = settings.model_name):
        # 경로설정 14라인
        path = settings.OCR_MODEL
        self.reader1 = Reader(['ko'],
                model_storage_directory= path,
                user_network_directory= path,
                recog_network= model_name)
        # easyocr reader 생성, easyocr 기본모델로 실행
        self.reader2 = Reader(['ko'])
        self.text_list = text_list
        self.giho = giho

    def read(self, img):
        '''
        input: 이미지
        output: result2_si, result2_giho, result2_num
        '''
        # 이미지 전처리
        y = img.shape[0]
        x = img.shape[1]
        img_si = img.copy()[:int(y*0.33),:]
        img_giho = img.copy()[:,:int(x*0.26)]
        img_num = img.copy()[int(y*0.31):,int(x*0.19):]
 
        result2_si =  self.reader1.readtext(img_si, allowlist=allowlist_si)
        result2_giho =  self.reader1.readtext(img_giho, allowlist=allowlist_giho)
        result2_num =  self.reader1.readtext(img_num, allowlist=allowlist_num)
        # 시
        if len(result2_si) == 0:
            print('시: 노 디텍션')
            result2_si = None
        else:
            for (bbox, string, confidence) in result2_si:
                print(f"시: {string}({confidence}) {bbox}")
                result2_si = self.matching(string, self.text_list)
        # 기호
        if len(result2_giho) == 0:
            print('기호: 노 디텍션')
            result2_giho = None
        else:
            for (bbox, string, confidence) in result2_giho:
                print(f"기호: {string}({confidence}) {bbox}")
                result2_giho = self.matching(string, self.giho)
        # 숫자      
        try:
            print('넘: ', result2_num[0][1][:4], result2_num[0])
            result2_num = int(result2_num[0][1][:4])
        except:
            print(result2_num)
            result2_num = None
        return result2_si, result2_giho, result2_num


    # 유사도 매칭
    def matching(self, text, text_list):
        '''
        input: text(비교할 텍스트), text_list(비교 기준 리스트)
        '''
        # 비교 기준 리스트
        # 최고 일치 점수 및 일치 단어 초기화
        max_score = 0
        matched_string = None
        # 각 단어와의 유사도 계산 및 최고 일치 찾기
        for word in text_list:
            score = fuzz.ratio(text, word)
            if score > max_score:
                max_score = score
                matched_string = word
        # 결과 출력
        if matched_string:
            print(f"{text} => {matched_string} (유사도: {max_score}% 매칭)")
            text = matched_string
        else:
            print(f"{text} : 일치하는 단어가 없습니다.")
            text = None
        return text

    def jacad_match(self, text, text_list):
        max_score = 0  # 최대 점수 초기화
        matched_string = None
        def jaccard_similarity(counter1, counter2):
            # Counter 객체의 키를 사용하여 set 생성
            set1 = set(counter1.keys())
            set2 = set(counter2.keys())
            
            # 교집합과 합집합 계산
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            
            # 자카드 유사도 계산
            score = len(intersection) / len(union)
            return score

        for word in text_list:
            score = jaccard_similarity(Counter(text), Counter(word))
            if score > max_score:
                max_score = score
                matched_string = word
        # 결과
        if matched_string:
            print(f"{text} => {matched_string} (유사도: {max_score}% 자카드 매칭)")
        else:
            print(f"{text} : 일치하는 단어가 없습니다.")


 
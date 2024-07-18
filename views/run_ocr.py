import os
import cv2
from easyocr.easyocr import *
from fuzzywuzzy import fuzz
from collections import Counter



# 커스텀 설정
model_name = 'best_accuracy'

# GPU 설정
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
custom_model = os.path.join(base, 'rsc', 'user_network')

class OcrReader:

    def __init__(self, model_name='best_accuracy'):
        path = custom_model
        self.reader1 = Reader(['ko'],
                model_storage_directory= path,
                user_network_directory= path,
                recog_network= model_name)
        # easyocr reader 생성, easyocr 기본모델로 실행
        self.reader2 = Reader(['ko'])
        self.text_list = []
        self.si = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
        self.gu = ['종로', '중', '용산', '성동', '광진', '동대문', '중랑', '성북', '강북', '도봉', '노원', '은평', '서대문', '마포', '양천', '강서', '구로', '금천', '영등포', '동작', '관악', '서초', '강남', '송파', '강동', '중', '서', '동', '영도', '부산진', '동래', '남', '북', '해운대', '사하', '금정', '강서', '연제', '수영', '사상', '기장', '중', '동', '서', '남', '북', '수성', '달서', '달성', '군위', '중', '동', '미추홀', '연수', '남동', '부평', '계양', '서', '강화', '옹진', '동', '서', '남', '북', '광산', '동', '중', '서', '유성', '대덕', '수원', '수원', '수원', '수원', '성남', '성남', '성남', '의정부', '안양', '안양', '부천', '광명', '평택', '동두천', '안산', '안산', '고양', '고양', '고양', '과천', '구리', '남양주', '오산', '시흥', '군포', '의왕', '하남', '용인', '용인', '용인', '파주', '이천', '안성', '김포', '화성', '광주', '양주', '포천', '여주', '연천', '가평', '양평', '춘천', '원주', '강릉', '동해', '태백', '속초', '삼척', '홍천', '횡성', '영월', '평창', '정선', '철원', '화천', '양구', '인제', '고성', '양양', '청주', '청주', '청주', '청주', '충주', '제천', '보은', '옥천', '영동', '증평', '진천', '괴산', '음성', '단양', '천안', '천안', '공주', '보령', '아산', '서산', '논산', '계룡', '당진', '금산', '부여', '서천', '청양', '홍성', '예산', '태안', '전주', '전주', '군산', '익산', '정읍', '남원', '김제', '완주', '진안', '무주', '장수', '임실', '순창', '고창', '부안', '목포', '여수', '순천', '나주', '광양', '담양', '곡성', '구례', '고흥', '보성', '화순', '장흥', '강진', '해남', '영암', '무안', '함평', '영광', '장성', '완도', '진도', '신안', '포항', '포항', '경주', '김천', '안동', '구미', '영주', '영천', '상주', '문경', '경산', '군위', '의성', '청송', '영양', '영덕', '청도', '고령', '성주', '칠곡', '예천', '봉화', '울진', '울릉', '창원', '창원', '창원', '창원', '창원', '진주', '통영', '사천', '김해', '밀양', '거제', '양산', '의령', '함안', '창녕', '고성', '남해', '하동', '산청', '함양', '거창', '합천', '제주', '서귀포']
        self.giho = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '거', '너', '더', '러', '머', '버', '서', '어', '저', '처', '커', '터', '퍼', '허']
        for s in set(self.si):
            for g in set(self.gu):
                self.text_list.append(s+g)
        
        self.text_list = self.text_list + self.giho
        print(self.text_list)

    def read(self, img):
        result1 =  self.reader1.readtext(img)
        result2 =  self.reader2.readtext(img)
        # 결과 출력1
        if len(result1) == 0:
            print('노 디텍션 result1')
        else:
            for (bbox, string, confidence) in result1:
                print('커스텀')
                print(f"{string}({confidence}) {bbox}")
                # # bbox 그려진 이미지 만들기
                # img1 = cv2.rectangle(img1, (int(bbox[0][0]), int(bbox[0][1])), (int(bbox[2][0]), int(bbox[2][1])), (0, 255, 0), 2)
                # img1 = cv2.putText(img1, string, (int(bbox[0][0]), int(bbox[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # 결과 출력2
        if len(result2) == 0:
            print('노 디텍션 result2')
        else:
            for (bbox, string, confidence) in result2:
                print('노말')
                print(f"{string}({confidence}) {bbox}")
                self.matching(string, self.text_list)
                self.jacad_match(string, self.text_list)

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
        else:
            print(f"{text} : 일치하는 단어가 없습니다.")

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


 
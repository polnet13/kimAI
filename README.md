# kimAI
- CCTV 영상 분석 및 이륜차 번호판 탐지 
- 모델은 별도 배포 함

# 패키지
conda install pytorch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 pytorch-cuda=12.1 -c pytorch -c nvidia
pip install PySide6==6.4.3
pip install ultralytics==8.2.pip install opencv-python==4.9.027
pip3 install lapx==0.5.2 
pip install opencv-python==4.10.0
pip3 install numpy==1.26.4
pip3 install easyocr
pip install fuzzywuzzy
pip install python-Levenshtein  

# 프로젝트 구조
```
root
├─ apps
│  └─ model_setting (장고앱에서 마이그레이션 지원)
│      └─ models.py
├─ control (필요한 함수 모음)
├─ module (★★ 커스텀 모델 클래스 ★★)
├─ rsc  
│  ├─ models (디텍션 모델)
│  ├─ user_network (OCR 커스텀 모델)
│  └─ ui(ui 파일)
├─ saved_model (OCR 커스텀 모델)
├─ views
│  ├─ mainWindowManager.py (pyside6 슬롯함수 작성)
│  └─ orm.py (장고 orm 컨트롤 코드)
├─ main.py (스타팅 포인트)
├─ settings.py (전역변수 등 세팅)
├─ manage.py (장고 명령어 관련 코드)
├─ db.sqlite3 (장고에서 생성한 DB)
└─ README.md 
```

# 커스텀 모듈 만드는 방법
- module.generic 모듈의 CustomBaseClass 상속받아 enrolled 디렉터리에 코드 작성
- module.readme.md 참고해서 작성

# ui파일 => 파이썬 파일로 변환
untitled.ui 파일 위치에서 명령어 실행
pyside6-uic untitled.ui -o untitled_ui.py

# 0. 모델 작성
Path: root/apps/model_setting/models.py

# 1. 모델 마이그레이션 준비 
python manage.py makemigrations model_setting

# 2. 모델 마이그레이트
python manage.py migrate

#### Using Pyinstaller
python manage.py deploy

## Todo
- 해상도가 큰 영상 느려지는 것 리사이즈로 해결(640*360)
- 탭 적절하게 자동변환되도록
- 반응형 옵션창 
- 안내판 지우고 모두 테이블로 대체(반응형으로 구현하기 위함)

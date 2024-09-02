# kimAI
- CCTV 영상 분석 및 이륜차 번호판 탐지 
- 모델은 별도 배포 함

# 가상환경
conda create -n pol_ai python=3.11
conda install pytorch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 pytorch-cuda=12.1 -c pytorch -c nvidia

# 패키지
pip install PySide6==6.4.3
pip install ultralytics==8.2
pip3 install lapx==0.5.2 
pip install fuzzywuzzy
<!-- pip3 install easyocr -->
pip install opencv-python==4.10.0.82
pip install python-Levenshtein  
pip3 install numpy==1.26.4

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
<!-- untitled.ui 파일 위치에서 명령어 실행 -->
pyside6-uic untitled.ui -o untitled_ui.py  
pyside6-uic mosaic.ui -o mosaic_ui.py  
pyside6-uic bike.ui -o bike_ui.py  
pyside6-uic cctv.ui -o cctv_ui.py  


#### Using Pyinstaller
python manage.py deploy

 

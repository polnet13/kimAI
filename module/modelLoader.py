from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QLabel, QGridLayout, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from module.sharedData import DT



class ModelClass:
    '''
    슬라이더와 모델의 상호작용을 위한 클래스
    '''

    def __init__(self):

        self.layout = None
        self.detector = None
        # UI 구성 요소 생성
        self.layout = QVBoxLayout()
        self.combo_box = QComboBox()
        sub_layout = QHBoxLayout()
        self.slider_container = QVBoxLayout()
        self.label1_container = QVBoxLayout()  # 슬라이더 값을 출력할 레이블을 위한 레이아웃
        self.label2_container = QVBoxLayout()  # 슬라이더 값을 출력할 레이블을 위한 레이아웃
        self.btn_container = QGridLayout()
        self.combo_box.addItems(DT.sliderDict.keys())
        self.combo_box.currentIndexChanged.connect(self.change_sliders)
        self.progress_bar = QVBoxLayout()
        # 레이아웃 설정
        sub_layout.addLayout(self.label2_container)
        sub_layout.addLayout(self.label1_container)
        sub_layout.addLayout(self.slider_container)
        self.layout.addWidget(self.combo_box)
        self.layout.addSpacing(10)  # 일정 간격 추가
        self.layout.addLayout(sub_layout)
        self.layout.addSpacing(20)  # 일정 간격 추가
        self.layout.addLayout(self.btn_container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addSpacing(20)  # 일정 간격 추가
        self.layout.addLayout(self.progress_bar)
        # 슬라이더, 버튼 생성
        self.change_sliders(0)
  

    def change_sliders(self, index):
        '''
        드롭다운 메뉴(콤보박스)의 선택에 따라 슬라이더를 변경하고,
        디텍터를 활성화 하는 함수
        '''
        # 기존 슬라이더, 레이블, 버튼 삭제
        for i in reversed(range(self.slider_container.count())):
            self.slider_container.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.label1_container.count())):
            self.label1_container.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.label2_container.count())):
            self.label2_container.itemAt(i).widget().deleteLater()
        # 기존 버튼 제거
        for i in reversed(range(self.btn_container.count())):
            self.btn_container.itemAt(i).widget().deleteLater()
        # 선택된 메뉴에 대한 슬라이더 생성
        selected_menu_text = self.combo_box.itemText(index)
        DT.setSelectedMode(selected_menu_text)
        # 디텍터 초기화
        DT.reset()
        # 슬라이더 생성
        slider_values_dict = DT.sliderDict[selected_menu_text]
        for arg, value in slider_values_dict.items():
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(99)
            slider.setValue(value)
            label1 = QLabel(str(value))  # 슬라이더 값을 표시할 QLabel 생성
            label2 = QLabel(arg)  # 슬라이더 값을 표시할 QLabel 생성
            slider.valueChanged.connect(lambda value, slider=slider, label1=label1, arg=arg: self.update_label(value, selected_menu_text, label1, arg))  # 슬라이더 값 변경 시 호출될 슬롯 연결
            self.slider_container.addWidget(slider)
            self.label1_container.addWidget(label1)
            self.label2_container.addWidget(label2)
        # 버튼 생성
        for i in range(len(DT.detector.btn_names)):
            button = QPushButton(DT.detector.btn_names[i])
            self.btn_container.addWidget(button, i // 3, i % 3)
            # 버튼 이벤트 연결
            button.clicked.connect(DT.detector.btns[i])
        # 모델 생성은 변수들 초기화 후 마지막으로 진행
        DT.setDetector(selected_menu_text)

    def update_label(self, value, selected_menu_text, label1, arg):
        label1.setText(str(value))
        DT.sliderDict[selected_menu_text][arg] = value



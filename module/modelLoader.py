from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QLabel, QWidget, QScrollArea
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from functools import partial
from module.generic import ArgsDict
from module import enrolled
from control import tools



class ModelClass:
    '''
    슬라이더와 모델의 상호작용을 위한 클래스
    '''

    def __init__(self):

        self.layout = None
        self.detector = None
        self.make_optionbox()
        # 모델 사전 등록


    def update_label(self, value, selected_menu_text, label1, arg):
        label1.setText(str(value))
        ArgsDict.arg_dict[selected_menu_text][arg] = value

    def make_optionbox(self):
        # UI 구성 요소 생성
        self.combo_box = QComboBox()
        self.combo_box.addItems(ArgsDict.arg_dict.keys())
        self.combo_box.currentIndexChanged.connect(self.change_sliders)

        self.slider_container = QVBoxLayout()
        self.label1_container = QVBoxLayout()  # 슬라이더 값을 출력할 레이블을 위한 레이아웃
        self.label2_container = QVBoxLayout()  # 슬라이더 값을 출력할 레이블을 위한 레이아웃

        # 레이아웃 설정
        self.layout = QVBoxLayout()
        sub_layout = QHBoxLayout()
        sub_layout.addLayout(self.label2_container)
        sub_layout.addLayout(self.slider_container)
        sub_layout.addLayout(self.label1_container)
        self.layout.addWidget(self.combo_box)
        self.layout.addLayout(sub_layout)

        # 초기 슬라이더 설정 (첫 번째 메뉴 기준)
        self.change_sliders(0)
        

    def change_sliders(self, index):
        '''
        드롭다운 메뉴(콤보박스)의 선택에 따라 슬라이더를 변경하고,
        디텍터를 활성화 하는 함수
        '''
        self.detector = None  # 기존 디텍터 메모리 해제 코드로 수정 필요
        # 기존 슬라이더 및 레이블 삭제
        for i in reversed(range(self.slider_container.count())):
            self.slider_container.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.label1_container.count())):
            self.label1_container.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.label2_container.count())):
            self.label2_container.itemAt(i).widget().deleteLater()

        # 선택된 메뉴에 대한 슬라이더 생성
        selected_menu_text = self.combo_box.itemText(index)
        ArgsDict.selected_mode = selected_menu_text

        slider_values_dict = ArgsDict.arg_dict[selected_menu_text]
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
        
        # 모델 생성
        ArgsDict.setDetector(selected_menu_text)




 



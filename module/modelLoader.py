from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QLabel, QGridLayout, QPushButton, QTableView, QHeaderView
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from module.sharedData import DT
from PySide6 import QtGui
from control import tools
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject


class ModelClass(QObject):
    '''
    슬라이더와 모델의 상호작용을 위한 클래스
    '''
    # 시그널
    reset = Signal()



    def __init__(self):
        super().__init__()
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
        # 테이블 생성
        self.tableview_df = QTableView()
        header = self.tableview_df.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.tableview_df)
        # 레이아웃 설정
        self.layout.addSpacing(5)  # 일정 간격 추가
        self.layout.addLayout(sub_layout)
        self.layout.addSpacing(5)  # 일정 간격 추가
        self.layout.addLayout(self.btn_container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addSpacing(5)  # 일정 간격 추가
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
        select_mode = self.combo_box.itemText(index)
        DT.setSelectedMode(select_mode)
        self.detector = DT.detector()
        # 슬라이더 생성
        slider_values_dict = DT.sliderDict[select_mode]
        for arg, value in slider_values_dict.items():
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(99)
            slider.setValue(value)
            label1 = QLabel(str(value))  # 슬라이더 값을 표시할 QLabel 생성
            label2 = QLabel(arg)  # 버튼명을 표시할 QLabel 생성
            slider.valueChanged.connect(lambda value, label1=label1, label2=label2, arg=arg: self.update_label(value, select_mode, label1, label2, arg))  # 슬라이더 값 변경 시 호출될 슬롯 연결
            self.slider_container.addWidget(slider)
            self.label1_container.addWidget(label1)
            self.label2_container.addWidget(label2)
        # 버튼 생성
        for i in range(len(DT.detector.btn_names)):
            button = QPushButton(DT.detector.btn_names[i])
            self.btn_container.addWidget(button, i // 3, i % 3)
            # 버튼 이벤트 연결
            button.clicked.connect(self.detector.btns[i])
        # 모델 생성은 변수들 초기화 후 마지막으로 진행
        # 시그널 연결
        self.detector.signal_start.connect(self.receive_start)
        self.detector.signal_end.connect(self.receive_end)
        self.detector.signal_df_to_tableview_df.connect(self.df_to_tableview_df)
        self.reset.emit()

    def update_label(self, value, selected_menu_text, label1, label2, arg):
        label1.setText(str(value))  # 슬라이더 값
        label2.setText(str(value))  # 버튼명
        DT.sliderDict[selected_menu_text][arg] = value

    def receive_start(self, value):
        # 시작 버튼명을 f'시작({value})'로 변경
        self.btn_container.itemAt(0).widget().setText(f'시작({value})')

    def receive_end(self, value):
        # 종료 버튼명을 f'시작({value})'로 변경
        if value+1 < DT.start_point:
            return
        self.btn_container.itemAt(1).widget().setText(f'끝({value})')

    
    #########################
    # 테이블뷰 선택된 행 삭제 #
    #########################
    def delete_listview_row(self):
        index = self.tableview_df.currentIndex().row()
        # 디텍터 마다 테이블 삭제시 작동하는 함수를 다르게 하기 위해서 detector에 위임함
        DT.df.drop(index).reset_index(drop=True)
        # 테이블뷰 다시 출력
        self.df_to_tableview_df()
        self.tableview_df.update()
        
 
    # df => 리스트뷰
    def df_to_tableview_df(self):
        '''detector.df를 테이블에 출력'''
        # 모델 초기화를 데터 추가 전에 수행
        self.qmodel = QtGui.QStandardItemModel()  # 초기 행과 열의 수를 설정하지 않음
        columns = DT.df_plot.columns
        self.qmodel.setColumnCount(len(columns))
        self.qmodel.setHorizontalHeaderLabels(columns)
        for row in range(len(DT.df_plot)):
            value_objs = [QtGui.QStandardItem(str(value)) for value in DT.df_plot.iloc[row]]
            self.qmodel.appendRow(value_objs)
        self.tableview_df.setModel(self.qmodel)
        print('df_to_tableview_df 실행')
        print(DT.df_plot)

 
        




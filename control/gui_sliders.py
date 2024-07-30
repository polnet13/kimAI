from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QLabel, QWidget, QScrollArea
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from functools import partial
from module.generic import ArgsDict


class SliderClass:
    '''
    make_slider 슬라이더 객체를 반환 
    set_slider_value  슬라이더 값을 설정 
    get_slider_value  슬라이더 값을 가져옴
    get_slider_by_name  슬라이더 이름으로 슬라이더 객체를 찾음
    '''

    def __init__(self, _dict) -> None:
        '''
        args: dict
        key: str(gui용 name)
        val: [str(ObjectName), dict(변수 객체), int(최소값), int(최대값), int(값)] 
        '''
        # slider
        self.option_box = None
        ArgsDict.clear()
        ArgsDict.makeValues(_dict)
        self.make_optionbox(_dict)


    def make_optionbox(self, _dict):
        self.option_box = QVBoxLayout()
        for key, val in _dict.items():
            row_layout = QHBoxLayout()
            label = QLabel(key)
            row_layout.addWidget(label)
            slider = QSlider()
            slider.setOrientation(Qt.Horizontal)
            slider.setValue(val[0])
            slider.setMinimum(val[1])
            slider.setMaximum(val[2])
            # 슬라이더 값 표시 라벨 생성
            value_label = QLabel(str(val[2]))
            row_layout.addWidget(value_label)
            slider.valueChanged.connect(partial(self.slider_value_changed, objname=key, slider=slider, value_label=value_label))
            row_layout.addWidget(slider)
            self.option_box.addLayout(row_layout)

    # 딕셔너리 새로 반영
    def update(self, _dict):
        self.option_box = None
        ArgsDict.clear()
        ArgsDict.makeValues(_dict)
        self.make_optionbox(_dict)
    

    def slider_value_changed(self, value, objname, slider, value_label):
        value_label.setText(str(value))
        ArgsDict.setValue(objname, value)



    def make_slider(self, name, min, max, default):
        SliderOBJ = QSlider()
        SliderOBJ.setObjectName(f"{name}")
        SliderOBJ.setMinimum(min)
        SliderOBJ.setMaximum(max)
        SliderOBJ.setSliderPosition(default)
        self.slider.append(SliderOBJ)
        return SliderOBJ  

    def add_slider_to_frame(self, frame, name, min, max, value):
        slider = self.make_slider(name, min, max, value)
        frame.layout().addWidget(slider)  # 프레임의 레이아웃에 슬라이더 추가

    def set_slider_value(self, name, value):
        slider = self.get_slider_by_name(name)
        if slider:
            slider.setValue(value)

    def get_slider_value(self, name):
        slider = self.get_slider_by_name(name)
        if slider:
            return slider.value()
        return None


    def make_roi_mosaic(self, x1, y1, x2, y2):
        self.roi_mosaic.append([x1, y1, x2, y2])
        return self.roi_mosaic
    
 


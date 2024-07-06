# pt 파일을 onnx 파일로 변환하는 코드
from ultralytics import YOLO

file_path = "/home/prudent13/YOLOv8/models/motobike_e300_b8_s640.pt"
model = YOLO(file_path)
print(model.model.nc)
names = [v for k, v in model.model.names.items()]
model.export(format = "onnx")
print(f'{names}')
print(file_path)

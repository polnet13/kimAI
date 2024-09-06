


import cv2



file = r'C:\Users\prude\OneDrive\탕 화면\외곽-5_CLIP-20240831T200543-20240901T143043_CH01\외곽-5_CLIP-20240831T200543-20240901T143043_CH01.mp4'



cap = cv2.VideoCapture(file)
ret, frame = cap.read()
print(type(ret), ret, type(frame))

ret, frame = cap.read()
print(type(ret), ret, type(frame))


ret, frame = cap.read()
print(type(ret), ret, type(frame))


ret, frame = cap.read()
print(type(ret), ret, type(frame))


ret, frame = cap.read()
print(type(ret), ret, type(frame))



 
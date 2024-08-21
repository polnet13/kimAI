import os

main ='pyside6-uic untitled.ui -o untitled_ui.py'
mosaic = 'pyside6-uic mosaic.ui -o mosaic_ui.py'  
bike = 'pyside6-uic bike.ui -o bike_ui.py'
cctv = 'pyside6-uic cctv.ui -o cctv_ui.py'

texts = [main, mosaic, bike, cctv]

import os 

parent = os.path.abspath(os.path.dirname(__file__))
ui_path = os.path.join(parent, 'rsc', 'ui')
os.chdir(ui_path)

for row in texts:
    print(row)
    os.system(row)
 
# 스타팅 포인트
import sys 
import multiprocessing
from PySide6.QtWidgets import *
from module.mainWindowManager import mainWindow


class csswindow(mainWindow):

    def __init__(self):
        super().__init__()
    

def main():
    app = QApplication(sys.argv) 
    window = csswindow()
    window.show()
    sys.exit(app.exec())
 

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()  


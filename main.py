# 스타팅 포인트
import sys, os
import multiprocessing
from PySide6.QtWidgets import *
from views.mainWindowManager import mainWindow
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from views.sharedData import DT


class csswindow(mainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(QCoreApplication.translate(
            "MainWindow", 
            "K-Pol AI", 
            None
            ))
        icon_path = os.path.join(DT.BASE_DIR, 'rsc', 'ico', 'main.jpg')
        print(icon_path)
        self.setWindowIcon(QIcon(icon_path))
    


def main():
    app = QApplication(sys.argv) 
    # apply_stylesheet(app, theme=theme[4])
    window = csswindow()
    window.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()  


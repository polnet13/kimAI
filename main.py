# 스타팅 포인트
import sys 
import multiprocessing
from PySide6.QtWidgets import *
from views.mainWindowManager import mainWindow
from qt_material import apply_stylesheet
from qt_material import list_themes

# theme = list_themes()


class csswindow(mainWindow):

    def __init__(self):
        super().__init__()
    

def main():
    app = QApplication(sys.argv) 
    # apply_stylesheet(app, theme=theme[4])
    window = csswindow()
    window.show()
    sys.exit(app.exec())
 

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()  


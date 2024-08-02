# 스타팅 포인트
import sys 
import os
import multiprocessing
from PySide6.QtWidgets import *
from views.mainWindowManager import mainWindow
from PySide6.QtCore import Qt

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception as e:
    print(e)


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


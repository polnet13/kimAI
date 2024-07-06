# 스타팅 포인트
import os
import settings
from PySide6.QtCore import Qt, QFile, QIODevice
import multiprocessing
import torch

# CPU 스레드 수를 4로 설정
torch.set_num_threads(4)


try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception as e:
    print(e)


from PySide6.QtWidgets import *
from views.mainWindowManager import mainWindow
import sys 


class csswindow(mainWindow):
    def __init__(self):
        super().__init__()

    
def main():
    app = QApplication(sys.argv) 
    # theme = theme_kind[0]  # 테마 종류 선택
    # if theme is not None:
    #     apply_stylesheet(app, theme=theme, invert_secondary=False, extra=extra)
    window = csswindow()
    window.show()
    sys.exit(app.exec())


extra = {'density_scale': '-1'}
 
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()  


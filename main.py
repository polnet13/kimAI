# 스타팅 포인트
import os
import settings
from PySide6.QtCore import Qt, QFile, QIODevice
import multiprocessing


try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception as e:
    print(e)


from PySide6.QtWidgets import *
from views.mainWindowManager import mainWindow
import sys 
# from PySide6.QtCore import QFile
# from qt_material import apply_stylesheet 


class csswindow(mainWindow):
    def __init__(self):
        super().__init__()
        # self.apply_css()
        # yolo 모델 생성

    # # CSS 파일 적용'
    # def apply_css(self):
    #     base = os.path.dirname(__file__)
    #     css_path = os.path.join(base, 'rsc', 'ui','theme.css')
    #     file = QFile(css_path)
    #     if file.open(QIODevice.ReadOnly | QIODevice.Text):
    #         style_sheet = file.readAll().data().decode()
    #         self.setStyleSheet(style_sheet)
    #         file.close()
    
def main():
    app = QApplication(sys.argv) 
    # theme = theme_kind[0]  # 테마 종류 선택
    # if theme is not None:
    #     apply_stylesheet(app, theme=theme, invert_secondary=False, extra=extra)
    window = csswindow()
    window.show()
    sys.exit(app.exec())

# 테마 종류
# theme_kind = [
#     None,
#     'dark_lightgreen.xml',
#     'light_cyan_500.xml',
#  ]

extra = {'density_scale': '-1'}
 
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()  


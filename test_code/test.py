import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QPainter, QColor, QStyleOptionButton

class HoverButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOptionButton()
        option.initFrom(self)

        # 기본 버튼 그리기
        self.style().drawControl(QStyle.CE_PushButton, option, painter, self)

        # 마우스 호버 시 빨간색 밑줄 그리기
        if option.state & QStyle.State_MouseOver:
            rect = option.rect
            painter.setPen(QColor(255, 0, 0))  # 빨간색
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    button = HoverButton("Hover me")
    button.show()
    sys.exit(app.exec_())
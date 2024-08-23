# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cctv.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_CCTV(object):
    def setupUi(self, CCTV):
        if not CCTV.objectName():
            CCTV.setObjectName(u"CCTV")
        CCTV.resize(370, 570)
        self.verticalLayoutWidget = QWidget(CCTV)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 371, 571))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_multi_open = QPushButton(self.verticalLayoutWidget)
        self.btn_multi_open.setObjectName(u"btn_multi_open")

        self.horizontalLayout.addWidget(self.btn_multi_open)

        self.btn_multi_reset = QPushButton(self.verticalLayoutWidget)
        self.btn_multi_reset.setObjectName(u"btn_multi_reset")

        self.horizontalLayout.addWidget(self.btn_multi_reset)

        self.btn_multi_complete_open = QPushButton(self.verticalLayoutWidget)
        self.btn_multi_complete_open.setObjectName(u"btn_multi_complete_open")

        self.horizontalLayout.addWidget(self.btn_multi_complete_open)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.label_thr = QLabel(self.verticalLayoutWidget)
        self.label_thr.setObjectName(u"label_thr")

        self.horizontalLayout_4.addWidget(self.label_thr)

        self.slider_move_thr = QSlider(self.verticalLayoutWidget)
        self.slider_move_thr.setObjectName(u"slider_move_thr")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.slider_move_thr.setFont(font)
        self.slider_move_thr.setMinimum(1)
        self.slider_move_thr.setValue(50)
        self.slider_move_thr.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.slider_move_thr)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.textBrowser_multi = QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser_multi.setObjectName(u"textBrowser_multi")

        self.verticalLayout.addWidget(self.textBrowser_multi)

        self.vLayout_dongzip_statusbar = QVBoxLayout()
        self.vLayout_dongzip_statusbar.setObjectName(u"vLayout_dongzip_statusbar")

        self.verticalLayout.addLayout(self.vLayout_dongzip_statusbar)


        self.retranslateUi(CCTV)

        QMetaObject.connectSlotsByName(CCTV)
    # setupUi

    def retranslateUi(self, CCTV):
        CCTV.setWindowTitle(QCoreApplication.translate("CCTV", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("CCTV", u"CCTV \uad00\uc2ec\uc601\uc5ed \ucd94\ucd9c\ud558\uae30(\ub3d9\uc601\uc0c1 \uc5ec\ub7ec\uac1c \uc120\ud0dd)", None))
        self.btn_multi_open.setText(QCoreApplication.translate("CCTV", u"\ud30c\uc77c \uc5f4\uae30", None))
        self.btn_multi_reset.setText(QCoreApplication.translate("CCTV", u"reset", None))
        self.btn_multi_complete_open.setText(QCoreApplication.translate("CCTV", u"\uc644\ub8cc \uc5f4\uae30", None))
        self.label.setText(QCoreApplication.translate("CCTV", u"\ubbfc\uac10\ub3c4 ", None))
        self.label_thr.setText(QCoreApplication.translate("CCTV", u"50", None))
    # retranslateUi


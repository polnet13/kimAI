# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mosaic.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSlider,
    QTableView, QVBoxLayout, QWidget)
from views.sharedData import DT

class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_mosaic_start.clicked.connect(self.btn_mosaic_start_clicked)
        self.btn_mosaic_start.clicked.connect(self.btn1)

    def btn1(self):
        print('btn1')


    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(343, 565)
        self.verticalLayoutWidget_12 = QWidget(Form)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 341, 561))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_12)
        self.label.setObjectName(u"label")

        self.verticalLayout_7.addWidget(self.label)

        self.progressBar_mosaic = QProgressBar(self.verticalLayoutWidget_12)
        self.progressBar_mosaic.setObjectName(u"progressBar_mosaic")
        self.progressBar_mosaic.setValue(0)

        self.verticalLayout_7.addWidget(self.progressBar_mosaic)

        self.tableView_mosaic_ID = QTableView(self.verticalLayoutWidget_12)
        self.tableView_mosaic_ID.setObjectName(u"tableView_mosaic_ID")
        self.tableView_mosaic_ID.setStyleSheet(u"background-color: rgb(40, 44, 52);\n"
"selection-background-color: rgb(255, 35, 86);\n"
"alternate-background-color: rgb(157, 255, 29);\n"
"")
        self.tableView_mosaic_ID.horizontalHeader().setVisible(False)

        self.verticalLayout_7.addWidget(self.tableView_mosaic_ID)

        self.tableView_mosaic_frame = QTableView(self.verticalLayoutWidget_12)
        self.tableView_mosaic_frame.setObjectName(u"tableView_mosaic_frame")
        self.tableView_mosaic_frame.setStyleSheet(u"background-color: rgb(40, 44, 52);\n"
"border: 1px solid #CCCCCC;\n"
"gridline-color: #CCCCCC;\n"
"selection-background-color: #E1F5FE;\n"
"selection-color: #0366d6;\n"
"font-family: \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n"
"\n"
"color:\n"
"")

        self.verticalLayout_7.addWidget(self.tableView_mosaic_frame)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_mosaic_start = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_start.setObjectName(u"btn_mosaic_start")

        self.horizontalLayout_5.addWidget(self.btn_mosaic_start)

        self.btn_mosaic_end = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_end.setObjectName(u"btn_mosaic_end")

        self.horizontalLayout_5.addWidget(self.btn_mosaic_end)

        self.btn_mosaic_analyze = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_analyze.setObjectName(u"btn_mosaic_analyze")

        self.horizontalLayout_5.addWidget(self.btn_mosaic_analyze)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_mosaic_add_frame = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_add_frame.setObjectName(u"btn_mosaic_add_frame")

        self.horizontalLayout_6.addWidget(self.btn_mosaic_add_frame)

        self.btn_mosaic_add_frams = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_add_frams.setObjectName(u"btn_mosaic_add_frams")

        self.horizontalLayout_6.addWidget(self.btn_mosaic_add_frams)

        self.btn_mosaic_video_out = QPushButton(self.verticalLayoutWidget_12)
        self.btn_mosaic_video_out.setObjectName(u"btn_mosaic_video_out")

        self.horizontalLayout_6.addWidget(self.btn_mosaic_video_out)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)


        self.verticalLayout_7.addLayout(self.verticalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_11 = QLabel(self.verticalLayoutWidget_12)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_7.addWidget(self.label_11)

        self.slider_bike_mosaic = QSlider(self.verticalLayoutWidget_12)
        self.slider_bike_mosaic.setObjectName(u"slider_bike_mosaic")
        self.slider_bike_mosaic.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.slider_bike_mosaic)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ubaa8\uc790\uc774\ud06c", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_start.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 4", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_start.setText(QCoreApplication.translate("Form", u"\uc2dc\uc791 \uc810", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_end.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 5", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_end.setText(QCoreApplication.translate("Form", u"\ub05d \uc810", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_analyze.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 6", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_analyze.setText(QCoreApplication.translate("Form", u"\ubd84\uc11d", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_add_frame.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 1", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_add_frame.setText(QCoreApplication.translate("Form", u"\ud504\ub808\uc784 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_add_frams.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 2", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_add_frams.setText(QCoreApplication.translate("Form", u"\uc804\uccb4 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_video_out.setToolTip(QCoreApplication.translate("Form", u"\ub2e8\ucd95\ud0a4: 3", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_video_out.setText(QCoreApplication.translate("Form", u"\uc0dd\uc131", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\ubaa8\uc790\uc774\ud06c \uc815\ub3c4", None))
    # retranslateUi

    def btn_mosaic_start_clicked(self):
        n = DT.cap_num
        print("btn_mosaic_start_clicked", n)


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QStatusBar, QTabWidget, QTableView,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1123, 650)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.playSlider = QSlider(self.centralwidget)
        self.playSlider.setObjectName(u"playSlider")
        self.playSlider.setEnabled(True)
        self.playSlider.setGeometry(QRect(40, 540, 721, 20))
        self.playSlider.setOrientation(Qt.Horizontal)
        self.btn_region_reset = QPushButton(self.centralwidget)
        self.btn_region_reset.setObjectName(u"btn_region_reset")
        self.btn_region_reset.setGeometry(QRect(100, 580, 111, 31))
        self.btn_fileopen = QPushButton(self.centralwidget)
        self.btn_fileopen.setObjectName(u"btn_fileopen")
        self.btn_fileopen.setGeometry(QRect(680, 580, 81, 31))
        self.btn_play = QToolButton(self.centralwidget)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setGeometry(QRect(40, 580, 41, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 40, 720, 480))
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QFrame.WinPanel)
        self.playTimer = QLabel(self.centralwidget)
        self.playTimer.setObjectName(u"playTimer")
        self.playTimer.setGeometry(QRect(710, 560, 64, 15))
        self.btn_init_detection = QPushButton(self.centralwidget)
        self.btn_init_detection.setObjectName(u"btn_init_detection")
        self.btn_init_detection.setGeometry(QRect(230, 580, 131, 31))
        self.btn_page_print = QPushButton(self.centralwidget)
        self.btn_page_print.setObjectName(u"btn_page_print")
        self.btn_page_print.setGeometry(QRect(550, 580, 111, 31))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(780, 40, 331, 491))
        self.tab_control = QWidget()
        self.tab_control.setObjectName(u"tab_control")
        self.check_realsize = QCheckBox(self.tab_control)
        self.check_realsize.setObjectName(u"check_realsize")
        self.check_realsize.setEnabled(True)
        self.check_realsize.setGeometry(QRect(10, 410, 301, 19))
        self.check_realsize.setChecked(True)
        self.checkbox_yolo = QCheckBox(self.tab_control)
        self.checkbox_yolo.setObjectName(u"checkbox_yolo")
        self.checkbox_yolo.setGeometry(QRect(10, 440, 211, 19))
        self.checkbox_yolo.setChecked(False)
        self.verticalLayoutWidget = QWidget(self.tab_control)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 311, 391))
        self.frame_option = QVBoxLayout(self.verticalLayoutWidget)
        self.frame_option.setObjectName(u"frame_option")
        self.frame_option.setContentsMargins(0, 3, 0, 3)
        self.tabWidget.addTab(self.tab_control, "")
        self.tab_multi = QWidget()
        self.tab_multi.setObjectName(u"tab_multi")
        self.verticalLayoutWidget_3 = QWidget(self.tab_multi)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(20, 60, 291, 391))
        self.vLayout_dongzip_statusbar = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vLayout_dongzip_statusbar.setObjectName(u"vLayout_dongzip_statusbar")
        self.vLayout_dongzip_statusbar.setContentsMargins(0, 0, 0, 0)
        self.btn_dongzip_reset = QPushButton(self.tab_multi)
        self.btn_dongzip_reset.setObjectName(u"btn_dongzip_reset")
        self.btn_dongzip_reset.setGeometry(QRect(119, 17, 93, 26))
        self.btn_dongzip_reset_2 = QPushButton(self.tab_multi)
        self.btn_dongzip_reset_2.setObjectName(u"btn_dongzip_reset_2")
        self.btn_dongzip_reset_2.setGeometry(QRect(218, 17, 92, 26))
        self.btn_dongzip = QPushButton(self.tab_multi)
        self.btn_dongzip.setObjectName(u"btn_dongzip")
        self.btn_dongzip.setGeometry(QRect(21, 17, 92, 26))
        self.tabWidget.addTab(self.tab_multi, "")
        self.tab_detect = QWidget()
        self.tab_detect.setObjectName(u"tab_detect")
        self.tableView = QTableView(self.tab_detect)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 10, 311, 441))
        self.tabWidget.addTab(self.tab_detect, "")
        self.tab_info = QWidget()
        self.tab_info.setObjectName(u"tab_info")
        self.textBrowser = QTextBrowser(self.tab_info)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 311, 441))
        self.tabWidget.addTab(self.tab_info, "")
        self.label_fps = QLabel(self.centralwidget)
        self.label_fps.setObjectName(u"label_fps")
        self.label_fps.setGeometry(QRect(790, 580, 299, 20))
        self.label_xy = QLabel(self.centralwidget)
        self.label_xy.setObjectName(u"label_xy")
        self.label_xy.setGeometry(QRect(790, 540, 299, 20))
        self.label_roi = QLabel(self.centralwidget)
        self.label_roi.setObjectName(u"label_roi")
        self.label_roi.setGeometry(QRect(790, 560, 299, 21))
        self.label_cap_num = QLabel(self.centralwidget)
        self.label_cap_num.setObjectName(u"label_cap_num")
        self.label_cap_num.setGeometry(QRect(790, 600, 311, 18))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setContextMenuPolicy(Qt.NoContextMenu)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btn_play.clicked.connect(MainWindow.slot_btn_play)
        self.btn_region_reset.clicked.connect(MainWindow.slot_btn_region_reset)
        self.btn_fileopen.clicked.connect(MainWindow.slot_btn_fileopen)
        self.btn_dongzip_reset_2.clicked.connect(MainWindow.slot_btn_open_complete)
        self.btn_dongzip_reset.clicked.connect(MainWindow.slot_btn_multi_reset)
        self.btn_dongzip.clicked.connect(MainWindow.slot_btn_multi_open)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_region_reset.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc2ec\uc601\uc5ed reset", None))
        self.btn_fileopen.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5f4\uae30", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"play", None))
        self.label.setText("")
        self.playTimer.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.btn_init_detection.setText(QCoreApplication.translate("MainWindow", u"\ud0d0\uc9c0\ub0b4\uc5ed \ucd08\uae30\ud654", None))
        self.btn_page_print.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ud654\uba74 \uc800\uc7a5", None))
        self.check_realsize.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\uc81c \uc0ac\uc774\uc988\ub85c \ubd84\uc11d", None))
        self.checkbox_yolo.setText(QCoreApplication.translate("MainWindow", u"AI \uac10\uc9c0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_control), QCoreApplication.translate("MainWindow", u"\ucee8\ud2b8\ub864", None))
        self.btn_dongzip_reset.setText(QCoreApplication.translate("MainWindow", u"reset", None))
        self.btn_dongzip_reset_2.setText(QCoreApplication.translate("MainWindow", u"\uc644\ub8cc \uc5f4\uae30", None))
        self.btn_dongzip.setText(QCoreApplication.translate("MainWindow", u"\uba40\ud2f0 open", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_multi), QCoreApplication.translate("MainWindow", u"\uba40\ud2f0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_detect), QCoreApplication.translate("MainWindow", u"\ud0d0\uc9c0 \ub9ac\uc2a4\ud2b8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_info), QCoreApplication.translate("MainWindow", u"\uc548\ub0b4", None))
        self.label_fps.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub808\uc784/\ucd08", None))
        self.label_xy.setText(QCoreApplication.translate("MainWindow", u"\ud574\uc0c1\ub3c4", None))
        self.label_roi.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc2ec\uc601\uc5ed", None))
        self.label_cap_num.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub808\uc784 \ubc88\ud638", None))
    # retranslateUi


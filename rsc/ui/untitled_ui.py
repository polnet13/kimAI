# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1179, 612)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"background-color: rgb(40, 44, 52);\n"
"\n"
"color: rgb(211, 211, 211);\n"
"\n"
"QPushButton {\n"
"    border: 1px solid #CCCCCC;\n"
"	font-size: 11px; /* \uae00\uc790 \ud06c\uae30 */\n"
"	padding: 5px 5px; /* \ub0b4\ubd80 \uc5ec\ubc31 */\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"	font-size: 12px; /* \uae00\uc790 \ud06c\uae30 */\n"
"    color: black; /* \ud638\ubc84 \uc0c1\ud0dc \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    }")
        self.leftMenuBg = QFrame(self.centralwidget)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setGeometry(QRect(0, 0, 60, 581))
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftMenuFrame.sizePolicy().hasHeightForWidth())
        self.leftMenuFrame.setSizePolicy(sizePolicy1)
        self.leftMenuFrame.setStyleSheet(u"QFrame {\n"
"    border-right: 1px solid rgb(0, 0, 0); /* \uc624\ub978\ucabd \ud14c\ub450\ub9ac\ub9cc \uc124\uc815 */\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"	font-size: 11px; /* \uae00\uc790 \ud06c\uae30 */\n"
"	padding: 5px 5px; /* \ub0b4\ubd80 \uc5ec\ubc31 */\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 255, 127);\n"
"	font-size: 12px; /* \uae00\uc790 \ud06c\uae30 */\n"
"    color: black; /* \ud638\ubc84 \uc0c1\ud0dc \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    }")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.topMenu.sizePolicy().hasHeightForWidth())
        self.topMenu.setSizePolicy(sizePolicy2)
        self.topMenu.setStyleSheet(u"")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy3)
        self.btn_home.setMinimumSize(QSize(0, 45))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        font1.setItalic(False)
        self.btn_home.setFont(font1)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_cctv = QPushButton(self.topMenu)
        self.btn_cctv.setObjectName(u"btn_cctv")
        sizePolicy3.setHeightForWidth(self.btn_cctv.sizePolicy().hasHeightForWidth())
        self.btn_cctv.setSizePolicy(sizePolicy3)
        self.btn_cctv.setMinimumSize(QSize(0, 45))
        self.btn_cctv.setFont(font1)
        self.btn_cctv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cctv.setLayoutDirection(Qt.LeftToRight)
        self.btn_cctv.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_cctv)

        self.btn_mosaic = QPushButton(self.topMenu)
        self.btn_mosaic.setObjectName(u"btn_mosaic")
        sizePolicy3.setHeightForWidth(self.btn_mosaic.sizePolicy().hasHeightForWidth())
        self.btn_mosaic.setSizePolicy(sizePolicy3)
        self.btn_mosaic.setMinimumSize(QSize(0, 45))
        self.btn_mosaic.setFont(font1)
        self.btn_mosaic.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_mosaic.setLayoutDirection(Qt.LeftToRight)
        self.btn_mosaic.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_mosaic)

        self.btn_bike = QPushButton(self.topMenu)
        self.btn_bike.setObjectName(u"btn_bike")
        sizePolicy3.setHeightForWidth(self.btn_bike.sizePolicy().hasHeightForWidth())
        self.btn_bike.setSizePolicy(sizePolicy3)
        self.btn_bike.setMinimumSize(QSize(0, 45))
        self.btn_bike.setFont(font1)
        self.btn_bike.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_bike.setLayoutDirection(Qt.LeftToRight)
        self.btn_bike.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_bike)

        self.btn_112 = QPushButton(self.topMenu)
        self.btn_112.setObjectName(u"btn_112")
        sizePolicy3.setHeightForWidth(self.btn_112.sizePolicy().hasHeightForWidth())
        self.btn_112.setSizePolicy(sizePolicy3)
        self.btn_112.setMinimumSize(QSize(0, 45))
        self.btn_112.setFont(font1)
        self.btn_112.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_112.setLayoutDirection(Qt.LeftToRight)
        self.btn_112.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_112)


        self.verticalMenuLayout.addWidget(self.topMenu)

        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalMenuLayout.addItem(self.verticalSpacer)

        self.btn_settings = QPushButton(self.leftMenuFrame)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy3.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy3)
        self.btn_settings.setMinimumSize(QSize(0, 45))
        self.btn_settings.setFont(font1)
        self.btn_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_settings.setLayoutDirection(Qt.LeftToRight)
        self.btn_settings.setStyleSheet(u"")

        self.verticalMenuLayout.addWidget(self.btn_settings)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)

        self.widget_center = QWidget(self.centralwidget)
        self.widget_center.setObjectName(u"widget_center")
        self.widget_center.setGeometry(QRect(60, -10, 1111, 591))
        font2 = QFont()
        font2.setFamilies([u"Arial Black"])
        font2.setBold(True)
        self.widget_center.setFont(font2)
        self.widget_center.setStyleSheet(u"QPushButton {\n"
"    border: 1px solid #CCCCCC;\n"
"	border-radius: 10px; /* \ub465\uadfc \ubaa8\uc11c\ub9ac */\n"
"	font-size: 12px; /* \uae00\uc790 \ud06c\uae30 */\n"
"	padding: 2px 2px; /* \ub0b4\ubd80 \uc5ec\ubc31 */\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"    color: black; /* \ud638\ubc84 \uc0c1\ud0dc \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    }")
        self.stackedWidget = QStackedWidget(self.widget_center)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(740, 20, 370, 570))
        self.label_cap_num = QLabel(self.widget_center)
        self.label_cap_num.setObjectName(u"label_cap_num")
        self.label_cap_num.setGeometry(QRect(500, 540, 161, 31))
        self.playSlider = QSlider(self.widget_center)
        self.playSlider.setObjectName(u"playSlider")
        self.playSlider.setEnabled(True)
        self.playSlider.setGeometry(QRect(10, 510, 721, 20))
        self.playSlider.setOrientation(Qt.Horizontal)
        self.btn_region_reset = QPushButton(self.widget_center)
        self.btn_region_reset.setObjectName(u"btn_region_reset")
        self.btn_region_reset.setGeometry(QRect(140, 530, 91, 31))
        self.btn_fileopen = QPushButton(self.widget_center)
        self.btn_fileopen.setObjectName(u"btn_fileopen")
        self.btn_fileopen.setGeometry(QRect(370, 530, 81, 31))
        self.playTimer = QLabel(self.widget_center)
        self.playTimer.setObjectName(u"playTimer")
        self.playTimer.setGeometry(QRect(663, 540, 61, 31))
        self.playTimer.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.btn_page_print = QPushButton(self.widget_center)
        self.btn_page_print.setObjectName(u"btn_page_print")
        self.btn_page_print.setGeometry(QRect(250, 530, 101, 31))
        self.slider_delay = QSlider(self.widget_center)
        self.slider_delay.setObjectName(u"slider_delay")
        self.slider_delay.setGeometry(QRect(250, 570, 161, 22))
        self.slider_delay.setMinimum(0)
        self.slider_delay.setMaximum(50)
        self.slider_delay.setSingleStep(1)
        self.slider_delay.setPageStep(1)
        self.slider_delay.setValue(0)
        self.slider_delay.setOrientation(Qt.Horizontal)
        self.label_2 = QLabel(self.widget_center)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 570, 101, 16))
        self.label_delay_time = QLabel(self.widget_center)
        self.label_delay_time.setObjectName(u"label_delay_time")
        self.label_delay_time.setGeometry(QRect(420, 570, 51, 16))
        self.label_delay_time.setFont(font)
        self.label_delay_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.btn_play = QPushButton(self.widget_center)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setGeometry(QRect(10, 540, 51, 28))
        self.btn_play.setStyleSheet(u"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 225, 208);\n"
"	font-size: 11px; /* \uae00\uc790 \ud06c\uae30 */\n"
"	padding: 5px 5px; /* \ub0b4\ubd80 \uc5ec\ubc31 */\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"	font-size: 12px; /* \uae00\uc790 \ud06c\uae30 */\n"
"    color: black; /* \ud638\ubc84 \uc0c1\ud0dc \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 */\n"
"    }")
        self.stackedWidget_play = QStackedWidget(self.widget_center)
        self.stackedWidget_play.setObjectName(u"stackedWidget_play")
        self.stackedWidget_play.setGeometry(QRect(10, 20, 721, 481))
        self.page_play = QWidget()
        self.page_play.setObjectName(u"page_play")
        self.label = QLabel(self.page_play)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 720, 480))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"")
        self.label.setFrameShape(QFrame.WinPanel)
        self.stackedWidget_play.addWidget(self.page_play)
        self.page_tableview = QWidget()
        self.page_tableview.setObjectName(u"page_tableview")
        self.tableView = QTableView(self.page_tableview)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 0, 700, 480))
        self.stackedWidget_play.addWidget(self.page_tableview)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setContextMenuPolicy(Qt.NoContextMenu)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(-1)
        self.stackedWidget_play.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"\ud50c\ub808\uc774\uc5b4", None))
        self.btn_cctv.setText(QCoreApplication.translate("MainWindow", u"\uc601\uc0c1\ubd84\uc11d", None))
        self.btn_mosaic.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\uc790\uc774\ud06c", None))
        self.btn_bike.setText(QCoreApplication.translate("MainWindow", u"\uc774\ub95c\ucc28", None))
        self.btn_112.setText(QCoreApplication.translate("MainWindow", u"\ucd9c\ub3d9\uc218\ub2f9", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.label_cap_num.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub808\uc784 \ubc88\ud638", None))
        self.btn_region_reset.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc2ec\uc601\uc5ed \ub9ac\uc14b", None))
#if QT_CONFIG(tooltip)
        self.btn_fileopen.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: o", None))
#endif // QT_CONFIG(tooltip)
        self.btn_fileopen.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5f4\uae30", None))
        self.playTimer.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.btn_page_print.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ud654\uba74 \uc800\uc7a5", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc7ac\uc0dd \uc9c0\uc5f0\uc2dc\uac04", None))
        self.label_delay_time.setText(QCoreApplication.translate("MainWindow", u"0 ms", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"play", None))
        self.label.setText("")
    # retranslateUi


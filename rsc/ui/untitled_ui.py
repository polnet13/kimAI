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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QKeySequenceEdit, QLabel,
    QLayout, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QScrollBar, QSizePolicy, QSlider,
    QSpacerItem, QStackedWidget, QStatusBar, QTableView,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1159, 613)
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#widget_center {	\n"
"	ba"
                        "ckground-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"/*\n"
"\n"
"\ud0ed\uc704\uc82f */\n"
"#tabWidget {	\n"
"	background-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"QPushButton {	\n"
"	background-color: rgb(112, 112, 112);\n"
"	color: rgb(220, 220, 220)\n"
"	padding: 5px 5px;         /* \ubc84\ud2bc \ub0b4\ubd80 \uc5ec\ubc31 */\n"
"    font-size: 15px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: r"
                        "gb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	backgrou"
                        "nd-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: "
                        "solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px"
                        "; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSet"
                        "tings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableView {\n"
"    background-color: #F0F0F0;\n"
"    border: 1px solid #CCCCCC;\n"
"    gridline-color: #CCCCCC;\n"
"    selection-background-color: #E1F5FE;\n"
"    selection-color: #0366d6;\n"
"    font-family: \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    border: 1px solid #0366d6;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #F0F0F0;\n"
"    border: 1px solid #CCCCCC;\n"
"    padding: 4px;\n"
"    font-weight: bold;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QTableView::horizontalHeader {\n"
"    background-color: #f0f0f0;  /* \ud5e4\ub354 \ubc30\uacbd\uc0c9 */\n"
"    color: #333;                /* \ud5e4\ub354 \uae00\uc790\uc0c9 */\n"
"}\n"
"\n"
"QTableVie"
                        "w::verticalHeader {\n"
"    background-color: #e0e0e0;  /* \uc778\ub371\uc2a4 \ubc30\uacbd\uc0c9 */\n"
"    color: #555;                /* \uc778\ub371\uc2a4 \uae00\uc790\uc0c9 */\n"
"}\n"
"\n"
"\n"
" ////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, "
                        "198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-li"
                        "ne:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: m"
                        "argin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url("
                        ":/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: to"
                        "p right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
" "
                        "   width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	c"
                        "olor: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
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
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
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

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topMenu.sizePolicy().hasHeightForWidth())
        self.topMenu.setSizePolicy(sizePolicy)
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy1)
        self.btn_home.setMinimumSize(QSize(0, 45))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.btn_home.setFont(font1)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_cctv = QPushButton(self.topMenu)
        self.btn_cctv.setObjectName(u"btn_cctv")
        sizePolicy1.setHeightForWidth(self.btn_cctv.sizePolicy().hasHeightForWidth())
        self.btn_cctv.setSizePolicy(sizePolicy1)
        self.btn_cctv.setMinimumSize(QSize(0, 45))
        self.btn_cctv.setFont(font1)
        self.btn_cctv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cctv.setLayoutDirection(Qt.LeftToRight)
        self.btn_cctv.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_cctv)

        self.btn_mosaic = QPushButton(self.topMenu)
        self.btn_mosaic.setObjectName(u"btn_mosaic")
        sizePolicy1.setHeightForWidth(self.btn_mosaic.sizePolicy().hasHeightForWidth())
        self.btn_mosaic.setSizePolicy(sizePolicy1)
        self.btn_mosaic.setMinimumSize(QSize(0, 45))
        self.btn_mosaic.setFont(font1)
        self.btn_mosaic.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_mosaic.setLayoutDirection(Qt.LeftToRight)
        self.btn_mosaic.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_mosaic)

        self.btn_bike = QPushButton(self.topMenu)
        self.btn_bike.setObjectName(u"btn_bike")
        sizePolicy1.setHeightForWidth(self.btn_bike.sizePolicy().hasHeightForWidth())
        self.btn_bike.setSizePolicy(sizePolicy1)
        self.btn_bike.setMinimumSize(QSize(0, 45))
        self.btn_bike.setFont(font1)
        self.btn_bike.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_bike.setLayoutDirection(Qt.LeftToRight)
        self.btn_bike.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_bike)

        self.btn_temp2 = QPushButton(self.topMenu)
        self.btn_temp2.setObjectName(u"btn_temp2")
        sizePolicy1.setHeightForWidth(self.btn_temp2.sizePolicy().hasHeightForWidth())
        self.btn_temp2.setSizePolicy(sizePolicy1)
        self.btn_temp2.setMinimumSize(QSize(0, 45))
        self.btn_temp2.setFont(font1)
        self.btn_temp2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_temp2.setLayoutDirection(Qt.LeftToRight)
        self.btn_temp2.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_temp2)

        self.btn_temp1_2 = QPushButton(self.topMenu)
        self.btn_temp1_2.setObjectName(u"btn_temp1_2")
        sizePolicy1.setHeightForWidth(self.btn_temp1_2.sizePolicy().hasHeightForWidth())
        self.btn_temp1_2.setSizePolicy(sizePolicy1)
        self.btn_temp1_2.setMinimumSize(QSize(0, 45))
        self.btn_temp1_2.setFont(font1)
        self.btn_temp1_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_temp1_2.setLayoutDirection(Qt.LeftToRight)
        self.btn_temp1_2.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_temp1_2)

        self.btn_temp1_3 = QPushButton(self.topMenu)
        self.btn_temp1_3.setObjectName(u"btn_temp1_3")
        sizePolicy1.setHeightForWidth(self.btn_temp1_3.sizePolicy().hasHeightForWidth())
        self.btn_temp1_3.setSizePolicy(sizePolicy1)
        self.btn_temp1_3.setMinimumSize(QSize(0, 45))
        self.btn_temp1_3.setFont(font1)
        self.btn_temp1_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_temp1_3.setLayoutDirection(Qt.LeftToRight)
        self.btn_temp1_3.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_temp1_3)

        self.btn_temp1_4 = QPushButton(self.topMenu)
        self.btn_temp1_4.setObjectName(u"btn_temp1_4")
        sizePolicy1.setHeightForWidth(self.btn_temp1_4.sizePolicy().hasHeightForWidth())
        self.btn_temp1_4.setSizePolicy(sizePolicy1)
        self.btn_temp1_4.setMinimumSize(QSize(0, 45))
        self.btn_temp1_4.setFont(font1)
        self.btn_temp1_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_temp1_4.setLayoutDirection(Qt.LeftToRight)
        self.btn_temp1_4.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_temp1_4)

        self.btn_temp1 = QPushButton(self.topMenu)
        self.btn_temp1.setObjectName(u"btn_temp1")
        sizePolicy1.setHeightForWidth(self.btn_temp1.sizePolicy().hasHeightForWidth())
        self.btn_temp1.setSizePolicy(sizePolicy1)
        self.btn_temp1.setMinimumSize(QSize(0, 45))
        self.btn_temp1.setFont(font1)
        self.btn_temp1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_temp1.setLayoutDirection(Qt.LeftToRight)
        self.btn_temp1.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.btn_temp1)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalMenuLayout.addItem(self.verticalSpacer)

        self.btn_settings = QPushButton(self.leftMenuFrame)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy1.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy1)
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
        self.widget_center.setGeometry(QRect(60, -10, 1091, 591))
        self.stackedWidget = QStackedWidget(self.widget_center)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(740, 20, 371, 571))
        self.stack_settings = QWidget()
        self.stack_settings.setObjectName(u"stack_settings")
        self.horizontalScrollBar = QScrollBar(self.stack_settings)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        self.horizontalScrollBar.setGeometry(QRect(70, 220, 160, 16))
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)
        self.verticalScrollBar = QScrollBar(self.stack_settings)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setGeometry(QRect(290, 280, 16, 160))
        self.verticalScrollBar.setOrientation(Qt.Vertical)
        self.horizontalSlider = QSlider(self.stack_settings)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(90, 190, 160, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.verticalSlider = QSlider(self.stack_settings)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setGeometry(QRect(140, 360, 22, 160))
        self.verticalSlider.setOrientation(Qt.Vertical)
        self.keySequenceEdit = QKeySequenceEdit(self.stack_settings)
        self.keySequenceEdit.setObjectName(u"keySequenceEdit")
        self.keySequenceEdit.setGeometry(QRect(90, 260, 113, 24))
        self.label_12 = QLabel(self.stack_settings)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(230, 30, 64, 15))
        self.progressBar_6 = QProgressBar(self.stack_settings)
        self.progressBar_6.setObjectName(u"progressBar_6")
        self.progressBar_6.setGeometry(QRect(20, 340, 291, 23))
        self.progressBar_6.setValue(24)
        self.label_13 = QLabel(self.stack_settings)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 20, 64, 15))
        self.label_xy_ = QLabel(self.stack_settings)
        self.label_xy_.setObjectName(u"label_xy_")
        self.label_xy_.setGeometry(QRect(100, 20, 64, 15))
        self.label_fps_ = QLabel(self.stack_settings)
        self.label_fps_.setObjectName(u"label_fps_")
        self.label_fps_.setGeometry(QRect(100, 50, 64, 15))
        self.stackedWidget.addWidget(self.stack_settings)
        self.stack_home = QWidget()
        self.stack_home.setObjectName(u"stack_home")
        self.label_10 = QLabel(self.stack_home)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 20, 64, 15))
        self.stackedWidget.addWidget(self.stack_home)
        self.stack_temp = QWidget()
        self.stack_temp.setObjectName(u"stack_temp")
        self.stackedWidget.addWidget(self.stack_temp)
        self.stack_mosaic = QWidget()
        self.stack_mosaic.setObjectName(u"stack_mosaic")
        self.verticalLayoutWidget_12 = QWidget(self.stack_mosaic)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 341, 561))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
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

        self.stackedWidget.addWidget(self.stack_mosaic)
        self.stack_bike = QWidget()
        self.stack_bike.setObjectName(u"stack_bike")
        self.gridLayoutWidget = QWidget(self.stack_bike)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 440, 331, 121))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 5, 1, 1)

        self.text_num = QLineEdit(self.gridLayoutWidget)
        self.text_num.setObjectName(u"text_num")
        self.text_num.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.text_num, 0, 6, 1, 1)

        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 3, 5, 1, 1)

        self.text_si = QLineEdit(self.gridLayoutWidget)
        self.text_si.setObjectName(u"text_si")
        self.text_si.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.text_si, 0, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 1, 6, 1, 1)

        self.text_giho = QLineEdit(self.gridLayoutWidget)
        self.text_giho.setObjectName(u"text_giho")
        self.text_giho.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.text_giho, 0, 5, 1, 1)

        self.pushButton_4 = QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 3, 1, 1, 1)

        self.pushButton_6 = QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout.addWidget(self.pushButton_6, 3, 6, 1, 1)

        self.tableView_bike = QTableView(self.stack_bike)
        self.tableView_bike.setObjectName(u"tableView_bike")
        self.tableView_bike.setGeometry(QRect(20, 20, 311, 411))
        self.stackedWidget.addWidget(self.stack_bike)
        self.stack_cctv = QWidget()
        self.stack_cctv.setObjectName(u"stack_cctv")
        self.btn_multi_open = QPushButton(self.stack_cctv)
        self.btn_multi_open.setObjectName(u"btn_multi_open")
        self.btn_multi_open.setGeometry(QRect(20, 20, 92, 26))
        self.verticalLayoutWidget_3 = QWidget(self.stack_cctv)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(19, 223, 311, 321))
        self.vLayout_dongzip_statusbar = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vLayout_dongzip_statusbar.setObjectName(u"vLayout_dongzip_statusbar")
        self.vLayout_dongzip_statusbar.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.stack_cctv)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(19, 53, 81, 16))
        self.btn_multi_complete_open = QPushButton(self.stack_cctv)
        self.btn_multi_complete_open.setObjectName(u"btn_multi_complete_open")
        self.btn_multi_complete_open.setGeometry(QRect(217, 20, 92, 26))
        self.slider_multi_thr = QSlider(self.stack_cctv)
        self.slider_multi_thr.setObjectName(u"slider_multi_thr")
        self.slider_multi_thr.setGeometry(QRect(119, 53, 191, 22))
        self.slider_multi_thr.setFont(font1)
        self.slider_multi_thr.setMinimum(1)
        self.slider_multi_thr.setValue(50)
        self.slider_multi_thr.setOrientation(Qt.Horizontal)
        self.btn_multi_reset = QPushButton(self.stack_cctv)
        self.btn_multi_reset.setObjectName(u"btn_multi_reset")
        self.btn_multi_reset.setGeometry(QRect(118, 20, 93, 26))
        self.textBrowser_multi = QTextBrowser(self.stack_cctv)
        self.textBrowser_multi.setObjectName(u"textBrowser_multi")
        self.textBrowser_multi.setGeometry(QRect(20, 80, 311, 131))
        self.stackedWidget.addWidget(self.stack_cctv)
        self.label = QLabel(self.widget_center)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 720, 480))
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QFrame.WinPanel)
        self.label_cap_num = QLabel(self.widget_center)
        self.label_cap_num.setObjectName(u"label_cap_num")
        self.label_cap_num.setGeometry(QRect(10, 530, 211, 18))
        self.playSlider = QSlider(self.widget_center)
        self.playSlider.setObjectName(u"playSlider")
        self.playSlider.setEnabled(True)
        self.playSlider.setGeometry(QRect(10, 510, 721, 20))
        self.playSlider.setOrientation(Qt.Horizontal)
        self.btn_region_reset = QPushButton(self.widget_center)
        self.btn_region_reset.setObjectName(u"btn_region_reset")
        self.btn_region_reset.setGeometry(QRect(100, 560, 111, 31))
        self.btn_fileopen = QPushButton(self.widget_center)
        self.btn_fileopen.setObjectName(u"btn_fileopen")
        self.btn_fileopen.setGeometry(QRect(650, 560, 81, 31))
        self.btn_play = QToolButton(self.widget_center)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setGeometry(QRect(20, 560, 61, 31))
        self.btn_play.setStyleSheet(u"color: #ffffff;\n"
"background-color: rgb(61, 50, 44);")
        self.playTimer = QLabel(self.widget_center)
        self.playTimer.setObjectName(u"playTimer")
        self.playTimer.setGeometry(QRect(653, 530, 71, 20))
        self.btn_page_print = QPushButton(self.widget_center)
        self.btn_page_print.setObjectName(u"btn_page_print")
        self.btn_page_print.setGeometry(QRect(510, 560, 121, 31))
        self.checkbox_yolo = QCheckBox(self.widget_center)
        self.checkbox_yolo.setObjectName(u"checkbox_yolo")
        self.checkbox_yolo.setGeometry(QRect(420, 530, 81, 19))
        self.checkbox_yolo.setChecked(False)
        self.check_realsize = QCheckBox(self.widget_center)
        self.check_realsize.setObjectName(u"check_realsize")
        self.check_realsize.setEnabled(True)
        self.check_realsize.setGeometry(QRect(510, 530, 121, 19))
        self.check_realsize.setChecked(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setContextMenuPolicy(Qt.NoContextMenu)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btn_page_print.clicked.connect(MainWindow.slot_btn_print)
        self.btn_play.clicked.connect(MainWindow.slot_btn_play)
        self.btn_fileopen.clicked.connect(MainWindow.slot_btn_fileopen)
        self.btn_region_reset.clicked.connect(MainWindow.slot_btn_region_reset)

        self.stackedWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"home", None))
        self.btn_cctv.setText(QCoreApplication.translate("MainWindow", u"CCTV", None))
        self.btn_mosaic.setText(QCoreApplication.translate("MainWindow", u"Mosaic", None))
        self.btn_bike.setText(QCoreApplication.translate("MainWindow", u"\ucea0\ub2e8\uc18d", None))
        self.btn_temp2.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.btn_temp1_2.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.btn_temp1_3.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.btn_temp1_4.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.btn_temp1.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\ud574\uc0c1\ub3c4", None))
        self.label_xy_.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_fps_.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"home", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_start.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 4", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_start.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791 \uc810", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_end.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 5", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_end.setText(QCoreApplication.translate("MainWindow", u"\ub05d \uc810", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_analyze.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 6", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_analyze.setText(QCoreApplication.translate("MainWindow", u"\ubd84\uc11d", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_add_frame.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 1", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_add_frame.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub808\uc784 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_add_frams.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 2", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_add_frams.setText(QCoreApplication.translate("MainWindow", u"\uc804\uccb4 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.btn_mosaic_video_out.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: 3", None))
#endif // QT_CONFIG(tooltip)
        self.btn_mosaic_video_out.setText(QCoreApplication.translate("MainWindow", u"\uc0dd\uc131", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\uc790\uc774\ud06c \uc815\ub3c4", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.btn_multi_open.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c \uc5f4\uae30", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ubbfc\uac10\ub3c4", None))
        self.btn_multi_complete_open.setText(QCoreApplication.translate("MainWindow", u"\uc644\ub8cc \uc5f4\uae30", None))
        self.btn_multi_reset.setText(QCoreApplication.translate("MainWindow", u"reset", None))
        self.label.setText("")
        self.label_cap_num.setText(QCoreApplication.translate("MainWindow", u"\ud504\ub808\uc784 \ubc88\ud638", None))
        self.btn_region_reset.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc2ec\uc601\uc5ed \ub9ac\uc14b", None))
#if QT_CONFIG(tooltip)
        self.btn_fileopen.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: o", None))
#endif // QT_CONFIG(tooltip)
        self.btn_fileopen.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5f4\uae30", None))
#if QT_CONFIG(tooltip)
        self.btn_play.setToolTip(QCoreApplication.translate("MainWindow", u"\ub2e8\ucd95\ud0a4: s", None))
#endif // QT_CONFIG(tooltip)
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"play", None))
        self.playTimer.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.btn_page_print.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \ud654\uba74 \uc800\uc7a5", None))
        self.checkbox_yolo.setText(QCoreApplication.translate("MainWindow", u"AI \uac10\uc9c0", None))
#if QT_CONFIG(tooltip)
        self.check_realsize.setToolTip(QCoreApplication.translate("MainWindow", u"\ud574\uc0c1\ub3c4\uac00 \ub192\uc740 \uacbd\uc6b0 \uc2e4\uc81c \uc0ac\uc774\uc988\ub85c \ubd84\uc11d\ud558\uba74 \ub290\ub824\uc9c8 \uc218 \uc788\uc74c", None))
#endif // QT_CONFIG(tooltip)
        self.check_realsize.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\uc81c \uc0ac\uc774\uc988", None))
    # retranslateUi


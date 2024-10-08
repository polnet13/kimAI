# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLayout,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(370, 570)
        self.verticalLayoutWidget_12 = QWidget(Settings)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 361, 561))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.label = QLabel(self.verticalLayoutWidget_12)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_7.addWidget(self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget_12)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2)

        self.checkBox_cuda = QCheckBox(self.verticalLayoutWidget_12)
        self.checkBox_cuda.setObjectName(u"checkBox_cuda")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBox_cuda.sizePolicy().hasHeightForWidth())
        self.checkBox_cuda.setSizePolicy(sizePolicy1)
        self.checkBox_cuda.setChecked(True)

        self.verticalLayout_7.addWidget(self.checkBox_cuda)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.textBrowser = QTextBrowser(self.verticalLayoutWidget_12)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(100)
        sizePolicy2.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy2)
        self.textBrowser.setMaximumSize(QSize(340, 170))
        self.textBrowser.setInputMethodHints(Qt.ImhNone)

        self.verticalLayout_7.addWidget(self.textBrowser)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Form", None))
        self.label.setText(QCoreApplication.translate("Settings", u"\uc124\uc815", None))
        self.label_2.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_cuda.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.checkBox_cuda.setText(QCoreApplication.translate("Settings", u"CUDA \uac00\uc18d(\uac1c\ubc1c\uc6a9 \uc635\uc158)", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Settings", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\ud504\ub85c\uadf8\ub7a8 \uc81c\uc548 </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">prudent13@naver.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\ubcf8 \ud504\ub85c\uadf8\ub7a8\uc740 \ub525\ub7ec\ub2dd"
                        "\uc744 \ud65c\uc6a9\ud574\uc11c \uac1d\uccb4(\uc0ac\ub78c, \uc790\ub3d9\ucc28 \ub4f1)\ub97c \uc778\uc2dd\ud560 \uc218 \uc788\uace0 </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\uc6c0\uc9c1\uc784 \uac10\uc9c0 \uc54c\uace0\ub9ac\uc998\uc744 \uc801\uc6a9\ud558\uc5ec CCTV \uc601\uc0c1\uc744 \ubd84\uc11d\uc744 \ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\ub610\ud55c \uc5d1\uc140\uacfc \uac19\uc740 \uc815\ud615\ub370\uc774\ud130\ub97c \ucc98\ub9ac, \uc2dc\uac01\ud654 \ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4. </p></body></html>", None))
    # retranslateUi


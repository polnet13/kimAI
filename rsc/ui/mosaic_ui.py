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
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_mosaic(object):
    def setupUi(self, mosaic):
        if not mosaic.objectName():
            mosaic.setObjectName(u"mosaic")
        mosaic.resize(370, 570)
        self.verticalLayoutWidget_12 = QWidget(mosaic)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 371, 571))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_11 = QLabel(self.verticalLayoutWidget_12)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_7.addWidget(self.label_11)

        self.slider_mosaic = QSlider(self.verticalLayoutWidget_12)
        self.slider_mosaic.setObjectName(u"slider_mosaic")
        self.slider_mosaic.setMaximum(100)
        self.slider_mosaic.setValue(50)
        self.slider_mosaic.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.slider_mosaic)

        self.label = QLabel(self.verticalLayoutWidget_12)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.label_2 = QLabel(self.verticalLayoutWidget_12)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2)

        self.tableView_mosaic_ID = QTableView(self.verticalLayoutWidget_12)
        self.tableView_mosaic_ID.setObjectName(u"tableView_mosaic_ID")
        self.tableView_mosaic_ID.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.tableView_mosaic_ID.sizePolicy().hasHeightForWidth())
        self.tableView_mosaic_ID.setSizePolicy(sizePolicy)
        self.tableView_mosaic_ID.setStyleSheet(u"background-color: rgb(40, 44, 52);\n"
"selection-background-color: rgb(255, 35, 86);\n"
"alternate-background-color: rgb(157, 255, 29);\n"
"")
        self.tableView_mosaic_ID.horizontalHeader().setVisible(False)

        self.verticalLayout_7.addWidget(self.tableView_mosaic_ID)

        self.label_3 = QLabel(self.verticalLayoutWidget_12)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.tableView_mosaic_frame = QTableView(self.verticalLayoutWidget_12)
        self.tableView_mosaic_frame.setObjectName(u"tableView_mosaic_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.tableView_mosaic_frame.sizePolicy().hasHeightForWidth())
        self.tableView_mosaic_frame.setSizePolicy(sizePolicy1)
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

        self.progressBar_mosaic = QProgressBar(self.verticalLayoutWidget_12)
        self.progressBar_mosaic.setObjectName(u"progressBar_mosaic")
        self.progressBar_mosaic.setValue(0)

        self.verticalLayout_7.addWidget(self.progressBar_mosaic)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_4 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_5.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_5.addWidget(self.pushButton_6)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_1 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_1.setObjectName(u"pushButton_1")

        self.horizontalLayout_6.addWidget(self.pushButton_1)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_6.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_6.addWidget(self.pushButton_3)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)


        self.verticalLayout_7.addLayout(self.verticalLayout_10)


        self.retranslateUi(mosaic)

        QMetaObject.connectSlotsByName(mosaic)
    # setupUi

    def retranslateUi(self, mosaic):
        mosaic.setWindowTitle(QCoreApplication.translate("mosaic", u"Form", None))
        self.label_11.setText(QCoreApplication.translate("mosaic", u"\ubaa8\uc790\uc774\ud06c \uc815\ub3c4", None))
        self.label.setText(QCoreApplication.translate("mosaic", u"50", None))
        self.label_2.setText(QCoreApplication.translate("mosaic", u"\uac1d\uccb4", None))
        self.label_3.setText(QCoreApplication.translate("mosaic", u"frame", None))
#if QT_CONFIG(tooltip)
        self.pushButton_4.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 4", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_4.setText(QCoreApplication.translate("mosaic", u"\uc2dc\uc791 \uc810", None))
#if QT_CONFIG(tooltip)
        self.pushButton_5.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 5", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_5.setText(QCoreApplication.translate("mosaic", u"\ub05d \uc810", None))
#if QT_CONFIG(tooltip)
        self.pushButton_6.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 6", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_6.setText(QCoreApplication.translate("mosaic", u"\ubd84\uc11d", None))
#if QT_CONFIG(tooltip)
        self.pushButton_1.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 1", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_1.setText(QCoreApplication.translate("mosaic", u"\ud504\ub808\uc784 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 2", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("mosaic", u"\uc804\uccb4 \ucd94\uac00", None))
#if QT_CONFIG(tooltip)
        self.pushButton_3.setToolTip(QCoreApplication.translate("mosaic", u"\ub2e8\ucd95\ud0a4: 3", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_3.setText(QCoreApplication.translate("mosaic", u"\uc0dd\uc131", None))
    # retranslateUi


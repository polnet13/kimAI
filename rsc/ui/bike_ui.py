# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bike.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_Bike(object):
    def setupUi(self, Bike):
        if not Bike.objectName():
            Bike.setObjectName(u"Bike")
        Bike.resize(370, 570)
        self.verticalLayoutWidget_12 = QWidget(Bike)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 371, 571))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_12)
        self.label.setObjectName(u"label")

        self.verticalLayout_7.addWidget(self.label)

        self.progressBar_mosaic = QProgressBar(self.verticalLayoutWidget_12)
        self.progressBar_mosaic.setObjectName(u"progressBar_mosaic")
        self.progressBar_mosaic.setValue(0)

        self.verticalLayout_7.addWidget(self.progressBar_mosaic)

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
        self.text_si = QLineEdit(self.verticalLayoutWidget_12)
        self.text_si.setObjectName(u"text_si")
        self.text_si.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.text_si)

        self.text_giho = QLineEdit(self.verticalLayoutWidget_12)
        self.text_giho.setObjectName(u"text_giho")
        self.text_giho.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.text_giho)

        self.text_num = QLineEdit(self.verticalLayoutWidget_12)
        self.text_num.setObjectName(u"text_num")
        self.text_num.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.text_num)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_4 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_6.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_6.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_6.addWidget(self.pushButton_6)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)


        self.verticalLayout_7.addLayout(self.verticalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_1 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_1.setObjectName(u"pushButton_1")

        self.horizontalLayout_7.addWidget(self.pushButton_1)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_7.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.retranslateUi(Bike)

        QMetaObject.connectSlotsByName(Bike)
    # setupUi

    def retranslateUi(self, Bike):
        Bike.setWindowTitle(QCoreApplication.translate("Bike", u"Form", None))
        self.label.setText(QCoreApplication.translate("Bike", u"\uc774\ub95c\ucc28 \ub2e8\uc18d \uc790\ub3d9\ud654", None))
        self.pushButton_4.setText(QCoreApplication.translate("Bike", u"4", None))
        self.pushButton_5.setText(QCoreApplication.translate("Bike", u"5", None))
        self.pushButton_6.setText(QCoreApplication.translate("Bike", u"6", None))
        self.pushButton_1.setText(QCoreApplication.translate("Bike", u"1", None))
        self.pushButton_2.setText(QCoreApplication.translate("Bike", u"2", None))
        self.pushButton_3.setText(QCoreApplication.translate("Bike", u"3", None))
    # retranslateUi


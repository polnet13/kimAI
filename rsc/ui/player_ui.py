# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'player.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSlider, QTableView, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(366, 561)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_12 = QWidget(Form)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 361, 561))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.label_2 = QLabel(self.verticalLayoutWidget_12)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget_12)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(30)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_7.addWidget(self.horizontalSlider)

        self.btn_open_file = QPushButton(self.verticalLayoutWidget_12)
        self.btn_open_file.setObjectName(u"btn_open_file")

        self.verticalLayout_7.addWidget(self.btn_open_file)

        self.tableView = QTableView(self.verticalLayoutWidget_12)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setMinimumSize(QSize(339, 0))

        self.verticalLayout_7.addWidget(self.tableView)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"a: -1\ud504\ub808\uc784, s:\uc815\uc9c0/\ud50c\ub808\uc774, d: +1 \ud504\ub808\uc784", None))
        self.btn_open_file.setText(QCoreApplication.translate("Form", u"\ud30c\uc77c \uc5f4\uae30", None))
    # retranslateUi


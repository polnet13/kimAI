# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'singo.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

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
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 349, 561))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 20)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_tag = QHBoxLayout()
        self.horizontalLayout_tag.setObjectName(u"horizontalLayout_tag")
        self.label = QLabel(self.verticalLayoutWidget_12)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_tag.addWidget(self.label)


        self.verticalLayout_10.addLayout(self.horizontalLayout_tag)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_2)

        self.horizontalLayout_name = QHBoxLayout()
        self.horizontalLayout_name.setObjectName(u"horizontalLayout_name")
        self.label_name = QLabel(self.verticalLayoutWidget_12)
        self.label_name.setObjectName(u"label_name")

        self.horizontalLayout_name.addWidget(self.label_name)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_name.addItem(self.horizontalSpacer)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget_12)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_name.addWidget(self.lineEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_name)

        self.label_6 = QLabel(self.verticalLayoutWidget_12)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_10.addWidget(self.label_6)

        self.horizontalLayout_file = QHBoxLayout()
        self.horizontalLayout_file.setObjectName(u"horizontalLayout_file")
        self.btn_sagun = QPushButton(self.verticalLayoutWidget_12)
        self.btn_sagun.setObjectName(u"btn_sagun")

        self.horizontalLayout_file.addWidget(self.btn_sagun)

        self.btn_individual = QPushButton(self.verticalLayoutWidget_12)
        self.btn_individual.setObjectName(u"btn_individual")

        self.horizontalLayout_file.addWidget(self.btn_individual)


        self.verticalLayout_10.addLayout(self.horizontalLayout_file)

        self.horizontalLayout_checkbox = QHBoxLayout()
        self.horizontalLayout_checkbox.setObjectName(u"horizontalLayout_checkbox")
        self.checkBox_dongil = QCheckBox(self.verticalLayoutWidget_12)
        self.checkBox_dongil.setObjectName(u"checkBox_dongil")
        self.checkBox_dongil.setChecked(True)

        self.horizontalLayout_checkbox.addWidget(self.checkBox_dongil)

        self.checkBox_ftx = QCheckBox(self.verticalLayoutWidget_12)
        self.checkBox_ftx.setObjectName(u"checkBox_ftx")
        self.checkBox_ftx.setChecked(True)

        self.horizontalLayout_checkbox.addWidget(self.checkBox_ftx)


        self.verticalLayout_10.addLayout(self.horizontalLayout_checkbox)

        self.horizontalLayout_point1 = QHBoxLayout()
        self.horizontalLayout_point1.setObjectName(u"horizontalLayout_point1")
        self.btn_point_1 = QPushButton(self.verticalLayoutWidget_12)
        self.btn_point_1.setObjectName(u"btn_point_1")

        self.horizontalLayout_point1.addWidget(self.btn_point_1)

        self.label_point1 = QLabel(self.verticalLayoutWidget_12)
        self.label_point1.setObjectName(u"label_point1")

        self.horizontalLayout_point1.addWidget(self.label_point1)


        self.verticalLayout_10.addLayout(self.horizontalLayout_point1)

        self.horizontalLayout_point2 = QHBoxLayout()
        self.horizontalLayout_point2.setObjectName(u"horizontalLayout_point2")
        self.btn_point_2 = QPushButton(self.verticalLayoutWidget_12)
        self.btn_point_2.setObjectName(u"btn_point_2")

        self.horizontalLayout_point2.addWidget(self.btn_point_2)

        self.label_point2 = QLabel(self.verticalLayoutWidget_12)
        self.label_point2.setObjectName(u"label_point2")

        self.horizontalLayout_point2.addWidget(self.label_point2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_point2)


        self.verticalLayout_7.addLayout(self.verticalLayout_10)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.horizontalLayout_make_df = QHBoxLayout()
        self.horizontalLayout_make_df.setObjectName(u"horizontalLayout_make_df")
        self.btn_make_df = QPushButton(self.verticalLayoutWidget_12)
        self.btn_make_df.setObjectName(u"btn_make_df")

        self.horizontalLayout_make_df.addWidget(self.btn_make_df)

        self.btn_del = QPushButton(self.verticalLayoutWidget_12)
        self.btn_del.setObjectName(u"btn_del")

        self.horizontalLayout_make_df.addWidget(self.btn_del)

        self.btn_run = QPushButton(self.verticalLayoutWidget_12)
        self.btn_run.setObjectName(u"btn_run")

        self.horizontalLayout_make_df.addWidget(self.btn_run)


        self.verticalLayout_7.addLayout(self.horizontalLayout_make_df)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_12)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_7.addWidget(self.pushButton_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ucd9c\ub3d9\uc218\ub2f9 \uc790\ub3d9\ud654", None))
        self.label_name.setText(QCoreApplication.translate("Form", u"\uc774\ub984", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\ud30c\uc77c \ub4f1\ub85d(2\uac1c)", None))
        self.btn_sagun.setText(QCoreApplication.translate("Form", u"\uc0ac\uac74\uac80\uc0c9\ub9ac\uc2a4\ud2b8", None))
        self.btn_individual.setText(QCoreApplication.translate("Form", u"\uac1c\uc778\ubcc4 \ucd9c\ub3d9\uc218\ub2f9 \ud30c\uc77c", None))
        self.checkBox_dongil.setText(QCoreApplication.translate("Form", u"\ub3d9\uc77c\uac74 \uc81c\uc678", None))
        self.checkBox_ftx.setText(QCoreApplication.translate("Form", u"FTX \uc81c\uc678", None))
        self.btn_point_1.setText(QCoreApplication.translate("Form", u"?? \uc88c\ud45c \uc785\ub825", None))
        self.label_point1.setText(QCoreApplication.translate("Form", u"(224, 255)", None))
        self.btn_point_2.setText(QCoreApplication.translate("Form", u"?? \uc88c\ud45c \uc785\ub825", None))
        self.label_point2.setText(QCoreApplication.translate("Form", u"(654, 255)", None))
        self.btn_make_df.setText(QCoreApplication.translate("Form", u"\uc815\ub9ac", None))
        self.btn_del.setText(QCoreApplication.translate("Form", u"\uc120\ud0dd \ud589 \uc0ad\uc81c(del)", None))
        self.btn_run.setText(QCoreApplication.translate("Form", u"\uc5d1\uc140 \ucd9c\ub825", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\uc790\ub3d9\ud654 \uc2e4\ud589", None))
    # retranslateUi


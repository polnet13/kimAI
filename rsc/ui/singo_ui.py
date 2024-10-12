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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(370, 570)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(370, 570))
        self.verticalLayoutWidget_12 = QWidget(Form)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 361, 569))
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

        self.groupBox_team = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_team.setObjectName(u"groupBox_team")
        self.groupBox_team.setMinimumSize(QSize(0, 60))
        self.horizontalLayoutWidget_2 = QWidget(self.groupBox_team)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 20, 341, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ra_team_1 = QRadioButton(self.horizontalLayoutWidget_2)
        self.ra_team_1.setObjectName(u"ra_team_1")
        self.ra_team_1.setMinimumSize(QSize(20, 0))
        self.ra_team_1.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.ra_team_1)

        self.ra_team_2 = QRadioButton(self.horizontalLayoutWidget_2)
        self.ra_team_2.setObjectName(u"ra_team_2")
        self.ra_team_2.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.ra_team_2)

        self.ra_team_3 = QRadioButton(self.horizontalLayoutWidget_2)
        self.ra_team_3.setObjectName(u"ra_team_3")
        self.ra_team_3.setMinimumSize(QSize(60, 0))
        self.ra_team_3.setMaximumSize(QSize(60, 100))

        self.horizontalLayout_3.addWidget(self.ra_team_3)

        self.ra_team_4 = QRadioButton(self.horizontalLayoutWidget_2)
        self.ra_team_4.setObjectName(u"ra_team_4")
        self.ra_team_4.setMinimumSize(QSize(60, 0))
        self.ra_team_4.setMaximumSize(QSize(60, 100))

        self.horizontalLayout_3.addWidget(self.ra_team_4)


        self.verticalLayout_10.addWidget(self.groupBox_team)

        self.groupBox_rank = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_rank.setObjectName(u"groupBox_rank")
        self.groupBox_rank.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setBold(False)
        self.groupBox_rank.setFont(font)
        self.horizontalLayoutWidget = QWidget(self.groupBox_rank)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 20, 341, 21))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ra_rank_1 = QRadioButton(self.horizontalLayoutWidget)
        self.ra_rank_1.setObjectName(u"ra_rank_1")

        self.horizontalLayout_2.addWidget(self.ra_rank_1)

        self.ra_rank_2 = QRadioButton(self.horizontalLayoutWidget)
        self.ra_rank_2.setObjectName(u"ra_rank_2")

        self.horizontalLayout_2.addWidget(self.ra_rank_2)

        self.ra_rank_3 = QRadioButton(self.horizontalLayoutWidget)
        self.ra_rank_3.setObjectName(u"ra_rank_3")

        self.horizontalLayout_2.addWidget(self.ra_rank_3)

        self.ra_rank_4 = QRadioButton(self.horizontalLayoutWidget)
        self.ra_rank_4.setObjectName(u"ra_rank_4")

        self.horizontalLayout_2.addWidget(self.ra_rank_4)

        self.ra_rank_5 = QRadioButton(self.horizontalLayoutWidget)
        self.ra_rank_5.setObjectName(u"ra_rank_5")

        self.horizontalLayout_2.addWidget(self.ra_rank_5)


        self.verticalLayout_10.addWidget(self.groupBox_rank)

        self.horizontalLayout_name = QHBoxLayout()
        self.horizontalLayout_name.setSpacing(10)
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

        self.groupBox_files = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_files.setObjectName(u"groupBox_files")
        self.groupBox_files.setMinimumSize(QSize(0, 70))
        self.layoutWidget = QWidget(self.groupBox_files)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 30, 311, 30))
        self.horizontalLayout_file = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_file.setObjectName(u"horizontalLayout_file")
        self.horizontalLayout_file.setContentsMargins(0, 0, 0, 0)
        self.btn_sagun = QPushButton(self.layoutWidget)
        self.btn_sagun.setObjectName(u"btn_sagun")

        self.horizontalLayout_file.addWidget(self.btn_sagun)

        self.btn_individual = QPushButton(self.layoutWidget)
        self.btn_individual.setObjectName(u"btn_individual")

        self.horizontalLayout_file.addWidget(self.btn_individual)


        self.verticalLayout_10.addWidget(self.groupBox_files)

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


        self.verticalLayout_7.addLayout(self.verticalLayout_10)

        self.groupBox_points = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_points.setObjectName(u"groupBox_points")
        self.groupBox_points.setMinimumSize(QSize(0, 110))
        self.verticalLayoutWidget = QWidget(self.groupBox_points)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 321, 80))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_point2 = QHBoxLayout()
        self.horizontalLayout_point2.setObjectName(u"horizontalLayout_point2")
        self.btn_point_2 = QPushButton(self.verticalLayoutWidget)
        self.btn_point_2.setObjectName(u"btn_point_2")

        self.horizontalLayout_point2.addWidget(self.btn_point_2)

        self.label_point2 = QLabel(self.verticalLayoutWidget)
        self.label_point2.setObjectName(u"label_point2")

        self.horizontalLayout_point2.addWidget(self.label_point2)


        self.verticalLayout.addLayout(self.horizontalLayout_point2)

        self.horizontalLayout_point1 = QHBoxLayout()
        self.horizontalLayout_point1.setObjectName(u"horizontalLayout_point1")
        self.btn_point_1 = QPushButton(self.verticalLayoutWidget)
        self.btn_point_1.setObjectName(u"btn_point_1")

        self.horizontalLayout_point1.addWidget(self.btn_point_1)

        self.label_point1 = QLabel(self.verticalLayoutWidget)
        self.label_point1.setObjectName(u"label_point1")

        self.horizontalLayout_point1.addWidget(self.label_point1)


        self.verticalLayout.addLayout(self.horizontalLayout_point1)


        self.verticalLayout_7.addWidget(self.groupBox_points)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.horizontalLayout_make_df = QHBoxLayout()
        self.horizontalLayout_make_df.setObjectName(u"horizontalLayout_make_df")
        self.horizontalLayout_make_df.setSizeConstraint(QLayout.SetMinimumSize)
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
        self.label.setText(QCoreApplication.translate("Form", u"\ucd9c\ub3d9\uc218\ub2f9 \uc790\ub3d9\ud654 (Test \ubc84\uc804)", None))
        self.groupBox_team.setTitle(QCoreApplication.translate("Form", u"\ud300", None))
        self.ra_team_1.setText(QCoreApplication.translate("Form", u"1\ud300", None))
        self.ra_team_2.setText(QCoreApplication.translate("Form", u"2\ud300", None))
        self.ra_team_3.setText(QCoreApplication.translate("Form", u"3\ud300", None))
        self.ra_team_4.setText(QCoreApplication.translate("Form", u"4\ud300", None))
        self.groupBox_rank.setTitle(QCoreApplication.translate("Form", u"\uacc4\uae09", None))
        self.ra_rank_1.setText(QCoreApplication.translate("Form", u"\uc21c\uacbd", None))
        self.ra_rank_2.setText(QCoreApplication.translate("Form", u"\uacbd\uc7a5", None))
        self.ra_rank_3.setText(QCoreApplication.translate("Form", u"\uacbd\uc0ac", None))
        self.ra_rank_4.setText(QCoreApplication.translate("Form", u"\uacbd\uc704", None))
        self.ra_rank_5.setText(QCoreApplication.translate("Form", u"\uacbd\uac10", None))
        self.label_name.setText(QCoreApplication.translate("Form", u"\uc774\ub984", None))
        self.groupBox_files.setTitle(QCoreApplication.translate("Form", u"\ud30c\uc77c \ub4f1\ub85d(2\uac1c)", None))
        self.btn_sagun.setText(QCoreApplication.translate("Form", u"\uc0ac\uac74\uac80\uc0c9\ub9ac\uc2a4\ud2b8", None))
        self.btn_individual.setText(QCoreApplication.translate("Form", u"\uac1c\uc778\ubcc4 \ucd9c\ub3d9\uc218\ub2f9 \ud30c\uc77c", None))
        self.checkBox_dongil.setText(QCoreApplication.translate("Form", u"\ub3d9\uc77c\uac74 \uc81c\uc678", None))
        self.checkBox_ftx.setText(QCoreApplication.translate("Form", u"FTX \uc81c\uc678", None))
        self.groupBox_points.setTitle(QCoreApplication.translate("Form", u"\ubc84\ud2bc \uc88c\ud45c \uc785\ub825", None))
        self.btn_point_2.setText(QCoreApplication.translate("Form", u"?? \uc88c\ud45c \uc785\ub825", None))
        self.label_point2.setText(QCoreApplication.translate("Form", u"(654, 255)", None))
        self.btn_point_1.setText(QCoreApplication.translate("Form", u"?? \uc88c\ud45c \uc785\ub825", None))
        self.label_point1.setText(QCoreApplication.translate("Form", u"(224, 255)", None))
        self.btn_make_df.setText(QCoreApplication.translate("Form", u"\uc815\ub9ac", None))
        self.btn_del.setText(QCoreApplication.translate("Form", u"\uc120\ud0dd \ud589 \uc0ad\uc81c(del)", None))
        self.btn_run.setText(QCoreApplication.translate("Form", u"hwp \ucd9c\ub825", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\ub9e4\ud06c\ub85c \uc2e4\ud589", None))
    # retranslateUi


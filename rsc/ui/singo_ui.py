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
    QRadioButton, QSizePolicy, QVBoxLayout, QWidget)

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
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 0, 371, 571))
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

        self.groupBox_team = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_team.setObjectName(u"groupBox_team")
        self.groupBox_team.setMinimumSize(QSize(0, 50))
        self.horizontalLayoutWidget_2 = QWidget(self.groupBox_team)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 20, 341, 21))
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
        self.groupBox_rank.setMinimumSize(QSize(0, 50))
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

        self.groupBox = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 50))
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(50, 20, 265, 24))

        self.verticalLayout_10.addWidget(self.groupBox)

        self.groupBox_files = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_files.setObjectName(u"groupBox_files")
        self.groupBox_files.setMinimumSize(QSize(0, 60))
        self.layoutWidget = QWidget(self.groupBox_files)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 331, 30))
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

        self.groupBox_2 = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 55))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 20, 331, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 3, 0, 0)
        self.checkBox_dongil = QCheckBox(self.horizontalLayoutWidget_3)
        self.checkBox_dongil.setObjectName(u"checkBox_dongil")
        self.checkBox_dongil.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBox_dongil)

        self.checkBox_ftx = QCheckBox(self.horizontalLayoutWidget_3)
        self.checkBox_ftx.setObjectName(u"checkBox_ftx")
        self.checkBox_ftx.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBox_ftx)


        self.verticalLayout_10.addWidget(self.groupBox_2)


        self.verticalLayout_7.addLayout(self.verticalLayout_10)

        self.groupBox_points = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_points.setObjectName(u"groupBox_points")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_points.sizePolicy().hasHeightForWidth())
        self.groupBox_points.setSizePolicy(sizePolicy2)
        self.groupBox_points.setMinimumSize(QSize(0, 100))
        self.groupBox_points.setMaximumSize(QSize(16777215, 400))
        self.verticalLayoutWidget = QWidget(self.groupBox_points)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 331, 80))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_point2 = QHBoxLayout()
        self.horizontalLayout_point2.setObjectName(u"horizontalLayout_point2")
        self.btn_point_1 = QPushButton(self.verticalLayoutWidget)
        self.btn_point_1.setObjectName(u"btn_point_1")

        self.horizontalLayout_point2.addWidget(self.btn_point_1)

        self.label_point_1 = QLabel(self.verticalLayoutWidget)
        self.label_point_1.setObjectName(u"label_point_1")

        self.horizontalLayout_point2.addWidget(self.label_point_1)


        self.verticalLayout.addLayout(self.horizontalLayout_point2)

        self.horizontalLayout_point1 = QHBoxLayout()
        self.horizontalLayout_point1.setObjectName(u"horizontalLayout_point1")
        self.btn_point_2 = QPushButton(self.verticalLayoutWidget)
        self.btn_point_2.setObjectName(u"btn_point_2")

        self.horizontalLayout_point1.addWidget(self.btn_point_2)

        self.label_point_2 = QLabel(self.verticalLayoutWidget)
        self.label_point_2.setObjectName(u"label_point_2")

        self.horizontalLayout_point1.addWidget(self.label_point_2)


        self.verticalLayout.addLayout(self.horizontalLayout_point1)


        self.verticalLayout_7.addWidget(self.groupBox_points)

        self.groupBox_3 = QGroupBox(self.verticalLayoutWidget_12)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_3)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 331, 71))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_make_df = QHBoxLayout()
        self.horizontalLayout_make_df.setObjectName(u"horizontalLayout_make_df")
        self.horizontalLayout_make_df.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_make_df.setContentsMargins(10, -1, 10, -1)
        self.btn_make_df = QPushButton(self.verticalLayoutWidget_2)
        self.btn_make_df.setObjectName(u"btn_make_df")

        self.horizontalLayout_make_df.addWidget(self.btn_make_df)

        self.btn_del = QPushButton(self.verticalLayoutWidget_2)
        self.btn_del.setObjectName(u"btn_del")

        self.horizontalLayout_make_df.addWidget(self.btn_del)

        self.btn_hwp = QPushButton(self.verticalLayoutWidget_2)
        self.btn_hwp.setObjectName(u"btn_hwp")

        self.horizontalLayout_make_df.addWidget(self.btn_hwp)


        self.verticalLayout_2.addLayout(self.horizontalLayout_make_df)

        self.btn_macro = QPushButton(self.verticalLayoutWidget_2)
        self.btn_macro.setObjectName(u"btn_macro")

        self.verticalLayout_2.addWidget(self.btn_macro)


        self.verticalLayout_7.addWidget(self.groupBox_3)


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
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\uc774\ub984", None))
        self.groupBox_files.setTitle(QCoreApplication.translate("Form", u"\ud30c\uc77c \ub4f1\ub85d(2\uac1c)", None))
        self.btn_sagun.setText(QCoreApplication.translate("Form", u"\uc0ac\uac74\uac80\uc0c9\ub9ac\uc2a4\ud2b8", None))
        self.btn_individual.setText(QCoreApplication.translate("Form", u"\uac1c\uc778\ubcc4 \ucd9c\ub3d9\uc218\ub2f9 \ud30c\uc77c", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\ud544\ud130\ub9c1 \uc635\uc158", None))
        self.checkBox_dongil.setText(QCoreApplication.translate("Form", u"\ub3d9\uc77c\uac74 \uc81c\uc678", None))
        self.checkBox_ftx.setText(QCoreApplication.translate("Form", u"FTX \uc81c\uc678", None))
        self.groupBox_points.setTitle(QCoreApplication.translate("Form", u"\ubc84\ud2bc \uc88c\ud45c \uc785\ub825", None))
        self.btn_point_1.setText(QCoreApplication.translate("Form", u"'\uc784\uc758\ub4f1\ub85d' \uc88c\ud45c", None))
        self.label_point_1.setText(QCoreApplication.translate("Form", u"(654, 255)", None))
        self.btn_point_2.setText(QCoreApplication.translate("Form", u"'\uc811\uc218\ubc88\ud638' \uc88c\ud45c", None))
        self.label_point_2.setText(QCoreApplication.translate("Form", u"(224, 255)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\ucee8\ud2b8\ub864", None))
        self.btn_make_df.setText(QCoreApplication.translate("Form", u"\uc815\ub9ac", None))
        self.btn_del.setText(QCoreApplication.translate("Form", u"\ud589 \uc0ad\uc81c(del)", None))
        self.btn_hwp.setText(QCoreApplication.translate("Form", u"hwp \ucd9c\ub825", None))
        self.btn_macro.setText(QCoreApplication.translate("Form", u"\ub9e4\ud06c\ub85c \uc2e4\ud589", None))
    # retranslateUi


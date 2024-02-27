# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExcelIcon.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(100, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(100, 120))
        self.label_icon = QLabel(Form)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setEnabled(True)
        self.label_icon.setGeometry(QRect(10, 10, 85, 85))
        self.label_icon.setPixmap(QPixmap(u"icons/xls-file.png"))
        self.label_icon.setScaledContents(True)
        self.label_fn = QLabel(Form)
        self.label_fn.setObjectName(u"label_fn")
        self.label_fn.setGeometry(QRect(18, 100, 71, 20))
        self.label_fn.setTextFormat(Qt.AutoText)
        self.label_fn.setScaledContents(False)
        self.label_fn.setAlignment(Qt.AlignCenter)
        self.label_x = QLabel(Form)
        self.label_x.setObjectName(u"label_x")
        self.label_x.setEnabled(True)
        self.label_x.setGeometry(QRect(30, 30, 51, 51))
        self.label_x.setMouseTracking(False)
        self.label_x.setPixmap(QPixmap(u"icons/red2.png"))
        self.label_x.setScaledContents(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_icon.setText("")
        self.label_fn.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_x.setText("")
    # retranslateUi


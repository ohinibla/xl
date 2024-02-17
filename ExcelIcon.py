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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_frame_icon(object):
    def setupUi(self, frame_icon):
        if not frame_icon.objectName():
            frame_icon.setObjectName(u"frame_icon")
        frame_icon.resize(102, 125)
        self.label_excel_icon = QLabel(frame_icon)
        self.label_excel_icon.setObjectName(u"label_excel_icon")
        self.label_excel_icon.setGeometry(QRect(2, 13, 75, 75))
        self.label_excel_icon.setPixmap(QPixmap(u"../xl/icons/xls-file.png"))
        self.label_excel_icon.setScaledContents(True)
        self.label_redx_icon = QLabel(frame_icon)
        self.label_redx_icon.setObjectName(u"label_redx_icon")
        self.label_redx_icon.setGeometry(QRect(56, 1, 25, 25))
        self.label_redx_icon.setPixmap(QPixmap(u"../xl/icons/red2.png"))
        self.label_redx_icon.setScaledContents(True)
        self.label_file_name = QLabel(frame_icon)
        self.label_file_name.setObjectName(u"label_file_name")
        self.label_file_name.setGeometry(QRect(7, 93, 70, 18))

        self.retranslateUi(frame_icon)

        QMetaObject.connectSlotsByName(frame_icon)
    # setupUi

    def retranslateUi(self, frame_icon):
        frame_icon.setWindowTitle(QCoreApplication.translate("frame_icon", u"Frame", None))
        self.label_excel_icon.setText("")
        self.label_redx_icon.setText("")
        self.label_file_name.setText(QCoreApplication.translate("frame_icon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">file_name</span></p></body></html>", None))
    # retranslateUi


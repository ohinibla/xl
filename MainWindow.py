# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setGeometry(QRect(9, 9, 781, 471))
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.frame_side = QFrame(self.frame_main)
        self.frame_side.setObjectName(u"frame_side")
        self.frame_side.setGeometry(QRect(11, 11, 211, 451))
        self.frame_side.setFrameShape(QFrame.Box)
        self.frame_side.setFrameShadow(QFrame.Raised)
        self.switch_find_duplicates = QCheckBox(self.frame_side)
        self.switch_find_duplicates.setObjectName(u"switch_find_duplicates")
        self.switch_find_duplicates.setGeometry(QRect(26, 160, 127, 28))
        self.switch_save_files = QCheckBox(self.frame_side)
        self.switch_save_files.setObjectName(u"switch_save_files")
        self.switch_save_files.setGeometry(QRect(26, 200, 90, 28))
        self.btn_exit = QPushButton(self.frame_side)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(20, 390, 171, 34))
        self.btn_exit.setMinimumSize(QSize(84, 0))
        self.btn_exit.setMaximumSize(QSize(16777215, 34))
        self.btn_find_duplicates = QPushButton(self.frame_side)
        self.btn_find_duplicates.setObjectName(u"btn_find_duplicates")
        self.btn_find_duplicates.setGeometry(QRect(20, 50, 171, 34))
        self.btn_find_duplicates.setMinimumSize(QSize(84, 0))
        self.btn_find_duplicates.setMaximumSize(QSize(16777215, 34))
        self.frame_main_file = QFrame(self.frame_main)
        self.frame_main_file.setObjectName(u"frame_main_file")
        self.frame_main_file.setGeometry(QRect(229, 11, 541, 449))
        self.frame_main_file.setFrameShape(QFrame.Box)
        self.frame_main_file.setFrameShadow(QFrame.Raised)
        self.grp_open_files = QGroupBox(self.frame_main_file)
        self.grp_open_files.setObjectName(u"grp_open_files")
        self.grp_open_files.setGeometry(QRect(10, 20, 521, 401))
        self.btn_open_files = QPushButton(self.grp_open_files)
        self.btn_open_files.setObjectName(u"btn_open_files")
        self.btn_open_files.setGeometry(QRect(427, 30, 84, 34))
        self.entry_filename = QLineEdit(self.grp_open_files)
        self.entry_filename.setObjectName(u"entry_filename")
        self.entry_filename.setGeometry(QRect(10, 32, 400, 28))
        self.entry_filename.setReadOnly(True)
        self.scrollArea = QScrollArea(self.grp_open_files)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(30, 80, 471, 301))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 469, 299))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.frame_info = QFrame(self.centralwidget)
        self.frame_info.setObjectName(u"frame_info")
        self.frame_info.setGeometry(QRect(9, 487, 782, 51))
        self.frame_info.setFrameShape(QFrame.Box)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.progressBar = QProgressBar(self.frame_info)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(50, 14, 681, 23))
        self.progressBar.setValue(50)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 18))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.btn_exit.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.switch_find_duplicates.setText(QCoreApplication.translate("MainWindow", u"Save Duplicates", None))
        self.switch_save_files.setText(QCoreApplication.translate("MainWindow", u"Save Files", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.btn_find_duplicates.setText(QCoreApplication.translate("MainWindow", u"Find Duplicates", None))
        self.grp_open_files.setTitle(QCoreApplication.translate("MainWindow", u"Select files:", None))
        self.btn_open_files.setText(QCoreApplication.translate("MainWindow", u"Open Files", None))
        self.entry_filename.setText("")
        self.entry_filename.setPlaceholderText(QCoreApplication.translate("MainWindow", u"...", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi


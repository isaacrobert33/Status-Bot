# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appwaJazU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(682, 506)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 691, 511))
        self.frame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(30, 30, 47);\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.textBrowser = QTextBrowser(self.frame)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(80, 30, 521, 351))
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet(u"font: 8pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.user_input = QLineEdit(self.frame)
        self.user_input.setObjectName(u"user_input")
        self.user_input.setGeometry(QRect(210, 400, 241, 31))
        self.user_input.setStyleSheet(u"QLineEdit {\n"
"	border-radius: 8px;\n"
"}")
        self.start_btn = QPushButton(self.frame)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(290, 440, 93, 28))
        font1 = QFont()
        font1.setBold(True)
        font1.setWeight(75)
        self.start_btn.setFont(font1)
        self.start_btn.setStyleSheet(u"border-radius: 6px;\n"
"background-color: rgb(26, 140, 68);\n"
"color: rgb(255, 255, 255);")
        self.start_btn.setFlat(False)
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 490, 691, 21))
        self.widget.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.status = QLabel(self.widget)
        self.status.setObjectName(u"status")
        self.status.setGeometry(QRect(0, 0, 671, 16))
        font2 = QFont()
        font2.setFamily(u"Courier")
        font2.setPointSize(8)
        self.status.setFont(font2)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 20, 221, 21))
        font3 = QFont()
        font3.setFamily(u"Baskerville Old Face")
        font3.setPointSize(8)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setWeight(50)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 8pt \"Baskerville Old Face\";\n"
"background-color: rgb(30, 30, 47);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.status.setText(QCoreApplication.translate("MainWindow", u"Click START to begin a task!", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">WEB AUTOMATOR</span></p></body></html>", None))
    # retranslateUi


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'web_watcher.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 266)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 100, 151, 81))
        self.pushButton.setObjectName("pushButton")
        self.url = QtWidgets.QLineEdit(self.centralwidget)
        self.url.setGeometry(QtCore.QRect(50, 50, 681, 41))
        self.url.setObjectName("url")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 110, 111, 31))
        self.label_2.setObjectName("label_2")
        self.rb_10m = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_10m.setGeometry(QtCore.QRect(50, 150, 108, 19))
        self.rb_10m.setObjectName("rb_10m")
        self.rb_5m = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_5m.setGeometry(QtCore.QRect(140, 150, 108, 19))
        self.rb_5m.setObjectName("rb_5m")
        self.rb_1m = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_1m.setGeometry(QtCore.QRect(210, 150, 108, 19))
        self.rb_1m.setObjectName("rb_1m")
        self.lbl_print = QtWidgets.QLabel(self.centralwidget)
        self.lbl_print.setGeometry(QtCore.QRect(120, 190, 551, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_print.setFont(font)
        self.lbl_print.setText("")
        self.lbl_print.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_print.setObjectName("lbl_print")
        self.rb_30s = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_30s.setGeometry(QtCore.QRect(290, 150, 108, 19))
        self.rb_30s.setObjectName("rb_30s")
        self.rb_5s = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_5s.setGeometry(QtCore.QRect(370, 150, 108, 19))
        self.rb_5s.setObjectName("rb_5s")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 100, 151, 81))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.rb_10m.clicked.connect(MainWindow.setCycle)
        self.pushButton.clicked.connect(MainWindow.startChk)
        self.rb_5m.clicked.connect(MainWindow.setCycle)
        self.rb_1m.clicked.connect(MainWindow.setCycle)
        self.rb_30s.clicked.connect(MainWindow.setCycle)
        self.rb_5s.clicked.connect(MainWindow.setCycle)
        self.pushButton_2.clicked.connect(MainWindow.stopChk)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "웹감지툴"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "URL 입력 상자"))
        self.label_2.setText(_translate("MainWindow", "옵션선택"))
        self.rb_10m.setText(_translate("MainWindow", "10분"))
        self.rb_5m.setText(_translate("MainWindow", "5분"))
        self.rb_1m.setText(_translate("MainWindow", "1분"))
        self.rb_30s.setText(_translate("MainWindow", "30초"))
        self.rb_5s.setText(_translate("MainWindow", "5초"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


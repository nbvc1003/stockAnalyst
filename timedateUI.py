# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timedateUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(599, 311)
        self.btnNow = QtWidgets.QPushButton(Form)
        self.btnNow.setGeometry(QtCore.QRect(390, 40, 181, 111))
        self.btnNow.setObjectName("btnNow")
        self.timeEdit = QtWidgets.QTimeEdit(Form)
        self.timeEdit.setGeometry(QtCore.QRect(40, 40, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(40, 80, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit.setGeometry(QtCore.QRect(40, 130, 194, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(50, 260, 501, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.btnTime = QtWidgets.QPushButton(Form)
        self.btnTime.setGeometry(QtCore.QRect(30, 180, 93, 28))
        self.btnTime.setObjectName("btnTime")
        self.btnDate = QtWidgets.QPushButton(Form)
        self.btnDate.setGeometry(QtCore.QRect(150, 180, 93, 28))
        self.btnDate.setObjectName("btnDate")
        self.btnAll = QtWidgets.QPushButton(Form)
        self.btnAll.setGeometry(QtCore.QRect(280, 180, 93, 28))
        self.btnAll.setObjectName("btnAll")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnNow.setText(_translate("Form", "현재날짜/시간 지정"))
        self.btnTime.setText(_translate("Form", "시간적용"))
        self.btnDate.setText(_translate("Form", "날짜적용"))
        self.btnAll.setText(_translate("Form", "둘다적용"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


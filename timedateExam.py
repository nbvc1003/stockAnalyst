import sys, datetime
from testPackage.timedateUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication

# pyuic5 -x 파일명.ui -o 출력명.py


class Main(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnNow.clicked.connect(self.now)
        self.btnTime.clicked.connect(self.time)
        self.btnDate.clicked.connect(self.date)
        self.btnAll.clicked.connect(self.all)

    def now(self):
        now = datetime.datetime.now()
        self.dateTimeEdit.setDateTime(now)
        self.dateEdit.setDate(datetime.date(2019, 4 ,5))

    def time(self):
        now = datetime.datetime.now()
        self.lineEdit.setText(now.strftime("%H:%M:%S"))

    def date(self):
        now = datetime.datetime.now()
        self.lineEdit.setText(now.strftime("%Y-%m-%d"))
    def all(self):
        now = datetime.datetime.now()
        self.lineEdit.setText(now.strftime("%Y-%m-%d %H:%M:%S"))


app = QApplication([])
ex = Main()
ex.show()
sys.exit(app.exec_())
import sys, datetime
from examples.timedateUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



# pyuic5 -x 파일명.ui -o 출력명.py


class Main(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnNow.clicked.connect(self.now)
        self.btnTime.clicked.connect(self.time)
        self.btnDate.clicked.connect(self.date)
        self.btnAll.clicked.connect(self.all)

        self.TestPlot()

    def TestPlot(self):
        N = 5
        value = (20, 30, 30, 35, 25)
        ind = np.arange(N)
        width = 0.35

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.bar(ind, value, width)
        ax.set_xticklabels(['G1','G2','G3','G4','G5'])

        canvas = FigureCanvas(fig)
        canvas.draw()

        lay = QHBoxLayout()
        self.setLayout(lay)
        lay.addWidget(canvas)
        canvas.show()



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
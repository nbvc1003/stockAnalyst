import random, sys
import matplotlib.pyplot as plt
from datetime import date, timedelta

from PyQt5.uic.properties import QtWidgets, QtCore
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import uic

from examples.testMainUI import Ui_MainWindow
MainUI = "../UI/testMainUI.ui"

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # uic.loadUi(MainUI,self)# .ui 직접로드
        self.setupUi(self) # .py 로드

        self.iniUI()
        self.mainState = 0
        self.setUI()


    def iniUI(self):

        value = (20, 30, 30, 35, 25)
        ind = [1,2,3,4,5]
        width = 0.35

        fig = plt.Figure()
        self.ax = fig.add_subplot(111)
        self.ax.bar(ind, value, width)

        canvas = FigureCanvas(fig)
        canvas.draw()

        lay = QHBoxLayout()
        self.setLayout(lay)
        lay.addWidget(canvas)

        canvas.show()

#===============================================================================

    def setUI(self):
        now = date.today()
        print(type(now ))
        self.dateEdit.setDate(date.today() + timedelta(days=-30))
        #time2 + timedelta(days=-3)
        self.dateEdit_2.setDate(date.today() )

        self.btn_start.setEnabled(True)
        self.lineEdit_1.setText('AMD')
        self.lineEdit_2.setText('AAPL')
        self.lineEdit_1.setFocus()

        # connect 방식으로 함수를 연결할때 인자를 사용할수 없기때문에
        # 중간에 람다함수를 사용하여 인자를 전달하도록 작성한다.
        # 이때 clicked 함수에서 리턴되는 값이 2개 이므로 값2개를 받고 그중 button객체만 전달하면 된다.
        # 필요하다면 state변수도 전달 한다.
        self.btn_start.clicked.connect(lambda state, button = self.btn_start : self.btnTest(state, button))

        ## UI slots

    def aStart(self):

        self.btn_start.setEnabled(False)
        self.lineEdit_1.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

        print(self.lineEdit_1.text())
        print(self.lineEdit_2.text())

        input1 = self.lineEdit_1.text()
        input2 = self.lineEdit_2.text()

        # d = date.today()
        # start = date(2019, 1, 1)
        # end = date(d.year, d.month, d.day)

        qstart = self.dateEdit.date()
        start = qstart.toPyDate()

        qend = self.dateEdit_2.date()
        end = qend.toPyDate()

        if (input1, input2 != None) and (len(input1) > 0 and len(input2) > 0):
            self.inputData(input1, input2, start, end)
        else:
            print('입력코드값 오류')

    def cancel(self):
        self.btn_start.setEnabled(True)
        self.lineEdit_1.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_1.setText('AMD')
        self.lineEdit_2.setText('AAPL')
        self.lineEdit_1.setFocus()
        self.m.plotClear()

    def inputData(self, targetStockCode, compStockCode, start, end ):
        print('inputData')
        if targetStockCode == None :
            targetStockCode = 'AMD'

        if compStockCode == None :
            compStockCode = 'AAPL'
        try:
            targetStock_df = data.DataReader(targetStockCode, "yahoo", start, end)  # start ~ end 까지
            compStock_df = data.DataReader(compStockCode, "yahoo", start, end)  # start ~ end 까지
        except RemoteDataError as ede:
            self.textEdit_info.append('애러발생 {}'.format(ede))
            print('애러발생 {}'.format(ede))
            return
        except Exception as err:
            print(type(err))
            return

        if  targetStock_df is None or compStock_df is None:
            self.textEdit_info.append('오류발생 !!!!!')
            return

        tsd = targetStock_df['Close']
        csd = compStock_df['Close']
        #===================================================================================
        ## from scipy import stats 사용할경우
        # slope, intersecept, r_value, p_value, stderr = stats.linregress(tsd, csd)
        # ConsolePrint(slope, intersecept, r_value, p_value)
        # MPlot(plt, tsd, csd, slope, intersecept)
        # print(tsd, type(tsd))
        # ry = polyval([slope, intersecept], tsd)
        # print(targetStock_df['Close'])
        #========================================================================

        # print('tsd',tsd)
        # print('csd',csd)

        if len(tsd) != len(csd):
            self.textEdit_info.append('데이터의 길이가 다릅니다. !!!!!')
            return


        corr = tsd.corr(csd)
        print('corr:',corr)

        self.textEdit_info.append('종목:{}/{}'.format(targetStockCode,compStockCode ))
        self.textEdit_info.append('기간:{}/{}'.format(start, end))
        if corr > 0:
            self.textEdit_info.append('상관관계 : {}'.format(corr))

        # self.plot(list(tsd), list(csd), markup='k.')

    def plot(self, *data, markup=None, title='NoTitle', legend=None, xLabel=None, yLabel=None):
        if len(data) == 0:
            data = [random.random() for i in range(25)]
        if markup is None:
            markup = 'k.'
        # ax = self.figure.add_subplot(111)
        plt.plot(data[0], data[1], markup)
        self.ax.plot(data[0], data[1], markup)
        plt.title(title)

        if legend != None and len(legend) > 0:
            plt.legend(['11', '22'])

        plt.show()





app = QApplication([])
ex = Main()
ex.show()
sys.exit(app.exec_())
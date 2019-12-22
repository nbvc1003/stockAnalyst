from datetime import date, timedelta

# from PyQt5.QtCore import QDate
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from numpy import polyval
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from scipy import stats
import random, sys
# import statsmodels.formula.api as sm
from PyQt5 import uic

# MainUI = "../UI/testMainUI.ui"

## 메인 클래스
from old.testMainUI import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
# class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        # uic.loadUi(MainUI,self)

        self.setupUi(self)
        self.iniUI()
        self.mainState = 0

        self.setUI()

    def iniUI(self):
        self.m = PlotCanvas(self, width=5, height=4)
        self.m.move(20, 200)
        self.show()

    # 콜솔 출력부프린트
    def ConsolePrint(slope=0, intersecept=0, r_value=0, p_value=0):
        print('기울기 :', slope)
        print('절편 :', intersecept)
        print('상관계수 :', r_value)
        print('유의수준 :', p_value)

    # 그래프 출력부
    def MPlot(plt, tsd , csd, slope, intersecept):
        # print(tsd , csd, slope, intersecept)
        ry = polyval([slope, intersecept], tsd)
        plt.plot(tsd, csd, 'k.')
        plt.plot(tsd, ry, 'r')
        # plt.title('{}/{}'.format(targetStockCode, compStockCode))
        # plt.xlabel(targetStockCode)
        # plt.ylabel(compStockCode)
        # plt.legend(['price', 'polyval'])
        # plt.show()

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

        if (input1 ,input2 != None) and (len(input1) > 0 and len(input2) > 0):
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

        self.m.plot(list(tsd), list(csd), markup='k.')
        # self.m.plot(tsd, ry, markup='r')


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
###
    def plot(self, *data, markup = None, title = 'NoTitle', legend = None,  xLabel = None, yLabel = None):
        if len(data) == 0:
            data = [random.random() for i in range(25)]
        if markup is None:
            markup = 'k.'
        # ax = self.figure.add_subplot(111)
        self.ax.plot(data[0], data[1], markup)
        self.ax.set_title(title)

        if legend != None and len(legend) > 0 :
            self.ax.legend(['11','22'])

        self.draw()

    def plotClear(self):

        self.ax.set_title("NoTitle")

        self.draw()


app = QApplication([])
ex = Main()
# ex.show()
sys.exit(app.exec_())

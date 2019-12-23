from datetime import date, timedelta
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
# import numpy as np
# from numpy import polyval
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from scipy import stats
import random, sys
import pandas as pd
# import statsmodels.formula.api as sm
from PyQt5 import uic

MainUI = "../UI/testMainUI.ui"

## 메인 클래스
# class Main(QMainWindow, Ui_MainWindow): 
class Main(QMainWindow): #  ui파일로 로드 하는 방식
    def __init__(self):
        super().__init__()

        uic.loadUi(MainUI,self)
        # self.setupUi(self)
        self.iniUI()
        self.mainState = 0
        self.setUI()


    def iniUI(self):
        self.m = PlotCanvas(self)
        self.m.move(20, 280) # 초기 위치 설정
        # self.show()


#===============================================================================

    def setUI(self):

        print(date.today())
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
        # self.btn_start.clicked.connect(lambda state, button = self.btn_start : self.btnTest(state, button))

    def btnTest(self,state, btn):
        print(state, type(state))
        print(btn)
        print('btn test')

## UI slots
    ## start 버튼
    def aStart(self):

        self.btn_start.setEnabled(False)
        self.lineEdit_1.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

        print(self.lineEdit_1.text())
        print(self.lineEdit_2.text())

        input1 = self.lineEdit_1.text()
        input2 = self.lineEdit_2.text()
        self.lineEdit_1.setText(input1.upper())
        self.lineEdit_2.setText(input2.upper())

        qstart = self.dateEdit.date()
        start = qstart.toPyDate()

        qend = self.dateEdit_2.date()
        end = qend.toPyDate()

        if (input1 ,input2 != None) and (len(input1) > 0 and len(input2) > 0):
            self.inputData(input1, input2, start, end)
        else:
            print('입력코드값 오류')

    # 취소버튼
    def cancel(self):

        self.dateEdit.setDate(date.today() + timedelta(days=-30))
        self.dateEdit_2.setDate(date.today() )

        self.btn_start.setEnabled(True)
        self.lineEdit_1.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        # self.lineEdit_1.setText('AMD')
        # self.lineEdit_2.setText('AAPL')
        self.lineEdit_1.setFocus()
        self.m.plotClear()



    def inputData(self, targetStockCode, compStockCode, start, end ):
        print('inputData targetStockCode :', targetStockCode,  compStockCode)

        # 코드 채크
        if targetStockCode == None :
            targetStockCode = 'AMD'

        if compStockCode == None :
            compStockCode = 'AAPL'

        # 날짜 채크
        if end > date.today():
            end = date.today()
            self.dateEdit_2.setDate(date.today())

        if start > end:
            print("날짜 입력 오류 !!!")
            self.dateEdit.setDate(date.today() + timedelta(days=-30))
            self.dateEdit_2.setDate(date.today())
            return

        self.textEdit_info.append("=============================================")

        try:
            targetStock_df = data.DataReader(targetStockCode, "yahoo", start, end)  # start ~ end 까지
            compStock_df = data.DataReader(compStockCode, "yahoo", start, end)  # start ~ end 까지

        except RemoteDataError as ede:
            self.textEdit_info.append('애러발생 {}'.format(ede))
            print('애러발생 1{}'.format(ede))
            return
        except Exception as err:
            self.textEdit_info.append('애러발생 {}'.format(err))
            print('애러발생 2{}'.format(err))
            return

        if  targetStock_df is None or compStock_df is None:
            self.textEdit_info.append('오류발생 !!!!!')
            return
        #
        # print(targetStock_df)
        # print(compStock_df)
        print(targetStock_df.size)
        print(compStock_df.size)
        

        tsd = targetStock_df['Close']
        csd = compStock_df['Close']

        #가져온 데이터의 길이가 다르면
        if tsd.size > csd.size:
            csd = pd.merge(tsd, csd, on='Date', how='outer')
            csd = csd['Close_y']
        elif tsd.size < csd.size:
            tsd = pd.merge(csd, tsd, on='Date', how='outer')
            tsd = tsd['Close_y']

        print("2",tsd.size)
        print("2",csd.size)




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

        if len(tsd) < 1:
            self.textEdit_info.append(targetStockCode +' 종목 정보를 가져오지 못했습니다.')
            return
        if len(csd) < 1:
            self.textEdit_info.append(compStockCode +' 종목 정보를 가져오지 못했습니다.')
            return
        if len(tsd) != len(csd):
            self.textEdit_info.append(  '데이터의 길이가 다릅니다. !!!!! {} / {}'.format(len(tsd), len(csd))  )
            return


        tsd.fillna(method='bfill')
        csd.fillna(method='bfill')

        if tsd.isnull().values.any():
            tsd = tsd.fillna(0)
        if csd.isnull().values.any():
            csd = csd.fillna(0)


        print(tsd)
        print(csd)


        corr = tsd.corr(csd)
        print('corr:',corr)

        title = '{} / {}'.format(targetStockCode,compStockCode )
        self.textEdit_info.append("종목: "+ title)
        # print((end - start).days, self.lbl_prierd.)
        self.lbl_prierd.setText(str((end - start).days) + "days")
        # self.lbl_prierd.setText((end - start).days)
        self.textEdit_info.append('기간:{} ~ {}'.format(start, end))
        self.textEdit_info.append('상관관계 : {}'.format(corr))



        self.m.plot(list(tsd), list(csd),title=title,  markup='k.',xlabel=targetStockCode,ylabel=compStockCode, start=start, end=end)

        # self.m.plot(tsd, ry, markup='r')


## PlotCanvas
## matplotlib 와 PyQt5 를 연동하는 클래스
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)

    def plot(self, *data, markup = None, title = '', xlabel='', ylabel='', start=None, end=None):

        if len(data) == 0:
            print('data len is 0 !!!!!!!')
            data = [random.random() for i in range(25)]
        if markup is None:
            markup = 'k.'

        self.ax.plot(data[0], data[1], markup)
        titleplus = title + ' ({} ~ {})'.format(start, end)
        self.ax.set_title(titleplus)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.draw()

    def plotClear(self):
        self.ax.cla()
        self.draw()


app = QApplication([])
ex = Main()
ex.show()
sys.exit(app.exec_())

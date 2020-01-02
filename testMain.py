from datetime import date, timedelta
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import numpy as np
from numpy import polyval
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QMessageBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# from scipy import stats
import random, sys
import pandas as pd
# import statsmodels.formula.api as sm
from PyQt5 import uic
## local modules
import modules.tableWidget
import modules.dataLoader as md

MainUI = "UI/testMainUI.ui"
LINE_EDIT_1 = 0
LINE_EDIT_2 = 1

from UI.testMainUI import Ui_StockAnlyst
## 메인 클래스
class Main(QMainWindow, Ui_StockAnlyst):
# class Main(QMainWindow):  # ui파일로 로드 하는 방식
    def __init__(self):
        super().__init__()

        # uic.loadUi(MainUI, self)
        self.setupUi(self)

        self.iniUI()
        self.setWindowTitle('금융상품분석툴')

        menubar = self.menuBar()

        helpMenu = menubar.addMenu('Help')

        aboutButton = QAction('About', self)
        aboutButton.triggered.connect(self.aboutMsg)
        helpMenu.addAction(aboutButton)

        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        helpMenu.addAction(exitButton)

        self.statusBar().showMessage('빅데이터 분석 2차 프로젝트 1조 2020.1.3')
        self.setUI()


    def iniUI(self):
        self.m = PlotCanvas(self)
        # self.m = modules.plotCanvas.PlotCanvas(self)
        self.m.move(30, 290)  # 초기 위치 설정

        self.rb_1m.clicked.connect(self.rbtn_setPeriod)
        self.rb_3m.clicked.connect(self.rbtn_setPeriod)
        self.rb_6m.clicked.connect(self.rbtn_setPeriod)
        self.rb_1y.clicked.connect(self.rbtn_setPeriod)
        self.rb_2y.clicked.connect(self.rbtn_setPeriod)

        self.btn_more1.clicked.connect(self.btnMore1)
        self.btn_more2.clicked.connect(self.btnMore2)

        self.btn_resultClear.clicked.connect(self.btnResultClear)
        self.btn_save.clicked.connect(self.btnResultSave)
        # self.stockName1 = ''
        # self.stockName2 = ''

        # self.lbl_prierd.clicked.connect(self.btnMore2)

        # self.show()

    # ===============================================================================

    def setLineEditValue(self, code , opt, cat, name):
        # print('name :', name)
        if cat == 'kospi':
            code = code + '.KS'
        elif cat == 'kosdaq':
            code = code + '.KQ'

        if opt == LINE_EDIT_1:
            self.lineEdit_1.setText(code)
            # self.stockName1 = name
        elif opt == LINE_EDIT_2:
            self.lineEdit_2.setText(code)
            # self.stockName2 = name

    # ===============================================================================

    def setUI(self):

        print(date.today())
        self.dateEdit.setDate(date.today() + timedelta(days=-30))
        # time2 + timedelta(days=-3)
        self.dateEdit_2.setDate(date.today())

        self.btn_start.setEnabled(True)
        self.lineEdit_1.setText('AMD')
        self.lineEdit_2.setText('AAPL')
        self.lineEdit_1.setFocus()

        # connect 방식으로 함수를 연결할때 인자를 사용할수 없기때문에
        # 중간에 람다함수를 사용하여 인자를 전달하도록 작성한다.
        # 이때 clicked 함수에서 리턴되는 값이 2개 이므로 값2개를 받고 그중 button객체만 전달하면 된다.
        # 필요하다면 state변수도 전달 한다.
        # self.btn_start.clicked.connect(lambda state, button = self.btn_start : self.btnTest(state, button))

    def btnTest(self, state, btn):
        print(state, type(state))
        print(btn)
        print('btn test')

    ## UI slots
    ## start 버튼
    def aStart(self):

        # 입력 ui 비활성화
        self.btn_start.setEnabled(False)
        self.lineEdit_1.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

        # print(self.lineEdit_1.text())
        # print(self.lineEdit_2.text())

        # 소문자 대문자로
        input1 = self.lineEdit_1.text()
        input2 = self.lineEdit_2.text()
        input1 = input1.upper()
        input2 = input2.upper()
        self.lineEdit_1.setText(input1.upper())
        self.lineEdit_2.setText(input2.upper())

        # qstart = self.dateEdit.date()
        # start = qstart.toPyDate()
        start = self.dateEdit.date().toPyDate()

        # qend = self.dateEdit_2.date()
        # end = qend.toPyDate()
        end = self.dateEdit_2.date().toPyDate()

        self.lbl_prierd.setText(str((end - start).days) + " day")

        if (input1, input2 != None) and (len(input1) > 0 and len(input2) > 0):
            self.inputData(input1, input2, start, end)
        else:
            print('입력코드값 오류')

        # test = modules.dataLoader.DataLoader()
        #
        # test.get_NameBySymbol(input1)


    # 취소버튼
    def cancel(self):

        # self.stockName1 = ''
        # self.stockName2 = ''

        self.btn_start.setEnabled(True)
        self.lineEdit_1.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_1.setFocus()
        self.m.plotClear()

        self.lbl_name1.setText('')
        self.lbl_name2.setText('')


    def rbtn_setPeriod(self):
        if self.rb_1m.isChecked():
            self.dateEdit.setDate(date.today() + timedelta(days=-30))
            self.dateEdit_2.setDate(date.today())
        elif self.rb_3m.isChecked():
            self.dateEdit.setDate(date.today() + timedelta(days=-30 * 3))
            self.dateEdit_2.setDate(date.today())
        elif self.rb_6m.isChecked():
            self.dateEdit.setDate(date.today() + timedelta(days=-30 * 6))
            self.dateEdit_2.setDate(date.today())
        elif self.rb_1y.isChecked():
            self.dateEdit.setDate(date.today() + timedelta(days=-30 * 12))
            self.dateEdit_2.setDate(date.today())
        elif self.rb_2y.isChecked():
            self.dateEdit.setDate(date.today() + timedelta(days=-30 * 24))
            self.dateEdit_2.setDate(date.today())

    def btnMore1(self):
        self.tw1 = modules.tableWidget.TableWidget(self, LINE_EDIT_1)
        self.tw1.move(self.pos())
        self.tw1.show()

    def btnMore2(self):
        self.tw2 = modules.tableWidget.TableWidget(self, LINE_EDIT_2)
        self.tw2.move(self.pos())
        self.tw2.show()

    def btnResultSave(self):
        temptxt = self.textEdit_info.toPlainText()
        self.save_dialog(temptxt)


    def btnResultClear(self):
        self.textEdit_info.clear()

    def aboutMsg(self):
        QMessageBox.about(self, "about",
                          '''
                          
프로그램명: 금융상품분석툴
제작자: nbvc
e-mail: nbvc1003@gmail.com
내용: 과제 프로젝트 산출물
버전: v 0.1.alpha
        
        ''')





    def inputData(self, targetStockCode, compStockCode, start, end):
        print('inputData targetStockCode :', targetStockCode, compStockCode)

        # 코드 채크
        if targetStockCode == None:
            targetStockCode = 'AMD'

        if compStockCode == None:
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

        self.textEdit_info.append("========================")

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

        if targetStock_df is None or compStock_df is None:
            self.textEdit_info.append('오류발생 !!!!!')
            return

        tsd = targetStock_df['Close']
        csd = compStock_df['Close']

        # 가져온 데이터의 길이가 다르면
        if tsd.size > csd.size:
            csd = pd.merge(tsd, csd, on='Date', how='outer')
            csd = csd['Close_y']
        elif tsd.size < csd.size:
            tsd = pd.merge(csd, tsd, on='Date', how='outer')
            tsd = tsd['Close_y']

        print("2", tsd.size)
        print("2", csd.size)

        if len(tsd) < 1:
            self.textEdit_info.append(targetStockCode + ' 종목 정보를 가져오지 못했습니다.')
            return
        if len(csd) < 1:
            self.textEdit_info.append(compStockCode + ' 종목 정보를 가져오지 못했습니다.')
            return

        # 데이터 길이가 다를경우 강제로 사이즈 조절
        if len(tsd) > len(csd):
            tsd = tsd[0:len(csd)]

        elif len(tsd) < len(csd):
            csd = csd[0:len(tsd)]


        tsd.fillna(method='bfill')
        csd.fillna(method='bfill')
        tsd.fillna(method='ffill')
        csd.fillna(method='ffill')

        if tsd.isnull().values.any():
            print('tsd isnull')
            tsd = tsd.fillna(tsd.mean())
        if csd.isnull().values.any():
            print('csd isnull')
            csd = csd.fillna(csd.mean())

        corr = tsd.corr(csd)
        targetName = modules.dataLoader.DataLoader.instance().get_NameBySymbol(targetStockCode)
        compName = modules.dataLoader.DataLoader.instance().get_NameBySymbol(compStockCode)
        # codes = '{} / {}'.format(targetStockCode, compStockCode)
        self.textEdit_info.append("종목: {}({})".format(targetName,targetStockCode ))
        self.textEdit_info.append("비교: {}({})".format(compName,compStockCode ))
        # self.textEdit_info.append("심볼: " + codes)
        self.textEdit_info.append('기간:{} ~ {}'.format(start, end))
        self.textEdit_info.append('상관관계 : {}'.format(corr))
        self.m.plot2(tsd, csd)

        title = '{} / {}'.format(targetStockCode, compStockCode)
        self.m.plot1(list(tsd), list(csd), title=title, markup='k.', xlabel=targetStockCode, ylabel=compStockCode,
                     start=start, end=end)

        self.lbl_name1.setText(targetName)
        self.lbl_name2.setText(compName)


    def save_dialog(self, text):
        defualtFileName = './resutText.txt'
        try:
            save_dialog = QFileDialog()
            save_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_path = save_dialog.getSaveFileName(self,  'Save as... File', defualtFileName,
                                                    filter='All Files(*.*);; Text Files(*.txt)')

            if file_path[0]:
                self.file_path = file_path
                file_open = open(self.file_path[0], 'w')
                self.file_name = (self.file_path[0].split('/'))[-1]
                self.statusBar().showMessage('Saved at: {}'.format(self.file_path[0]))
                self.setWindowTitle("{} - Notepad".format(self.file_name))
                with file_open:
                    file_open.write(text)
                    # self.need_saving(False)

        except FileNotFoundError as why:
            self.error_box(why)
            pass



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

    def plot1(self, *data, markup=None, title='', xlabel='', ylabel='', start=None, end=None):

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

    def plot2(self, xdata, ydata):

        data = np.array([xdata.values, ydata.values])
        # print('data[0]',data[0])

        # data = np.array()
        # print('data',data)
        # data[0] = xdata.values
        # data[1] = ydata.values
        # print(data)
        data = data.T
        m, n = data.shape
        # print(m, n)
        A = np.array([data[:, 0], np.ones(m)]).T
        b = data[:, 1]
        # print("A :", A)
        Q, R = self.qr_householder(A)
        b_hat = Q.T.dot(b)

        R_upper = R[:n, :]
        b_upper = b_hat[:n]

        # print(R_upper, b_upper)

        x = np.linalg.solve(R_upper, b_upper)
        slope, intercept = x

        print(slope, intercept)

        ry = polyval([slope, intercept], xdata)
        self.ax.plot(xdata, ry, 'r-')
        self.draw()

    def plotClear(self):
        self.ax.cla()
        self.draw()

    def qr_householder(self, A):
        m, n = A.shape
        Q = np.eye(m)  # Orthogonal transform so far
        R = A.copy()  # Transformed matrix so far

        for j in range(n):
            # Find H = I - beta*u*u' to put zeros below R[j,j]
            x = R[j:, j]
            normx = np.linalg.norm(x)
            rho = -np.sign(x[0])
            u1 = x[0] - rho * normx
            u = x / u1
            u[0] = 1
            beta = -rho * u1 / normx

            R[j:, :] = R[j:, :] - beta * np.outer(u, u).dot(R[j:, :])
            Q[:, j:] = Q[:, j:] - beta * Q[:, j:].dot(np.outer(u, u))

        return Q, R


app = QApplication([])
ex = Main()
ex.show()
if app.exec_() == 0:
    sys.exit()

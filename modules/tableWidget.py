import sys, re
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QPushButton, \
    QHBoxLayout, QRadioButton

class TableWidget(QWidget):

    def __init__(self, parent=None, opt=0):
        super().__init__()
        self.cPage = 0
        self.maxPage = 0
        self.pageperMax = 40
        self.table = QTableWidget()
        self.initUI()
        self.parent = parent
        self.editTab = opt


    def initUI(self):
        self.setWindowTitle('테이블팝업윈도우')
        self.setGeometry(100, 100, 400,800)

        self.createKospiTable()
        self.table.cellClicked.connect(self.updateUiCellClick)

        self.makeKospiTable()

        self.layout = QVBoxLayout()

        tab_layout = QHBoxLayout()
        self.rbtn_kospi = QRadioButton("KOSPI")
        self.rbtn_kospi.clicked.connect(self.btn_tab_kospi)
        tab_layout.addWidget(self.rbtn_kospi)

        self.rbtn_nyse = QRadioButton("NYSE")
        self.rbtn_nyse.clicked.connect(self.btn_tab_nyse)
        tab_layout.addWidget(self.rbtn_nyse)

        self.rbtn_nasdaq = QRadioButton("NSDAQ")
        self.rbtn_nasdaq.clicked.connect(self.btn_tab_nasdaq)
        tab_layout.addWidget(self.rbtn_nasdaq)
        self.rbtn_kospi.setChecked(True)


        self.layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        for text, slot in ( ("Prev Page", self.btn_page_pre), ("Next Page", self.btn_page_next)):
            button = QPushButton(text)
            btn_layout .addWidget(button)
            button.clicked.connect(slot)

        self.layout.addLayout(tab_layout)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        # self.show()

    def createKospiTable(self):
        self.df = pd.read_csv('../forExe/kospi_kosdaq_code.csv', encoding='euc-kr')
        # print(df.tail())
        print('1',len(self.df.index))

        self.df.replace(to_replace=r'\'', value='',regex=True,inplace=True)

        self.df['종목코드'] = self.df['종목코드'].dropna(axis=0)
        self.df['종목명'] = self.df['종목명'].dropna(axis=0)
        self.df['업종명'] = self.df['업종명'].dropna(axis=0)
        self.df['대분류'] = self.df['대분류'].dropna(axis=0)
        self.df = self.df[self.df['대분류'] == '주식']
        print('2', len(self.df.index))
        # for i in df.index:
        #     if df['업종명'][i] != 'KOSPI' and df['업종명'][i] != 'KOSDAQ':
        print('3', len(self.df.index))
        self.maxPage = len(self.df.index) // self.pageperMax
        self.table.setRowCount(self.pageperMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('이름','코드'))
        self.table.clearContents()

    def makeKospiTable(self):
        self.table.clearContents()
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            # print(df.columns.values.)
            # print(list(df.columns.values).index('종목명'))
            if r >= len(self.df.index):
                break

            _index = r - (self.cPage * self.pageperMax)
            # print(_index, r)
            # print(self.df.iloc[r,list(self.df.columns.values).index('종목명')])
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('종목명')]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('종목코드')]))

    def createNyseTable(self):
        self.df = pd.read_csv('../forExe/nyse_symbol.csv', encoding='utf-8')
        # print(len(self.df.index))
        for i in self.df.index:
            temp = self.df.at[i, 'Symbol']
            if '^'in temp or '.' in temp:
                self.df.drop(i, axis=0, inplace=True)

        self.df['Symbol'] = self.df['Symbol'].dropna(axis=0)
        self.df['Name'] = self.df['Name'].dropna(axis=0)
        # self.df.replace(to_replace=r'\^', value='',regex=True,inplace=True)

        # print(self.df.Symbol)
        # print(len(self.df.index))

        self.maxPage = len(self.df.index) // self.pageperMax
        self.table.setRowCount(self.pageperMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('이름','심볼'))
        self.table.clearContents()

    def makeNyseTable(self):
        self.table.clearContents()
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            if r >= len(self.df.index):
                break
            _index = r - (self.cPage * self.pageperMax)
            # print(_index, r)
            # print(self.df.iloc[r,list(self.df.columns.values).index('Symbol')])
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('Name')]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('Symbol')]))
        
    def createNasdaqTable(self):
        self.df = pd.read_csv('../forExe/nsdaq_symbol.csv', encoding='utf-8')
        for i in self.df.index:
            temp = self.df.at[i, 'Symbol']
            if '^'in temp or '.' in temp:
                self.df.drop(i, axis=0, inplace=True)

        self.df['Symbol'] = self.df['Symbol'].dropna(axis=0)
        self.df['Name'] = self.df['Name'].dropna(axis=0)

        self.maxPage = len(self.df.index) // self.pageperMax
        self.table.setRowCount(self.pageperMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('이름','심볼'))
        self.table.clearContents()

    def makeNasdaqTable(self):
        self.table.clearContents()
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            if r >= len(self.df.index):
                break
            _index = r - (self.cPage * self.pageperMax)
            # print(_index, r)
            # print(self.df.iloc[r,list(self.df.columns.values).index('Symbol')])
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('Name')]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('Symbol')]))

    def btn_tab_kospi(self):
        self.cPage = 0
        self.createKospiTable()
        self.makeKospiTable()
        pass
    def btn_tab_nyse(self):
        self.cPage = 0
        self.createNyseTable()
        self.makeNyseTable()
        pass
    def btn_tab_nasdaq(self):
        self.cPage = 0
        self.createNasdaqTable()
        self.makeNasdaqTable()

    def btn_page_pre(self):
        self.table.scrollToTop()
        if self.cPage > 0:
            self.cPage -= 1
        print('page :' , self.cPage)
        self.table.clearContents()

        if self.rbtn_kospi.isChecked():
            self.makeKospiTable()
        elif self.rbtn_nyse.isChecked():
            self.makeNyseTable()
        elif self.rbtn_nasdaq.isChecked():
            self.makeNasdaqTable()

    def btn_page_next(self):
        # self.table.scrollToBottom()
        self.table.scrollToTop()
        if self.cPage < self.maxPage:
            self.cPage += 1
        print('page :', self.cPage)
        self.table.clearContents()

        if self.rbtn_kospi.isChecked():
            self.makeKospiTable()
        elif self.rbtn_nyse.isChecked():
            self.makeNyseTable()
        elif self.rbtn_nasdaq.isChecked():
            self.makeNasdaqTable()


    def updateUiCellClick(self, r, i):
        index = r + (self.cPage * self.pageperMax)
        print(r, index)
        if self.rbtn_kospi.isChecked():
            code = self.df.iloc[index, list(self.df.columns.values).index('종목코드')]
            # code = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', code)
            # code = code[1:]
            self.parent.recivedKospiCodeSet(code, self.editTab)
        elif self.rbtn_nyse.isChecked():
            code = self.df.iloc[index, list(self.df.columns.values).index('Symbol')]
            self.parent.recivedNyseSet(code, self.editTab)
        elif self.rbtn_nasdaq.isChecked():
            code = self.df.iloc[index, list(self.df.columns.values).index('Symbol')]
            self.parent.recivedNasdatSet(code, self.editTab)




if __name__ == "__main__":
    app = QApplication([])
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())








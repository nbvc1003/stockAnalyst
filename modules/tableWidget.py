import sys, re
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QPushButton, \
    QHBoxLayout, QRadioButton

class TableWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.cPage = 0
        self.maxPage = 0
        self.pageperMax = 40
        self.table = QTableWidget()
        self.initUI()
        self.parent = parent


    def initUI(self):
        self.setWindowTitle('테이블팝업윈도우')
        self.setGeometry(100, 100, 400,800)
        self.createKospiTable()
        self.makeKospiTabke()

        self.layout = QVBoxLayout()

        tab_layout = QHBoxLayout()
        for text, slot in ( ("KOSPI", self.btn_tab_kospi), ("NYSE", self.btn_tab_nyse), ("NSDAQ", self.btn_tab_nasdaq)):
            rbtn = QRadioButton(text)
            if text == 'KOSPI':
                rbtn.setChecked(True)
            tab_layout .addWidget(rbtn)
            rbtn.clicked.connect(slot)

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

        self.table.cellClicked.connect(self.updateUiCellClick)
        self.df = pd.read_csv('../forExe/kospi_kosdaq_code.csv', encoding='euc-kr')

        # print(df.tail())
        print('1',len(self.df.index))

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

    def makeKospiTabke(self):
        self.table.clearContents()
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            # print(df.columns.values.)
            # print(list(df.columns.values).index('종목명'))
            if r >= len(self.df.index):
                break

            _index = r - (self.cPage * self.pageperMax)
            print(_index, r)
            print(self.df.iloc[r,list(self.df.columns.values).index('종목명')])
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('종목명')]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   self.df.iloc[r,list(self.df.columns.values).index('종목코드')]))

    def createNyseTable(self):
        pass
    def makeNyseTable(self):
        pass
    def createNasdaqTable(self):
        pass
    def makeNasdaqTable(self):
        pass

    def btn_tab_kospi(self):
        self.cPage = 0
        self.makeKospiTabke()
        pass
    def btn_tab_nyse(self):
        pass
    def btn_tab_nasdaq(self):
        pass


    def btn_page_pre(self):
        self.table.scrollToTop()
        if self.cPage > 0:
            self.cPage -= 1
        print('page :' , self.cPage)
        self.table.clearContents()
        self.makeKospiTabke()

    def btn_page_next(self):
        self.table.scrollToBottom()
        if self.cPage < self.maxPage:
            self.cPage += 1

        print('page :', self.cPage)
        self.table.clearContents()
        self.makeKospiTabke()

    def updateUiCellClick(self, r, i):
        index = r + (self.cPage * self.pageperMax)
        print(r, index)
        code = self.df.iloc[index, list(self.df.columns.values).index('종목코드')]
        code = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', code)
        # code = code[1:]
        self.parent.resiveData(code)



if __name__ == "__main__":
    app = QApplication([])
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())








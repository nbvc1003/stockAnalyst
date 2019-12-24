import sys, re
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cPage = 0
        self.pageperMax = 20
        self.initUI()


    def initUI(self):
        self.setWindowTitle('테이블팝업윈도우')
        self.setGeometry(100, 100, 200,200)
        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        # self.show()

    def createTable(self):
        self.table = QTableWidget()

        df = pd.read_csv('../forExe/kospi_kosdaq_code.csv', encoding='euc-kr')

        print(df.tail())
        print('1',df.size)

        df['종목코드'] = df['종목코드'].dropna(axis=0)
        df['종목명'] = df['종목명'].dropna(axis=0)
        df['업종명'] = df['업종명'].dropna(axis=0)
        df['대분류'] = df['대분류'].dropna(axis=0)

        df = df[df['대분류'] == '주식']
        print('2', df.size)
        # for i in df.index:
        #     if df['업종명'][i] != 'KOSPI' and df['업종명'][i] != 'KOSDAQ':
        print('3', df.size)

        self.table.setRowCount(self.pageMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('code','name'))

        # _pageCount = self.pageperMax * self.cPage
        # if  len(df['종목명']) >= (self.pageperMax * self.cPage):
        #     _pageCount = self.pageperMax
        # else:
        #     _pageCount = len(df['종목명']) % self.pageperMax

        # for r in range(   len(df['종목명']) ):
        #     self.table.setItem(r, 1, QTableWidgetItem(str(r)))




if __name__ == "__main__":
    app = QApplication([])
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())








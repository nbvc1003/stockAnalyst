
import sys
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QPushButton, \
    QHBoxLayout, QRadioButton, QLabel, QLineEdit
import modules.dataLoader

class TableWidget(QWidget):

    def __init__(self, parent=None, opt=0):
        super().__init__()

        # self.dataLoader = modules.dataLoader.DataLoader()

        self.cPage = 0
        self.maxPage = 0
        self.pageperMax = 40
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)# index 삭제
        self.initUI()
        self.parent = parent
        self.editTab = opt


    def initUI(self):
        self.setWindowTitle('종목코드리스트')
        self.setGeometry(100, 100, 400,600)

        self.createKospiTable()
        self.table.cellClicked.connect(self.updateUiCellClick)

        self.addTableListItems()

        self.layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.ledit = QLineEdit()
        btn_search = QPushButton('Search')
        btn_search.clicked.connect(lambda x:self.btn_search(self.ledit.text()))
        search_layout.addWidget(self.ledit)
        search_layout.addWidget(btn_search)


        tab_layout = QHBoxLayout()
        self.rbtn_kospi = QRadioButton("KOSPI")
        self.rbtn_kospi.clicked.connect(self.btn_tab_kospi)
        tab_layout.addWidget(self.rbtn_kospi)

        # self.rbtn_kosdaq = QRadioButton("KOSDAQ")
        # self.rbtn_kosdaq.clicked.connect(self.btn_tab_kosdaq)
        # tab_layout.addWidget(self.rbtn_kosdaq)

        self.rbtn_nyse = QRadioButton("NYSE")
        self.rbtn_nyse.clicked.connect(self.btn_tab_nyse)
        tab_layout.addWidget(self.rbtn_nyse)

        self.rbtn_nasdaq = QRadioButton("NASDAQ")
        self.rbtn_nasdaq.clicked.connect(self.btn_tab_nasdaq)
        tab_layout.addWidget(self.rbtn_nasdaq)
        self.rbtn_kospi.setChecked(True)

        self.layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        for text, slot in ( ("Prev Page", self.btn_page_pre), ("Next Page", self.btn_page_next)):
            button = QPushButton(text)
            btn_layout .addWidget(button)
            button.clicked.connect(slot)

        self.layout.addLayout(search_layout)
        self.layout.addLayout(tab_layout)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)


    def createKospiTable(self):

        # self.df = pd.read_csv('readFiles/kospi_list.csv',names=['Name','Symbol','업종','주요제품',
        #                                                             '상장일','결산월','대표자명','홈페이지','지역'], encoding='utf-8')
        self.df = modules.dataLoader.DataLoader.instance().get_DF(modules.dataLoader.KOSPI)

        self.df['Symbol'] = self.df['Symbol'].dropna(axis=0)
        self.df['Name'] = self.df['Name'].dropna(axis=0)

        ### Dictionary 형으로 변경
        # dfDic = self.df.set_index('Symbol')
        # dfDic = dfDic['Name'].to_dict()

        print('2', len(self.df.index))
        # for i in df.index:
        #     if df['업종명'][i] != 'KOSPI' and df['업종명'][i] != 'KOSDAQ':
        print('3', len(self.df.index))
        self.maxPage = len(self.df.index) // self.pageperMax
        self.table.setRowCount(self.pageperMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('이름','코드'))
        self.table.clearContents()


    def createKosdaqTable(self):

        # self.df = pd.read_csv('readFiles/kosdaq_list.csv',names=['Name','Symbol','업종','주요제품',
        #                                                            '상장일','결산월','대표자명','홈페이지','지역'], encoding='utf-8')
        self.df = modules.dataLoader.DataLoader.instance().get_DF(modules.dataLoader.KODAQ)

        self.df['Symbol'] = self.df['Symbol'].dropna(axis=0)
        self.df['Name'] = self.df['Name'].dropna(axis=0)

        ### Dictionary 형으로 변경
        # dfDic = self.df.set_index('Symbol')
        # dfDic = dfDic['Name'].to_dict()

        print('2', len(self.df.index))
        # for i in df.index:
        #     if df['업종명'][i] != 'KOSPI' and df['업종명'][i] != 'KOSDAQ':
        print('3', len(self.df.index))
        self.maxPage = len(self.df.index) // self.pageperMax
        self.table.setRowCount(self.pageperMax)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('이름','코드'))
        self.table.clearContents()

    def createNyseTable(self):
        # self.df = pd.read_csv('readFiles/nyse_symbol.csv', encoding='utf-8')
        self.df = modules.dataLoader.DataLoader.instance().get_DF(modules.dataLoader.NYSE)

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

    def createNasdaqTable(self):
        # self.df = pd.read_csv('readFiles/nsdaq_symbol.csv', encoding='utf-8')
        self.df = modules.dataLoader.DataLoader.instance().get_DF(modules.dataLoader.NASDAQ)
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

    def addTableListItems(self):
        self.table.clearContents()
        col_index_name = list(self.df.columns.values).index('Name')
        col_index_code = list(self.df.columns.values).index('Symbol')
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            if r >= len(self.df.index):
                break
            _index = r - (self.cPage * self.pageperMax)
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   self.df.iloc[r,col_index_name]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   self.df.iloc[r,col_index_code]))
    def addSearchListItems(self, keyword):
        self.table.clearContents()
        sdf = self.df[self.df['Name'].str.contains(keyword)]
        self.cPage = 0
        self.maxPage = len(sdf.index) // self.pageperMax

        col_index_name = list(sdf.columns.values).index('Name')
        col_index_code = list(sdf.columns.values).index('Symbol')
        for r in range((self.cPage * self.pageperMax), (self.cPage * self.pageperMax)+ self.pageperMax):
            if r >= len(sdf.index):
                break
            _index = r - (self.cPage * self.pageperMax)
            self.table.setItem(_index, 0, QTableWidgetItem(
                                   sdf.iloc[r,col_index_name]))
            self.table.setItem(_index, 1, QTableWidgetItem(
                                   sdf.iloc[r,col_index_code]))


    ##----------------------------------------------------------------------------------------------
    # UI EVENT DELEGATE
    ##----------------------------------------------------------------------------------------------

    def btn_search(self, keyword):

        if keyword != None and len(keyword) > 0:
            self.addSearchListItems(keyword)


    def btn_tab_kospi(self):
        self.ledit.setText('')
        self.cPage = 0
        self.createKospiTable()
        self.addTableListItems()

    def btn_tab_kosdaq(self):
        self.ledit.setText('')
        self.cPage = 0
        self.createKosdaqTable()
        self.addTableListItems()

    def btn_tab_nyse(self):
        self.ledit.setText('')
        self.cPage = 0
        self.createNyseTable()
        # self.makeNyseTable()
        self.addTableListItems()

    def btn_tab_nasdaq(self):
        self.ledit.setText('')
        self.cPage = 0
        self.createNasdaqTable()
        # self.makeNasdaqTable()
        self.addTableListItems()

    def btn_page_pre(self):
        self.table.scrollToTop()
        if self.cPage > 0:
            self.cPage -= 1
        print('page :' , self.cPage)
        self.table.clearContents()
        self.addTableListItems()


    def btn_page_next(self):
        # self.table.scrollToBottom()
        self.table.scrollToTop()
        if self.cPage < self.maxPage:
            self.cPage += 1
        print('page :', self.cPage)
        self.table.clearContents()
        self.addTableListItems()


    def updateUiCellClick(self, r, i):

        # print(type(self.table.currentIndex()), r, i)
        if self.table.item(r,i) == None:
            return
        # print(self.table.item(r,i).text())

        # index = r + (self.cPage * self.pageperMax)
        # code = self.df.iloc[index, list(self.df.columns.values).index('Symbol')]
        # name = self.df.iloc[index, list(self.df.columns.values).index('Name')]

        code = self.table.item(r, 1).text()
        name = self.table.item(r, 0).text()

        cat = "kospi"
        if self.rbtn_kospi.isChecked() == True :
            cat = "kospi"
        # elif self.rbtn_kosdaq.isChecked() == True :
        #     cat = "kosdaq"
        elif self.rbtn_nyse.isChecked() == True :
            cat = "nyse"
        elif self.rbtn_nasdaq.isChecked() == True :
            cat = "nasdaq"

        # main 에 이벤트 전달
        self.parent.setLineEditValue(code, self.editTab, cat, name)

if __name__ == "__main__":
    app = QApplication([])
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())








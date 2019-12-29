
import sys
import pandas as pd

BASE_PATH = "../forExe/"
KOSPI_CSV = ".csv"
NYSE_CSV = "nyse_symbol.csv"
NASDAQ_CSV = "nsdaq_symbol.csv"

KOSPI = 0
NYSE = 1
NASDAQ = 2



class dataLoader():
    def __init__(self):

        self.nyse_df = pd.read_csv('../readFiles/nyse_symbol.csv', encoding='utf-8')
        self.nasdaq_df = pd.read_csv('../readFiles/nsdaq_symbol.csv', encoding='utf-8')

        self.init()

    def init(self):
        self.kospi_df.replace(to_replace=r'\'', value='', regex=True, inplace=True)



    def read_File(self, file, encoding=None):
        self.kospi_df = pd.read_csv(file, encoding=encoding)
        self.nyse_df = pd.read_csv('../readFiles/nyse_symbol.csv', encoding='utf-8')
        self.nasdaq_df = pd.read_csv('../readFiles/nsdaq_symbol.csv', encoding='utf-8')


    def get_DF(self, arg):
        if arg == KOSPI:
            return self.kospi_df
        elif arg == NYSE:
            return self.nyse_df
        elif arg == NASDAQ:
            return self.nasdaq_df

    def get_SymbolByName(self, name):
        pass

    def get_NameBySymbol(self, symbol):
        pass




if __name__ == "__main__":
    # app = QApplication([])
    ex = dataLoader()
    # print(type(ex.get_NameBySymbol('AMD')), str(ex.get_NameBySymbol('AMD')))
    print(ex.get_NameBySymbol('AAPL'))

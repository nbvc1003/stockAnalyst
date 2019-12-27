
import sys
import pandas as pd

BASE_PATH = "../forExe/"
KOSPI_CSV = "kospi_kosdaq_code.csv"
NYSE_CSV = "nyse_symbol.csv"
NASDAQ_CSV = "nsdaq_symbol.csv"

KOSPI = 0
NYSE = 1
NASDAQ = 2

class dataLoader():
    def __init__(self):
        self.kospi_df = pd.read_csv('../forExe/kospi_kosdaq_code.csv', encoding='euc-kr')
        self.nyse_df = pd.read_csv('../forExe/nyse_symbol.csv', encoding='utf-8')
        self.nasdaq_df = pd.read_csv('../forExe/nsdaq_symbol.csv', encoding='utf-8')


    def init(self):
        pass

    def get_DF(self, arg):
        if arg == KOSPI:
            return self.kospi_df
        elif arg == NYSE:
            return self.nyse_df
        elif arg == NASDAQ:
            return self.nasdaq_df

    def get_SymbolByName(self, name):

        result = str(self.kospi_df['종목코드'][self.kospi_df['종목명'] == name])
        if len(result) < 1:
            result = str(self.nyse_df['Symbol'][self.nyse_df['Name'] == name])
        if len(result) < 1:
            result = str(self.nasdaq_df['Symbol'][self.nasdaq_df['Name'] == name])
        return result

    def get_NameBySymbol(self, symbol):
        # print(symbol)
        result = str(self.nasdaq_df['Name'][self.nasdaq_df['Symbol'] == symbol])
        return result


if __name__ == "__main__":
    # app = QApplication([])
    ex = dataLoader()
    print(type(ex.get_NameBySymbol('AMD')), str(ex.get_NameBySymbol('AMD')))

    print(type(ex.get_SymbolByName('삼성전자')), str(ex.get_SymbolByName('삼성전자')))
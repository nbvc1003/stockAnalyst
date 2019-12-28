
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
        self.kospi_df = pd.read_csv('../readFiles/kospi_kosdaq_code.csv', encoding='euc-kr')
        self.nyse_df = pd.read_csv('../readFiles/nyse_symbol.csv', encoding='utf-8')
        self.nasdaq_df = pd.read_csv('../readFiles/nsdaq_symbol.csv', encoding='utf-8')

        self.init()

    def init(self):
        self.kospi_df.replace(to_replace=r'\'', value='', regex=True, inplace=True)

    def get_DF(self, arg):
        if arg == KOSPI:
            return self.kospi_df
        elif arg == NYSE:
            return self.nyse_df
        elif arg == NASDAQ:
            return self.nasdaq_df

    def get_SymbolByName(self, name):
        print(type(self.kospi_df.columns.values), self.kospi_df.columns.values)
        result = self.kospi_df.iloc[self.kospi_df.index[self.kospi_df['종목명'] == name][0], 4]
        if len(result) < 1:
            result = self.nyse_df.iloc[self.nyse_df.index[self.nyse_df['Name'] == name][0], 4]
        if len(result) < 1:
            result = self.nasdaq_df.iloc[self.nasdaq_df.index[self.nasdaq_df['Name'] == name][0], 4]
        return result

    def get_NameBySymbol(self, symbol):
        # print(symbol)
        # df.loc[df["names"] == "Kilho", ["names", "points"]]를 실행하면, ‘names’ 열의 값이 “Kilho”인 행의 값 중에서 ‘names’와 ‘points’ 열에 해당하는 값들만을 얻을 수 있습니


        result = self.kospi_df['종목명'][self.kospi_df['종목코드'] == symbol]
        if len(result) < 1:
            result = self.nyse_df['Name'][self.nyse_df['Symbol'] == symbol]

        if len(result) < 1:
            result = self.nasdaq_df['Name'][self.nasdaq_df['Symbol'] == symbol]

        return result.tolist()



if __name__ == "__main__":
    # app = QApplication([])
    ex = dataLoader()
    # print(type(ex.get_NameBySymbol('AMD')), str(ex.get_NameBySymbol('AMD')))
    print(ex.get_NameBySymbol('AAPL'))

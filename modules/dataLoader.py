
import sys
import pandas as pd

BASE_PATH = "../readFiles/"

KOSPI = 0
KODAQ = 1
NYSE = 2
NASDAQ = 3



class DataLoader(object):

    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance


    def __init__(self):
        self.init()

    def init(self):
        self.read_File()


    def read_File(self):

        self.kospi_df = pd.read_csv('readFiles/kospi_list.csv', names=['Name', 'Symbol', '업종', '주요제품',
                                                                         '상장일', '결산월', '대표자명', '홈페이지', '지역'],
                                      encoding='utf-8')
        self.kosdaq_df = pd.read_csv('readFiles/kosdaq_list.csv', names=['Name', 'Symbol', '업종', '주요제품',
                                                                          '상장일', '결산월', '대표자명', '홈페이지', '지역'],
                                      encoding='utf-8')

        self.nyse_df = pd.read_csv('readFiles/nyse_symbol.csv', encoding='utf-8')
        self.nasdaq_df = pd.read_csv('readFiles/nsdaq_symbol.csv', encoding='utf-8')



    def get_DF(self, arg):
        if arg == KOSPI:
            return self.kospi_df
        elif arg == KODAQ:
            return self.kosdaq_df
        elif arg == NYSE:
            return self.nyse_df
        elif arg == NASDAQ:
            return self.nasdaq_df

    def get_SymbolByName(self, name):
        pass


    def get_NameBySymbol(self, symbol):

        ##특정값이 포함된 행들..
        #mock_data_filtered = mock_data[mock_data['country'].str.contains("Afghanistan|Nigeria")]

        symbol = symbol.replace('.KS','')
        symbol = symbol.replace('.KQ','')

        result = self.kospi_df[self.kospi_df['Symbol'].str.contains(symbol)]['Name']
        # print("result ", type(result), len(result), result)
        if len(result) < 1:
            result = self.kosdaq_df[self.kosdaq_df['Symbol'].str.contains(symbol)]['Name']

        if len(result) < 1:
            result = self.nyse_df[self.nyse_df['Symbol'].str.contains(symbol)]['Name']

        if len(result) < 1:
            result = self.nasdaq_df[self.nasdaq_df['Symbol'].str.contains(symbol)]['Name']

        return result.to_string(index=False).strip()


if __name__ == "__main__":
    # app = QApplication([])
    ex = DataLoader()
    # print(type(ex.get_NameBySymbol('AMD')), str(ex.get_NameBySymbol('AMD')))
    print(ex.get_NameBySymbol('AAPL'))

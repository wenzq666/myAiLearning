"""
数据预处理
    数据加载
    时间转换
    对时间排序
    数据去重
"""

import pandas as pd

class DataPreprocessing:
    def data_preproces(self, path):
        read_data = pd.read_csv(path)
        # print(data.head())
        # data.info()

        read_data['time'] = pd.to_datetime(read_data.time)
        # print(data.head())
        # data.info()

        read_data.sort_values(by='time', inplace=True)
        # print(data.head())
        # data.info()

        read_data.drop_duplicates(inplace=True)

        return read_data


if __name__ == '__main__':
    data = DataPreprocessing().data_preproces("../data/train.csv")
    print(data.head())
    data.info()







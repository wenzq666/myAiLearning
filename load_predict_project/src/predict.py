"""
预测
"""

import os
import pandas as pd
import datetime

from utils.log import Logger
from utils.common import DataPreprocessing
from sklearn.metrics import mean_absolute_error
import matplotlib.ticker as mick
import joblib
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15
pd.set_option('display.max_columns',None)


class PowerLoadPredict:
    def __init__(self, base_path):
        # 配置日志记录
        logfile_name = "predict_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.logfile = Logger('../', logfile_name).get_logger()
        # 获取数据源
        self.data_source = DataPreprocessing().data_preproces(os.path.join(base_path, 'data/test.csv'))
        # 历史数据转为字典，key:时间，value:负荷，目的是为了避免频繁操作dataframe，提高效率。实际开发场景中可以使用redis进行缓存
        self.data_dict = self.data_source.set_index('time')['power_load'].to_dict()
        # print(self.data_dict)
        self.model = joblib.load('../model/xgb.pkl')


    # 构造特征
    def feature_construct(self, time_key, time_key_load = None):
        # 解析时间特征
        if isinstance(time_key,str):
            time_key = pd.to_datetime(time_key)

        # 添加hour month特征
        hour = time_key.hour
        month = time_key.month

        # 转one-hot类型
        hour_list = [0] * 24
        month_list = [0] * 12
        # 把对应时间位置的值设为1
        hour_list[hour] = 1
        month_list[month - 1] = 1

        # 时间窗口的负荷特征
        time_key_load = time_key_load if time_key_load else self.data_dict
        first_one_hour = time_key_load.get(time_key - pd.Timedelta(hours=1),500)
        first_two_hour = time_key_load.get(time_key - pd.Timedelta(hours=2),500)
        first_three_hour = time_key_load.get(time_key - pd.Timedelta(hours=3),500)

        # 解析昨日
        yesterday_load = time_key_load.get(time_key - pd.Timedelta(days=1),500)


        # 构造成pd
        featrue_columns = ['first_one_hour', 'first_two_hour',
       'first_three_hour', 'yesterday_load', 'hour_0', 'hour_1', 'hour_2',
       'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
       'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15',
       'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21',
       'hour_22', 'hour_23', 'month_1', 'month_2', 'month_3', 'month_4',
       'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10',
       'month_11', 'month_12']

        featrue_list = [first_one_hour, first_two_hour, first_three_hour, yesterday_load, *hour_list, *month_list]

        return pd.DataFrame([featrue_list], columns=featrue_columns)


    def model_predict(self, time_key):
        if time_key is not None:
            pred_feature = self.feature_construct(time_key)
            pred = self.model.predict(pred_feature)
            return pred[0]
        else:
            data = self.data_source.copy()
            data = data[data.time > '2015-08-01 00:00:00']

            #初始化评估数据列表
            evaluate_list = []

            # 掩盖时间
            for time_key in data.time:
                # 掩盖当前时间之后的所有负荷数据
                time_key_load = {k:v for k,v in self.data_dict.items() if k < time_key}
                pred_feature = self.feature_construct(time_key, time_key_load)
                pred = self.model.predict(pred_feature)
                evaluate_list.append([time_key,self.data_dict[time_key],pred[0]])

            # 转DataFrame
            evaluate_df = pd.DataFrame(evaluate_list, columns=['time','true','pred'])

            # 评估
            mae = mean_absolute_error(evaluate_df.true, evaluate_df.pred)
            print('mae:',mae)

            # 绘图
            self.eval_plot(evaluate_df)




    def eval_plot(self,eval_df):
        plt.figure(figsize=(20,10))
        plt.plot(eval_df.time, eval_df.true, label='true')
        plt.plot(eval_df.time, eval_df.pred, label='pred')
        plt.xlabel('time')
        plt.ylabel('power_load')
        plt.show()








if __name__ == '__main__':
    pl = PowerLoadPredict('../')
    df = pl.feature_construct('2015-08-01')
    print(df)
    #
    # df = pl.model_predict('2015-08-01')
    # print(df)
    #
    # pl.model_predict(None)

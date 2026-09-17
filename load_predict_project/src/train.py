import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from utils.log import Logger
from utils.common import DataPreprocessing
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV,TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15

pd.set_option('display.max_columns',None)

class PowerLoadModel:
    def __init__(self, data_path):
        # 初始化日志对象
        log_file_name = "train_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.logger = Logger("../", log_file_name).get_logger()

        # 加载数据
        self.source_data = DataPreprocessing().data_preproces(data_path)
        # 初始化time对应的load字典
        self.time_key_load = self.source_data.set_index('time').to_dict()['power_load']
        # print(self.time_key_load)



    # 数据分析
    def ana_data(self):
        self.logger.info("================starting...=============")
        # 负荷整体分布情况
        fig = plt.figure(figsize=(30, 60))
        ax1 = fig.add_subplot(411)
        ax1.hist(self.source_data['power_load'])
        ax1.set_title("负荷整体分布情况")
        ax1.set_xlabel("负荷")
        ax1.set_ylabel("频率")
        # plt.show()

        #
        data = self.source_data.copy()
        print(data.head())

        # 提取小时信息
        data['hour'] = data['time'].dt.hour


        # 各个小时平均符合趋势
        per_hour_df = data.groupby(data['hour'],as_index=False)["power_load"].mean()


        ax2 = fig.add_subplot(412)
        ax2.plot(per_hour_df.hour,per_hour_df.power_load)
        ax2.set_title("各小时平均趋势")
        ax2.set_xlabel("小时")
        ax2.set_ylabel("平均负荷")
        ax2.set_xticks(range(24))
        plt.grid()

        # 月平均
        data['month'] = data['time'].dt.month
        per_month_df = data.groupby(data['month'],as_index=False)["power_load"].mean()
        print(per_month_df)

        ax3 = fig.add_subplot(413)
        ax3.plot(per_month_df.month,per_month_df.power_load)
        ax3.set_title("各月份平均趋势")
        ax3.set_xlabel("月份")
        ax3.set_ylabel("平均负荷")
        ax3.set_xticks(range(13))
        plt.grid()
        # plt.show()

        # 工作日和周末
        # 5,6是周末
        data['weekday'] = data['time'].dt.weekday
        # print(data.head(100))
        data['is_week'] = data['weekday'].apply(lambda x:1 if x in[5,6] else 0)
        workday_load = data[data['is_week'] == 0]['power_load'].mean()
        weekday_load = data[data['is_week'] == 1]['power_load'].mean()
        print(data)


        ax4 = fig.add_subplot(414)
        ax4.bar(['工作日','周末'],[workday_load,weekday_load])
        ax4.set_title("工作日与周末平均负荷情况")
        plt.tight_layout(pad=3.0)
        plt.show()
        self.logger.info("======================end...=============================")


    #特征工程
    def feature_engineering(self):
        """
        特征工程函数，用于处理原始数据并提取有用的特征
        参数:

            self: 类实例，包含源数据和必要的方法
        返回:
            tuple: 包含三个元素的元组
                - 处理后的特征数据 (DataFrame)
                - 目标变量 (Series)
                - 特征列名列表 (list)
        """
        # 创建源数据的副本，避免修改原始数据
        data = self.source_data.copy()
        print(data)
        # 从时间列中提取小时和月份特征
        data['hour'] = data.time.dt.hour
        data['month'] = data.time.dt.month
        print(data['hour'])
        print(data.time)

        # 获取前一个小时的时间
        for k,v in [("first_one_hour",1),("first_two_hour",2),("first_three_hour",3)]:
            last_n_hour = data.time - pd.Timedelta(v, unit='h')
            # 获取不到返回None  第一天和前三小时数据产生None
            last_n_load = last_n_hour.apply(lambda x:self.time_key_load.get(x))
            data[k] = last_n_load

        # print(data.head(100))
        last_1_day = data.time - pd.Timedelta(days=1)
        last_1_load = last_1_day.apply(lambda x: self.time_key_load.get(x))
        data['yesterday_load'] = last_1_load

        # 剔除空样本
        data.dropna(inplace=True)

        # 整理时间特征
        data = pd.get_dummies(data,columns=['hour','month'])
        # print(pd.head(100))
        print(data.columns)
        return data.iloc[:,2:],data.iloc[:,1],data.columns[2:]


    def model_train(self):
        # 数据集划分
        x, y, feature_names = self.feature_engineering()

        # 时间序列预测 得按时间顺序划分  测试集必须在训练集之后
        train_size, val_size, test_size = (int(len(x) * 0.6), int(len(x) * 0.2),
                                           len(x) - int(len(x) * 0.6) - int(len(x) * 0.2))
        x_train, x_val, x_test = (x.iloc[:train_size, :], x.iloc[train_size:train_size + val_size, :],
                                  x.iloc[train_size + val_size:, :])
        y_train, y_val, y_test = (y.iloc[:train_size], y.iloc[train_size:train_size + val_size],
                                  y.iloc[train_size + val_size:])
        

        # 网格搜索 交叉验证
        # 定义xbg模型  迭代树 数量的上线
        # xgb = XGBRegressor(n_estimators=1000, early_stopping_rounds=20)
        # # 定义参数
        # param_grid = {
        #     'max_depth': [3, 5, 7],
        #     'learning_rate': [0.01, 0.1, 0.2]
        # }
        #
        #
        # # 时间序列交叉验证
        # cv = TimeSeriesSplit(n_splits=5)
        #
        # # 定义网格搜索
        # grid_search = GridSearchCV(xgb, param_grid, cv=cv,verbose=50)
        # # 训练模型
        # grid_search.fit(x_train, y_train, eval_set=[(x_val, y_val)])
        # # 输出最佳模型
        # print(f"最佳模型: {grid_search.best_estimator_}")
        # # 最佳树数量
        # print(f"最佳树数量: {grid_search.best_estimator_.best_iteration}")
        # 输出最佳参数
        #print(f"最佳参数: {grid_search.best_params_}")

        # 模型训练
        xgb_best = XGBRegressor(n_estimators=191,max_depth=3,learning_rate=0.1)
        total_xtrain = pd.concat([x_train,x_val],axis=0)
        total_ytrain = pd.concat([y_train,y_val],axis=0)

        xgb_best.fit(total_xtrain,total_ytrain)

        y_pred = xgb_best.predict(x_test)
        mae = mean_absolute_error(y_test,y_pred)

        print(f"mae:{mae}")

        joblib.dump(xgb_best,'../model/xgb.pkl')




if __name__ == '__main__':
    pl = PowerLoadModel("../data/train.csv")
    # pl.ana_data()
    data1,data2,data3 = pl.feature_engineering()
    # print(data1)
    # print('*'*50)
    # print(data2)
    # print('*' * 50)
    # print(data3)
    pl.model_train()








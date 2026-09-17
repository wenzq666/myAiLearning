import jieba
import joblib
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier

from .config import Config
import warnings

warnings.filterwarnings('ignore')
# 设置pandas显示选项
pd.set_option('display.max_columns', None)

# 1. 加载配置文件.
# 加载配置
config = Config()

# 2. 加载模型和向量化器.
# 1. 加载随机森林模型(rf)
model:RandomForestClassifier = joblib.load(config.rf_model_path)


# 2. 加载向量化器(tfidf)
tfidf = joblib.load(config.tfidf_model_save_path)

# 4. 设置标签索引 和 名称对应关系.       # {0:'finance', 1: 'realty', ...}

classClassifier = {k:v for k,v in enumerate(open(config.class_datapath, 'r').read().split())}
# print(classClassifier)

# 3. 定义预测函数.
def predict_fun(data):      # data: 就是待预测的数据,字典格式,  例如:  {'text': '传奇3经典续作重现深挖品牌文化底蕴'}
    # 1. jieba分词
    text_cut = " ".join(jieba.lcut(data['text']))
    # print(text_cut)

    # 2. 向量化.
    text_tfidf = tfidf.transform([text_cut])
    # print(text_tfidf)

    # 3. 预测.
    y_pred = model.predict(text_tfidf)[0]
    # print(y_pred)


    # 5. 获取预测类别的名称.
    class_name = classClassifier[y_pred]

    # 6. 给原始数据新增pred_class(预测的类别), 并返回.
    data['pred_class'] = class_name

    # 7. 返回结果, 例如: {'text': '传奇3经典续作重现深挖品牌文化底蕴', 'pred_class': 'game'}
    return data


# 4. 测试
if __name__ == '__main__':
    data = {'text': '传奇3经典续作重现深挖品牌文化底蕴'}
    result = predict_fun(data)
    print(result)

    data = {'text': '华商基金举办北京客户交流会'}
    result = predict_fun(data)
    print(result)
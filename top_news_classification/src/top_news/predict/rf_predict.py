import joblib
import pandas as pd
import pickle
from src.top_news.config import Config
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import warnings
warnings.filterwarnings('ignore')

# 1. 加载配置文件.
# 设置pandas显示选项
pd.set_option('display.max_columns', None)
# 加载配置
conf = Config()



# 2. 加载模型和向量化器.
# 1. 加载随机森林模型(rf)
model = joblib.load(conf.rf_model_path)
# 2. 加载向量化器(tfidf)
tfidf = joblib.load(conf.tfidf_model_save_path)
# 3. 读取dev数据集, 分隔符为: ,(默认的, 可以不处理, 因为是csv文件)
process_dev_data = pd.read_csv(conf.process_dev_datapath, sep='\t', encoding='utf-8')

# 4. 对dev数据集进行向量化.
dev_data_words = tfidf.transform(process_dev_data['words'])


# 5. 模型预测.
y_pred = model.predict(dev_data_words)
y_true = process_dev_data['label']

# 计算准确率(accuracy): 正确预测的样本 占 总样本的比例
print("准确率:",accuracy_score(y_true, y_pred))

# 计算精确率(precision): 预测为正类的样本中, 实际为正类的样本所占的比例
# macro: 宏平均 对所有类别平等加权, micro: 微观平均
print("precision_score:",precision_score(y_true, y_pred, average='macro'))
# 计算召回率(recall): 实际为正类的样本中, 预测为正类的样本所占的比例
print("recall_score:",recall_score(y_true, y_pred, average='macro'))
# 计算F1-score: 精确率和召回率的调和平均数
print("f1_score:",f1_score(y_true, y_pred, average='macro'))

# 6.保存结果.
# 参1: 结果路径, 参2: 分隔符, 参3: 是否保存索引
process_dev_data['y_pred'] = y_pred
process_dev_data.to_csv(conf.predict_result_path, index_label=False, encoding='utf-8')

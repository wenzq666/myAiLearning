import joblib
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.top_news.config import Config
from tqdm import tqdm  # 引入 tqdm 用于进度条
pd.set_option('display.expand_frame_repr', False)  # 避免宽表格换行
pd.set_option('display.max_columns', None)  # 确保所有列可见

# 实例化配置对象, 用于获取: 文件路径等配置.
conf = Config()


# 2.读取训练数据.
# 2.1 pandas读取训练数据, 仅取前2W条数据(控制数据量, 加快训练速度)
process_train_data = pd.read_csv(conf.process_train_datapath, sep='\t')
#[0:20000]

# 2.2 提取特征列'words' -> 预处理后的文本数据.
words_data = process_train_data['words']
print(words_data)

# 2.3 提取标签列'label' -> 训练标签.
label_data = process_train_data['label']
print(label_data)


# 2.4 打印前5行.
print(process_train_data.head())


# 3. 文本特征提取(TF-IDF向量化)
# 3.1 读取停用词文件(停用词: 对分类无意义的词, 如: 的, 是等这些词), 按行分割为列表.
stop_words = open(conf.stopword_datapath, 'r' ,encoding='utf-8').read().split('\n')
print(stop_words)


# 3.2 初始化 TF-IDF向量化器, 指定停用词列表(过滤停用词的)
tfidf = TfidfVectorizer(stop_words=stop_words)

# 3.3 对文本特征进行拟合(学习词汇表) 并转换 TF-IDF特征矩阵
features = tfidf.fit_transform(words_data)

# 3.4 查看生成的词汇表(特征名称)列表
print(features)

# 3.5 查看词汇表中 词和索引的映射关系(字典形式: 词 -> 列索引)
print(tfidf.vocabulary_)

# 3.6 再次确认词汇表的大小.
print(len(tfidf.vocabulary_))



# 4. 模型的训练和评估
# 4.1 划分训练集和测试集.
# x_train, x_test, y_train ,y_test = train_test_split(features, label_data)

# 4.2 初始化随机森林分类器
# model = RandomForestClassifier()
total_trees = 100  # 定义总树数(默认是100)
model = RandomForestClassifier(n_estimators=0, warm_start=True, n_jobs=-1)

# 4.3 训练模型, 并使用tqdm 显示进度条
# model.fit(x_train, y_train)

# 4.3 训练模型, 并使用tqdm 显示进度条
with tqdm(total=total_trees, desc="训练随机森林") as pbar:
    for i in range(1, total_trees + 1):
        # 动态更新树的数量
        model.n_estimators = i
        # 训练新增的 1 棵树
        model.fit(features, label_data)
        # 更新进度条
        pbar.update(1)

# 4.4 模型预测和评估.
# y_pred = model.predict(x_test)
# 打印微平均精确率(所有类别合集计算的精确率, 适用于 多类别不平衡的场景)
# print("准确率：",accuracy_score(y_test, y_pred))
# print("精确率：",precision_score(y_test, y_pred, average="micro"))
# print("召回率：",recall_score(y_test, y_pred, average="micro"))
# print("F1：",f1_score(y_test, y_pred, average="micro"))

# 4.5 打印预测结果
# print(y_pred)


# 5. 模型和向量化器保存.
# 5.1 保存训练好的 随机森林模型.
joblib.dump(model, conf.rf_model_path)

# 5.2 保存训练好的 TF-IDF向量化器(后续预测时, 需要使用同一个向量化器转换新文本)
joblib.dump(tfidf, conf.tfidf_model_save_path)

# 5.3 提示保存成功.
print('保存完成')























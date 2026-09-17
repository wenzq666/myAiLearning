"""
分别对训练集 测试集 验证集进行预处理 并保存到data中
    任务 在原有数据集基础上增加words列 对原数据的text进行jieba分词 并用空格连接分词后的结果
"""
import jieba
from config import Config
import pandas as pd


config = Config()

# 要处理的文件路径
data_path_list = [config.train_datapath, config.test_datapath, config.dev_datapath]

process_path_list = [config.process_train_datapath,
                     config.process_test_datapath,
                     config.process_dev_datapath
                     ]

for item in range(3):
    # 读取数据
    process_data = pd.read_csv(data_path_list[item], sep='\t', names=['text', 'label'])
    # 分词  对输入文本进行分词, 分词后取前30个词并用空格连接
    process_data['words'] = process_data['text'].apply(lambda x:" ".join(jieba.lcut(x))[:30])
    # 保存
    process_data.to_csv(process_path_list[item], sep='\t', index = False, header=True)








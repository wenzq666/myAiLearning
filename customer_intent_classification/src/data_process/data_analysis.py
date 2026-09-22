import json
import pandas as pd
import matplotlib.pyplot as plt
from src.config import Config


plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


config = Config()


def load_json_data(file_path):
    df = pd.read_json(file_path, lines=True, encoding='utf-8')
    # df.info()
    # print(df.head())
    return df


def analyze_basic_info(df: pd.DataFrame):
    """数据集基础质量分析"""

    print(train_data['label'].value_counts())

    # 新增text_length
    train_data['sentence_length'] = train_data['sentence'].apply(lambda x: len(x))

    print(train_data.head())


def label_analysis(train_df):
    """标签分布分析"""

    label_count = train_df["label_des"].value_counts()
    print(label_count)

    print("\n===== 标签分布 =====")
    print(label_count)

    print("\n最多类别:")
    print(label_count.head(10))

    print("\n最少类别:")
    print(label_count.tail(10))

    # 画图
    plt.figure(figsize=(14, 5))
    label_count.plot(kind="bar")

    plt.title("训练集标签分布")
    plt.xlabel("标签")
    plt.ylabel("样本数量")

    # 118个标签全部显示会很乱，隐藏x轴文字
    plt.xticks([])

    plt.tight_layout()
    plt.show()


def text_length_analysis(train_df):
    """文本长度分析"""

    text_length = train_df["sentence"].str.len()

    print("\n===== 文本长度 =====")
    print(text_length.describe())

    plt.figure(figsize=(8, 5))
    plt.hist(text_length, bins=30)

    plt.title("训练集文本长度分布")
    plt.xlabel("文本长度")
    plt.ylabel("样本数量")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    #  #   Column     Non-Null Count  Dtype
    # ---  ------     --------------  -----
    #  0   id         10000 non-null  int64
    #  1   label      10000 non-null  int64
    #  2   sentence   10000 non-null  object
    #  3   label_des  10000 non-null  object

    # 标签分布不是很均衡
    # 60     471
    # 82     321
    # 97     314
    # 49     259
    # 1      238
    #       ...
    # 101     17
    # 11      16
    # 116      8

    train_data = load_json_data(config.train_datapath)
    # train_data 没有空值
    analyze_basic_info(train_data)
    print("=============================================")
    """
        存在明显类别不平衡
        头部类别：400+ 样本
             ↓
        部分类别：200~300
             ↓
        大量类别：50~100
             ↓
        尾部类别：甚至只有十几、二十条
        
        20 字以后快速减少，30～50 字已经比较少，虽然存在极少数 100+ 的长文本，但明显属于长尾。
        
    """
    label_analysis(train_data)
    text_length_analysis(train_data)


    # dev_data = load_json_data(config.dev_datapath)
    # analyze_basic_info(dev_data)
    print("=============================================")




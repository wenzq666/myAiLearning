from sklearn.datasets import load_iris #鸢尾花测试集
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split #分割训练集和测试集
from sklearn.preprocessing import StandardScaler     #分割标准化
from sklearn.neighbors import KNeighborsClassifier   #KNN 分类对象
from sklearn.metrics import accuracy_score           #模型评估

# 加载鸢尾花数据
def dm01_loadiris():
    iris_data = load_iris()
    #print(iris_data)
    print("键值：",iris_data.keys())
    print("前5条数据",iris_data.data[:5])
    print("前5标签",iris_data.target[:5])
    print("前5标签对应的名称",iris_data.target_names)
    print("特征名称",iris_data.feature_names)

def dm02_showiris():
    # 加载
    iris_data = load_iris()
    #
    iris_df = pd.DataFrame(iris_data.data,columns=iris_data.feature_names)
    iris_df['target'] = iris_data.target
    print(iris_df)

    #hue 分组字段
    sns.lmplot(data=iris_df,x='sepal length (cm)',y='sepal width (cm)',hue = 'target')
    plt.title('iris data')
    plt.tight_layout()
    plt.show()

def dm03_split_train_test():
    iris_data = load_iris()
    # 1.特征数据 2.标签数据 3.测试集比例
    # 返回值：训练集特征数据 测试集特征数据 训练集标签数据 测试集标签数据
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.2,random_state=66)

    print(f"训练集特征:{x_train},个数：{len(x_train)}")
    print(f"测试集特征:{x_test},个数：{len(x_test)}")
    print(f"训练集标签:{y_train},个数：{len(y_train)}")
    print(f"测试集标签:{y_test},个数：{len(y_test)}")


def dm04_iris_evaluate_test():
    iris_data = load_iris()
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.2,random_state=66)
    #标准化
    transfer = StandardScaler()
    # fit_transform 兼具fit和transform的功能 即 训练 转换 适用于第一次进行标准化的时候使用 一般用于处理训练集
    x_train = transfer.fit_transform(x_train)
    #transform 只有转换 适用于重复进行标准化的动作 一般用于对测试集进行标准化
    x_test = transfer.transform(x_test)

    # 模型对象
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train, y_train)

    # 模型预测
    y_pred = estimator.predict(x_test)
    print(y_pred)

    # 自定义测试数据集
    my_data = [[7.8,2.2,3.4,2.0]]
    # 标准化
    my_data = transfer.transform(my_data)
    y_pred_new = estimator.predict(my_data)
    print(y_pred_new)

    # 查看上诉数据集 每种类型概率的分类
    y_pred_proba = estimator.predict_proba(my_data)
    print(y_pred_proba)

    # 评估
    # 直接评分
    print(estimator.score(x_train,y_train))

    print(accuracy_score(y_test,y_pred))


if __name__ == '__main__':
    dm04_iris_evaluate_test()




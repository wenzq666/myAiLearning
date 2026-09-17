"""
鸢尾花 knn实现
"""
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score


def load_data():
    iris_data = load_iris()
    print(iris_data.data.shape)
    # 特征
    print(iris_data.data[:5])
    # 标签
    print(iris_data.target)
    # 特征名
    print(iris_data.feature_names)
    # 特征描述
    print(iris_data.DESCR)
    # 文件名
    print(iris_data.filename)

def show_iris():
    iris_data:Bunch = load_iris()
    print(type(iris_data))

    # 转df对象
    df = pd.DataFrame(iris_data.data,columns=iris_data.feature_names)
    df['label'] = iris_data.target

    x_label = 'sepal length (cm)'
    y_label = 'petal width (cm)'

    sns.lmplot(x = x_label,y = y_label,data = df,hue = 'label',fit_reg=True)
    # plt.label = x_label
    # plt.label = y_label
    plt.title = 'iris'
    plt.show()

def knn_iris():
    iris_data:Bunch = load_iris()
    # 数据集划分
    # 数据集划分 7:3
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.3,random_state=666)

    # 特征与处理 -- 标准化
    scaler = StandardScaler()
    # 训练集标准化
    x_train = scaler.fit_transform(x_train)
    # 直接套用训练集fit的结果 转换测试集
    x_test = scaler.transform(x_test)
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(x_train,y_train)

    #模型评估
    # 1. model.score()
    # 测试集特征，测试集标签
    acc = knn_model.score(x_test,y_test)
    print("KNN score:",acc)

    y_pred = knn_model.predict(x_test)
    # 真实值 测试值
    acc = accuracy_score(y_test,y_pred)
    print("accuracy:",acc)

    # 模型预测
    my_data = [[5.1, 3.5, 1.4, 0.2],
              [4.6, 3.1, 1.5, 0.2]]

    #  预测特征标准化  要和训练数据格式保持一致
    my_data = scaler.transform(my_data)
    my_pred = knn_model.predict(my_data)
    print("预测标签",my_pred)
    y_prob = knn_model.predict_proba(my_data)
    print("预测概率",y_prob)

    
def grid_searchCV_knn_iris():
    iris_data:Bunch = load_iris()
    # 数据集划分
    # 数据集划分 7:3
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.3,random_state=22)

    # 特征与处理 -- 标准化
    scaler = StandardScaler()
    # 训练集标准化
    x_train = scaler.fit_transform(x_train)
    # 直接套用训练集fit的结果 转换测试集
    x_test = scaler.transform(x_test)
    knn_model = KNeighborsClassifier()
    # knn_model.fit(x_train,y_train)

    # 网格搜索参数
    param_dict = {"n_neighbors":[1, 5, 7, 8]}
    knn_model = GridSearchCV(knn_model, param_dict, cv=5)
    knn_model.fit(x_train,y_train)
    print("最好的参数",knn_model.best_params_)
    print("最好的分数",knn_model.best_score_)
    print(knn_model.cv_results_)

    # 重新训练模型
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(x_train, y_train)

    #模型评估
    # 1. model.score()
    # 测试集特征，测试集标签
    acc = knn_model.score(x_test,y_test)
    print("KNN score:",acc)

    y_pred = knn_model.predict(x_test)
    # 真实值 测试值
    acc = accuracy_score(y_test,y_pred)
    print("accuracy:",acc)

    # 模型预测
    my_data = [[5.1, 3.5, 1.4, 0.2],
              [4.6, 3.1, 1.5, 0.2]]

    #  预测特征标准化  要和训练数据格式保持一致
    my_data = scaler.transform(my_data)
    my_pred = knn_model.predict(my_data)
    print("预测标签",my_pred)
    y_prob = knn_model.predict_proba(my_data)
    print("预测概率",y_prob)


if __name__ == '__main__':
    # load_data()
    # show_iris()
    # knn_iris()
    grid_searchCV_knn_iris()
























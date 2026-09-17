"""
随机森林多分类建模与评估：

请基于 Python 的 sklearn 库，使用随机森林分类器完成鸢尾花（Iris）数据集的分类建模，具体要求如下：

数据加载与划分
加载 sklearn 内置的鸢尾花数据集，将数据集按 7:3 的比例划分为训练集与测试集，设置随机种子 random_state=42 保证结果可复现。

模型初始化与训练
初始化随机森林分类器，基础参数设置：决策树数量 n_estimators=100，随机种子 random_state=42，其余参数保持默认；使用训练集完成模型训练。

模型效果评估
使用训练好的模型对测试集进行预测，计算并输出模型在测试集上的准确率，同时输出包含精确率、召回率、F1 值的分
"""
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score,  classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def show_iris_data():
    iris_data = load_iris()
    print(iris_data)
    print(iris_data.data)
    print(iris_data.target)


def load_iris_data():
    iris_data = load_iris()

    # 模型初始化与训练
    # 初始化随机森林分类器，基础参数设置：决策树数量
    # n_estimators = 100，随机种子
    # random_state = 42，其余参数保持默认；使用训练集完成模型训练。


    x_train, x_test , y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.3,random_state=42)
    # print(x_train)
    # 决策树数量 n_estimators=100，随机种子 random_state=42，
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)




    y_pred = model.predict(x_test)

    # 计算并输出模型在测试集上的准确率，同时输出包含精确率、召回率、F1 值的分
    accuracy = accuracy_score(y_test, y_pred)
    print(f"测试集准确率: {accuracy}")

    class_names = iris_data.target_names
    report = classification_report(y_test, y_pred, target_names=class_names, digits=3)
    print(report)






if __name__ == '__main__':
    # show_iris_data()
    load_iris_data()


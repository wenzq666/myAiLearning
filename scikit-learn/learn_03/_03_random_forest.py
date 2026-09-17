"""
CART决策树
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def titanic():
    # 数据加载
    titanic_data = pd.read_csv("./data/train.csv")
    # print(titanic_data.head())
    # titanic_data.info()
    # 预处理
    x = titanic_data[["Pclass","Sex","Age"]].copy()
    y = titanic_data["Survived"]
    x["Age"].fillna(value=x["Age"].mean())
    print(x.head())
    # 特征工程
    # get_dummies 把字符值类型的进行one-hot编码
    # 特征有几个类别就会转成几列 样本本身属于哪个类别 这个类别就赋值为1 其它类别为0
    x = pd.get_dummies(x)
    print(x.head())
    # CART树模型训练
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=666)

    # 模型评估
    dtc = DecisionTreeClassifier(criterion='gini',max_depth=4)
    dtc.fit(x_train,y_train)


    #随机森林模型
    rfc = RandomForestClassifier(max_depth=6,random_state=666)
    rfc.fit(x_train,y_train)


    #网格搜索 + 交叉验证
    param_dict = {
        "n_estimators": [70, 100, 130, 150],
        "max_depth": [6, 10, 12],
        "random_state": [666]
    }
    gs_cv = GridSearchCV(rfc,param_grid=param_dict,cv = 5)
    gs_cv.fit(x_train,y_train)
    print("训练集最好参数",gs_cv.best_params_)
    print("训练的最好分数",gs_cv.best_score_)



    # 模型预测
    # 准确率
    dtc_score = dtc.score(x_test,y_test)
    print("CART准确率",dtc_score)

    rfc_acc = rfc.score(x_test, y_test)
    print("随机森林准确率", rfc_acc)

    tree_pred = rfc.predict(x_test)

    y_pred = dtc.predict(x_test)

    report = classification_report(y_test,y_pred)

    print("cart树报告",report)
    print('*' * 50)
    tree_report = classification_report(y_test,tree_pred)
    print("随机森林树报告", tree_report)


    # 绘制图像
    # plt.figure(figsize=(100,100))
    # plot_tree(dtc,
    #           max_depth=10,
    #           filled=True,
    #           feature_names=['Pclass', 'Age', 'Sex_female', 'Sex_male'],
    #           class_names=['died', 'survived'])
    # plt.show()






if __name__ == '__main__':
    titanic()
























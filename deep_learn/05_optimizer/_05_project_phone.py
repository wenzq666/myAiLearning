import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from torchsummary import summary
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


class PhoneModel(nn.Module):
    def __init__(self, features, class_nums):
        super().__init__()
        # 第一层
        self.h1_linear = nn.Linear(in_features=features, out_features=64)
        self.h1_drop = nn.Dropout(0.3)

        # 加一层
        self.h1_linear_in = nn.Linear(in_features=64, out_features=128)
        self.h1_drop_in = nn.Dropout(0.3)

        # 第二层
        self.h2_linear = nn.Linear(in_features=128, out_features=256)
        self.h2_drop = nn.Dropout(0.4)

        # 第一层
        self.out = nn.Linear(in_features=256, out_features=class_nums)


    def forward(self, x):
        h1_activate = self.h1_drop(torch.relu(self.h1_linear(x)))

        h1_in_activate = self.h1_drop_in(torch.relu(self.h1_linear_in(h1_activate)))

        h2_activate = self.h2_drop(torch.relu(self.h2_linear(h1_in_activate)))

        return self.out(h2_activate)


def get_data():
    data = pd.read_csv("./data/手机价格预测.csv")
    # 获取特征和标签
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    # 同一类型
    x = x.astype(np.float32)
    y = y.astype(np.int64)

    # 切分数据集
    x_train,x_test,y_train,y_test  = train_test_split(x,y ,test_size=0.3,random_state=66)

    # 标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 转张量
    # print(type(x_train))
    # print(type(x_test))
    # print(type(y_train))
    # print(type(y_test))

    # DataFrame --> numpy --> tensor
    x_train = torch.tensor(x_train)
    x_test = torch.tensor(x_test)
    y_train = torch.tensor(y_train.values)
    y_test = torch.tensor(y_test.values)

    # 创建DataSet
    train_DataSet = TensorDataset(x_train,y_train)
    test_DataSet = TensorDataset(x_test,y_test)

    # 加工特征数量 和 类别数量
    features = x_train.shape[1]  # (1400, 20)
    class_nums = len(np.unique(y))

    # 返回 训练集DataSet  测试集DataSet  特征数量  类别数量
    return train_DataSet, test_DataSet, features, class_nums


def model_train(train_DataSet, test_DataSet, features, class_nums):
    # 4个准备
    # DataLoader
    train_dataloader = DataLoader(dataset=train_DataSet, batch_size=32, shuffle=True)
    # model  搭建神经网络 并实例化
    model = PhoneModel(features, class_nums).to('cuda')
    # 损失函数
    criterion = nn.CrossEntropyLoss()
    # 优化器
    optimizer = optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.99))
    # 调整学习率
    lr_scheduler = optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=0.8)

    # 2个循环-->5个步骤
    epochs = 250
    avg_loss_list = []
    model.train()
    for epoch in range(epochs):
        # 计算每轮的平均损失
        total_loss = 0.0
        iter_nums = 0.0

        for batch_x, batch_y in train_dataloader:
            batch_x = batch_x.to('cuda')
            batch_y = batch_y.to('cuda')
            # 5个步骤
            # 前向传播
            y_pred = model(batch_x)
            # 计算损失
            loss = criterion(y_pred, batch_y)
            # 梯度清零
            optimizer.zero_grad()
            # 反向传播
            loss.backward()
            # 梯度更新
            optimizer.step()
            total_loss += loss.item()
            iter_nums += 1
        # 本轮平均损失
        acg_loss = total_loss/iter_nums
        avg_loss_list.append(acg_loss)
        print(f"第{epoch+1}轮平均损失：{acg_loss}")
    lr_scheduler.step()
    # 绘制损失曲线
    plt.plot(range(epochs), avg_loss_list)
    plt.grid()
    plt.show()

    # 保存模型
    torch.save(model.state_dict(),'./model/phone_model.pth')


def valid(test_DataSet,features, class_nums):
    # 加载模型
    # 模型实例化
    model = PhoneModel(features, class_nums).to('cuda')
    # 通过文件加载模型参数
    model.load_state_dict(torch.load('./model/phone_model.pth'))

    model.eval()

    # 计算准确率
    total_samples = len(test_DataSet)
    test_dataloader = DataLoader(test_DataSet, batch_size=32,shuffle=False)
    total_right_simples = 0
    for batch_x, batch_y in test_dataloader:
        batch_x = batch_x.to('cuda')
        batch_y = batch_y.to('cuda')
        # 计算预测正确的样本数
        y_pred = model(batch_x)
        # 需要找到最大值对应的类别 才是预测的标签
        y_pred_label = torch.argmax(y_pred, dim=1)

        right_simples = (y_pred_label == batch_y).sum()
        total_right_simples += right_simples

    print(f"测试集的准确率是：{total_right_simples/total_samples}")




if __name__ == '__main__':
    train_DataSet, test_DataSet, features, class_nums = get_data()
    # print(train_DataSet[0])
    # print(test_DataSet[0])
    # print(features)
    # print(class_nums)
    # model_train(train_DataSet, test_DataSet, features, class_nums)
    #
    valid(test_DataSet,features, class_nums)




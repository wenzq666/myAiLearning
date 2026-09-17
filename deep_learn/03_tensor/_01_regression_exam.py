from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import torch.nn as nn # 封装了所以的神经网络模块，损失函数
import torch.optim as optim # 有各种优化器(各种梯度下降法)


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def create_dateset():
    x, y, coef = make_regression(
        n_samples=100,
        n_features=1,
        noise=10,
        coef=True, #返回真实权重， 后续用训练出来的模型权重和真实权重对比
        bias=14.5, # 偏置项
        random_state=0
    )
    # numpy 转 tensor
    x = torch.tensor(x,dtype = torch.float32)
    y = torch.tensor(y,dtype = torch.float32)

    return x, y, coef


def plt_show(x, y, coef):
    # 可视化展示
    # 散点图
    plt.scatter(x, y)
    # 折线图
    x_plot = torch.linspace(x.min(), x.max(), 10000)
    y_plot = x_plot * coef + 14.5
    plt.plot(x_plot, y_plot)
    plt.grid()
    plt.title("线性回归数据情况")
    plt.show()


def train(x, y):
    # 4 2 5原则 进行学习建模训练
    # 准备数据集对象 把张量x y 放到对象中统一管理 支撑dataloader的创建及遍历
    dataset = TensorDataset(x, y)
    # 支撑 DataLoader 的创建和使用
    # __getitem()__ 可以通过dataset[索引]进行访问
    # data_0 = dataset[0]
    # print(data_0)
    # # __len()__
    # print(len(dataset))

    # 准备DataLoader  根据dataset创建加载器
    # 讲dataset数据集打乱顺序 切成一批一批的数据  每一批数据用来进行模型训练和参数更新
    # batch_size一般指定为2的幂次方
    # shuffle 打乱
    data_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True)

    # 2 准备模型   搭建神经网络结构 并实例化成一个模型对象
    # in_features 输入的特征数
    # out_features 输出的特征数
    model = nn.Linear(in_features=1, out_features=1)
    print(f"模型初始化 偏置项:{model.bias}")
    print(f"模型初始化 权重:{model.weight}")

    # 3 准备损失函数
    mse_loss = nn.MSELoss()

    # 4 准备优化器
    # params 要训练的模型参数 优化器会进行管理(梯度清零，参数更新)
    # model.parameters() 获取模型参数
    # lr 学习率
    optim_sgd = optim.SGD(params=model.parameters(), lr=0.0001)


    # 二 两层循环
    # 对于从0开始的模型训练 轮次设置的大一点
    # 对于微调任务 轮次一般不超过5
    epochs = 100

    # 记录每次的平均损失
    epochs_loss_list = []

    for i in range(epochs):
        # 记录总损失 每迭代一次就进行累加
        total_loss = 0.0
        # 迭代次数
        iter_counts = 0
        for x_train, y_train in data_loader:
            # 5个步骤
            # 前向传播
            y_pred = model(x_train)

            # 根据预测和真实计算损失
            loss = mse_loss(y_pred, y_train.reshape(-1, 1))

            # loss 类型是张量  取出数字再累加
            # 累加损失
            total_loss += loss.item()

            # iter_counts
            iter_counts += 1

            # 梯度清零
            optim_sgd.zero_grad()

            # 反向传播 自动微分
            loss.backward()

            # 参数更新
            optim_sgd.step()


            print(f"{i+1}轮次迭代损失是:{loss}")

        w = model.weight.item()
        b = model.bias.item()
        # 权重梯度
        w_grad = model.weight.grad.item()
        # 偏置梯度
        b_grad = model.bias.grad.item()
        print(f"第{i+1}轮 权重 w={w:.4f}, 偏置 b={b:.4f} ，权重梯度={w_grad:.4f}, 偏置梯度={b_grad:.4f}")

        # 计算平均损失
        print(f"本轮损失{total_loss}")
        print(f"本轮迭代次数{iter_counts}")
        avg_loss = total_loss / iter_counts
        # 记录每轮的平均损失
        epochs_loss_list.append(avg_loss)

        print(f"第{i+1}轮平均损失是{avg_loss}")

    print(f"每轮的平均损失{epochs_loss_list}")

    plt.plot(range(epochs), epochs_loss_list)
    plt.title("损失变换曲线")
    plt.grid()
    plt.show()

    # 原始数据散点图
    plt.scatter(x, y)

    # 训练模型折线图
    print(f"模型训练完 偏置项:{model.bias}")
    print(f"模型训练完 权重:{model.weight}")

    x_plot = torch.linspace(x.min(), x.max(), steps=10000)
    y_plot = x_plot * model.weight + model.bias

    print(type(x_plot))
    print(type(y_plot))

    print(x_plot.requires_grad)
    print(y_plot.requires_grad)

    plt.plot(x_plot, y_plot.detach().squeeze(), label = '训练模型')

    # 真实的折线
    y_plot = x_plot * coef + 14.5
    plt.plot(x_plot, y_plot,label = '真实模型')


    plt.legend()
    plt.grid()

    plt.show()






if __name__ == '__main__':
    x, y, coef = create_dateset()
    # print(x)
    # print(y)
    # print(coef)
    # plt_show(x, y, coef)
    train(x, y)
    # print(range(1000))





































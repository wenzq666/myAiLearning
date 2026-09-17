import torch
import torch.nn as nn
from typing import Any
from torchsummary import summary

class MyModel(nn.Module):

    def __init__(self, *args: Any, **kwargs: Any):
        # 调用父类初始化
        super().__init__(*args, **kwargs)

        # 定义神经网络的各个组件
        # 从第一个隐藏层开始构建,
        # 第一个隐藏层全连接神经网络 输入层3  输出层3
        self.h_linear_1 = nn.Linear(in_features=3, out_features=3)
        # 第一层用xavier
        nn.init.xavier_normal_(self.h_linear_1.weight)

        # 第一个隐藏层全连接神经网络 输入层3  输出层2
        self.h_linear_2 = nn.Linear(in_features=3, out_features=2)
        # 第一层用kaiming
        nn.init.kaiming_normal_(self.h_linear_2.weight)

        # 输出层连接神经网络 输入层2  输出层2
        self.out_linear = nn.Linear(in_features=2, out_features=4)


    def forward(self, x):
        """
        前向传播, 重写父类forward()
        :param x:
        :return:
        """
        # 输入是 x
        h_output_1 = self.h_linear_1(x)
        # print(h_output_1)
        h_output_1_activated = torch.relu(h_output_1)
        # print(h_output_1)

        h_output_2 = self.h_linear_2(h_output_1_activated)
        h_output_2_activated = torch.sigmoid(h_output_2)

        h_output_3 = self.out_linear(h_output_2_activated)
        # output_activated = torch.softmax(h_output_3, dim=-1)

        return h_output_3



if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"==device==:{device}")


    model = MyModel().to(device)
    x_input = torch.randn(100,3).to(device)

    y_true = torch.randint(0, 3, size=(100,), dtype=torch.int64).to(device)

    y_pred = model(x_input)

    # 定义损失函数
    # 交叉熵损失函数
    loss_func = nn.CrossEntropyLoss()

    # 底层自动做了 one-hot转换  标签列数据是int64的
    loss = loss_func(y_pred, y_true)
    print(loss)




    # summary(model=model, input_size=[3,], batch_size=16)























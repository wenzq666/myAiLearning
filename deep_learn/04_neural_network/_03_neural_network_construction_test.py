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
        # 第一个隐藏层全连接神经网络 输入层3  输出层4
        self.h_linear_1 = nn.Linear(in_features=3, out_features=4)
        # 第一层用xavier
        nn.init.xavier_normal_(self.h_linear_1.weight)

        # 第一个隐藏层全连接神经网络 输入层4  输出层5
        self.h_linear_2 = nn.Linear(in_features=4, out_features=5)
        # 第一层用kaiming
        nn.init.kaiming_normal_(self.h_linear_2.weight)

        # 输出层连接神经网络 输入层5  输出层3
        self.out_linear = nn.Linear(in_features=5, out_features=3)


    def forward(self, x):
        """
        前向传播, 重写父类forward()
        :param x:
        :return:
        """
        # 输入是 x
        h_output_1 = self.h_linear_1(x)
        h_output_1_activated = torch.relu(h_output_1)

        h_output_2 = self.h_linear_2(h_output_1_activated)
        h_output_2_activated = torch.sigmoid(h_output_2)

        h_output_3 = self.out_linear(h_output_2_activated)
        output_activated = torch.softmax(h_output_3, dim=-1)

        return output_activated



if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"==device==:{device}")

    model = MyModel().to(device)
    # x_input = torch.randn(2,3)
    # y_pred = model(x_input)
    # print(y_pred)

    summary(model=model, input_size=[3,], batch_size=16)























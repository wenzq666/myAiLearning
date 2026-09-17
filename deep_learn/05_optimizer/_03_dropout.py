import torch
import torch.nn as nn


class MyModule(nn.Module):

    def __init__(self):
        super().__init__()
        # 隐藏层 1：256 个神经元，激活 ReLU
        self.h1_linear = nn.Linear(in_features=784, out_features=256)
        self.h1_dropout = nn.Dropout(p=0.9)

        # 隐藏层 2：128 个神经元，激活 ReLU
        self.h2_linear = nn.Linear(in_features=256, out_features=128)
        self.h2_dropout = nn.Dropout(p=0.95)

        # 输出层：10 个神经元，激活 Softmax
        self.out_linear = nn.Linear(in_features=128, out_features=10)


    def forward(self, x):
        # 隐藏层 1：256 个神经元，激活 ReLU
        h1_output_dropout = self.h1_dropout(torch.relu(self.h1_linear(x)))
        # print(h1_output_dropout)

        # 隐藏层 2：128 个神经元，激活 ReLU
        h2_output_dropout = self.h2_dropout(torch.relu(self.h2_linear(h1_output_dropout)))
        # print(h2_output_dropout)

        # 输出层：10 个神经元，激活 Softmax
        return torch.softmax(self.out_linear(h2_output_dropout), dim=-1)


if __name__ == '__main__':
    model = MyModule()
    # model.eval()

    x = torch.randn(3, 784)

    y_pred = model(x)
    print(y_pred)







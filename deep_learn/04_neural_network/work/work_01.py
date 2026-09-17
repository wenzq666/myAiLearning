"""
现有一个手写体识别的10分类任务,
就是将一张手写字图片识别出0-9中的一个数字,
数据的输入特征数是784, 对应的是28×28像素点的一张图片, 请根据如下神经网络结构的要求,
搭建一个全连接神经网络.
**神经网络结构:**
- 输入：784 维展平像素（28×28=784）
- 隐藏层 1：256 个神经元，激活 ReLU
- 隐藏层 2：128 个神经元，激活 ReLU
- 输出层：10 个神经元，激活 Softmax
"""
# 一个继承, 两个方法搭建神经网络
import torch
import torch.nn as nn


class HandNumberModule(nn.Module):

    def __init__(self):
        super().__init__()
        # 隐藏层 1：256 个神经元，激活 ReLU
        self.h1_linear = nn.Linear(in_features=784, out_features=256)

        # 隐藏层 2：128 个神经元，激活 ReLU
        self.h2_linear = nn.Linear(in_features=256, out_features=128)

        # 输出层：10 个神经元，激活 Softmax
        self.out_linear = nn.Linear(in_features=128, out_features=10)


    def forward(self, x):
        # 隐藏层 1：256 个神经元，激活 ReLU
        h1_output_activated = torch.relu(self.h1_linear(x))

        # 隐藏层 2：128 个神经元，激活 ReLU
        h2_output_activated = torch.relu(self.h2_linear(h1_output_activated))

        # 输出层：10 个神经元，激活 Softmax
        return torch.softmax(self.out_linear(h2_output_activated), dim=-1)




















































































































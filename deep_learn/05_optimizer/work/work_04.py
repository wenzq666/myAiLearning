"""
请在下方的 Python 代码块中，补全代码以验证：同一个输入在训练模式下和测试模式下经过 Dropout 层后的输出差异。
"""
import torch
import torch.nn as nn

# 1. 创建一个形状为 (1, 5) 的全 1 张量作为输入
inputs = torch.ones(1, 5)
print("输入数据:", inputs)

# TODO: 2. 定义一个 Dropout 层，失活概率 p=0.4
dropout = nn.Dropout(p=0.4)

# TODO: 3. 将模型设置为训练模式(提示: dropout.train())，并打印输出结果
dropout.train()
out_with_drop = dropout(inputs)
print(out_with_drop)

# TODO: 4. 将模型设置为评估模式（提示:dropout.eval()），并打印输出结果
dropout.eval()
out_without_drop = dropout(inputs)
print(out_without_drop)
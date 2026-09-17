"""
### 第四题：目标检测边界框回归（CV回归任务）

**场景背景**：
在目标检测任务中，除了分类，还需要精确定位物体的边界框。
假设我们通过模型特征预测边界框的2个偏移量 $(dx, dy)$。
为了让模型在预测产生较大偏差时不易梯度爆炸，且在微调时更平滑，我们选择使用 Smooth L1 损失函数。

请在已有代码的基础上, 补全损失函数, 以及模型训练的两层循环逻辑
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import SmoothL1Loss
from torch.utils.data import Dataset, DataLoader


# 1. 模拟构建数据集
class BBoxDataset(Dataset):
    def __init__(self):
        # 模拟80个样本，每个样本8维特征
        self.x = torch.randn(80, 8)
        # 真实的2维边界框偏移量
        self.y = torch.randn(80, 2)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


# 2. 构建DataLoader
dataset = BBoxDataset()
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)


# 3. 定义回归模型
class BBoxRegressor(nn.Module):
    def __init__(self):
        super(BBoxRegressor, self).__init__()
        self.fc = nn.Linear(8, 2)

    def forward(self, x):
        return self.fc(x)


model = BBoxRegressor()

# ==================== TODO 留空部分 ====================
# TODO 1. 初始化Smooth L1损失函数
criterion = SmoothL1Loss()

# 2.  (这里已完成) 初始化RMSprop优化器，设置学习率为0.01
optimizer = optim.RMSprop(model.parameters(), lr=0.01)
# =======================================================

# 4. 训练循环
epochs = 3
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        # ==================== TODO 留空部分 ====================
        # TODO 3: 步骤一 - 前向传播
        y_pred = model(batch_x)

        # TODO 4: 步骤二 - 计算损失
        loss = criterion(y_pred, batch_y)

        # TODO 5: 步骤三 - 梯度清零
        optimizer.zero_grad()

        # TODO 6: 步骤四 - 反向传播
        loss.backward()

        # TODO 7: 步骤五 - 参数更新
        optimizer.step()

        # =======================================================
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
"""
**场景背景**：
某电商平台需要对上架的商品图像进行自动分类。
图像特征提取器会将每张图片转化为16维的特征向量，目标是将商品分到3个类别中
（如：0表示衣服，1表示鞋子，2表示包包）。这是一个多分类任务。

请在已有代码的基础上, 补全损失函数, 以及模型训练的两层循环逻辑
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import CrossEntropyLoss
from torch.utils.data import Dataset, DataLoader


# 1. 模拟构建数据集
class FashionDataset(Dataset):
    def __init__(self):
        # 模拟120个样本，每个样本16维特征
        self.x = torch.randn(120, 16)
        # 随机生成0, 1, 2三种类别标签，类型为long
        self.y = torch.randint(0, 3, (120,)).long()

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


# 2. 构建DataLoader
dataset = FashionDataset()
dataloader = DataLoader(dataset, batch_size=20, shuffle=True)


# 3. 定义多分类模型（输出层不加softmax，因为CrossEntropyLoss内部会处理）
class MultiClassifier(nn.Module):
    def __init__(self):
        super(MultiClassifier, self).__init__()
        self.fc = nn.Linear(16, 3)

    def forward(self, x):
        return self.fc(x)


model = MultiClassifier()

# ==================== TODO 留空部分 ====================
# TODO 1. 初始化多分类交叉熵损失函数
criterion = CrossEntropyLoss()

# 2.  (这里已完成) 初始化Adam优化器，设置学习率为0.005, betas设置为(0.9,0.95)
optimizer = optim.Adam(model.parameters(), betas=(0.9, 0.95), lr=0.01)
# =======================================================

# 4. 训练循环
epochs = 3
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        # ==================== TODO 留空部分 ====================
        # TODO 3: 步骤一 - 前向传播
        y_pred = model(batch_x)

        # TODO 4: 步骤二 - 计算损失值
        loss = criterion(y_pred, batch_y)

        # TODO 5: 步骤三 - 梯度清零
        optimizer.zero_grad()

        # TODO 6: 步骤四 - 反向传播
        loss.backward()

        # TODO 7: 步骤五 - 更新参数
        optimizer.step()

        # =======================================================
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
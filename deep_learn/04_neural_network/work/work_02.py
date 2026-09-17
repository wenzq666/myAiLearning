"""
### 第二题：工业零件缺陷检测（CV二分类任务）
**场景背景**：
在智能制造工业流水线上，需要通过相机拍摄零件图像并提取出1 0维的特征向量，
以此来判断零件是否合格（0表示合格，1表示有缺陷）。这是一个典型的二分类任务。

请在已有代码的基础上, 补全损失函数, 以及模型训练的两层循环逻辑.
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


# 1. 模拟构建数据集
class DefectDataset(Dataset):
    def __init__(self):
        # 模拟100个样本，每个样本10维特征
        self.x = torch.randn(100, 10)
        # 随机生成0或1的标签，并转换为float类型以适配BCELoss
        self.y = torch.randint(0, 2, (100, 1)).float()

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


# 2. 构建DataLoader
dataset = DefectDataset()
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)


# 3. 定义一个简单的二分类模型
class BinaryClassifier(nn.Module):
    def __init__(self):
        super(BinaryClassifier, self).__init__()
        self.linear = nn.Linear(10, 1)
        self.sigmoid = nn.Sigmoid()  # BCELoss前需要通过Sigmoid激活函数

    def forward(self, x):
        return self.sigmoid(self.linear(x))


model = BinaryClassifier()

# ==================== TODO 留空部分 ====================
# TODO 1. 初始化二分类交叉熵损失函数
criterion = nn.BCELoss()

# 2. (这里已完成) 初始化SGD优化器，设置学习率为0.01，动量(momentum)为0.9
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
# =======================================================

# 4. 开始模型训练循环
epochs = 3
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        # ==================== TODO 留空部分 ====================
        # TODO 3: 步骤一 - 前向传播计算预测值
        y_pred = model(batch_x)

        # TODO 4: 步骤二 - 计算损失值
        loss = criterion(y_pred, batch_y)

        # TODO 5: 步骤三 - 梯度清零
        optimizer.zero_grad()

        # TODO 6: 步骤四 - 反向传播计算梯度
        loss.backward()

        # TODO 7: 步骤五 - 更新模型参数
        optimizer.step()

        # =======================================================
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
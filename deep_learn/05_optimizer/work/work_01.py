"""
**业务背景**
某商业银行希望构建一个自动化风险评估系统，根据客户的基本信息（如年龄、年收入、负债比率、信用历史长度、现有贷款数量等）
将其划分为三类风险等级：
- **0**：低风险（优质客户）
- **1**：中等风险（一般客户）
- **2**：高风险（潜在违约客户）

文本数据已经处理好, 是经过预训练模型后转换为了15维的特征向量。

请在已有代码的基础上, 补全损失函数, 优化器, 以及模型训练的两层循环逻辑
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import CrossEntropyLoss
from torch.utils.data import Dataset, DataLoader


# 1. 模拟构建数据集（200个样本，每个样本15维特征，3类标签）
class CreditDataset(Dataset):
    def __init__(self):
        self.x = torch.randn(200, 15)  # 特征
        self.y = torch.randint(0, 3, (200,))  # 标签 0,1,2

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


# 2. 构建 DataLoader
dataset = CreditDataset()
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)


# 3. 定义风险等级分类器（单层线性）
class RiskClassifier(nn.Module):
    def __init__(self):
        super(RiskClassifier, self).__init__()
        self.fc = nn.Linear(15, 3)  # 输入15维，输出3类

    def forward(self, x):
        return self.fc(x)


model = RiskClassifier().to('cuda')

# ==================== TODO 留空部分 ====================
# TODO 1. 初始化多分类交叉熵损失函数
criterion = CrossEntropyLoss()

# TODO 2. 初始化 Adam 优化器，学习率设为 0.001, 指定两个β系数分别为0.9与0.99
optimizer = optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.99))

# 4. 训练循环
epochs = 10
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to('cuda')
        batch_y = batch_y.to('cuda')
        # ==================== TODO 留空部分 ====================
        # TODO 3. 前向传播
        outputs = model(batch_x)

        # TODO 4. 计算损失
        loss = criterion(outputs, batch_y)

        # TODO 5. 梯度清零
        optimizer.zero_grad()

        # TODO 6. 反向传播
        loss.backward()

        # TODO 7. 更新模型参数
        optimizer.step()

        # =======================================================

    print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
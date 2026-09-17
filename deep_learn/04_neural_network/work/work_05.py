"""
### 第五题：电影评论情感分类（NLP场景）

**场景背景**：
我们需要对电影评论进行情感倾向分类（共4个情感级别：0至3）。
文本数据已经处理好, 是经过预训练模型后转换为了32维的句向量。

请在已有代码的基础上, 补全损失函数, 以及模型训练的两层循环逻辑
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import CrossEntropyLoss
from torch.utils.data import Dataset, DataLoader


# 1. 模拟构建数据集
class ReviewDataset(Dataset):
    def __init__(self):
        # 模拟150个样本，每个样本32维文本特征向量
        self.x = torch.randn(150, 32)
        # 4个情感级别分类标签
        self.y = torch.randint(0, 4, (150,)).long()

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


# 2. 构建DataLoader
dataset = ReviewDataset()
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)


# 3. 定义文本分类器
class TextClassifier(nn.Module):
    def __init__(self):
        super(TextClassifier, self).__init__()
        self.fc = nn.Linear(32, 4)

    def forward(self, x):
        return self.fc(x)


model = TextClassifier()

# ==================== TODO 留空部分 ====================
# TODO 1. 初始化多分类交叉熵损失函数
criterion = CrossEntropyLoss()

# 2.  (这里已完成) 初始化Adam优化器，设置学习率为1e-2, betas=(0.9,0.99)
optimizer = optim.Adam(model.parameters(), lr=1e-2, betas=(0.9,0.99))

# 4. 训练循环
epochs = 10
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        # ==================== TODO 留空部分 ====================
        # TODO 3: 步骤一 - 前向传播
        y_pred = model(batch_x)#

        # TODO 4: 步骤二 - 计算损失
        loss = criterion(y_pred, batch_y)

        # TODO 5: 步骤三 - 梯度清零
        optimizer.zero_grad()

        # TODO 6: 步骤四 - 反向传播
        loss.backward()

        # TODO 7: 步骤五 - 更新模型参数
        optimizer.step()

        # =======================================================

        # =======================================================
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
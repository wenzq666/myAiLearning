"""
**场景背景**：
我们需要对电影评论进行情感倾向分类（共4个情感级别：0至3）。
文本经过预训练模型后转换为了32维的句向量。
由于训练后期模型容易在最优点附近震荡，我们希望使用“等间隔学习率衰减(StepLR)”方法，在每过2个Epoch后，将学习率降低为原来的一半。
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt


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
dataloader = DataLoader(dataset, batch_size=30, shuffle=True)


# 3. 定义文本分类器
class TextClassifier(nn.Module):
    def __init__(self):
        super(TextClassifier, self).__init__()
        self.fc = nn.Linear(32, 4)

    def forward(self, x):
        return self.fc(x)


model = TextClassifier().to('cuda')

#  初始化多分类交叉熵损失函数
criterion = nn.CrossEntropyLoss()

# ==================== TODO 留空部分 ====================
# TODO 1.
# 初始化RmsProp优化器，设置学习率为1e-2, β系数为0.9
optimizer = optim.RMSprop(model.parameters(), lr=1e-2, alpha=0.9)

# TODO 2. 初始化等间隔学习率衰减器(StepLR)，设置每过2个epoch(step_size=2)学习率乘以0.5(gamma=0.5)
scheduler = optim.lr_scheduler.StepLR(optimizer=optimizer, step_size=2, gamma= 0.5)
# =======================================================

# 4. 训练循环
current_lr_list = []
epochs = 100
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        batch_x = batch_x.to('cuda')
        batch_y = batch_y.to('cuda')
        # ==================== TODO 留空部分 ====================
        # 步骤一 - 前向传播
        y_pred = model(batch_x)

        # 步骤二 - 计算损失
        loss = criterion(y_pred, batch_y)

        # 步骤三 - 梯度清零
        optimizer.zero_grad()

        # 步骤四 - 反向传播
        loss.backward()

        # 步骤五 - 更新模型参数
        optimizer.step()

    # 获取当前Epoch更新前的学习率，用于打印观察
    current_lr = scheduler.get_last_lr()[0]
    current_lr_list.append(current_lr)

    # ==================== TODO 留空部分 ====================
    # TODO 3: 每一个epoch结束后，更新学习率衰减器的状态
    scheduler.step()

    # =======================================================
    print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}, LR: {current_lr:.4f}")

plt.plot(range(epochs), current_lr_list)
plt.grid()
plt.show()

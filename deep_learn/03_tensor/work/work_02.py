import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 已知数据 ----------
torch.manual_seed(42)
true_w = torch.tensor([[2.1], [1.8], [2.5], [-1.2]])  # 真实权重
true_b = 8.5
x = torch.randn(150, 4) * 1.5
y = x @ true_w + true_b + torch.randn(150, 1) * 2.0


# ---------- 已定义的网络类和实例化模型 ----------
class SalesPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ---------- 请补全以下训练代码 ----------

# 4 准备
# 1) 数据加载器
# TODO: 创建 TensorDataset 和 DataLoader
dataset = TensorDataset(x, y)

dataloader = DataLoader(dataset=dataset, batch_size=16, shuffle=True)


# 2) 模型实例化, 已做好
model = SalesPredictor()

# 3) 损失函数（MSE）
# TODO: 定义损失
mse_loss = nn.MSELoss()

# 4) 优化器（SGD，学习率设为 1e-2，因为网络较深可以适当调大）
# TODO: 定义优化器
optim_sgd = optim.SGD(params=model.parameters(), lr=1e-2)

# 2 层循环
epochs = 500
train_losses = []

for epoch in range(epochs):
    batch_loss_sum = 0.0
    steps = 0
    for x_batch, y_batch in dataloader:
        # 5 步法
        # 1) 前向传播
        # TODO: pred = ?
        y_pred = model(x_batch)
        # 2) 计算损失
        # TODO: loss = ?
        loss = mse_loss(y_pred, y_batch.reshape(-1, 1))
        # 3) 梯度清零
        # TODO: optimizer.zero_grad()
        optim_sgd.zero_grad()
        # 4) 反向传播
        # TODO: loss.backward()
        loss.backward()
        # 5) 更新参数
        # TODO: optimizer.step()
        optim_sgd.step()
        batch_loss_sum += loss.item()
        steps += 1

    avg_epoch_loss = batch_loss_sum / steps
    train_losses.append(avg_epoch_loss)
    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_epoch_loss:.4f}")

# 绘制损失曲线
# TODO: 绘制 train_losses，添加标题、网格
plt.plot(range(epochs), train_losses)
plt.title("损失变换曲线")
plt.grid()
plt.show()



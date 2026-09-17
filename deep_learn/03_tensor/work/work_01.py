import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 已知数据（张量形式）----------
torch.manual_seed(0)
# 真实关系: y = 2.0*x1 - 1.5*x2 - 0.8*x3 - 1.2*x4 + 15 + 噪声
x = torch.randn(200, 4) * 2
y = (2.0 * x[:, 0:1] - 1.5 * x[:, 1:2] - 0.8 * x[:, 2:3] - 1.2 * x[:, 3:4] + 15
     + torch.randn(200, 1) * 1.5)


# ---------- 已定义的全连接网络类及实例化 ----------
class HousePriceModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ---------- 请补全以下训练代码 ----------

# 4 个准备工作
# 1) 准备数据集对象和 DataLoader
# TODO: 创建 TensorDataset 和 DataLoader
dataset = TensorDataset(x, y)

dataloader = DataLoader(dataset=dataset, batch_size=32, shuffle=True)

# 2) 模型实例化, 已做好
model = HousePriceModel()

# 3) 准备损失函数（回归任务使用均方误差）
# TODO: 定义 MSELoss
mse_loss = nn.MSELoss()

# 4) 准备优化器（使用 SGD，学习率设为 1e-3）
# TODO: 定义 optim.SGD
optim_sgd = optim.SGD(params=model.parameters(), lr=1e-3)

# 2 层循环
epochs = 600
loss_list = []

for epoch in range(epochs):
    total_loss = 0.0
    iter_count = 0

    # 内层循环遍历 DataLoader
    for x_batch, y_batch in dataloader:
        # 5 个核心步骤
        # 1) 前向传播得到预测值
        # TODO: y_pred = ?
        y_pred = model(x_batch)

        # 2) 计算损失（注意 y_batch 形状为 (batch, 1)，y_pred 也是 (batch, 1)）
        # TODO: loss = ?
        loss = mse_loss(y_pred, y_batch.reshape(-1, 1))
        # 3) 梯度清零
        # TODO:
        optim_sgd.zero_grad()
        # 4) 反向传播
        # TODO:
        loss.backward()
        # 5) 参数更新
        # TODO:
        optim_sgd.step()
        total_loss += loss.item()
        iter_count += 1

    avg_loss = total_loss / iter_count
    loss_list.append(avg_loss)
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, 平均损失: {avg_loss:.4f}")

# 绘制损失变化曲线
# TODO: 使用 plt.plot() 绘制 loss_list，添加标题、网格
plt.plot(range(epochs), loss_list)
plt.title("损失变换曲线")
plt.grid()
plt.show()
# 绘制预测值 vs 真实值折线图（评估模型整体表现）
# TODO: 使用plt.scatter()绘制真实数据散点图, plt.plot()绘制训练模型折线图, plt.plot()绘制真实模型折线图
# 绘制预测值 vs 真实值散点图（评价拟合效果）
model.eval()
with torch.no_grad():
    y_pred_all = model(x)  # 全部数据的预测值

plt.subplot(1, 2, 2)
plt.scatter(y.numpy(), y_pred_all.numpy(), label='预测 vs 真实')
# 绘制理想参考线 (y=x)
min_val = min(y.min().item(), y_pred_all.min().item())
max_val = max(y.max().item(), y_pred_all.max().item())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='理想拟合 (y=x)')
plt.xlabel('真实房价 (万元)')
plt.ylabel('预测房价 (万元)')
plt.title('预测值与真实值散点对比')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
















































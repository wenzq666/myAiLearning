import torch
import torch.nn as nn
from torchsummary import summary


# -------------------- 待补全的模型定义 --------------------
class MyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # ========== TODO 请在此处补全网络层的定义 ==========
        # 提示：使用 nn.Conv2d, nn.MaxPool2d, nn.Flatten, nn.Linear
        self.conv_1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=0) # 32 * 26 * 26
        self.pool_1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)  # 32 * 13 * 13

        self.conv_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=0)
        self.pool_2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0) # 64 * 5 * 5

        self.flat = nn.Flatten()

        self.liner_1 = nn.Linear(in_features=1600,out_features=256)

        self.out = nn.Linear(in_features=256, out_features=10)
        # 参数严格按照上方架构图指定

    def forward(self, x):
        # ==========  TODO 请在此处补全前向传播逻辑 ==========
        # 提示：按顺序应用各层，注意激活函数（torch.relu）
        # 展平操作：x = self.flatten(x)
        conv_result_1 = torch.relu(self.conv_1(x))
        pool_result_1 = self.pool_1(conv_result_1)

        conv_result_2 = torch.relu(self.conv_2(pool_result_1))
        pool_result_2 = self.pool_2(conv_result_2)

        linear_result_1 = torch.relu(self.liner_1(self.flat(pool_result_2)))
        return self.out(linear_result_1)


# -------------------- 主程序 --------------------
if __name__ == '__main__':
    model = MyCNN().to('cuda')
    summary(model, input_size=(3, 28, 28), batch_size=1, device='cuda')
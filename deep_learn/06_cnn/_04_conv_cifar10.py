import torch
from sklearn.preprocessing import StandardScaler
from torchvision.datasets import CIFAR10
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import torch.nn as nn
from torchsummary import summary
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim


def create_dataset():
    train = CIFAR10(root='./data', train=True, transform=ToTensor())
    test = CIFAR10(root='./data', train=False, transform=ToTensor())


    return train, test


class ImageModel(nn.Module):
    def __init__(self):
        super().__init__()

        # 第一个卷积层
        self.conv_1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.norm_1 = nn.BatchNorm2d(num_features=16)

        # 第一个池化层
        self.pool_1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)


        # 加一层 #######################################################
        # 第二个卷积层
        self.conv_2_in= nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.norm_2_in = nn.BatchNorm2d(num_features=32)

        # 第二个池化层
        self.pool_2_in = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        ###############################################################

        # 第二个卷积层
        self.conv_2= nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.norm_2 = nn.BatchNorm2d(num_features=64)

        # 第二个池化层
        self.pool_2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # 第一个全连接
        self.linear_1 = nn.Linear(in_features=4096, out_features=2304)
        # self.h1_drop = nn.Dropout(0.3)


        # 后加入层
        self.linear_in_1 = nn.Linear(in_features=2304, out_features=1152)
        # self.h1_in_drop = nn.Dropout(0.3)

        # 第二个全连接层
        self.linear_2 = nn.Linear(in_features=1152, out_features=576)
        self.h2_drop = nn.Dropout(0.4)

        # 第二个后加入层
        self.linear_in_2 = nn.Linear(in_features=576, out_features=288)
        self.h2_in_drop = nn.Dropout(0.5)

        self.out = nn.Linear(in_features=288, out_features=10)

        # 展平
        self.flat = nn.Flatten()


    def forward(self, x):
        conv_result_1 = torch.relu(self.norm_1(self.conv_1(x)))
        pool_result_1 = self.pool_1(conv_result_1)

        conv_result_2_in = torch.relu(self.norm_2_in(self.conv_2_in(conv_result_1)))
        pool_result_2_in = self.pool_2_in(conv_result_2_in)

        conv_result_2 = torch.relu(self.norm_2(self.conv_2(pool_result_2_in)))
        pool_result_2 = self.pool_2(conv_result_2)

        # 全连接层输入需要把 pool_result_2 展平
        # print(self.flat(pool_result_2).shape)
        # a = input()
        linear_result_1 = torch.relu(self.linear_1(self.flat(pool_result_2)))

        linear_result_in_1 = torch.relu(self.linear_in_1(linear_result_1))

        linear_result_2 = self.h2_drop(torch.relu(self.linear_2(linear_result_in_1)))

        linear_result_3 = self.h2_in_drop(torch.relu(self.linear_in_2(linear_result_2)))

        return self.out(linear_result_3)


class CifarGPU(Dataset):
    def __init__(self, dataset, device='cuda'):

        """
        初始化函数，将整个数据集加载到指定设备(GPU)上
        Args:
            dataset: 输入的数据集，应该是torch.utils.data.Dataset的子类
            device: 指定设备，默认为'cuda'，表示使用GPU
        """
        # 一次性把所有数据搬到 GPU，使用torch.stack将图像堆叠成一个张量，并移动到指定设备
        self.data = torch.stack([img for img, _ in dataset]).to(device)
        # 将数据集的目标标签转换为张量，并移动到指定设备
        self.targets = torch.tensor(dataset.targets, device=device)

    def __len__(self):
        """
        返回数据集的大小
        Returns:
            int: 数据集中样本的数量
        """
        return len(self.targets)

    def __getitem__(self, idx):
        """
        获取指定索引的数据项
        Args:
            idx (int): 要获取的数据项的索引
        Returns:
            tuple: 包含图像数据和对应标签的元组
        """
        return self.data[idx], self.targets[idx]


def model_train():
    ## 4 2 5
    ## 4 准备
    # 准备DataLoader
    gpu_train = CifarGPU(train_dataset)
    # print(len(gpu_train))
    # a = input()
    dataloader = DataLoader(gpu_train, batch_size=256, shuffle=True)

    # 准备模型
    model = ImageModel().to('cuda')

    # 准备损失函数
    criterion = nn.CrossEntropyLoss()

    # 准备优化器
    optimizer = optim.Adam(model.parameters(), lr=1e-3, betas=(0.9,0.98), weight_decay=5e-4)
    lr_scheduler = optim.lr_scheduler.StepLR(optimizer=optimizer, step_size = 5, gamma=0.87)

    ## 2 循环
    epochs = 10


    for epoch in range(epochs):
        total_loss = 0.
        inet_nums = 0.
        right_total = 0
        for batch_x, batch_y in dataloader:
            # batch_x = batch_x.to('cuda', non_blocking=True)
            # batch_y = batch_y.to('cuda', non_blocking=True)

            ## 5 步骤
            # 前向传播
            y_pred = model(batch_x)

            y_pred_labels = torch.argmax(y_pred, dim=-1)
            right_samples = (y_pred_labels == batch_y).sum()
            right_total += right_samples

            # 损失计算
            loss = criterion(y_pred, batch_y)

            # 梯度清零
            optimizer.zero_grad()

            # 反向传播
            loss.backward()

            # 参数更新
            optimizer.step()

            total_loss += loss.item()
            inet_nums += 1

        print(f"第{epoch+1}轮平均损失：{total_loss/inet_nums}")

        lr_scheduler.step()

        print(f"第{epoch+1}轮训练集准确率{right_total/len(train_dataset)}")
    torch.save(model.state_dict(), "./model/image.pth")



def model_valid():

    model = ImageModel().to('cuda')
    model.load_state_dict(torch.load("./model/image.pth"))

    model.eval()

    dataloader_test = DataLoader(dataset=test_dataset,batch_size=32,shuffle=False)

    total_sets = len(test_dataset)
    right_total = 0

    for batch_x, batch_y in dataloader_test:
        batch_x = batch_x.to('cuda')
        batch_y = batch_y.to('cuda')

        y_pred = model(batch_x)

        y_pred_labels = torch.argmax(y_pred, dim=-1)

        right_samples = (y_pred_labels == batch_y).sum()
        right_total += right_samples
    print(f"正确率:{right_total/total_sets}")


from torch.utils.tensorboard import SummaryWriter

def view():
    model = ImageModel()
    model.eval()  # 建议加上，避免 dropout/batchnorm 在 trace 时的干扰

    writer = SummaryWriter('./logs')
    x = torch.randn(1, 3, 32, 32)
    try:
        writer.add_graph(model, x)
        print("add_graph 成功")
    except Exception as e:
        print("add_graph 失败:", e)
    writer.flush()  # 显式刷一下
    writer.close()


def plot_filters(layer, n=16):
    filters = layer.weight.data.cpu()
    fig, axes = plt.subplots(1, n, figsize=(15, 3))
    for i in range(n):
        f = filters[i]  # 第 i 个卷积核
        f = (f - f.min()) / (f.max() - f.min())  # 归一化
        axes[i].imshow(f.permute(1, 2, 0))  # RGB 卷积核
        axes[i].axis('off')
    plt.show()

if __name__ == '__main__':
    train_dataset, test_dataset = create_dataset()

    # plt.imshow(train_dataset.data[555])
    #
    # plt.title(train_dataset.targets[555])
    #
    # plt.show()
    model = ImageModel()
    # summary(model, input_size=(3, 32, 32), batch_size=1, device='cuda')

    # model_train()
    # model_valid()

    # view()
    plot_filters(model.conv_1)

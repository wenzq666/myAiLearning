import torch
import torch.nn as nn
import matplotlib.pyplot as plt


img = plt.imread("./data/img.png")
print(img.shape) # (500:高, 507:宽, 3:通道)
# 维度交换 (500:高, 507:宽, 3:通道) -- > (batch_size, channel, height, width)
# 转张量
img = torch.tensor(img)
# 维度交换
img = torch.permute(img, dims = (2, 0, 1))
print(img.shape)
# 升维
img = torch.unsqueeze(img, dim = 0)
print(img.shape) # torch.Size([1, 3, 500, 507])

# 平面图像 3维数据(H, W, C)
"""
    参数
        1. in_channels 输入数据的通道数
        2. out_channels 输出数据的通道数, 有几个卷积核就是几个通道
        3. kernel_size 卷积核大小, 高和宽一般相等
        4. stride 滑动步长  默认1
        5. padding 补齐圈数 
    形状
        对于Conv2d, 输入数据是四维张量(batch_size, channel, height, width)
"""
conv = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=5, stride=1, padding=0)

conv_result = conv(img)
print(type(conv_result)) # <class 'torch.Tensor'>
print(conv_result.shape) # torch.Size([1, 3, 496, 503])

print('*'*50)

# 卷积层的输出 作为池化层的输入
#pool = nn.MaxPool2d(kernel_size=4, stride=2, padding=0)
pool = nn.AvgPool2d(kernel_size=4, stride=2, padding=0)
pool_result = pool(conv_result)
print(type(pool_result)) # <class 'torch.Tensor'>
print(pool_result.shape) # torch.Size([1, 3, 247, 250])



# 卷积后图像
img_conv = pool_result[0] # 第一张图片
# 3, 496, 503
print(img_conv.shape)

img_conv = torch.permute(img_conv, dims = (1, 2, 0)).detach()
plt.imshow(img_conv)
plt.show()












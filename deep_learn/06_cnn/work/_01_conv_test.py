import torch
import torch.nn as nn
import matplotlib.pyplot as plt


# 读取图片
img = plt.imread("../data/img.png")
print(img.shape) # (500, 507, 3)

# 转张量
img = torch.tensor(img).to('cuda')
print(type(img)) # <class 'torch.Tensor'>
print(img.shape) # torch.Size([500, 507, 3])
# 维度交换 -- > (batch_size, channel, height, width)
img = torch.permute(img, dims=(2, 0, 1))
# 升1维
img = torch.unsqueeze(img, dim = 0)
print(img.shape) # torch.Size([1, 3, 500, 507])

# 卷积层  ((500 - 5) / 1 ) + 1 = 496    ((507 - 5) / 1 ) + 1 = 503
conv = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=5, padding=0, stride=1, device='cuda')
conv_result = conv(img)
print(conv_result.shape) # torch.Size([1, 3, 496, 503])

# 池化层  (496 -5 / 2 ) + 1 = 264      (503 -5 / 2 ) + 1 = 250
pool = nn.MaxPool2d(kernel_size=5, stride=13, padding=0)
pool_result = pool(conv_result)
print(pool_result.shape) # torch.Size([1, 3, 246, 250])


pool_img = pool_result[0]
pool_img = torch.permute(pool_img, dims = (1, 2, 0)).cpu().detach()
min_val = pool_img.min()
max_val = pool_img.max()
if max_val > min_val:
    pool_img_normalized = (pool_img - min_val) / (max_val - min_val)
else:
    # 如果所有像素值都一样（比如全0），直接设为0
    pool_img_normalized = torch.zeros_like(pool_img)
plt.imshow(pool_img_normalized)
plt.imsave("../data/img_2.png",pool_img_normalized.numpy().copy())
plt.show()




















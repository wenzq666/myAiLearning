import numpy as np
import matplotlib.pyplot as plt
import torch

# p = np.linspace(0.01, 0.99, 500)
#
# L  = - np.log(p)          # 失函数
# dL = - 1 / p              # 对 p 的导数
#
# # 对 logits 的梯度（二分类：z 为正确类 logit，p = sigmoid(z)）
# z = np.linspace(-8, 8, 500)
# pz = 1 / (1 + np.exp(-z))
# grad_z = pz - 1          # y = 1 时, dL/dz = p - y
#
# fig, axes = plt.subplots(1, 3, figsize=(16, 4))
#
# axes[0].plot(p, L, 'b')
# axes[0].set_title(r'Loss  $L(p) = -\log(p)$')
# axes[0].set_xlabel('p (prob of correct class)')
# axes[0].set_ylabel('Loss')
# axes[0].grid(alpha=0.3)
#
# axes[1].plot(p, dL, 'r')
# axes[1].set_title(r'$dL/dp = -1/p$')
# axes[1].set_xlabel('p')
# axes[1].grid(alpha=0.3)
#
# axes[2].plot(z, grad_z, 'g')
# axes[2].set_title(r'$dL/dz = p - y$  (y=1)')
# axes[2].axhline(0, color='gray', lw=0.5)
# axes[2].set_xlabel('logit z')
# axes[2].grid(alpha=0.3)
#
# plt.tight_layout()
# plt.show()


print(torch.log(torch.tensor(0.99)))

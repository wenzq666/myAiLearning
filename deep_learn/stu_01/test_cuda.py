import time

import torch


print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))


x = torch.rand(8000, 8000, device='cuda')
# while True:
#     y = x @ x          # 不停做矩阵乘法，GPU 就一直处于满载状态

s_time = time.time()
for i in range(100):
    print(i)
    y = x @ x
# time.sleep(1)
print(time.time() - s_time)

# 0.0710611343383789

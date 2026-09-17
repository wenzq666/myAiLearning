import torch


# 矩阵乘法  第一个矩阵的列 = 第二个矩阵的行 @
t1 = torch.tensor([[1,2],[3,4]], dtype=torch.float32, device='cuda')
t2 = torch.tensor([[5,6,7],[8,9,0]], dtype=torch.float32, device='cuda')

t3 = t1 @ t2
t4 = t1.matmul(t2)
t5 = torch.matmul(t1, t2)
print(t3)
print(t4)
print(t5)


print('$'*50)
r1 = torch.randn(5, 3,device='cuda')
r2 = torch.randn(3, 10,device='cuda')

print(r1 @ r2)












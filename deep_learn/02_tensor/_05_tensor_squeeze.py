import torch


t1 = torch.tensor([[1,2,3],[4,5,6]])
print(t1)
print(t1.shape)

# 升维
# dim=0 新张量在前加一个大小为1的维度
t2 = t1.unsqueeze(dim=0) # (1,2,3)
print(t2)
print(t2.shape)

t3 = t1.unsqueeze(dim=1) # (2,1,3)
print(t3)
print(t3.shape)


t4 = t1.unsqueeze(dim=2) # (2,3,1)
print(t4)
print(t4.shape)

print('*'*50)
# 降维
t5 = torch.randn(size=(1,2,1,3,6,1))
t6 = t5.squeeze()
print(t6)
print(t6.shape)













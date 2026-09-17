import torch


torch.manual_seed(88)

# cat() 拼接多个张量   不增加维度, 在指定的dim上叠加  除了dim可以不通 其他位子维度得相同
t1 = torch.randint(0,10,size=(1,2,3))
t2 = torch.randint(0,10,size=(2,2,3))
print(t1)
print(t2)
print('===============================')
t3 = torch.cat([t1,t2],dim=0)
print(t3.shape)
print(t3)


print('*'*50)

# stack() 拼接多个张量 会增加维度 在指定dim上增加一个维度 形状大小是拼接张量的个数
# 各个张量的形状大小必须一致
t5 = torch.randint(0,10,size=(1,2,3))
t6 = torch.randint(0,10,size=(1,2,3))
print(t5)
print(t6)
print('===============================')
t7 = torch.stack([t5,t6],dim=3)
print(t7.shape)
print(t7)


print('#'*50)
tr1 = torch.randint(0,10,size=(3,5))
tr2 = torch.randint(0,10,size=(3,5))

tr_new_1 = torch.cat([tr1,tr2],dim=0)
print(tr_new_1.shape)
tr_new_2 = torch.cat([tr1,tr2],dim=1)
print(tr_new_2.shape)
print('===============================')
tr_new_3 = torch.stack([tr1,tr2],dim=0)
print(tr_new_3.shape)
tr_new_4 = torch.stack([tr1,tr2],dim=1)
print(tr_new_4.shape)
tr_new_5 = torch.stack([tr1,tr2],dim=2)
print(tr_new_5.shape)


















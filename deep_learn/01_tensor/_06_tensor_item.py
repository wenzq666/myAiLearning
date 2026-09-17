import torch


# tensor.item()  取只有一个值的张量的值
t1 = torch.tensor([2.100])
item = t1.item()
print(item)
print(type(item))


# 张量中有多个元素时 无法通过item()取出元素
# RuntimeError: a Tensor with 3 elements cannot be converted to Scalar
# t2 = torch.tensor([3,4,5])
# t2.item()







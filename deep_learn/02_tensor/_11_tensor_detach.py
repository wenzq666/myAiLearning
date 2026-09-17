import torch


# detach() 创建一个试图，在这个试图的操作不会影响到模型的训练
# 使用场景 : 模型评估
# 看模型效果的评估 不希望影响到模型的训练 可以通过 张量.detach()
# 从计算图中剥离 不参与梯度的计算以及参数的更新


# 对requires_grad = True 的张量 转numpy
t1 = torch.tensor([1,2,3],requires_grad=True,dtype=torch.float32)
n1 = t1.detach().numpy()
print(n1)























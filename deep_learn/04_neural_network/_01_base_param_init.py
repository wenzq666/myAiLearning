import torch.nn as nn


linear = nn.Linear(3, 2)

# 均匀分布  (0, 1)
# nn.init.uniform_(linear.weight)

# 固定值
nn.init.constant_(linear.weight, 66)

# # 全0
# nn.init.zeros_(linear.weight)
#
# #全1
# nn.init.ones_(linear.weight)
#
# #正态分布
# nn.init.normal_(linear.weight)
#
# # Kaiming  HE初始化
# # 考虑了输入神经元数量的影响
# # 均匀分布   [-sqrt(6/输入层神经元个数), (6/输入层神经元个数)]
# nn.init.kaiming_uniform_(linear.weight)
#
# # 正态分布 以0为均值  以sqrt(2/输入层神经元个数) 为标准差
# nn.init.kaiming_normal_(linear.weight)
#
#
# # xavier初始化
# # 考虑了输入以及输出神经元数量的影响
# # 均匀分布  [-sqrt(6/输入+输除 层神经元个数), (6/输入+输除 层神经元个数)]
# nn.init.xavier_uniform_(linear.weight)
#
# # 正态分布 以0为均值  以sqrt(2/输入+输除 层神经元个数) 为标准差
# nn.init.xavier_normal_(linear.weight)

print(linear.weight)




























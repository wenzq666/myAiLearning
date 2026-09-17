import math  # 计算库


def dataloader(batch_size):
    """
    数据加载器 -> 生成器
    :param batch_size: 批次样本数
    """
    # todo:1-读取文本数据集 readlines
    with open('./data/jaychou_lyrics.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()

    print(data[:5])
    # print('数据集总样本数:', len(data))
    # todo:2-计算总样本数
    total_samples = len(data)

    # todo:3-计算批次数
    # batch_nums = math.ceil(total_samples / batch_size)
    batch_nums = math.floor(total_samples / batch_size)
    print('总样本数:', total_samples, '批次数:', batch_nums)

    # todo:4-遍历批次数, 基于起始下标和结束下标切片获取当前批次样本
    # 第一批数据(0): 0:4
    # 第二批数据(1): 4:8
    # 第三批数据(2): 8:12
    # 第idx批数据(idx): idx*4:(idx+1)*4
    for idx in range(batch_nums):
        yield data[idx * batch_size:(idx + 1) * batch_size]


g = dataloader(batch_size=4)
print(next(g))
print(next(g))
print('=' * 80)
for i in g:
    print(i)
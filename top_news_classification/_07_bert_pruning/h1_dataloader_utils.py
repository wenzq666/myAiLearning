from tqdm import tqdm  # 进度条
import torch  # 深度学习框架
from torch.utils.data import Dataset, DataLoader  # 数据集对象, 数据加载器对象.
from transformers import BertTokenizer  # BERT分词器
import time  # 时间处理
from config import Config  # 配置文件类
from transformers.utils import PaddingStrategy  # 控制填充策略

# 创建配置文件对象
conf = Config()


# todo 1.定义函数, 加载并处理原始数据集.
def load_raw_data(file_path):
    """
    从指定文件中加载数据, 处理为: '文件内容-标签索引'的元组列表, 供后续封装使用.
    :param file_path: 原始数据文件的路径
    :return: 列表嵌套元组, 例如: [('文本字符串', 标签整数索引), ('文本字符串', 标签整数索引), (...)]
    """
    # 1. 初始化结果列表, 存储处理后的数据.
    data_list = []

    # 2. 打开源文件.
    with open(file_path, 'r', encoding='utf-8') as f:
        # 3. 一次性读取所有行, 并遍历, 获取到每行数据.
        for line in f:
            # 4. 去除首尾空白
            line = line.strip()

            # 5. 如果行数据为空, 则跳过.
            if not line:
                continue

            # 6. 切割, 获取到: 文本 和 标签.
            text, label = line.split("\t")

            # 7. 将标签从字符串转成整数(类别索引), 例如: '3' -> 3
            label = int(label)

            # 8. 封装为元组, 例如: ('文本字符串', 3) 添加到列表中.
            data_list.append((text, label))

            # 9. 返回处理结果.
    return data_list



# todo 2. 自定义数据集类(继承PyTorch中的DataSet)
class TextDataset(Dataset):
    # 1. 初始化函数
    def __init__(self, data_list):
        """
        初始化数据集, 接收原始数据列表, 将其转换为 DataLoader可以识别的格式.
        :param data_list: 列表嵌套元组, 例如: [('文本字符串', 3), ('文本字符串', 3), (...)]
        """
        # 1. 创建数据集对象.
        self.data_list = data_list

    # 2. 获取数据集大小
    def __len__(self):
        return len(self.data_list)

    # 3. 获取指定索引的数据
    def __getitem__(self, index):
        # 返回结果---> text: 文本字符串, label: 标签索引(整数形式)
        text, label = self.data_list[index]
        return text, label


# todo 3. 定义整理函数 -> 批量处理某一批次数据
def collate_fn(batch):
    """
    给DataLoader的一个批次(Batch)原始数据进行预处理: 分词, 填充, 转张量
    :param batch: 某一批次的数据, 例如: [(text1, label1), (text2, label2), ...]
    :return: 元组形式, 三个值分别是: input_ids , attention_mask, labels
        input_ids: 分词后token的ID, 形状为: (batch_size, max_length)
        attention_mask: 注意力掩码, 标记有效token和填充token, 形状和 input_ids一致.
        labels: 批次标签, 形状为: (batch_size,)
    """
    # 1. 提取文本和标签
    text, label = zip(*batch)
    # 2. 调用BERT分词器的batch_encode_plus()方法, 对批量文本进行编码.
    """
    常用参数: 
        add_special_tokens=True,            # 是否添加特殊标记(CLS, SEP, PAD, ...)
        padding='max_length',               # 填充策略
        max_length=conf.pad_size,           # 最大长度
        truncation=True,                    # 是否截断
        return_attention_mask=True,         # 是否返回注意力掩码
        return_tensors='pt'                 # 返回张量格式
    """

    # 3. 获取分词结果
    tokenized_result = conf.tokenizer(text,
                                      add_special_tokens=True,
                                      padding="max_length",
                                      max_length=conf.pad_size,
                                      truncation=True,
                                      return_attention_mask=True,
                                      return_tensors='pt'
                                      )

    # 4. 把列表转换为PyTorch张量(模型计算需要张量格式),
    # 如果return_tensors='pt', 则input_ids和attention_mask不用转, 只需将labels转张量
    input_ids = tokenized_result['input_ids']
    attention_mask = tokenized_result['attention_mask']
    label = torch.tensor(label)

    # 5. 返回结果, 即: 模型可以直接使用的张量. input_ids, attention_mask, labels
    return input_ids, attention_mask, label


# todo 4. 构建数据加载器函数
def build_dataloader():
    """
    构建训练集, 验证集, 测试集的数据加载器(DataLoader)
    :return: 包含单个DataLoader的元素, 顺序为: (train_dataloader, dev_dataloader, test_dataloader)
    """
    # 1. 调用load_raw_data()函数, 加载原始数据 -> 训练集, 验证集, 测试集
    train_list = load_raw_data(conf.train_datapath)
    test_list = load_raw_data(conf.test_datapath)
    dev_list = load_raw_data(conf.dev_datapath)

    # 2. 将上述的数据(列表嵌套元组) -> 自定义数据集对象
    train_dataset = TextDataset(train_list)
    test_dataset = TextDataset(test_list)
    dev_dataset = TextDataset(dev_list)

    # 3. 构建DataLoader: 指定批次大小, 是否打乱数据, 批量处理函数.
    train_dataloader = DataLoader(train_dataset, batch_size=conf.batch_size, shuffle=True, collate_fn=collate_fn, pin_memory=True)
    test_dataloader = DataLoader(test_dataset, batch_size=conf.batch_size, shuffle=True, collate_fn=collate_fn, pin_memory=True)
    dev_dataloader = DataLoader(dev_dataset, batch_size=conf.batch_size, shuffle=True, collate_fn=collate_fn, pin_memory=True)

    # 4. 返回三个数据集的dataloader结果
    return train_dataloader, test_dataloader, dev_dataloader


# todo 程序的主入口
if __name__ == '__main__':
    # # 测试1: load_raw_data()函数
    # data_list = load_raw_data(conf.train_datapath)
    # print(data_list)

    # # 测试2: TextDataset()类
    # text_dataset = TextDataset(data_list)
    # print(text_dataset[0])

    # 测试3: build_dataloader()函数
    train_loader, test_loader, dev_loader = build_dataloader()

    for item in train_loader:
        print(item)
        break

    # 测试4: 获取数据集加载器对象.

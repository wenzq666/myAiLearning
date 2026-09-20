import torch                        # 深度学习框架
import torch.nn as nn               # 神经网络模块
from transformers import BertModel, BertTokenizer  # Bert模型, 分词器
from config import Config           # 配置文件类

# todo 1.加载配置文件信息.
conf = Config()

# todo 2. 定义BiLSTM分类模型框架
class BiLSTMClassifier(nn.Module):
    # todo 2.1 初始化模型.
    def __init__(self):
        # 1. 继承父类初始化方法
        super().__init__()

        # 2. 定义嵌入层, 将词的整数id转换成(稠密)向量表示.
        # 输入维度: config.bert_config.vocab_size(21128, 词汇表大小)
        # 输出维度: config.embed_size
        self.embed = nn.Embedding(conf.bert_config.vocab_size, conf.embed_size)

        # 3. 定义双向LSTM层(BiLSTM)
        # conf.embed_size: 输入特征维度(即: 词向量维度)
        # hidden_size_lstm: LSTM隐藏层维度
        # num_layers: LSTM层数
        # batch_first: 输入张量的维度顺序为: [batch_size, seq_len, input_size]
        # bidirectional: 是否启用双向LSTM(前后两个方向都计算, 输出维度会翻倍)
        self.lstm = nn.LSTM(input_size=conf.embed_size, hidden_size=conf.hidden_size_lstm, num_layers=conf.num_layers, batch_first=True, bidirectional=True)
        # self.lstm = nn.LSTM(input_size=conf.embed_size, hidden_size=2, num_layers=conf.num_layers, batch_first=True, bidirectional=True)

        # 4. 随机失活层.
        self.dropout = nn.Dropout(p=conf.dropout)

        # 5. 定义全连接分类层, 输入维度:双向LSTM输出维度翻倍, 输出维度: conf.num_classes(10个类别)
        self.out = nn.Linear(in_features=conf.hidden_size_lstm * 2, out_features=10)

        pass
    # todo 2.2 定义前向传播方法.
    def forward(self, input_ids, attention_mask):
        # 嵌入层
        embed = self.embed(input_ids)

        # 使用 attention_mask 掩码填充 token 的嵌入（核心处理）:
        # embedding结果与attention_mask做哈达玛积
        # embedding结果的形状是(batch_size, seq_len, embed_size)
        # attention_mask从(batch_size, seq_len)升维到(batch_size, seq_len, 1)
        attention_mask = attention_mask.unsqueeze(dim=-1)
        # print(embed.shape)
        # print(f"手动掩码之前的词嵌入结果:{embed}")
        embed = embed * attention_mask
        # print(f"手动掩码之后的词嵌入结果:{embed}")

        # LSTM 层, 掩码后的embedding结果作为输入, 输出是三个结果lstm_out, (hidden, cn)
        # lstm_out: 所有时间步的输出, (batch, seq_len, num_directions * hidden_size)
        # hidden: 最后一个时间步的隐藏状态, (num_layers * num_directions, batch, hidden_size),每一层、每个方向的最后时间步隐藏状态
        # cn: 最后一个时间步的细胞状态
        lstm_out, (hidden, cn) = self.lstm(embed)
        # print(f"lstm_out, LSTM输出的形状:{lstm_out.shape}")
        # print(lstm_out)

        # 取最后一时间步的隐藏状态（填充 token 已置 0，无需再次处理）
        lstm_out = lstm_out[:,-1,:]
        # print(lstm_out)
        # Dropout 和全连接层
        lstm_out = self.dropout(lstm_out)
        # a = input()
        #  13. 返回分类结果.
        return self.out(lstm_out)


# todo 3.测试代码
if __name__ == '__main__':
    # 1. 创建BiLSTM模型师实例.
    model = BiLSTMClassifier()
    # 2. 准备示例文本, 用于测试 模型的输入数据.
    texts = ['王者', '今天很好']
    tokenizer = BertTokenizer.from_pretrained(conf.bert_path)

    # 3. 编码文本 -> 将原始文本转成模型所需要的 的输入数据(Token ID, Attention Mask)
    encode_inputs = tokenizer(
        texts,                      # 待编码的文本列表
        padding='max_length',       # 填充至最大长度.
        max_length = 6,           # 最大序列长度
        return_tensors='pt'         # 返回PyTorch张量
    )

    # 4. 提取模型输入张量: 从编码结果中拿出 Token ID 和 Attention Mask张量.
    input_ids = encode_inputs['input_ids']
    attention_mask = encode_inputs['attention_mask']
    print(f'input_ids: {input_ids}')
    print(f'attention_mask: {attention_mask}')
    print('-' * 40)

    # 5. 创建自定义的BERT分类模型
    logits = model(input_ids, attention_mask)
    print(f'logits: {logits}')      # 未归一化的分类得分(每行对应1个样本, 每列对应1个类别)
    print('-' * 40)

    # 7. 计算类别概率, 对logits做softmax()归一化, 得到每个类别在[0, 1]区间的概率
    probs = torch.softmax(logits, dim=-1)
    print(f'probs: {probs}')
    print('-' * 40)

    # 8. 获取预测分类: 即概率最大的类别索引.
    preds = torch.argmax(logits, dim=-1)
    print(f'preds: {preds}')        # 最终结果: 每个样本的预测类别索引.
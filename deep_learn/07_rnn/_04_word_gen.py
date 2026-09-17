import jieba
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from torchsummary import summary



def build_vocab():

    unique_words = []
    all_words = []


    with open('./data/jaychou_lyrics.txt','r',encoding='utf-8') as f :
        for line in f:
            sentence_words = jieba.lcut(line)
            all_words.extend(sentence_words)
            all_words.extend(" ")
            # print(sentence_words)
            for word in sentence_words:

                if word not in unique_words:
                    unique_words.append(word)

    # print(unique_words)

    # 根据 unique_words 加工 word_to_index
    word_to_index = {w:idx for idx,w in enumerate(unique_words)}

    # print(word_to_index)

    # 根据 unique_words --> word_count
    word_count = len(unique_words)

    # 把原数据 转换成索引形式
    corpus_idx = []
    for word in all_words:
        idx = word_to_index[word]
        corpus_idx.append(idx)
    # print(corpus_idx)


    return unique_words, word_to_index, word_count, corpus_idx


# 定义数据集
class LyricsDataSet(Dataset):
    # 初始化此索引 词个数
    def __init__(self, corpus_idx, num_chars):
        self.corpus_idx = corpus_idx
        self.num_chars = num_chars
        self.word_count = len(self.corpus_idx)
        # 能拿到的句子的数量
        # self.number = self.word_count // self.num_chars
        self.number = self.word_count - self.num_chars -1

    def __len__(self):
        return self.number

    def __getitem__(self, idx):
        # idx指词的索引，并将其修正索引值到文档的范围里面
        start = min(max(idx, 0), self.word_count - self.num_chars - 1)
        # 输入值
        x = self.corpus_idx[start: start + self.num_chars]
        # 网络预测结果（目标值）
        y = self.corpus_idx[start + 1: start + 1 + self.num_chars]
        # 返回结果
        return torch.tensor(x), torch.tensor(y)


class TextGenerator(nn.Module):
    # 两个方法
    def __init__(self, word_count):
        super().__init__()
        # 词嵌入层
        self.embd = nn.Embedding(word_count, 128)
        self.rnn = nn.RNN(input_size=128, hidden_size=256, num_layers=1, batch_first=True)
        self.out = nn.Linear(in_features=256, out_features=word_count)

    def forward(self, x, hx=None):
        # x (batch_size, seq_len)
        # x = x.int()
        # print("x",x.shape)
        embed = self.embd(x)# (batch_size, seq_len, emd_dim)
        # print("embed", embed.shape)
        rnn_output, rnn_hidden = self.rnn(embed, hx)
        # print("rnn_output", rnn_output.shape)
        # print("rnn_hidden", rnn_hidden.shape)

        # print(output.shape)
        # a = input()

        # 全连接输入维度得是二维的
        # rnn_output (batch_size, seq_len, hidden_size)
        # (-1, 256) 转二维张量
        rnn_output_reshape = rnn_output.reshape(-1, rnn_output.shape[-1])
        # print("rnn_output_reshape",rnn_output_reshape.shape)
        output = self.out(rnn_output_reshape)

        return output, rnn_hidden

    def init_hidden(self, bs):
        # num_layers batch_size hidden_size
        return torch.zeros(1, bs, 256)


def model_train():
    unique_words, word_to_index, word_count, corpus_idx = build_vocab()
    # 4 个准备
    # 数据集
    lyrics = LyricsDataSet(corpus_idx, 15)

    lyrics_dataloader = DataLoader(lyrics, batch_size=128, shuffle=True)

    # 模型
    model = TextGenerator(word_count).to('cuda')

    # 损失函数
    criterion = nn.CrossEntropyLoss()

    # 优化器
    optimizer = optim.Adam(model.parameters(),lr=1e-4, betas=(0.9, 0.99))

    # 2个循环
    epochs = 20

    for epoch in range(epochs):
        iter_num, total_loss = 0, 0.
        for batch_x, batch_y in lyrics_dataloader:
            batch_x = batch_x.to('cuda')
            batch_y = batch_y.to('cuda')
            hidden = model.init_hidden(batch_x.shape[0])
            # 5个步骤
            # 前向传播
            output, hidden = model(batch_x)

            # 计算损失
            # print(output.shape) # torch.Size([40, 5703])
            # print(batch_y.shape) # torch.Size([8, 5])
            # a = input()
            batch_y = batch_y.reshape(-1)
            loss = criterion(output, batch_y)

            # 梯度清零
            optimizer.zero_grad()

            # 反向传播
            loss.backward()

            # 参数更新
            optimizer.step()

            total_loss += loss.item()
            iter_num += 1
        # 本轮
        print(f"{epoch+1}轮,loss:{total_loss/iter_num:.2f}")
    # 训练结束
    torch.save(model.state_dict(),"./model/model.pth")


def predict():
    unique_words, word_to_index, word_count, corpus_idx = build_vocab()
    model = TextGenerator(word_count).to('cuda')
    model.load_state_dict(torch.load("./model/model.pth"))

    hx = model.init_hidden(1)
    #
    model.eval()

    word_idx = word_to_index['嫣然']
    generate_sentence = [word_idx]

    for _ in range(25):
        # 模型预测
        output, hidden = model(torch.tensor([[word_idx]]).to('cuda'))
        # 获取预测结果
        word_idx = torch.argmax(output)
        generate_sentence.append(word_idx.item())
        # 更新 word_index
        word_idx = word_idx.item()


    index_to_word = {v:k for k, v in word_to_index.items()}
    # 根据产生的索引获取对应的词，并进行打印
    for idx in generate_sentence:
        print(index_to_word[idx], end='')



if __name__ == '__main__':
    # unique_words, word_to_index, word_count, corpus_idx = build_vocab()

    # dataset = LyricsDataSet(corpus_idx, 5)
    # x, y = dataset[0]
    #
    # print("输入值：", x)
    # print("目标值：", y)
    # model = TextGenerator(word_count)
    # for name, par in model.named_parameters():
    #     print(f"{name}:{par.shape}")

    model_train()
    # summary(model, input_size=(5, ),batch_size=2,device='cpu')
    predict()







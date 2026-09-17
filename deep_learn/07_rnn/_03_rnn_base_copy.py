import torch
import torch.nn as nn
import jieba



jieba.setLogLevel(jieba.logging.INFO)

unique_list = []
all_words = []
# 今天天气不好
data = ["今天天气为晴","今天天气有小雨"]
for sentence in data:
    cut_result = jieba.lcut(sentence)
    all_words.append(cut_result)
    # print(cut_result)
    for word in cut_result:
        if word not in unique_list:
            unique_list.append(word)
print(unique_list)
print(all_words)


# 构建词与索引字典
word_2_id = {word:i for i,word in enumerate(unique_list)}
print(word_2_id)


# 构建nn,Embedding 词表大小 词向量维度
embed = nn.Embedding(num_embeddings=len(unique_list), embedding_dim=5)
print(embed)

# 把原始文本(all_words) 转索引
sentence_index = []
for sentence in all_words:
    tem = []
    for word in sentence:
        index = word_2_id[word]
        tem.append(index)
    sentence_index.append(tem)

print(sentence_index)

# 把索引数据传到 embed中
# sen_tensor = torch.tensor(sentence_index)

sen_tensor = torch.tensor(sentence_index)

sen_embed = embed(sen_tensor)
print(sen_embed)
print(sen_embed.shape) # torch.Size([2, 3, 5]) 两个句子 每个句子分三个词  五个维度

print("#######################################")
# RNN循环神经网络
# input_size 输入维度   词向量维度
# hidden_size 隐藏层的输出维度   隐藏层几个神经元就是几
# num_layers  循环神经网络的层数
rnn = nn.RNN(input_size=5, hidden_size=6, num_layers=1,batch_first=True)

# 定义隐藏层
# 默认 (seq_len, batch_size, embedding_dim)
# 如果指定了 batch_first=True  则为(batch_size, seq_len, embedding_dim)

# 初始化隐藏层状态 (num_layers, batch_size, hidden_size)
init_hidden = torch.zeros(size=(1, 2, 6))

# 2 3 5
rnn_out, h_out = rnn(sen_embed, init_hidden)
print(rnn_out)
print(rnn_out.shape)
print('########################')
print(h_out)
print(h_out.shape)











































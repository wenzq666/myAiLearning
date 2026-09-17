import torch
import torch.nn as nn
import jieba

# ['今天天气', '为', '晴']
# ['今天天气', '不好']
# data = ["今天天气为晴","今天天气不好"]
# cut_result = jieba.lcut("今天天气不好")
# print(cut_result)


# 词嵌入
# 分词
unique_list = []
all_words = []
data = ["今天天气为晴","今天天气不好"]
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
word_2_id = {word:i+1 for i,word in enumerate(unique_list)}
print(word_2_id)


# 构建nn,Embedding 词表大小 词向量维度
embed = nn.Embedding(num_embeddings=len(unique_list)+1, embedding_dim=5,padding_idx=0)
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
max_len = max(len(seq) for seq in sentence_index)
for seq in sentence_index:
    if len(seq) < max_len:
        seq.extend([0] * (max_len - len(seq))) # 不够长的在末尾补0

sen_tensor = torch.tensor(sentence_index)

sen_embed = embed(sen_tensor)
print(sen_embed)
print(sen_embed.shape)










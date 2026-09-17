import torch
import torch.nn as nn
import jieba

# -------------------- 1. 数据准备 & 构建词表（请补全）--------------------
data = ["今天天气为晴", "今天天气有小雨"]

# TODO 任务一：补全分词和构建词表的逻辑
# 1.1 对 data 中的每个句子进行分词，将结果存入 all_words（保留原始顺序）
# 1.2 提取所有不重复的词，存入 unique_words（去重且保持出现顺序）
all_words = []
unique_words = []

# ---------- 你的all_words与unique_words加工代码写在这里（任务一） ----------
for sentence in data:
    # 使用 jieba.lcut 进行分词
    cut_result = jieba.lcut(sentence)
    all_words.append(cut_result)
    for word in cut_result:
        if word not in unique_words:
            unique_words.append(word)

# ------------------------------------------------

print(f"分词结果: {all_words}")  # 期望: [['今天天气', '为', '晴'], ['今天天气', '有', '小雨']]
print(f"词表: {unique_words}")  # 期望: ['今天天气', '为', '晴', '有', '小雨']

# 1.3 构建词到索引的映射字典
# ---------- 你的word_to_id加工代码写在这里（任务一） ----------
word_to_id = {word:idx for idx,word in enumerate(unique_words)}
print(word_to_id)


vocab_size = len(unique_words)
print(f"词表大小: {vocab_size}")

# 1.4 将分词结果转换为索引张量 (batch_size=2, seq_len=3)
sentence_idx_list = []
for sentence in all_words:
    tmp = [word_to_id[word] for word in sentence]
    sentence_idx_list.append(tmp)

input_tensor = torch.tensor(sentence_idx_list)  # shape: [2, 3]
print(f"输入张量形状: {input_tensor.shape}")  # torch.Size([2, 3])


# -------------------- 2. 模型定义（请补全）--------------------
class TextFeatureExtractor(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_layers):
        super(TextFeatureExtractor, self).__init__()
        # TODO 任务二：定义 Embedding 层和 RNN 层
        # 参数要求：
        #    Embedding: 词表大小 -> embed_dim (8)
        #    RNN: input_size=embed_dim, hidden_size=6, num_layers=2, batch_first=True
        # ---------- 你的代码写在这里（任务二） ----------
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embed_dim)
        self.rnn = nn.RNN(input_size=embed_dim, hidden_size=6, num_layers=2, batch_first=True)

        # ------------------------------------------------

    def forward(self, x):
        # TODO 任务三：补全前向传播逻辑
        # 1. 将 x（索引张量）传入 embedding 层
        # 2. 将 embedding 的输出传入 RNN 层（使用默认的全零隐藏状态）
        # 3. 返回 RNN 的 output 和 hidden 状态
        # ---------- 你的代码写在这里（任务三） ----------
        embedded = self.embedding(x)  # shape: [batch, seq_len, embed_dim]
        output, hidden = self.rnn(embedded)  # 如果不传入 h0，自动使用全零初始化
        return output, hidden
        # ------------------------------------------------

    # -------------------- 3. 运行验证 --------------------
if __name__ == '__main__':
        # 实例化模型
        model = TextFeatureExtractor(
            vocab_size=vocab_size,
            embed_dim=8,
            hidden_size=6,
            num_layers=2
        )

        # 前向传播
        rnn_output, h_n = model(input_tensor)

        print("=" * 50)
        print(f"输入 input_tensor 的形状: {input_tensor.shape}")  # [2, 3]
        print(f"词嵌入后的隐含形状 (在RNN内部): [2, 3, 8]")
        print(f"RNN 输出 output 的形状: {rnn_output.shape}")  # 期望: torch.Size([2, 3, 6])
        print(f"最终隐藏状态 h_n 的形状: {h_n.shape}")  # 期望: torch.Size([2, 2, 6])
        print("=" * 50)
































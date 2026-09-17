"""
- `fasttext.train_unsupervised` 训练词向量, 参数要求
  - 模型：skipgram
  - 词向量维度：100
  - 训练轮数：5
  - 学习率：0.05
- 保存模型为 `train_seg.bin`，然后加载该模型

- 获取单词 **“服务”** 的词向量
- 查找与 **“服务”** 最邻近的5个词，并打印结果
"""


import fasttext


model = fasttext.train_unsupervised("./data/corpus_seg.txt",
                                    model="skipgram",
                                    dim=100,
                                    epoch=5,
                                    lr=0.05
                                    )
model.save_model("./model/train_seg.bin")

train_model = fasttext.load_model("./model/train_seg.bin")

print(train_model.get_word_vector("服务"))

print(train_model.get_nearest_neighbors("服务", k=5))



























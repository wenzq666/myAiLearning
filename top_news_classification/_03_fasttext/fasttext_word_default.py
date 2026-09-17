import fasttext
from config import Config
import datetime
import os

# todo 1. 加载项目配置
config = Config()

# todo 2. 模型训练: 使用 fasttext训练 单词级 文本分类模型
# fasttext.train_supervised(): fasttext的核心训练函数, 用于训练: 有监督学习分类模型
model = fasttext.train_supervised(config.process_train_datapath_word)

# todo 3. 打印模型训练后的关键信息.
# get_word_vector方法, 获取单词'日'的向量表示(长度: 10维), 查看数字的特征, 例如:
# [ 0.06251448  0.21214555 -0.5582269  -0.2776528  -0.40804806 -0.2712767, -0.03183828 -0.10957453  0.31537786  0.19355372]

# labels属性, 获取模型训练到的 所有类别标签

# 获取模型训练到的 类别数量


# get_words方法, 获取模型训练到的 所有单词及对应的词频
# print(model.get_words(include_freq=True))

# 用zip()函数, 配对: 单词和频率, 转为列表, 方便查看每个单词对应的出现次数.
# print(
#     list(zip(*model.get_words(include_freq=True))))
# print('-' * 40)

# todo 4. 模型保存. save_model方法保存模型
model.save_model(config.ft_model_save_path + "/word_model_default.bin")


# todo 5. 模型预测. predict方法预测结果


# todo 6. words属性, 查看模型学习到的词汇表


# todo 7. get_subwords方法, 模型子词查看.


# todo 8. get_dimension方法, 查看模型的向量维度.


# todo 9. test方法, 模型评估.  (样本数, 精确率, 召回率)
print(model.test(config.process_test_datapath_word)) # (10000, 0.9078, 0.9078)
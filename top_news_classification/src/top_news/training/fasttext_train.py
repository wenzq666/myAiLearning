import fasttext
from src.top_news.config import Config
import datetime

# todo 1. 加载项目配置
config = Config()


def fasttext_char_auto():
    # todo 2. 模型训练: 使用 fasttext训练 字符级 文本分类模型, 使用自动调参
    model = fasttext.train_supervised(config.process_train_datapath_char,
                                      autotuneValidationFile=config.process_dev_datapath_char,
                                      autotuneDuration=60
                                      )

    # todo 3. 模型保存.
    model.save_model(config.ft_model_save_path + "/char_model_auto.bin")

    # todo 5. 模型预测.

    # 6. 模型词表查看, 查看模型学习到的词汇表
    # print(model.words[:10])  # 取前10个字符, 方便我们快速了解词汇表内容.

    # 7. 模型子词查看.
    # print(model.get_subwords('日本地震海啸!'))

    # 8. 查看模型的向量维度.
    # print(model.get_dimension())

    # todo 9. 模型评估.  (样本数, 精确率, 召回率)
    print(model.test(config.process_test_datapath_char))  # (10000, 0.9192, 0.9192)


def fasttext_char_default():
    # todo 2. 模型训练: 使用 fasttext训练 字符级 文本分类模型
    # fasttext.train_supervised(): fasttext的核心训练函数, 用于训练: 有监督学习分类模型

    # model = fasttext.train_supervised(config.process_train_datapath_char)

    # todo 4. 模型保存. save_model方法保存模型

    # model.save_model(config.ft_model_save_path + "/char_model_default.bin")

    # 加载模型

    model = fasttext.load_model(config.ft_model_save_path + "/char_model_default.bin")

    # todo 3. 打印模型训练后的关键信息.
    # get_word_vector方法, 获取字符'日'的向量表示(长度: 10维), 查看数字的特征, 例如:
    # [ 0.06251448  0.21214555 -0.5582269  -0.2776528  -0.40804806 -0.2712767, -0.03183828 -0.10957453  0.31537786  0.19355372]

    print(model.get_word_vector("上"))

    # labels属性, 获取模型训练到的 所有类别标签
    print(model.get_labels())

    # 获取模型训练到的 类别数量

    # get_words方法, 获取模型训练到的 所有单词及对应的词频
    print(model.get_words(include_freq=True))

    # 用zip()函数, 配对: 字符和频率, 转为列表, 方便查看每个字符对应的出现次数.

    # todo 5. 模型预测. predict方法预测结果

    # todo 6. words属性, 查看模型学习到的词汇表

    # todo 7. get_subwords方法, 模型子词查看.

    # todo 8. get_dimension方法, 查看模型的向量维度.

    # todo 9. test方法, 模型评估.  (样本数, 精确率, 召回率)

    print(model.test(config.process_test_datapath_char))  # (10000, 0.8737, 0.8737)


def fasttext_word_auto():
    # todo 2. 模型训练: 使用 fasttext训练 字符级 文本分类模型
    model = fasttext.train_supervised(config.process_train_datapath_word,
                                      autotuneValidationFile=config.process_dev_datapath_word,
                                      autotuneDuration=60
                                      )

    # todo 3. 模型保存.
    model.save_model(config.ft_model_save_path + "/word_model_auto.bin")

    # todo 5. 模型预测.

    # todo 6. 模型词表查看, 查看模型学习到的词汇表
    # print(model.words[:10])  # 取前10个字符, 方便我们快速了解词汇表内容.

    # todo 7. 模型子词查看.
    # print(model.get_subwords('日本地震海啸!'))

    # todo 8. 查看模型的向量维度.
    # print(model.get_dimension())

    # todo 9. 模型评估.  (样本数, 精确率, 召回率)
    print(model.test(config.process_test_datapath_word))  # (10000, 0.9184, 0.9184)


def fasttext_word_default():
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
    print(model.test(config.process_test_datapath_word))  # (10000, 0.9078, 0.9078)



if __name__ == '__main__':
    # fasttext_char_auto()
    # fasttext_char_default()
    # fasttext_word_auto()
    # fasttext_word_default()
    pass
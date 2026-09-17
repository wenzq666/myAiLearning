import fasttext
from config import Config
import datetime

# todo 1. 加载项目配置
config = Config()

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
print(model.test(config.process_test_datapath_word)) # (10000, 0.9184, 0.9184)
import jieba  # 中文分词库, 将文本按照 词语 进行分割.
from config import Config  # 从config模块中, 导入Config类

# todo 1.加载配置文件.
config = Config()


# todo 2. 定义数据处理函数, 将原始文本 -> fasttext模型所需的输入格式.
# 格式为: __label__类别名 分词结果
# 例如: __label__education 中华 女子 学院 ： 本科 层次 仅 1 专业 招 男生
def process_data(datapath, process_datapath, is_char=True):
    """
    数据处理函数, 按照fasttext模型所需的格式输入.
    :param datapath: 原始数据文件的路径(输入)
    :param process_datapath: 处理后的数据文件路径(输出)
    :param is_char: 布尔值, True表示按照字符级别切割, False表示按词语级别切割(jieba分词)
    :return:
    """
    # 1. 打开原始数据文件
    with open(datapath, 'r', encoding='utf-8') as f:
        with open(process_datapath, 'w', encoding='utf-8') as fw:
            # 2. 循环读取每一行.
            for line in f:
                # 3. 去除首尾空格
                line = line.strip()
                # 4. 如果处理后为空, 说明是空行, 就跳过, 继续往后处理.
                if not line:
                    continue

                # 5. 分割文本和标签.
                text, label = line.split("\t")

                # 6. 把标签转成数字类型.
                label = int(label)

                # 7. 通过配置中的id2class_dict, 将标签整数 映射为 对应类别的字符串.
                # id2class_dict格式: {0: 'positive', 1: 'negative'}
                label_name = config.id2class_dict[label]

                # 8. 根据is_char参数决定文本分词方式
                if is_char:
                    # 8.1 字符级别分割， 例如： '天气好' -> '天 气 好'
                    text_result = " ".join(list(text))
                else:
                    # 8.2 词语级别分割, 使用jieba分词库进行分词.
                    # 例如: 今天天气很好' -> '今天 天气 很 好'
                    text_result = " ".join(jieba.lcut(text))

                # 9. 构建fasttext要求的数据格式.
                # 例如: __label__positive  天 气 好
                final_text = "__label__" + label_name + " " + text_result + "\n"

                # 10. 将构建好的行 写入到 处理后的数据文件中.
                fw.write(final_text)


# 测试
if __name__ == '__main__':
    # 训练集, 一个按字符级切分, 并保存到文件中, 一个按词语级切分, 并保存到文件中
    process_data(config.train_datapath, config.process_train_datapath_char, is_char=True)
    process_data(config.train_datapath, config.process_train_datapath_word, is_char=False)

    # 验证集, 一个按字符级切分, 并保存到文件中, 一个按词语级切分, 并保存到文件中
    process_data(config.dev_datapath, config.process_dev_datapath_char, is_char=True)
    process_data(config.dev_datapath, config.process_dev_datapath_word, is_char=False)


    # 测试集, 一个按字符级切分, 并保存到文件中, 一个按词语级切分, 并保存到文件中
    process_data(config.test_datapath, config.process_test_datapath_char, is_char=True)
    process_data(config.test_datapath, config.process_test_datapath_word, is_char=False)

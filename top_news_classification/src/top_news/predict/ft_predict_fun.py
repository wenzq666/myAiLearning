import fasttext
import jieba
import pickle
from src.top_news.config import Config

# todo 1. 加载配置文件.
# 加载配置
config = Config()


# todo 2. 加载模型.
model = fasttext.load_model(config.ft_model_save_path + "/word_model_auto.bin")


# todo 3. 定义预测函数.
def predict_fun(data):  # data就是待预测的数据, 例如: {'text': '北京大学20个院系综合实力及魅力展示'}
    # 1. 使用jieba对文本做分词处理.
    text_words = " ".join(jieba.lcut(data['text']))

    # 2. 使用加载的fasttext模型 对处理后的文本进行 预测, 获取预测结果.
    y_pred = model.predict(text_words) # (('__label__education',), array([0.84957111]))
    print(y_pred)

    # 3. 处理预测结果, 获取类别标签.
    text_words = y_pred[0][0].replace("__label__", "")

    # 4. 返回包含 原始文本 和 预测类别的结果字典
    data['pred_class'] = text_words
    return data
    


# todo 4. 测试
if __name__ == '__main__':
    data = {'text': '北京大学20个院系综合实力及魅力展示'}
    result = predict_fun(data)
    print(result)
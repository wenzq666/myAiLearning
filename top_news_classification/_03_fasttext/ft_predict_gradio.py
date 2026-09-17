import fasttext
import jieba
import pickle
from config import Config

import gradio as gr



# ---------- 1. 加载配置、模型、向量化器 ----------
config = Config()
model = fasttext.load_model(config.ft_model_save_path + "/word_model_auto.bin")


# ---------- 2. 定义预测函数（改：入参是字符串，出参直接返回类别名）----------
def predict_fun(data: str) -> str:  # data就是待预测的数据, 例如: {'text': '北京大学20个院系综合实力及魅力展示'}
    # 1. 使用jieba对文本做分词处理.
    text_words = " ".join(jieba.lcut(data))

    # 2. 使用加载的fasttext模型 对处理后的文本进行 预测, 获取预测结果.
    y_pred = model.predict(text_words) # (('__label__education',), array([0.84957111]))
    print(y_pred)

    # 3. 处理预测结果, 获取类别标签.
    text_words = y_pred[0][0].replace("__label__", "")

    # 4. 返回包含 原始文本 和 预测类别的结果字典
    # data['pred_class'] = text_words
    return text_words


# ---------- 3. Gradio 界面 ----------
demo = gr.Interface(
    fn=predict_fun,
    inputs=gr.Textbox(label="待分类文本", placeholder="请输入新闻标题，如：传奇3经典续作重现深挖品牌文化底蕴"),
    outputs=gr.Label(label="预测类别"),
    title="中文新闻文本分类器（fasttext）",
    description="输入一段中文文本，自动分词、向量化并预测所属类别",
    examples=[
        ["传奇3经典续作重现深挖品牌文化底蕴"],
        ["华商基金举办北京客户交流会"],
        ["北京二手房价格持续上涨"],
        ["A股三大指数集体收涨"],
    ],
)

if __name__ == '__main__':
    demo.launch()

import jieba
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.top_news.config import Config
import warnings

import gradio as gr

warnings.filterwarnings('ignore')

# ---------- 1. 加载配置、模型、向量化器 ----------
config = Config()
model: RandomForestClassifier = joblib.load(config.rf_model_path)
tfidf = joblib.load(config.tfidf_model_save_path)
classClassifier = {k: v for k, v in enumerate(open(config.class_datapath, 'r').read().split())}


# ---------- 2. 定义预测函数（改：入参是字符串，出参直接返回类别名）----------
def predict_text(text: str) -> str:
    # 1. jieba 分词
    text_cut = " ".join(jieba.lcut(text))
    # 2. TF-IDF 向量化
    text_tfidf = tfidf.transform([text_cut])
    # 3. 预测
    y_pred = model.predict(text_tfidf)[0]
    # 4. 返回类别名称
    return classClassifier[y_pred]


# ---------- 3. Gradio 界面 ----------
demo = gr.Interface(
    fn=predict_text,
    inputs=gr.Textbox(label="待分类文本", placeholder="请输入新闻标题，如：传奇3经典续作重现深挖品牌文化底蕴"),
    outputs=gr.Label(label="预测类别"),
    title="中文新闻文本分类器（随机森林 + TF-IDF）",
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

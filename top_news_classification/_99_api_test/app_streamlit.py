import streamlit as st
import requests
import time

# 1.streamlit创建画面
# 1. 设置标题
st.title('新闻分类项目')
st.write('这个一个新闻标题分类项目')

# 2. 获取用户输入的文本
text = st.text_input('请输入要查询分类的文本:')

# 2. 后台发送请求.
# 1. 准备url
MODEL_CONFIG = {
    "rf_predict": {"url": "http://127.0.0.1:8080/rf_predict", "name": "随机森林"},
    "ft_predict": {"url": "http://127.0.0.1:8080/ft_predict", "name": "Fasttext"},
    "bert_predict": {"url": "http://127.0.0.1:8080/bert_predict", "name": "Bert"},
}

default_model = "bert_predict"

selected_model = st.sidebar.selectbox(
    "选择分类模型",
    options=list(MODEL_CONFIG.keys()),
    format_func=lambda x: f"基于{MODEL_CONFIG[x]['name']}模型"
)

config = MODEL_CONFIG[selected_model]
url = config["url"]
button_name = f"获取分类 ({config['name']})"

if st.button(button_name):
    # 发送请求, 获取数据, 并将结果显示给用户.
    # 2. 获取任务开始时间
    start_time = time.time()

    # 3. 发送请求, 获取数据.
    response = requests.post(url=url, json={"text":text})

    # 4. 计算耗时.
    end_time = time.time()
    st.write(f"本次耗时:{(end_time-start_time)*1000} ms")

    # 5. 显示预测结果r.json()到网页.
    result = response.json()['pred_class']
    st.write(result)
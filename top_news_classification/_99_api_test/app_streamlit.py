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
url = "http://127.0.0.1:8080/ft_predict"

if url.endswith("ft_predict"):
    button_name = "基于Fasttext模型获取分类!"
elif url.endswith("ft_predict"):
    button_name = "基于随机森林模型获取分类!"


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
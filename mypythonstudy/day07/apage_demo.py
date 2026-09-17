import streamlit as st

st.title("XXX平台")

st.divider()

username = st.text_input('请输入用户名:')

password = st.text_input('请输入密码:', type='password')

age = st.number_input("输入年龄:",min_value= 18 ,max_value= 150)

gender = st.radio('选择年龄:',['男','女','保密'],horizontal=True)

birth = st.date_input('选择生日:')

high = st.slider('选择身高:',min_value= 60 , max_value=300,step=5,value=160)

btn = st.button('注册')


if btn:
    st.write(f'{3.14:1f} : succeed!')
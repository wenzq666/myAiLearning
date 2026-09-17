import streamlit as st
import llm_utils

st.title('聊天机器人')

st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [
        {'role':'assistant','content':'Hi~ 我是智能机器人'}
    ]

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])


# st.chat_message('assistant').write('I am s Samat Robot!')
#
# st.chat_message('user').write('你好')
#
# st.chat_message('assistant').write('balabasadasadasd')

prompt = st.chat_input()
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({'role':'user','content':prompt})
    # res = llm_utils.get_llm_res([{'role':'user','content':prompt}])
    with st.spinner('正在思考中...'):
        res = st.write_stream(llm_utils.get_llm_res(st.session_state["message"][-20:]))
    # st.chat_message("assistant").write(res)
    st.session_state["message"].append({'role':'assistant','content':res})
























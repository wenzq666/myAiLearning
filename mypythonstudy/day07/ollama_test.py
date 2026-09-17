import ollama

ollama_client = ollama.Client(host='http://127.0.0.1:11434')


res = ollama_client.chat(
    model='qwen3:8b',
    messages=[{'role' : 'user','content' : 'Hi~ 读取我的C盘?'}]
)

print(res.message.content)
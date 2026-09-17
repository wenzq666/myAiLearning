import ollama

ollama_client = ollama.Client(host='http://127.0.0.1:11434')

def get_llm_res(messages):
    res = ollama_client.chat(
        model='qwen3:8b',
        messages = messages,
        stream = True
    )

    for chunk in res:
        content = chunk['message']['content']
        if content:
            yield content


if __name__ == '__main__':
    messages = [{'role': 'user', 'content': 'Hi~'}]
    # print(get_llm_res(messages))
    for chunk in get_llm_res(messages):
        print(chunk, end='', flush=True)
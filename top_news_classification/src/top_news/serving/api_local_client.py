import requests


# url = "http://127.0.0.1:8080/rf_predict"
# url = "http://127.0.0.1:8080/ft_predict"
url = "http://127.0.0.1:8080/bert_predict"
json = {"text":"小明一把把把把住了"}
result = requests.post(url=url, json=json)
print(result.json())
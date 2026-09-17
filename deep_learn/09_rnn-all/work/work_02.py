from transformers import pipeline


model = pipeline(task='sentiment-analysis', model="../model/bert-base-chinese")

# [{'label': 'LABEL_0', 'score': 0.5480503439903259}]
print(model("今天天气真好，心情非常愉快！"))



























# 根据模型任务 统一输入输出格式
# AutoTokenizer 句子转索引
from transformers import AutoTokenizer, AutoModelForSequenceClassification



tokenizer = AutoTokenizer.from_pretrained("./model/bert-base-chinese")


model = AutoModelForSequenceClassification.from_pretrained("./model/bert-base-chinese")


# 定义句子
sentence = "小明一把把把把住了"

encoding = tokenizer(sentence, return_tensors='pt',padding=True,truncation=True,max_length=20)
# {'input_ids': tensor([[ 101, 2207, 3209,  671, 2828, 2828, 2828, 2828,  857,  749,  102]]),
# 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
# 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}
print(encoding)
























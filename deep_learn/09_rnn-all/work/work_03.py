from transformers import AutoTokenizer, AutoModelForSequenceClassification


tokenizer = AutoTokenizer.from_pretrained("../model/bert-base-chinese")

model = AutoModelForSequenceClassification.from_pretrained("../model/bert-base-chinese")

sentences = ["这部电影太精彩了！", "这个产品质量很差。"]



# {'input_ids': tensor([[ 101, 6821, 6956, 4510, 2512, 1922, 5125, 2506,  749, 8013,  102, 0 , 0, 0, 0, 0, 0, 0, 0, 0],
#                       [ 101, 6821,  702,  772, 1501, 6574, 7030, 2523, 2345,  511,  102, 0,  0, 0, 0, 0, 0, 0, 0, 0]]),
#  'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
#  'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])}
token = tokenizer(sentences,
                return_tensors='pt',
                padding='max_length',
                truncation=True,
                max_length=20
                )

# SequenceClassifierOutput(loss=None, logits=tensor([[0.1895, 0.0860],
#         [0.1219, 0.0192]], grad_fn=<AddmmBackward0>), hidden_states=None, attentions=None)
print(model(token['input_ids'], token['attention_mask']))

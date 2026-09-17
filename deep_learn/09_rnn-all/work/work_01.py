"""
**题目：** 你已经准备好了训练数据 `cooking.pre.train` 和验证数据 `cooking.pre.valid`。
请使用 FastText 库完成以下任务：

1. 使用自动调参训练一个文本分类模型。
2. 在验证集上评估模型的精确率 (Precision) 和召回率 (Recall)。
3. 使用训练好的模型，预测句子 `"How to bake a banana bread?"` 的标签。

请在下方写出实现以上功能的 Python 代码。
"""
import fasttext


model = fasttext.train_supervised("../data/cooking.pre.train",
                                 autotuneValidationFile = "../data/cooking.pre.valid",
                                 autotuneDuration = 60
                                  )

# (3000, 0.5536666666666666, 0.23944068040939886)
print(model.test("../data/cooking.pre.valid"))

# (('__label__baking',), array([0.87673032]))
print(model.predict("How to bake a banana bread?"))











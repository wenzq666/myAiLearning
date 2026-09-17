import fasttext


def default_param_fasttext():
    # 模型训练
    # model = fasttext.train_supervised("./data/cooking_train.txt")

    # 模型保存
    # model.save_model("./model/cooking.bin")

    # 模型加载
    cooking_model = fasttext.load_model("./model/cooking.bin")

    # 模型预测
    y_pred = cooking_model.predict(
        "Is there a \"common\" ratio for dumplings and added water when adding to a soup/stew recipe? ", k=5)
    # print(y_pred)

    # 模型评估
    eval_result = cooking_model.test("./data/cooking_valid.txt")
    print(eval_result)



def manual_param_fasttext():
    model = fasttext.train_supervised("./data/cooking.pre.train",
                                      lr = 0.9,
                                      epoch = 60 ,
                                      wordNgrams = 2,
                                      loss= "hs",
                                      )
    # 模型评估
    eval_result = model.test("./data/cooking.pre.valid")
    # (3000, 0.5963333333333334, 0.25789246071788957)
    print(eval_result)
    print(vars(model))


def auto_param_fasttext():
    model = fasttext.train_supervised("./data/cooking.pre.train",
                                      autotuneValidationFile = './data/cooking.pre.valid',
                                      autotuneDuration = 60*5
                                      )
    # 模型评估
    eval_result = model.test("./data/cooking.pre.valid")
    # (3000, 0.6016666666666667, 0.26019893325645094)
    print(eval_result)
    print(vars(model))


if __name__ == '__main__':

    # default_param_fasttext()
    # manual_param_fasttext()
    auto_param_fasttext()















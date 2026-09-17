import fasttext


def fasttext_train_default_param():
    # 无监督 训练词向量模型
    model = fasttext.train_unsupervised("./data/fil9")

    # 保存模型
    model.save_model("./model/model_fil9.bin")

    # 加载模型
    load_model = fasttext.load_model("./model/model_fil9.pth")

    word_vector = load_model.get_word_vector("my")
    print(word_vector)
    print(word_vector.shape)
    nearest_neighbors = load_model.get_nearest_neighbors("fuck")
    print(nearest_neighbors)
    dimension = load_model.get_dimension()
    print(dimension)

def fasttext_train_with_param():
    model = fasttext.train_unsupervised("./data/sy5ad",
                                model="cbow",
                                lr=0.001,
                                dim=10,
                                epoch=3,
                                verbose=3
                                )

    # 保存模型
    model.save_model("./model/model_fil9_with_param.bin")

    load_model = fasttext.load_model("./model/model_fil9_with_param.bin")

    word_vector = load_model.get_word_vector("my")
    print(word_vector)
    print(word_vector.shape)
    nearest_neighbors = load_model.get_nearest_neighbors("luck")
    print(nearest_neighbors)
    dimension = load_model.get_dimension()
    print(dimension)


if __name__ == '__main__':
    # fasttext_train_default_param()

    fasttext_train_with_param()



































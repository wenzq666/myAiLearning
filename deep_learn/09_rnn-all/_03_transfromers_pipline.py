from transformers import pipeline
import torch


def sentiment_analysis():
    model = pipeline(task="sentiment-analysis", model="./model/chinese_sentiment")

    # star 1 - 5
    y_pred = model("小明一把把把把住了")
    # [{'label': 'star 3', 'score': 0.32389169931411743}]
    print(y_pred)


def feature_extraction():
    model = pipeline(task="feature-extraction", model="./model/bert-base-chinese")

    # star 1 - 5
    y_pred = model("小明一把把把把住了")
    #
    print(y_pred)
    # torch.Size([1, 11, 768])
    print(torch.tensor(y_pred).shape)


if __name__ == '__main__':

    # sentiment_analysis()
    feature_extraction()
    pass





















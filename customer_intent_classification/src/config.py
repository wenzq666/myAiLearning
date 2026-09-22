import os
import torch
from transformers import BertModel, BertTokenizer, BertConfig


class Config:

    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        # 1.1 配置训练集的路径.
        self.train_datapath = self.BASE_DIR + "/data/raw/train.json"
        self.dev_datapath = self.BASE_DIR + "/data/raw/dev.json"
        self.test_datapath = self.BASE_DIR + "/data/raw/test_public.json"

        self.MODEL_DIR = self.BASE_DIR + "/models"

        self.testCNNModel = self.MODEL_DIR + "/textcnn"


        # 模型训练+预测的时候, 指定设备
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 训练设备，如果GPU可用，则为cuda，否则为cpu


        self.bert_save_model = self.MODEL_DIR + "/bert"

        # 3. BERT模型的相关配置.
        self.bert_path = self.BASE_DIR + "/models/bert/chinese-macbert-base"  # 预训练BERT模型的路径
        self.bert_model = BertModel.from_pretrained(self.bert_path) # 加载预训练BERT模型
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)  # BERT模型的分词器
        self.bert_config = BertConfig.from_pretrained(self.bert_path)  # BERT模型的配置


        self.INTERIM_DATA_DIR = self.BASE_DIR + "/data/interim"

        self.PROCESSED_DATA_DIR = self.BASE_DIR + "/data/processed"



if __name__ == '__main__':
    conf = Config()
    print(conf.testCNNModel)
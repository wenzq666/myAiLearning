"""
配置类
"""
import os
import torch
# 导入Bert相关组件, BertModel(BERT模型的主体), BertTokenizer(BERT的分词器), BertConfig(BERT的配置)
from transformers import BertModel, BertTokenizer, BertConfig



class Config:



    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

        # 1.1 配置训练集的路径.
        self.train_datapath = self.BASE_DIR + "/data/raw/train.txt"
        # 1.2 配置测试集的路径.
        self.test_datapath = self.BASE_DIR + "/data/raw/test.txt"
        # 1.3 配置验证集的路径.
        self.dev_datapath = self.BASE_DIR + "/data/raw/dev.txt"
        # 1.4 配置 类别定义文件 路径
        self.class_datapath = self.BASE_DIR + "/data/raw/class.txt"
        # 指定停止词路径
        self.stopword_datapath = self.BASE_DIR + "/data/raw/stopwords.txt"

        #===============================================================================================#

        # 2.1 数据预处理后训练集保存路径
        self.process_train_datapath = self.BASE_DIR + "/data/raw/processed/rf/process_train_data.txt"
        # 2.2 测试集预处理后保存路径
        self.process_test_datapath = self.BASE_DIR + "/data/raw/processed/rf/process_test_data.txt"
        # 2.3 验证集预处理后保存路径
        self.process_dev_datapath = self.BASE_DIR + "/data/raw/processed/rf/process_dev_data.txt"

        # 模型保存路径
        self.rf_model_path = self.BASE_DIR + "/models/rf/rf_model.pkl"
        self.tfidf_model_save_path = self.BASE_DIR + "/models/rf/tfidf_model.pkl"

        # 测试集预测结果保存路径
        self.predict_result_path = self.BASE_DIR + "/results/predict_result.csv"

        # ===============================================================================================#

        # 3.数据处理保存路径
        # 字符级别fasttext
        self.process_train_datapath_char = self.BASE_DIR + "/data/raw/processed/fasttext/train_process_char.txt"
        self.process_test_datapath_char = self.BASE_DIR + "/data/raw/processed/fasttext/test_process_char.txt"
        self.process_dev_datapath_char = self.BASE_DIR + "/data/raw/processed/fasttext/dev_process_char.txt"

        # 词级别fasttext
        self.process_train_datapath_word = self.BASE_DIR + "/data/raw/processed/fasttext/train_process_word.txt"
        self.process_test_datapath_word = self.BASE_DIR + "/data/raw/processed/fasttext/test_process_word.txt"
        self.process_dev_datapath_word = self.BASE_DIR + "/data/raw/processed/fasttext/dev_process_word.txt"

        # 4.模型路径
        self.ft_model_save_path = self.BASE_DIR + "/models/fasttext"

        # 5.处理完的数据（用于训练）
        self.final_data = self.BASE_DIR + "/data/raw/processed/fasttext"

        # 6.类别字典, 格式为: {0: "business", 1: "entertainment", 2: "sports", 3: "tech"...}
        self.id2class_dict = {i:line.strip() for i, line in enumerate(open(self.class_datapath))}

        # ===============================================================================================#

        self.model_name = "bert"  # 模型名称

        # 从类别文件中读取所有类别的名称.
        self.class_list = [line.strip() for line in open(self.class_datapath, encoding="utf-8")]  # 类别名单

        # 模型训练保存路径
        self.model_save_path = self.BASE_DIR + "/models/bert/save_models/bert_classifier_model.pt"  # 模型训练结果保存路径

        # 模型训练+预测的时候, 指定设备
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 训练设备，如果GPU可用，则为cuda，否则为cpu


        # 3. BERT模型的相关配置.
        self.bert_path = self.BASE_DIR + "/models/bert/bert-base-chinese"  # 预训练BERT模型的路径
        self.bert_model = BertModel.from_pretrained(self.bert_path) # 加载预训练BERT模型
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)  # BERT模型的分词器
        self.bert_config = BertConfig.from_pretrained(self.bert_path)  # BERT模型的配置


        # 4. 训练参数配置.
        self.num_classes = len(self.class_list)  # 类别数
        self.num_epochs = 2  # epoch数
        self.batch_size = 64  # mini-batch大小
        self.pad_size = 30    # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5  # 学习率

        # 5. 量化模型存放地址
        self.bert_model_quantization_model_path = self.BASE_DIR + "/models/bert/save_models/bert_classifier_quantization_model.pt"  # 模型训练结果保存路径



        self.num_classes = len(self.class_list)  # 类别数
        self.num_epochs = 2  # epoch数
        self.batch_size = 64  # mini-batch大小
        self.pad_size = 32    # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5  # 学习率

        # 5. 蒸馏模型存放地址
        self.bert_model_distill_model_path_hard = self.BASE_DIR + "/models/bert/save_models/bert_classifier_bilstm_model_hard.pt"  # 硬标签蒸馏模型训练结果保存路径
        self.bert_model_distill_model_path_soft = self.BASE_DIR + "/models/bert/save_models/bert_classifier_bilstm_model_soft.pt"  # 软标签蒸馏模型训练结果保存路径

        # 6. bert模型蒸馏 -> BiLSTM模型的参数配置.
        self.embed_size = 128
        self.hidden_size_lstm = 256
        self.lstm_learning_rate = 1e-3
        self.dropout = 0.3
        self.num_layers = 3
        self.lstm_epochs = 10


        # ===============================================================================================#

        # 5. 剪枝模型存放地址
        self.bert_model_pruning_model_path = self.BASE_DIR + "/models/bert/save_models/bert_classifier_pruning_model.pt"  # 模型训练结果保存路径




if __name__ == "__main__":
    config = Config()
    print(config.BASE_DIR)
    # print(config.test_datapath)
    # print(config.class_datapath)
    #
    # print(config.id2class_dict)
    #
    # with open(config.class_datapath, "r", encoding="utf-8") as f:
    #     for i in f.read().split("\n"):
    #         print(i)



import torch            # 用于深度学习模型的构建和训练
import datetime         # 时间处理包

# 导入Bert相关组件, BertModel(BERT模型的主体), BertTokenizer(BERT的分词器), BertConfig(BERT的配置)
from transformers import BertModel, BertTokenizer, BertConfig


# todo 1.定义变量, 记录当前时间(年月日格式)
current_date = datetime.datetime.now().strftime('%Y%m%d')   # 例如: 20250914


# todo 2. 定义配置文件类, 集中管理 模型和训练所需的参数.
class Config(object):
    def __init__(self):
        """
        配置类，包含模型和训练所需的各种参数。
        """

        # 1. 基础的模型信息, 例如: 模型名称
        self.model_name = "bert"  # 模型名称

        # 2. 路径配置.
        # 根目录
        self.root_path = '../'
        # 原始数据路径
        self.train_datapath = self.root_path + '_01_data/data/train.txt'
        self.test_datapath = self.root_path + '_01_data/data/test.txt'
        self.dev_datapath = self.root_path + '_01_data/data/dev.txt'
        # 类别文档
        self.class_path = self.root_path + "_01_data/data/class.txt"

        # 从类别文件中读取所有类别的名称.
        self.class_list = [line.strip() for line in open(self.class_path, encoding="utf-8")]  # 类别名单

        # 模型训练保存路径
        self.model_save_path = self.root_path + "_04_bert/save_models/bert_classifier_model.pt"  # 模型训练结果保存路径

        # 模型训练+预测的时候, 指定设备
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 训练设备，如果GPU可用，则为cuda，否则为cpu


        # 3. BERT模型的相关配置.
        self.bert_path = self.root_path + "/_04_bert/bert-base-chinese"  # 预训练BERT模型的路径
        self.bert_model = BertModel.from_pretrained(self.bert_path) # 加载预训练BERT模型
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)  # BERT模型的分词器
        self.bert_config = BertConfig.from_pretrained(self.bert_path)  # BERT模型的配置


        # 4. 训练参数配置.

class Config:
    def __init__(self):
        # todo 1.项目根目录
        self.root_path = '../'

        # todo 2.原始数据路径
        self.train_datapath = self.root_path + '_01_data/data/train.txt'
        self.test_datapath = self.root_path + '_01_data/data/test.txt'
        self.dev_datapath = self.root_path + '_01_data/data/dev.txt'
        # 类别文档
        self.class_doc_path = self.root_path +  "_01_data/data/class.txt"
        # _01_data\data\class.txt

        # todo 3.数据处理保存路径
        # 字符级别fasttext
        self.process_train_datapath_char = self.root_path + "_03_fasttext/final_data/train_process_char.txt"
        self.process_test_datapath_char = self.root_path + "_03_fasttext/final_data/test_process_char.txt"
        self.process_dev_datapath_char = self.root_path + "_03_fasttext/final_data/dev_process_char.txt"

        # 词级别fasttext
        self.process_train_datapath_word = self.root_path + "_03_fasttext/final_data/train_process_word.txt"
        self.process_test_datapath_word = self.root_path + "_03_fasttext/final_data/test_process_word.txt"
        self.process_dev_datapath_word = self.root_path + "_03_fasttext/final_data/dev_process_word.txt"

        # todo 4.模型路径
        self.ft_model_save_path = self.root_path + '_03_fasttext/save_models'

        # todo 5.处理完的数据（用于训练）
        self.final_data = self.root_path + '_03_fasttext/final_data'

        # todo 6.类别字典, 格式为: {0: 'business', 1: 'entertainment', 2: 'sports', 3: 'tech'...}
        self.id2class_dict = {i:line.strip() for i, line in enumerate(open(self.class_doc_path))}


# 测试代码
if __name__ == '__main__':
    config = Config()
    print(config.class_doc_path)

    # {0: 'finance', 1: 'realty', 2: 'stocks', 3: 'education', 4: 'science', 5: 'society', 6: 'politics', 7: 'sports',
    # 8: 'game', 9: 'entertainment'}
    print(config.id2class_dict)
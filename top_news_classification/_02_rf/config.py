"""
配置类
"""
class Config:


    def __init__(self):
        # 1.1 配置训练集的路径.
        self.train_datapath = '../_01_data/data/train.txt'
        # 1.2 配置测试集的路径.
        self.test_datapath = '../_01_data/data/test.txt'
        # 1.3 配置验证集的路径.
        self.dev_datapath = '../_01_data/data/dev.txt'
        # 1.4 配置 类别定义文件 路径
        self.class_datapath = '../_01_data/data/class.txt'

        # 2.1 数据预处理后训练集保存路径
        self.process_train_datapath = './data/process_train_data.txt'
        # 2.2 测试集预处理后保存路径
        self.process_test_datapath = './data/process_test_data.txt'
        # 2.3 验证集预处理后保存路径
        self.process_dev_datapath = './data/process_dev_data.txt'

        # 指定停止词路径
        self.stopword_datapath = '../_01_data/data/stopwords.txt'

        # 模型保存路径
        self.rf_model_path = '../_02_rf/model/rf_model.pkl'
        self.tfidf_model_save_path = '../_02_rf/model/tfidf_model.pkl'

        # 测试集预测结果保存路径
        self.predict_result_path = './result/predict_result.csv'



if __name__ == '__main__':
    config = Config()
    print(config.test_datapath)
    print(config.class_datapath)
    print(config.process_train_datapath)



"""
配置类
"""
class Config:


    def __init__(self):
        # 1.1 配置训练集的路径.
        self.train_datapath = './data/train.txt'
        # 1.2 配置测试集的路径.
        self.test_datapath = './data/test.txt'
        # 1.3 配置验证集的路径.
        self.dev_datapath = './data/dev.txt'
        # 1.4 配置 类别定义文件 路径
        self.class_datapath = './data/class.txt'


if __name__ == '__main__':
    config = Config()
    print(config.test_datapath)
    print(config.class_datapath)



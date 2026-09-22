from src.config import Config
from src.data_process.data_analysis import load_json_data

config = Config()

def load_cic_dataset():
    train_data = load_json_data(config.train_datapath)
    dev_data = load_json_data(config.dev_datapath)
    test_data = load_json_data(config.test_datapath)

    return train_data, dev_data, test_data
















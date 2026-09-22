from src.top_news.config import Config
import torch
from src.top_news.models.h2_bert_classifier_model import BertClassifier

# 压制警告.
import warnings
warnings.filterwarnings("ignore")


# todo 1.加载全局配置.
conf = Config()

# todo 2. 准备BERT预测模型.
model = BertClassifier()

model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

# 加载预训练模型的权重.
# 如果是gpu训练的模型, 用cpu设备加载会有错误, 设定map_location=conf.device指定设备解决此问题
# weights_only=True 限制 pickle 只能解析基础数值 / 张量，防止加载被篡改的 pth 文件导致代码注入、恶意脚本执行，PyTorch 官方推荐生产环境固定 weights_only=True。
model.load_state_dict(torch.load(conf.bert_model_quantization_model_path, map_location='cpu', weights_only=True))

# 模型放到设备上
# model.to('cpu')

# 设置模型为评估模式.
model.eval()

# todo 3. 定义预测函数, 接收文本数据, 返回分类结果.
def predict_fun(data_dict):
    """
    接收包含文本的字典, 通过BERT模型预测文本类别, 返回带预测结果的字典.
    :param data_dict: 输入字典, 格式为: {'text': '待预测文本内容'}
    :return:  {'text': '待预测文本内容', 'pred_class': '文本类别'}
    """
    # 1. 提取输入文本, 获取待预测的字符串.
    text = data_dict['text']

    # 2. 文本编码, 将原始文本 -> BERT模型可识别的token id
    """
    常用参数: 
        add_special_tokens=True,            # 是否添加特殊标记(CLS, SEP, PAD, ...)
        padding='max_length',               # 填充策略
        max_length=conf.pad_size,           # 最大长度
        truncation=True,                    # 是否截断
        return_attention_mask=True,         # 是否返回注意力掩码
        return_tensors='pt'                 # 返回张量格式
    """
    tokenized_result = conf.tokenizer(text,
                                      add_special_tokens=True,
                                      padding="max_length",
                                      max_length=conf.pad_size,
                                      truncation=True,
                                      return_attention_mask=True,
                                      return_tensors='pt'
                                      )


    # 3. 提取模型所需要的特征.
    input_ids = tokenized_result['input_ids']
    attention_mask = tokenized_result['attention_mask']


    # 4. 转换数据并指定设备.
    input_ids = input_ids.to('cpu')
    attention_mask = attention_mask.to('cpu')


    # 5. 模型预测动作. 禁用梯度计算以提高效率并减少内存占用
    with torch.no_grad():

        # 5.1 前向传播
        y_pred = model(input_ids, attention_mask)

        # 5.2 获取预测类别索引.
        y_pred_label = torch.argmax(y_pred, dim=-1)

        # 5.3 转换索引格式, 从PyTorch张量  -> Python的标量.
        y_pred_label = y_pred_label.item()

        # 5.4 获取预测类别. 根据索引 -> 类别名
        y_pred_name = conf.class_list[y_pred_label]

        # 5.5 打印结果

        # 5.6 添加预测结果到字典, 并返回.
        data_dict['pred_class'] = y_pred_name

    # 6. 返回结果
    return data_dict


# todo 4. 测试代码.
if __name__ == '__main__':
    # 1. 创建测试数据集.
    data_dict_ = {'text': '体验2D巅峰 倚天屠龙记十大创新概览'}
    # 2. 调用预测接口, 并打印结果.
    print(predict_fun(data_dict_))
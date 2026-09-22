import torch
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
from tqdm import tqdm
from src.top_news.models.h2_bert_classifier_model import BertClassifier
from src.top_news.config import Config
from src.top_news.training.h1_dataloader_utils import build_dataloader


def model2dev(model, data_loader, device):
    """
    在验证或测试集上评估 BERT 分类模型的性能。
    参数：
        model (nn.Module): BERT 分类模型。
        data_loader (DataLoader): 数据加载器（验证或测试集）。
        device (str): 设备（"cuda" 或 "cpu"）。
    返回：
        tuple: (分类报告, F1 分数, 准确度, 精确度，召回率)
            - report: 分类报告（包含每个类别的精确度、召回率、F1 分数等）。
            - f1score: 微平均 F1 分数。
            - accuracy: 准确度。
            - precision: 微平均精确度
            - recall: 微平均召回率
    """


    # todo 1. 设置模型为评估模式（禁用 dropout,并改变batch_norm行为）
    model.eval()
    # 2. 初始化列表，all_preds, all_labels, 存储预测结果和真实标签
    all_pred_list = []
    all_label_list = []
    # 3. todo torch.no_grad()禁用梯度计算以提高效率并减少内存占用
    with torch.no_grad():
        # 4. 遍历数据加载器，逐批次进行预测
        for batch in tqdm(data_loader):
            # 4.1 提取批次数据并移动到设备
            input_ids, attention_mask, label = batch
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            label = label.to(device)
            # 4.2 前向传播：模型预测
            y_pred = model(input_ids, attention_mask)

            # 4.3 获取预测结果（最大 logits分数 对应的类别）
            y_pred_labels = torch.argmax(y_pred, dim=-1)

            # 4.4 存储预测标签
            all_pred_list.extend(y_pred_labels.cpu().tolist())
            # 存储真实标签
            all_label_list.extend(label.cpu().tolist())


    # 5. 计算分类报告、F1 分数、准确率，精确率，召回率
    report = classification_report(all_label_list, all_pred_list)
    accuracy = accuracy_score(all_label_list, all_pred_list)
    precision = precision_score(all_label_list, all_pred_list, average='macro')
    recall = recall_score(all_label_list, all_pred_list, average='macro')
    f1 = f1_score(all_label_list, all_pred_list, average='macro')

    # 6. 返回评估结果
    return report, accuracy, precision, recall, f1


if __name__ == '__main__':
    config = Config()

    bert_model = BertClassifier()
    # weights_only 避免模型文件的注入攻击
    bert_model.load_state_dict(torch.load(config.model_save_path, map_location=config.device, weights_only=True))
    bert_model.to(config.device)
    # dataloader
    _, test_dataloader, dev_dataloader = build_dataloader()
    # 模型评估
    report_test, accuracy_test, precision_test, recall_test, f1_test = model2dev(bert_model, test_dataloader, config.device)
    print(f"测试集--准确率:{accuracy_test},精确率{precision_test},召回率{recall_test},f1值{f1_test}")

    report_dev, accuracy_dev, precision_dev, recall_dev, f1_dev = model2dev(bert_model, dev_dataloader, config.device)
    print(f"验证集--准确率:{accuracy_dev},精确率{precision_dev},召回率{recall_dev},f1值{f1_dev}")
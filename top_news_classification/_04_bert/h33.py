import torch  # 深度学习框架, 提供张量计算, 神经网络构建等...
import torch.nn as nn  # 神经网络模块, 损失函数, 网络层
from torch.optim import AdamW  # 优化器, 适用于Transformer类模型的优化器, 缓解梯度消失问题.

# 用于评估模型性能的库
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
from tqdm import tqdm  # 进度条
from config import Config  # 配置文件类
from model2dev_utils import model2dev  # 导入自定义验证函数(例如: 精确率, 召回率...)
from h1_dataloader_utils import build_dataloader  # 获取数据集加载器
from h2_bert_classifier_model import BertClassifier  # 导入BERT分类模型

# 忽略的警告信息
import warnings

warnings.filterwarnings("ignore")

# todo 1. 加载配置对象，包含模型参数、路径等
conf = Config()


# todo 2. 定义模型训练函数, 封装完整的训练流程(数据加载, 模型训练, 验证, 保存)
def model2train():
    # 1. 准备训练/验证/测试数据, 获取其对应的 数据集加载器.
    train_dataloader, test_dataloader, dev_dataloader = build_dataloader()

    # 【新增】一次性将整个训练集加载到GPU
    print("一次性将整个训练集加载到GPU...")
    # 先获取第一个batch的形状，用于计算总batch数
    first_batch = next(iter(train_dataloader))
    batch_size = first_batch[0].shape[0]

    # 初始化列表，用于存储所有批次的数据
    all_input_ids = []
    all_attention_mask = []
    all_labels = []

    # 遍历原始DataLoader，将所有数据加载到CPU内存
    for batch in tqdm(train_dataloader):
        input_ids, attention_mask, label = batch
        all_input_ids.append(input_ids)
        all_attention_mask.append(attention_mask)
        all_labels.append(label)

    # 将所有批次的数据拼接成一个大的Tensor，并一次性移动到GPU
    print("将数据移动到GPU...")
    all_input_ids = torch.cat(all_input_ids, dim=0).to(conf.device)
    all_attention_mask = torch.cat(all_attention_mask, dim=0).to(conf.device)
    all_labels = torch.cat(all_labels, dim=0).to(conf.device)

    # 计算总batch数
    total_samples = len(all_input_ids)
    total_batches = (total_samples + batch_size - 1) // batch_size

    # 创建一个函数，用于模拟DataLoader的迭代行为
    def get_batch(batch_idx):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, total_samples)
        return (
            all_input_ids[start_idx:end_idx],
            all_attention_mask[start_idx:end_idx],
            all_labels[start_idx:end_idx]
        )

    # 2. 初始化并配置模型.
    print(f"=======正在使用{conf.device}进行训练========")
    model = BertClassifier().to(conf.device)

    # 3. 定义损失函数, 使用: 交叉熵损失.
    criterion = nn.CrossEntropyLoss()

    # 4. 定义优化器, 使用: AdamW 优化器.
    optimizer = AdamW(model.parameters(), lr=conf.learning_rate)

    # 5. 初始化最优F1分数, 用于筛选性能最好的模型(即: 初始值为0, 后续更新)
    best_f1 = 0

    # 6. 具体的训练过程, 外层循环表示训练的轮数. 每轮都要遍历所有训练数据.
    for epoch in range(conf.num_epochs):

        # 6.1 设置模型为训练模式.
        model.train()

        # 6.2 初始化训练过程中的统计变量.total_loss(损失值), batch_count(迭代次数), train_preds(预测结果), train_labels(真实标签)
        total_loss = 0
        batch_count = 0

        train_pred_list = []
        train_label_list = []

        # 6.3 内层循环, 遍历训练集, 获取到每个批次, 逐批次更新模型.
        # 【修改】使用自定义的批次迭代方式
        for batch_idx in tqdm(range(total_batches), desc=f"Epoch {epoch + 1}"):
            # 6.3.1 从GPU数据集中获取批次数据
            input_ids, attention_mask, label = get_batch(batch_idx)

            # 6.3.2 前向传播：模型预测
            y_pred = model(input_ids, attention_mask)

            # 6.3.3 计算损失
            loss = criterion(y_pred, label)

            # 6.3.4 梯度清零, 保证参数更新准确
            optimizer.zero_grad()

            # 6.3.5 反向传播：计算梯度, 链式求导.
            loss.backward()

            # 6.3.6 参数更新(梯度更新), 基于梯度和优化器规则(AdamW)更新模型权重
            optimizer.step()

            # 6.3.7 累计损失值. 累计迭代次数
            total_loss += loss.item()
            batch_count += 1

            # 6.3.8 获取当前批次的预测标签.
            preds = torch.argmax(y_pred, dim=1)

            # 6.3.9 存储当前批次的预测标签和真实标签.
            train_pred_list.extend(preds.cpu().numpy())
            train_label_list.extend(label.cpu().numpy())

            # 6.4 每100个批次或者轮次末尾, 验证模型效果(在验证集评估模型并保存最优模型)
            if batch_count % 100 == 0 or batch_count == total_batches:

                # 6.5 如果验证 F1 分数优于历史最佳，保存模型
                print(f"第{epoch + 1}轮，第{batch_count}次 平均损失{total_loss / batch_count}")

                # 验证集的表现
                report, accuracy, precision, recall, current_f1 = model2dev(model=model, data_loader=dev_dataloader,
                                                                            device=conf.device)
                print(
                    f"第{epoch + 1}轮,第{batch_count}次--准确率:{accuracy},精确率:{precision},召回率:{recall},f1值:{current_f1}")

                model.train()

                if current_f1 > best_f1:
                    print(f"当前f1{current_f1} 历史最好{best_f1} =====> 开始保存")
                    # 保存模型
                    torch.save(model.state_dict(), conf.model_save_path)
                    # 更新f1
                    best_f1 = current_f1


# todo 3. 主程序入口.
if __name__ == '__main__':
    model2train()

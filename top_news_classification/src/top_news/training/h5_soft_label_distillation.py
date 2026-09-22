import torch  # 深度学习框架, 提供张量计算, 神经网络构建等...
import torch.nn as nn  # 神经网络模块, 损失函数, 网络层
from torch.optim import AdamW  # 优化器, 适用于Transformer类模型的优化器, 缓解梯度消失问题.

# 用于评估模型性能的库
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
from tqdm import tqdm  # 进度条
from config import Config  # 配置文件类
from model2dev_utils import model2dev  # 导入自定义验证函数(例如: 精确率, 召回率...)
from h1_dataloader_utils import build_dataloader  # 获取数据集加载器

from h2_bert_classifier_model import BertClassifier  # 教师模型, 导入BERT分类模型
from h3_bilstm_classifier_model import BiLSTMClassifier  # 学生模型, 导入Bilstm分类模型
import torch.nn.functional as F  # 函数模块, 激活函数, 损失函数等.


# 忽略的警告信息
import warnings

warnings.filterwarnings("ignore")


# todo 1. 加载配置对象，包含模型参数、路径等
conf = Config()


# todo 2. 定义模型训练函数, 封装完整的训练流程(数据加载, 模型训练, 验证, 保存)
def model2train():
    # 1. 准备训练/验证/测试数据, 获取其对应的 数据集加载器.
    train_dataloader, test_dataloader, dev_dataloader = build_dataloader()

    # 2. 初始化并配置模型.
    # 2.1 实例化教师模型.
    # 创建教师对象.
    teacher_model = BertClassifier()

    # 加载教师模型的预训练参数.
    print(conf.model_save_path)
    teacher_model.load_state_dict(torch.load(conf.model_save_path, weights_only=True))
    # print(teacher_model.parameters())
    teacher_model.to(conf.device)
    teacher_model.eval()
    # 2.2 创建学生模型.
    student_model = BiLSTMClassifier()
    student_model.to(conf.device)

    # 3. 定义损失函数, 使用: 交叉熵损失.
    criterion = nn.CrossEntropyLoss()

    # 4. 定义优化器, 使用: AdamW 优化器.
    optimizer = AdamW(student_model.parameters(), lr=conf.lstm_learning_rate)

    # 5. 初始化最优F1分数, 用于筛选性能最好的模型(即: 初始值为0, 后续更新)
    best_f1 = 0

    # 6. 具体的训练过程, 外层循环表示训练的轮数. 每轮都要遍历所有训练数据.
    for epoch in range(conf.lstm_epochs):

        # 6.1 设置教师模型为评估模式, 学生模型为训练模式.
        student_model.train()
        # 6.2 初始化训练过程中的统计变量.total_loss(损失值), batch_count(迭代次数)
        total_loss = 0
        batch_count = 0
        # 温度
        T = 2.
        # 系数
        alpha = 0.7

        # 6.3 内层循环, 遍历训练集, 获取到每个批次, 逐批次更新模型.
        for batch in tqdm(train_dataloader):
            # 6.3.1 提取批次数据并移动到指定设备
            input_ids, attention_mask, label = batch
            input_ids, attention_mask, label = input_ids.to(conf.device), attention_mask.to(conf.device), label.to(conf.device)
            # ----------------------------- 学生模型前向传播 -----------------------------
            # 6.3.2 前向传播：学生模型预测值
            student_logits = student_model(input_ids, attention_mask)
            # print(student_logits.shape)


            # ----------------------------- 老师模型前向传播 -----------------------------
            # 6.3.3 教师模型预测值与预测标签, 禁用梯度计算以提高效率并减少内存占用
            with torch.no_grad():
                teacher_logits = teacher_model(input_ids, attention_mask)
                teacher_label = torch.argmax(teacher_logits, dim=-1)
            # print(teacher_label.shape)
            # a = input()

            # 6.3.4 计算硬损失标签.
            hard_loss = criterion(student_logits, teacher_label)

            # todo 6.3.5 计算软标签损失: KL散度损失, 衡量学生和教师的平滑概率分布的差异. 首先计算学生模型和老师模型的对数概率
            student_log_probs = torch.log_softmax(student_logits / T, dim=-1)
            teacher_log_probs = torch.log_softmax(teacher_logits / T, dim=-1)
            # todo 6.3.6 具体的计算KL散度的动作.标准知识蒸馏损失中，软标签部分要乘以T**2, 确保软标签损失与硬标签损失在梯度量级上可比
            """
            kl_div参数说明:
            input: 输入张量，通常是学生模型输出的 log 概率
            target: 目标张量，通常是教师模型输出的分布。根据 log_target 的取值，可以是概率或 log 概率。形状需与 input 相同。
            reduction: 指定输出损失的归约方式(mean: 对所有元素的损失求平均, sum:对所有元素的损失求和, batchmean:按批次维度取平均)
            log_target: 指示 target 是否为 log 概率
                False（默认）：表示你传入的 target 是普通概率(softmax的输出), 函数内部会自动对 target 取对数
                True：target 已经是 log 概率
            """
            soft_loss = F.kl_div(input=student_log_probs,
                                 target=teacher_log_probs,
                                 reduction="batchmean",
                                 log_target=True) * (T ** 2)

            # todo 总损失是软标签损失和硬标签损失之和
            loss = (1-alpha)*hard_loss + alpha*soft_loss



            # 6.3.5 累计损失值. 累计迭代次数
            total_loss += hard_loss.item()
            batch_count += 1

            # 6.3.6 梯度清零, 保证参数更新准确
            optimizer.zero_grad()

            # 6.3.7 反向传播：计算梯度, 链式求导.
            loss.backward()

            # 6.3.8 参数更新(梯度更新), 基于梯度和优化器规则(AdamW)更新模型权重
            optimizer.step()

            # 6.4 每100个批次或者轮次末尾, 验证模型效果(在验证集评估模型并保存最优模型)
            if batch_count % 100 == 0 or batch_count == len(train_dataloader):

                # 6.4.1 调用model2dev函数, 计算在验证集的评估指标
                report, accuracy, precision, recall, f1 = model2dev(student_model, dev_dataloader, conf.device)

                # 6.4.2 打印平均损失
                print(f"第{epoch + 1}轮, 第{batch_count}次迭代, 平均损失是:{total_loss / batch_count}")
                print(f"第{epoch + 1}轮, 第{batch_count}次迭代, f1值是:{f1}")

                # 6.4.3 学生模型切换回训练模式
                student_model.train()

                # 6.4.4 如果f1值高于历史最优, 则进行保存
                if f1 > best_f1:
                    torch.save(student_model.state_dict(), conf.bert_model_distill_model_path_soft)
                    best_f1 = f1




# todo 3. 主程序入口.
if __name__ == '__main__':
    model2train()
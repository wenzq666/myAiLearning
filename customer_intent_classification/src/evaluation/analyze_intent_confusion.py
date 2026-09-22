import os

import pandas as pd
import torch

from sklearn.metrics import confusion_matrix
from transformers import AutoModelForSequenceClassification

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders


# =========================================================
# Config
# =========================================================

config = Config()


# =========================================================
# 1. 加载模型并预测 Dev
# =========================================================

def predict_dev():

    device = config.device

    # -----------------------------------------------------
    # 加载原始数据
    #
    # Dev 始终使用原始 Dev
    # -----------------------------------------------------

    train_df, dev_df, _ = load_cic_dataset()

    dev_df = (
        dev_df
        .copy()
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # 类别数量
    # -----------------------------------------------------

    num_classes = max(
        int(train_df["label"].max()),
        int(dev_df["label"].max())
    ) + 1

    # -----------------------------------------------------
    # 创建 DataLoader
    #
    # 这里只需要 dev_loader
    # -----------------------------------------------------

    _, dev_loader, _ = (
        create_macbert_dataloaders(
            train_df=train_df,
            dev_df=dev_df,
            batch_size=16,
            max_length=64
        )
    )

    # -----------------------------------------------------
    # 创建模型
    #
    # 和 train_macbert.py 保持一致
    # -----------------------------------------------------

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            config.bert_path,
            num_labels=num_classes
        )
    )

    # -----------------------------------------------------
    # 加载 Clean Weighted MacBERT
    # -----------------------------------------------------

    model_path = (
        config.bert_save_model
        + "/macbert_clean_weighted_best.pt"
    )

    if not os.path.exists(model_path):

        raise FileNotFoundError(
            f"找不到模型：{model_path}"
        )

    state_dict = torch.load(
        model_path,
        map_location=device
    )

    model.load_state_dict(
        state_dict
    )

    model.to(device)

    model.eval()

    # -----------------------------------------------------
    # 预测
    # -----------------------------------------------------

    predictions = []

    with torch.no_grad():

        for batch in dev_loader:

            input_ids = (
                batch["input_ids"]
                .to(device)
            )

            attention_mask = (
                batch["attention_mask"]
                .to(device)
            )

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = outputs.logits

            pred = torch.argmax(
                logits,
                dim=1
            )

            predictions.extend(
                pred.cpu().tolist()
            )

    # -----------------------------------------------------
    # 保存预测结果
    # -----------------------------------------------------

    dev_df["pred_label"] = predictions

    return dev_df


# =========================================================
# 2. 构建 Label Mapping
# =========================================================

def build_label_mapping(dev_df):

    label_mapping = (
        dev_df[
            [
                "label",
                "label_des"
            ]
        ]
        .drop_duplicates()
        .set_index("label")["label_des"]
        .to_dict()
    )

    return label_mapping


# =========================================================
# 3. 单向混淆分析
#
# 例如：
#
# 发货时间 -> 催促发货
#
# 与：
#
# 催促发货 -> 发货时间
#
# 分开统计
# =========================================================

def analyze_directional_confusion(
        dev_df,
        label_mapping
):

    # -----------------------------------------------------
    # 只保留预测错误的数据
    # -----------------------------------------------------

    error_df = dev_df[
        dev_df["label"]
        != dev_df["pred_label"]
    ].copy()

    # -----------------------------------------------------
    # 统计：
    #
    # true_label -> pred_label
    #
    # 出现次数
    # -----------------------------------------------------

    confusion_df = (
        error_df
        .groupby(
            [
                "label",
                "pred_label"
            ]
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    # -----------------------------------------------------
    # 标签描述
    # -----------------------------------------------------

    confusion_df[
        "true_label_des"
    ] = (
        confusion_df["label"]
        .map(label_mapping)
    )

    confusion_df[
        "pred_label_des"
    ] = (
        confusion_df["pred_label"]
        .map(label_mapping)
    )

    # -----------------------------------------------------
    # 每个真实类别的 Dev 样本数
    # -----------------------------------------------------

    support_dict = (
        dev_df["label"]
        .value_counts()
        .to_dict()
    )

    confusion_df[
        "true_support"
    ] = (
        confusion_df["label"]
        .map(support_dict)
    )

    # -----------------------------------------------------
    # 混淆比例
    #
    # 例如：
    #
    # 发货时间一共 40 条
    #
    # 其中 8 条预测成催促发货
    #
    # confusion_rate = 8 / 40
    # -----------------------------------------------------

    confusion_df[
        "confusion_rate"
    ] = (
        confusion_df["count"]
        /
        confusion_df["true_support"]
    )

    # -----------------------------------------------------
    # 排序
    # -----------------------------------------------------

    confusion_df = (
        confusion_df
        .sort_values(
            by=[
                "count",
                "confusion_rate"
            ],
            ascending=False
        )
        .reset_index(drop=True)
    )

    return confusion_df


# =========================================================
# 4. 双向混淆分析
#
# 把：
#
# A -> B
# B -> A
#
# 合并为：
#
# A <-> B
# =========================================================

def analyze_bidirectional_confusion(
        directional_df,
        label_mapping
):

    pair_records = {}

    for _, row in directional_df.iterrows():

        true_label = int(
            row["label"]
        )

        pred_label = int(
            row["pred_label"]
        )

        count = int(
            row["count"]
        )

        # -------------------------------------------------
        # 小 label 放前面
        #
        # 保证：
        #
        # (10, 20)
        # (20, 10)
        #
        # 最终都是：
        #
        # (10, 20)
        # -------------------------------------------------

        label_a = min(
            true_label,
            pred_label
        )

        label_b = max(
            true_label,
            pred_label
        )

        pair_key = (
            label_a,
            label_b
        )

        if pair_key not in pair_records:

            pair_records[
                pair_key
            ] = {

                "label_a":
                    label_a,

                "label_b":
                    label_b,

                "a_to_b":
                    0,

                "b_to_a":
                    0
            }

        # -------------------------------------------------
        # 判断方向
        # -------------------------------------------------

        if (
            true_label == label_a
            and
            pred_label == label_b
        ):

            pair_records[
                pair_key
            ][
                "a_to_b"
            ] += count

        else:

            pair_records[
                pair_key
            ][
                "b_to_a"
            ] += count

    # -----------------------------------------------------
    # 转 DataFrame
    # -----------------------------------------------------

    pair_df = pd.DataFrame(
        list(
            pair_records.values()
        )
    )

    # -----------------------------------------------------
    # 双向总混淆次数
    # -----------------------------------------------------

    pair_df[
        "total_confusion"
    ] = (
        pair_df["a_to_b"]
        +
        pair_df["b_to_a"]
    )

    # -----------------------------------------------------
    # 标签描述
    # -----------------------------------------------------

    pair_df[
        "label_a_des"
    ] = (
        pair_df["label_a"]
        .map(label_mapping)
    )

    pair_df[
        "label_b_des"
    ] = (
        pair_df["label_b"]
        .map(label_mapping)
    )

    # -----------------------------------------------------
    # 排序
    # -----------------------------------------------------

    pair_df = (
        pair_df
        .sort_values(
            by="total_confusion",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return pair_df


# =========================================================
# 5. 每个类别识别情况
# =========================================================

def analyze_class_performance(
        dev_df,
        label_mapping
):

    labels = sorted(
        dev_df["label"]
        .unique()
        .tolist()
    )

    matrix = confusion_matrix(
        dev_df["label"],
        dev_df["pred_label"],
        labels=labels
    )

    records = []

    for index, label in enumerate(labels):

        # -------------------------------------------------
        # 当前类别总样本
        # -------------------------------------------------

        support = int(
            matrix[index].sum()
        )

        # -------------------------------------------------
        # 正确预测数量
        # -------------------------------------------------

        correct = int(
            matrix[index][index]
        )

        # -------------------------------------------------
        # 错误数量
        # -------------------------------------------------

        errors = (
            support
            -
            correct
        )

        # -------------------------------------------------
        # 当前类别准确率
        # -------------------------------------------------

        if support > 0:

            class_accuracy = (
                correct
                /
                support
            )

        else:

            class_accuracy = 0.0

        records.append(
            {

                "label":
                    label,

                "label_des":
                    label_mapping.get(
                        label,
                        str(label)
                    ),

                "support":
                    support,

                "correct":
                    correct,

                "errors":
                    errors,

                "class_accuracy":
                    class_accuracy
            }
        )

    class_df = pd.DataFrame(
        records
    )

    # -----------------------------------------------------
    # 准确率最低的类别放前面
    # -----------------------------------------------------

    class_df = (
        class_df
        .sort_values(
            by=[
                "class_accuracy",
                "support"
            ],
            ascending=[
                True,
                False
            ]
        )
        .reset_index(drop=True)
    )

    return class_df


# =========================================================
# 6. Main
# =========================================================

def main():

    print(
        "正在使用 Clean Weighted MacBERT 预测 Dev..."
    )

    # =====================================================
    # 预测
    # =====================================================

    dev_df = predict_dev()

    # =====================================================
    # Label Mapping
    # =====================================================

    label_mapping = (
        build_label_mapping(
            dev_df
        )
    )

    # =====================================================
    # Dev 总体错误
    # =====================================================

    total_samples = len(
        dev_df
    )

    error_samples = (
        dev_df["label"]
        != dev_df["pred_label"]
    ).sum()

    error_rate = (
        error_samples
        /
        total_samples
    )

    print(
        "\n===== Dev Error Summary ====="
    )

    print(
        f"Samples : {total_samples}"
    )

    print(
        f"Errors  : {error_samples}"
    )

    print(
        f"Rate    : {error_rate:.4f}"
    )

    # =====================================================
    # 单向混淆
    # =====================================================

    directional_df = (
        analyze_directional_confusion(
            dev_df,
            label_mapping
        )
    )

    # =====================================================
    # 双向混淆
    # =====================================================

    bidirectional_df = (
        analyze_bidirectional_confusion(
            directional_df,
            label_mapping
        )
    )

    # =====================================================
    # 类别表现
    # =====================================================

    class_df = (
        analyze_class_performance(
            dev_df,
            label_mapping
        )
    )

    # =====================================================
    # 保存目录
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    # =====================================================
    # 保存单向混淆
    # =====================================================

    directional_path = (
        config.INTERIM_DATA_DIR
        + "/directional_confusion.csv"
    )

    directional_df.to_csv(
        directional_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 保存双向混淆
    # =====================================================

    bidirectional_path = (
        config.INTERIM_DATA_DIR
        + "/bidirectional_confusion.csv"
    )

    bidirectional_df.to_csv(
        bidirectional_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 保存类别表现
    # =====================================================

    class_path = (
        config.INTERIM_DATA_DIR
        + "/class_performance.csv"
    )

    class_df.to_csv(
        class_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 输出 Top 20 双向混淆
    # =====================================================

    print(
        "\n===== Top 20 双向混淆意图 ====="
    )

    print(
        bidirectional_df[
            [
                "label_a_des",
                "label_b_des",
                "a_to_b",
                "b_to_a",
                "total_confusion"
            ]
        ]
        .head(20)
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 输出最难识别类别
    # =====================================================

    print(
        "\n===== 最难识别的 20 个类别 ====="
    )

    print(
        class_df[
            [
                "label_des",
                "support",
                "correct",
                "errors",
                "class_accuracy"
            ]
        ]
        .head(20)
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 输出文件位置
    # =====================================================

    print(
        "\n===== Saved ====="
    )

    print(
        directional_path
    )

    print(
        bidirectional_path
    )

    print(
        class_path
    )


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    main()
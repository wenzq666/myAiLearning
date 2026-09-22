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
# 1. 加载 Clean Train
# =========================================================

def load_clean_train():

    clean_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    if not os.path.exists(clean_path):

        raise FileNotFoundError(
            f"找不到 Clean Train：{clean_path}"
        )

    train_df = pd.read_csv(
        clean_path
    )

    return train_df


# =========================================================
# 2. 加载模型并预测 Dev
# =========================================================

def predict_dev():

    device = config.device

    # -----------------------------------------------------
    # Clean Train
    #
    # 用于：
    # 1. 统计训练集类别数量
    # 2. 创建 DataLoader
    # -----------------------------------------------------

    train_df = load_clean_train()

    # -----------------------------------------------------
    # Dev 始终使用原始 Dev
    # -----------------------------------------------------

    _, dev_df, _ = load_cic_dataset()

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

    print(
        f"Train Samples : {len(train_df)}"
    )

    print(
        f"Dev Samples   : {len(dev_df)}"
    )

    print(
        f"Num Classes   : {num_classes}"
    )

    # -----------------------------------------------------
    # 创建 DataLoader
    #
    # train_loader 不使用
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
    # 与 train_macbert.py 保持一致
    # -----------------------------------------------------

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            config.bert_path,
            num_labels=num_classes
        )
    )

    # -----------------------------------------------------
    # Clean Weighted MacBERT 模型
    # -----------------------------------------------------

    model_path = (
        config.bert_save_model
        + "/macbert_clean_weighted_best.pt"
    )

    if not os.path.exists(model_path):

        raise FileNotFoundError(
            f"找不到模型：{model_path}"
        )

    print(
        f"Model Path    : {model_path}"
    )

    # -----------------------------------------------------
    # 加载模型参数
    # -----------------------------------------------------

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
    # Dev Prediction
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
    # 保存预测标签
    # -----------------------------------------------------

    dev_df[
        "pred_label"
    ] = predictions

    return (
        train_df,
        dev_df
    )


# =========================================================
# 3. Label Mapping
# =========================================================

def build_label_mapping(
        train_df,
        dev_df
):

    # -----------------------------------------------------
    # Train + Dev 一起构建 mapping
    #
    # 防止某些 label 只出现在其中一个数据集
    # -----------------------------------------------------

    train_mapping = (
        train_df[
            [
                "label",
                "label_des"
            ]
        ]
    )

    dev_mapping = (
        dev_df[
            [
                "label",
                "label_des"
            ]
        ]
    )

    mapping_df = pd.concat(
        [
            train_mapping,
            dev_mapping
        ],
        ignore_index=True
    )

    mapping_df = (
        mapping_df
        .drop_duplicates(
            subset=["label"]
        )
    )

    label_mapping = dict(
        zip(
            mapping_df["label"],
            mapping_df["label_des"]
        )
    )

    return label_mapping


# =========================================================
# 4. 单向混淆分析
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
    # 只保留预测错误
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
    # Label Description
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
    # Dev Support
    # -----------------------------------------------------

    dev_support_dict = (
        dev_df["label"]
        .value_counts()
        .to_dict()
    )

    confusion_df[
        "true_support"
    ] = (
        confusion_df["label"]
        .map(dev_support_dict)
    )

    # -----------------------------------------------------
    # Confusion Rate
    #
    # 比如：
    #
    # 发货时间：
    #
    # Dev = 40
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
            ascending=[
                False,
                False
            ]
        )
        .reset_index(drop=True)
    )

    return confusion_df


# =========================================================
# 5. 双向混淆分析
#
# A -> B
#
# B -> A
#
# 合并：
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
        # 保证：
        #
        # 10 -> 20
        # 20 -> 10
        #
        # 都归到：
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
        # A -> B
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

        # -------------------------------------------------
        # B -> A
        # -------------------------------------------------

        else:

            pair_records[
                pair_key
            ][
                "b_to_a"
            ] += count

    # -----------------------------------------------------
    # DataFrame
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
    # Label Description
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
# 6. 每个类别的表现
#
# 新增：
#
# train_support
# dev_support
# =========================================================

def analyze_class_performance(
        train_df,
        dev_df,
        label_mapping
):

    # -----------------------------------------------------
    # Train Support
    # -----------------------------------------------------

    train_support_dict = (
        train_df["label"]
        .value_counts()
        .to_dict()
    )

    # -----------------------------------------------------
    # Dev 中出现的所有 label
    # -----------------------------------------------------

    labels = sorted(
        dev_df["label"]
        .unique()
        .tolist()
    )

    # -----------------------------------------------------
    # Confusion Matrix
    # -----------------------------------------------------

    matrix = confusion_matrix(
        dev_df["label"],
        dev_df["pred_label"],
        labels=labels
    )

    records = []

    for index, label in enumerate(labels):

        # -------------------------------------------------
        # Train Support
        # -------------------------------------------------

        train_support = int(
            train_support_dict.get(
                label,
                0
            )
        )

        # -------------------------------------------------
        # Dev Support
        # -------------------------------------------------

        dev_support = int(
            matrix[index].sum()
        )

        # -------------------------------------------------
        # Correct
        # -------------------------------------------------

        correct = int(
            matrix[index][index]
        )

        # -------------------------------------------------
        # Errors
        # -------------------------------------------------

        errors = (
            dev_support
            -
            correct
        )

        # -------------------------------------------------
        # Class Accuracy
        # -------------------------------------------------

        if dev_support > 0:

            class_accuracy = (
                correct
                /
                dev_support
            )

        else:

            class_accuracy = 0.0

        # -------------------------------------------------
        # Record
        # -------------------------------------------------

        records.append(
            {

                "label":
                    label,

                "label_des":
                    label_mapping.get(
                        label,
                        str(label)
                    ),

                "train_support":
                    train_support,

                "dev_support":
                    dev_support,

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
    # 准确率低的排前面
    #
    # 同样准确率：
    #
    # Dev 样本多的排前面
    # -----------------------------------------------------

    class_df = (
        class_df
        .sort_values(
            by=[
                "class_accuracy",
                "dev_support"
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
# 7. Main
# =========================================================

def main():

    print(
        "\n正在分析 Clean Weighted MacBERT..."
    )

    # =====================================================
    # Prediction
    # =====================================================

    train_df, dev_df = (
        predict_dev()
    )

    # =====================================================
    # Label Mapping
    # =====================================================

    label_mapping = (
        build_label_mapping(
            train_df,
            dev_df
        )
    )

    # =====================================================
    # Dev Error Summary
    # =====================================================

    total_samples = len(
        dev_df
    )

    error_samples = int(
        (
            dev_df["label"]
            != dev_df["pred_label"]
        ).sum()
    )

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
    # Directional Confusion
    # =====================================================

    directional_df = (
        analyze_directional_confusion(
            dev_df,
            label_mapping
        )
    )

    # =====================================================
    # Bidirectional Confusion
    # =====================================================

    bidirectional_df = (
        analyze_bidirectional_confusion(
            directional_df,
            label_mapping
        )
    )

    # =====================================================
    # Class Performance
    # =====================================================

    class_df = (
        analyze_class_performance(
            train_df,
            dev_df,
            label_mapping
        )
    )

    # =====================================================
    # 创建输出目录
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    # =====================================================
    # 保存预测结果
    # =====================================================

    prediction_path = (
        config.INTERIM_DATA_DIR
        + "/clean_macbert_dev_predictions.csv"
    )

    dev_df.to_csv(
        prediction_path,
        index=False,
        encoding="utf-8-sig"
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
    # 保存 Class Performance
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
    # Top 20 双向混淆
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
    # 最难识别的 20 个类别
    #
    # 这次增加 train_support
    # =====================================================

    print(
        "\n===== 最难识别的 20 个类别 ====="
    )

    print(
        class_df[
            [
                "label_des",
                "train_support",
                "dev_support",
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
    # 输出文件
    # =====================================================

    print(
        "\n===== Saved ====="
    )

    print(
        prediction_path
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
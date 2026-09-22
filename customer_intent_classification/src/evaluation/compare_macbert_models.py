import os

import numpy as np
import pandas as pd
import torch

from sklearn.metrics import (
    accuracy_score,
    f1_score
)
from transformers import AutoModelForSequenceClassification

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()

BATCH_SIZE = 16
MAX_LENGTH = 64


# =========================================================
# 1. 加载 Clean Train + 原始 Dev
# =========================================================

def load_data():

    clean_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    if not os.path.exists(clean_path):
        raise FileNotFoundError(
            f"找不到 Clean Train：{clean_path}"
        )

    train_df = pd.read_csv(clean_path)

    _, dev_df, _ = load_cic_dataset()

    train_df["label"] = (
        train_df["label"].astype(int)
    )

    dev_df["label"] = (
        dev_df["label"].astype(int)
    )

    return train_df, dev_df


# =========================================================
# 2. Label Mapping
# =========================================================

def build_label_mapping(train_df, dev_df):

    mapping_df = pd.concat(
        [
            train_df[["label", "label_des"]],
            dev_df[["label", "label_des"]]
        ],
        ignore_index=True
    )

    label_mapping = (
        mapping_df
        .drop_duplicates(subset=["label"])
        .set_index("label")["label_des"]
        .to_dict()
    )

    return label_mapping


# =========================================================
# 3. 普通 Clean Weighted MacBERT
# =========================================================

def load_old_model(
        num_classes,
        device
):

    model_path = (
        config.bert_save_model
        + "/macbert_clean_weighted_best.pt"
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"找不到旧模型：{model_path}"
        )

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            config.bert_path,
            num_labels=num_classes
        )
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

    return model


# =========================================================
# 4. Label Semantic MacBERT
# =========================================================

def load_new_model(
        num_classes,
        device
):

    model_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"找不到新模型：{model_path}"
        )

    model = LabelSemanticMacBERT(
        bert_path=config.bert_path,
        num_classes=num_classes,
        temperature=0.05
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

    return model


# =========================================================
# 5. 旧模型预测
# =========================================================

def predict_old_model(
        model,
        dev_loader,
        device
):

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

            pred = torch.argmax(
                outputs.logits,
                dim=1
            )

            predictions.extend(
                pred.cpu().numpy().tolist()
            )

    return predictions


# =========================================================
# 6. 新模型预测
# =========================================================

def predict_new_model(
        model,
        dev_loader,
        device
):

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

            logits = (
                outputs[
                    "classification_logits"
                ]
            )

            pred = torch.argmax(
                logits,
                dim=1
            )

            predictions.extend(
                pred.cpu().numpy().tolist()
            )

    return predictions


# =========================================================
# 7. 整体指标
# =========================================================

def calculate_metrics(
        true_labels,
        predictions
):

    accuracy = accuracy_score(
        true_labels,
        predictions
    )

    macro_f1 = f1_score(
        true_labels,
        predictions,
        average="macro",
        zero_division=0
    )

    return accuracy, macro_f1


# =========================================================
# 8. 类别 Accuracy 对比
# =========================================================

def build_class_comparison(
        dev_df,
        old_predictions,
        new_predictions,
        label_mapping
):

    result = []

    labels = sorted(
        dev_df["label"]
        .unique()
        .tolist()
    )

    true_labels = (
        dev_df["label"]
        .values
    )

    old_predictions = np.array(
        old_predictions
    )

    new_predictions = np.array(
        new_predictions
    )

    for label in labels:

        mask = (
            true_labels == label
        )

        support = int(
            mask.sum()
        )

        old_correct = int(
            (
                old_predictions[mask]
                == label
            ).sum()
        )

        new_correct = int(
            (
                new_predictions[mask]
                == label
            ).sum()
        )

        old_accuracy = (
            old_correct / support
        )

        new_accuracy = (
            new_correct / support
        )

        result.append({

            "label":
                label,

            "label_des":
                label_mapping.get(
                    label,
                    str(label)
                ),

            "dev_support":
                support,

            "old_correct":
                old_correct,

            "new_correct":
                new_correct,

            "old_accuracy":
                old_accuracy,

            "new_accuracy":
                new_accuracy,

            "accuracy_change":
                new_accuracy
                - old_accuracy,

            "correct_change":
                new_correct
                - old_correct
        })

    return pd.DataFrame(
        result
    )


# =========================================================
# 9. 构建模型 Confusion Pair
# =========================================================

def build_confusion_pairs(
        true_labels,
        predictions
):

    confusion = {}

    for true_label, pred_label in zip(
            true_labels,
            predictions
    ):

        if true_label == pred_label:
            continue

        # ---------------------------------------------
        # 无方向 Pair：
        #
        # 例如 10 -> 20
        # 和   20 -> 10
        #
        # 都统计到 (10,20)
        # ---------------------------------------------

        label_a = min(
            true_label,
            pred_label
        )

        label_b = max(
            true_label,
            pred_label
        )

        key = (
            label_a,
            label_b
        )

        if key not in confusion:

            confusion[key] = {
                "total": 0,
                "a_to_b": 0,
                "b_to_a": 0
            }

        confusion[key]["total"] += 1

        if (
            true_label == label_a
            and pred_label == label_b
        ):

            confusion[key][
                "a_to_b"
            ] += 1

        else:

            confusion[key][
                "b_to_a"
            ] += 1

    return confusion


# =========================================================
# 10. 新旧 Confusion 对比
# =========================================================

def build_confusion_comparison(
        true_labels,
        old_predictions,
        new_predictions,
        label_mapping
):

    old_confusion = (
        build_confusion_pairs(
            true_labels,
            old_predictions
        )
    )

    new_confusion = (
        build_confusion_pairs(
            true_labels,
            new_predictions
        )
    )

    all_pairs = set(
        old_confusion.keys()
    ) | set(
        new_confusion.keys()
    )

    rows = []

    for label_a, label_b in all_pairs:

        old_info = (
            old_confusion.get(
                (label_a, label_b),
                {
                    "total": 0,
                    "a_to_b": 0,
                    "b_to_a": 0
                }
            )
        )

        new_info = (
            new_confusion.get(
                (label_a, label_b),
                {
                    "total": 0,
                    "a_to_b": 0,
                    "b_to_a": 0
                }
            )
        )

        old_total = (
            old_info["total"]
        )

        new_total = (
            new_info["total"]
        )

        rows.append({

            "label_a":
                label_a,

            "label_a_des":
                label_mapping.get(
                    label_a,
                    str(label_a)
                ),

            "label_b":
                label_b,

            "label_b_des":
                label_mapping.get(
                    label_b,
                    str(label_b)
                ),

            "old_a_to_b":
                old_info["a_to_b"],

            "old_b_to_a":
                old_info["b_to_a"],

            "new_a_to_b":
                new_info["a_to_b"],

            "new_b_to_a":
                new_info["b_to_a"],

            "old_confusion":
                old_total,

            "new_confusion":
                new_total,

            # 负数 = 混淆减少
            "confusion_change":
                new_total - old_total
        })

    comparison_df = pd.DataFrame(
        rows
    )

    return comparison_df


# =========================================================
# 11. Main
# =========================================================

def main():

    device = config.device

    print(
        f"\nDevice: {device}"
    )

    # =====================================================
    # Data
    # =====================================================

    train_df, dev_df = (
        load_data()
    )

    num_classes = (
        max(
            train_df["label"].max(),
            dev_df["label"].max()
        )
        + 1
    )

    label_mapping = (
        build_label_mapping(
            train_df,
            dev_df
        )
    )

    print(
        f"Dev Samples : {len(dev_df)}"
    )

    print(
        f"Num Classes : {num_classes}"
    )

    # =====================================================
    # DataLoader
    # =====================================================

    _, dev_loader,_ = (
        create_macbert_dataloaders(
            train_df=train_df,
            dev_df=dev_df,
            batch_size=BATCH_SIZE,
            max_length=MAX_LENGTH
        )
    )

    # =====================================================
    # Old Model
    # =====================================================

    print(
        "\nLoading old model..."
    )

    old_model = (
        load_old_model(
            num_classes,
            device
        )
    )

    print(
        "Predicting old model..."
    )

    old_predictions = (
        predict_old_model(
            old_model,
            dev_loader,
            device
        )
    )

    # -----------------------------------------------------
    # 释放旧模型显存
    # -----------------------------------------------------

    del old_model

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # =====================================================
    # New Model
    # =====================================================

    print(
        "\nLoading Label Semantic model..."
    )

    new_model = (
        load_new_model(
            num_classes,
            device
        )
    )

    print(
        "Predicting Label Semantic model..."
    )

    new_predictions = (
        predict_new_model(
            new_model,
            dev_loader,
            device
        )
    )

    # =====================================================
    # Metrics
    # =====================================================

    true_labels = (
        dev_df["label"]
        .astype(int)
        .tolist()
    )

    old_accuracy, old_f1 = (
        calculate_metrics(
            true_labels,
            old_predictions
        )
    )

    new_accuracy, new_f1 = (
        calculate_metrics(
            true_labels,
            new_predictions
        )
    )

    print(
        "\n"
        "===== Overall Comparison ====="
    )

    print(
        f"{'Model':<30}"
        f"{'Accuracy':>12}"
        f"{'Macro-F1':>12}"
    )

    print(
        "-" * 54
    )

    print(
        f"{'Clean Weighted MacBERT':<30}"
        f"{old_accuracy:>12.4f}"
        f"{old_f1:>12.4f}"
    )

    print(
        f"{'+ Label Semantic':<30}"
        f"{new_accuracy:>12.4f}"
        f"{new_f1:>12.4f}"
    )

    print(
        "-" * 54
    )

    print(
        f"{'Change':<30}"
        f"{new_accuracy-old_accuracy:>+12.4f}"
        f"{new_f1-old_f1:>+12.4f}"
    )

    # =====================================================
    # Class Comparison
    # =====================================================

    class_df = (
        build_class_comparison(
            dev_df=dev_df,
            old_predictions=old_predictions,
            new_predictions=new_predictions,
            label_mapping=label_mapping
        )
    )

    # =====================================================
    # Confusion Comparison
    # =====================================================

    confusion_df = (
        build_confusion_comparison(
            true_labels=true_labels,
            old_predictions=old_predictions,
            new_predictions=new_predictions,
            label_mapping=label_mapping
        )
    )

    # =====================================================
    # 保存
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    class_path = (
        config.INTERIM_DATA_DIR
        + "/label_semantic_class_comparison.csv"
    )

    confusion_path = (
        config.INTERIM_DATA_DIR
        + "/label_semantic_confusion_comparison.csv"
    )

    prediction_path = (
        config.INTERIM_DATA_DIR
        + "/label_semantic_dev_predictions.csv"
    )

    class_df.to_csv(
        class_path,
        index=False,
        encoding="utf-8-sig"
    )

    confusion_df.to_csv(
        confusion_path,
        index=False,
        encoding="utf-8-sig"
    )

    prediction_df = (
        dev_df.copy()
    )

    prediction_df[
        "old_pred_label"
    ] = old_predictions

    prediction_df[
        "new_pred_label"
    ] = new_predictions

    prediction_df[
        "old_pred_des"
    ] = (
        prediction_df[
            "old_pred_label"
        ]
        .map(label_mapping)
    )

    prediction_df[
        "new_pred_des"
    ] = (
        prediction_df[
            "new_pred_label"
        ]
        .map(label_mapping)
    )

    prediction_df.to_csv(
        prediction_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 提升最大的类别
    # =====================================================

    print(
        "\n"
        "===== Accuracy 提升最大的 15 个类别 ====="
    )

    improved = (
        class_df
        .sort_values(
            [
                "accuracy_change",
                "correct_change"
            ],
            ascending=[
                False,
                False
            ]
        )
        .head(15)
    )

    print(
        improved[
            [
                "label_des",
                "dev_support",
                "old_accuracy",
                "new_accuracy",
                "accuracy_change",
                "correct_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 下降最大的类别
    # =====================================================

    print(
        "\n"
        "===== Accuracy 下降最大的 15 个类别 ====="
    )

    declined = (
        class_df
        .sort_values(
            [
                "accuracy_change",
                "correct_change"
            ],
            ascending=[
                True,
                True
            ]
        )
        .head(15)
    )

    print(
        declined[
            [
                "label_des",
                "dev_support",
                "old_accuracy",
                "new_accuracy",
                "accuracy_change",
                "correct_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 原旧模型 Top 20 Confusion Pair 的变化
    #
    # 这里最重要。
    # 不是看新模型自己的 Top20，
    # 而是看旧模型原来最严重的问题有没有改善。
    # =====================================================

    print(
        "\n"
        "===== 原 Top 20 Confusion Pair 改善情况 ====="
    )

    old_top20 = (
        confusion_df
        .sort_values(
            "old_confusion",
            ascending=False
        )
        .head(20)
    )

    print(
        old_top20[
            [
                "label_a_des",
                "label_b_des",
                "old_confusion",
                "new_confusion",
                "confusion_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 改善最大的 Confusion Pair
    # =====================================================

    print(
        "\n"
        "===== 混淆改善最大的 15 个 Pair ====="
    )

    confusion_improved = (
        confusion_df[
            confusion_df[
                "old_confusion"
            ] > 0
        ]
        .sort_values(
            "confusion_change",
            ascending=True
        )
        .head(15)
    )

    print(
        confusion_improved[
            [
                "label_a_des",
                "label_b_des",
                "old_confusion",
                "new_confusion",
                "confusion_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 新增/恶化最大的 Confusion Pair
    # =====================================================

    print(
        "\n"
        "===== 混淆恶化最大的 15 个 Pair ====="
    )

    confusion_worse = (
        confusion_df
        .sort_values(
            "confusion_change",
            ascending=False
        )
        .head(15)
    )

    print(
        confusion_worse[
            [
                "label_a_des",
                "label_b_des",
                "old_confusion",
                "new_confusion",
                "confusion_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    print(
        "\n===== Saved ====="
    )

    print(class_path)
    print(confusion_path)
    print(prediction_path)


if __name__ == "__main__":
    main()
import os

import pandas as pd
import torch

from sklearn.metrics import accuracy_score, f1_score

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()


# =========================================================
# 1. 加载 Dev
# =========================================================

def load_dev():

    clean_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    train_df = pd.read_csv(clean_path)

    _, dev_df, _ = load_cic_dataset()

    train_df["sentence"] = (
        train_df["sentence"]
        .fillna("")
        .astype(str)
    )

    dev_df["sentence"] = (
        dev_df["sentence"]
        .fillna("")
        .astype(str)
    )

    train_df["label"] = (
        train_df["label"]
        .astype(int)
    )

    dev_df["label"] = (
        dev_df["label"]
        .astype(int)
    )

    return train_df, dev_df


# =========================================================
# 2. Label 映射
# =========================================================

def build_label_mapping(
        train_df,
        dev_df
):

    mapping_df = pd.concat(
        [
            train_df[
                ["label", "label_des"]
            ],
            dev_df[
                ["label", "label_des"]
            ]
        ],
        ignore_index=True
    )

    mapping_df["label_des"] = (
        mapping_df["label_des"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    mapping_df = (
        mapping_df
        .drop_duplicates(
            subset=["label"]
        )
    )

    return dict(
        zip(
            mapping_df["label"],
            mapping_df["label_des"]
        )
    )


# =========================================================
# 3. 模型预测
# =========================================================

def predict(
        model,
        dataloader,
        device
):

    model.eval()

    predictions = []

    with torch.no_grad():

        for batch in dataloader:

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
                pred
                .cpu()
                .numpy()
                .tolist()
            )

    return predictions


# =========================================================
# 4. 类别级统计
# =========================================================

def build_class_comparison(
        df,
        label_mapping
):

    rows = []

    for label_id, label_des in (
            label_mapping.items()
    ):

        class_df = df[
            df["label"] == label_id
        ]

        support = len(class_df)

        if support == 0:
            continue

        semantic_correct = (
            class_df[
                "semantic_pred"
            ]
            == label_id
        ).sum()

        hard_correct = (
            class_df[
                "hard_pred"
            ]
            == label_id
        ).sum()

        semantic_accuracy = (
            semantic_correct
            / support
        )

        hard_accuracy = (
            hard_correct
            / support
        )

        rows.append(
            {
                "label":
                    label_id,

                "label_des":
                    label_des,

                "support":
                    support,

                "semantic_correct":
                    semantic_correct,

                "hard_correct":
                    hard_correct,

                "semantic_accuracy":
                    semantic_accuracy,

                "hard_accuracy":
                    hard_accuracy,

                "correct_change":
                    hard_correct
                    - semantic_correct,

                "accuracy_change":
                    hard_accuracy
                    - semantic_accuracy
            }
        )

    return pd.DataFrame(rows)


# =========================================================
# 5. 构建无方向 Confusion Pair
# =========================================================

def build_confusion_pairs(
        df,
        pred_column,
        label_mapping
):

    confusion = {}

    for _, row in df.iterrows():

        true_label = int(
            row["label"]
        )

        pred_label = int(
            row[pred_column]
        )

        if true_label == pred_label:
            continue

        # 无方向 pair
        a = min(
            true_label,
            pred_label
        )

        b = max(
            true_label,
            pred_label
        )

        key = (
            a,
            b
        )

        confusion[key] = (
            confusion.get(
                key,
                0
            )
            + 1
        )

    rows = []

    for (
        label_a,
        label_b
    ), count in confusion.items():

        rows.append(
            {
                "label_a":
                    label_a,

                "label_a_des":
                    label_mapping[
                        label_a
                    ],

                "label_b":
                    label_b,

                "label_b_des":
                    label_mapping[
                        label_b
                    ],

                "confusion":
                    count
            }
        )

    return pd.DataFrame(rows)


# =========================================================
# 6. 对比 Confusion
# =========================================================

def compare_confusions(
        semantic_confusion,
        hard_confusion
):

    semantic_df = (
        semantic_confusion.rename(
            columns={
                "confusion":
                    "semantic_confusion"
            }
        )
    )

    hard_df = (
        hard_confusion.rename(
            columns={
                "confusion":
                    "hard_confusion"
            }
        )
    )

    result = pd.merge(
        semantic_df,
        hard_df[
            [
                "label_a",
                "label_b",
                "hard_confusion"
            ]
        ],
        on=[
            "label_a",
            "label_b"
        ],
        how="outer"
    )

    result[
        "semantic_confusion"
    ] = (
        result[
            "semantic_confusion"
        ]
        .fillna(0)
        .astype(int)
    )

    result[
        "hard_confusion"
    ] = (
        result[
            "hard_confusion"
        ]
        .fillna(0)
        .astype(int)
    )

    # outer merge 后，新出现的 Pair
    # label_des 可能为空，重新补
    return result


# =========================================================
# 7. Main
# =========================================================

def main():

    device = config.device

    print(
        f"Device: {device}"
    )

    train_df, dev_df = (
        load_dev()
    )

    label_mapping = (
        build_label_mapping(
            train_df,
            dev_df
        )
    )

    num_classes = (
        max(
            train_df["label"].max(),
            dev_df["label"].max()
        )
        + 1
    )

    # =====================================================
    # DataLoader
    # =====================================================

    _, dev_loader, _ = (
        create_macbert_dataloaders(
            train_df=train_df,
            dev_df=dev_df,
            batch_size=16,
            max_length=64
        )
    )

    # =====================================================
    # Label Semantic Model
    # =====================================================

    semantic_model = (
        LabelSemanticMacBERT(
            bert_path=
                config.bert_path,

            num_classes=
                num_classes,

            temperature=0.05
        )
    )

    semantic_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    semantic_model.load_state_dict(
        torch.load(
            semantic_path,
            map_location=device
        )
    )

    semantic_model = (
        semantic_model.to(device)
    )

    semantic_pred = predict(
        semantic_model,
        dev_loader,
        device
    )

    # 释放显存
    del semantic_model

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # =====================================================
    # Hard Negative Model
    # =====================================================

    hard_model = (
        LabelSemanticMacBERT(
            bert_path=
                config.bert_path,

            num_classes=
                num_classes,

            temperature=0.05
        )
    )

    hard_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_"
          "hard_negative_best.pt"
    )

    hard_model.load_state_dict(
        torch.load(
            hard_path,
            map_location=device
        )
    )

    hard_model = (
        hard_model.to(device)
    )

    hard_pred = predict(
        hard_model,
        dev_loader,
        device
    )

    # =====================================================
    # Predictions
    # =====================================================

    result_df = dev_df.copy()

    result_df[
        "semantic_pred"
    ] = semantic_pred

    result_df[
        "hard_pred"
    ] = hard_pred

    result_df[
        "semantic_pred_des"
    ] = (
        result_df[
            "semantic_pred"
        ]
        .map(label_mapping)
    )

    result_df[
        "hard_pred_des"
    ] = (
        result_df[
            "hard_pred"
        ]
        .map(label_mapping)
    )

    # =====================================================
    # Overall
    # =====================================================

    y_true = (
        result_df[
            "label"
        ].tolist()
    )

    semantic_accuracy = (
        accuracy_score(
            y_true,
            semantic_pred
        )
    )

    semantic_f1 = (
        f1_score(
            y_true,
            semantic_pred,
            average="macro",
            zero_division=0
        )
    )

    hard_accuracy = (
        accuracy_score(
            y_true,
            hard_pred
        )
    )

    hard_f1 = (
        f1_score(
            y_true,
            hard_pred,
            average="macro",
            zero_division=0
        )
    )

    print(
        "\n===== Overall Comparison ====="
    )

    print(
        f"{'Model':<35}"
        f"{'Accuracy':>12}"
        f"{'Macro-F1':>12}"
    )

    print(
        f"{'Label Semantic':<35}"
        f"{semantic_accuracy:>12.4f}"
        f"{semantic_f1:>12.4f}"
    )

    print(
        f"{'+ Hard Negative':<35}"
        f"{hard_accuracy:>12.4f}"
        f"{hard_f1:>12.4f}"
    )

    print(
        f"{'Change':<35}"
        f"{hard_accuracy-semantic_accuracy:>+12.4f}"
        f"{hard_f1-semantic_f1:>+12.4f}"
    )

    # =====================================================
    # Class Comparison
    # =====================================================

    class_comparison = (
        build_class_comparison(
            result_df,
            label_mapping
        )
    )

    print(
        "\n===== Biggest Class Improvements ====="
    )

    print(
        class_comparison
        .sort_values(
            [
                "correct_change",
                "accuracy_change"
            ],
            ascending=False
        )
        .head(15)
        [
            [
                "label_des",
                "support",
                "semantic_accuracy",
                "hard_accuracy",
                "correct_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    print(
        "\n===== Biggest Class Declines ====="
    )

    print(
        class_comparison
        .sort_values(
            [
                "correct_change",
                "accuracy_change"
            ],
            ascending=True
        )
        .head(15)
        [
            [
                "label_des",
                "support",
                "semantic_accuracy",
                "hard_accuracy",
                "correct_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Confusion Comparison
    # =====================================================

    semantic_confusion = (
        build_confusion_pairs(
            result_df,
            "semantic_pred",
            label_mapping
        )
    )

    hard_confusion = (
        build_confusion_pairs(
            result_df,
            "hard_pred",
            label_mapping
        )
    )

    confusion_comparison = (
        compare_confusions(
            semantic_confusion,
            hard_confusion
        )
    )

    # 补充 label_des
    confusion_comparison[
        "label_a_des"
    ] = (
        confusion_comparison[
            "label_a"
        ]
        .map(label_mapping)
    )

    confusion_comparison[
        "label_b_des"
    ] = (
        confusion_comparison[
            "label_b"
        ]
        .map(label_mapping)
    )

    confusion_comparison[
        "confusion_change"
    ] = (
        confusion_comparison[
            "hard_confusion"
        ]
        -
        confusion_comparison[
            "semantic_confusion"
        ]
    )

    print(
        "\n===== Biggest Confusion Improvements ====="
    )

    print(
        confusion_comparison
        .sort_values(
            "confusion_change"
        )
        .head(15)
        [
            [
                "label_a_des",
                "label_b_des",
                "semantic_confusion",
                "hard_confusion",
                "confusion_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    print(
        "\n===== Biggest Confusion Worsening ====="
    )

    print(
        confusion_comparison
        .sort_values(
            "confusion_change",
            ascending=False
        )
        .head(15)
        [
            [
                "label_a_des",
                "label_b_des",
                "semantic_confusion",
                "hard_confusion",
                "confusion_change"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 找出具体“修好的样本”
    #
    # Semantic 错
    # Hard Negative 对
    # =====================================================

    fixed_df = result_df[
        (
            result_df[
                "semantic_pred"
            ]
            != result_df[
                "label"
            ]
        )
        &
        (
            result_df[
                "hard_pred"
            ]
            == result_df[
                "label"
            ]
        )
    ].copy()

    # =====================================================
    # 找出具体“新增错误”
    #
    # Semantic 对
    # Hard Negative 错
    # =====================================================

    broken_df = result_df[
        (
            result_df[
                "semantic_pred"
            ]
            == result_df[
                "label"
            ]
        )
        &
        (
            result_df[
                "hard_pred"
            ]
            != result_df[
                "label"
            ]
        )
    ].copy()

    print(
        "\n===== Prediction Changes ====="
    )

    print(
        f"Fixed Samples  : "
        f"{len(fixed_df)}"
    )

    print(
        f"Broken Samples : "
        f"{len(broken_df)}"
    )

    print(
        f"Net Correct    : "
        f"{len(fixed_df)-len(broken_df):+d}"
    )

    # =====================================================
    # Save
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    class_path = (
        config.INTERIM_DATA_DIR
        + "/hard_negative_class_comparison.csv"
    )

    confusion_path = (
        config.INTERIM_DATA_DIR
        + "/hard_negative_confusion_comparison.csv"
    )

    prediction_path = (
        config.INTERIM_DATA_DIR
        + "/hard_negative_dev_predictions.csv"
    )

    fixed_path = (
        config.INTERIM_DATA_DIR
        + "/hard_negative_fixed_samples.csv"
    )

    broken_path = (
        config.INTERIM_DATA_DIR
        + "/hard_negative_broken_samples.csv"
    )

    class_comparison.to_csv(
        class_path,
        index=False,
        encoding="utf-8-sig"
    )

    confusion_comparison.to_csv(
        confusion_path,
        index=False,
        encoding="utf-8-sig"
    )

    result_df.to_csv(
        prediction_path,
        index=False,
        encoding="utf-8-sig"
    )

    fixed_df.to_csv(
        fixed_path,
        index=False,
        encoding="utf-8-sig"
    )

    broken_df.to_csv(
        broken_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\n===== Files Saved ====="
    )

    print(class_path)
    print(confusion_path)
    print(prediction_path)
    print(fixed_path)
    print(broken_path)


if __name__ == "__main__":
    main()
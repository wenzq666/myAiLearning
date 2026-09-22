import os

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from sklearn.metrics import accuracy_score, f1_score

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()


# =========================================================
# 1. 加载数据
# =========================================================

def load_data():

    train_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    train_df = pd.read_csv(
        train_path
    )

    _, dev_df, _ = (
        load_cic_dataset()
    )

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
# 2. Label Mapping
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
# 3. 加载 Temperature
# =========================================================

def load_temperature():

    temperature_path = (
        config.INTERIM_DATA_DIR
        + "/temperature.txt"
    )

    if not os.path.exists(
        temperature_path
    ):

        raise FileNotFoundError(
            "找不到 Temperature 文件："
            f"{temperature_path}\n"
            "请先运行："
            "python -m "
            "src.evaluation.calibrate_temperature"
        )

    with open(
        temperature_path,
        "r",
        encoding="utf-8"
    ) as f:

        temperature = float(
            f.read().strip()
        )

    if temperature <= 0:

        raise ValueError(
            f"Temperature 必须 > 0，"
            f"当前值：{temperature}"
        )

    return temperature


# =========================================================
# 4. 模型预测
#
# 注意：
# 这里使用的是校准后的概率：
#
# softmax(logits / temperature)
#
# Temperature Scaling 不改变 argmax，
# 所以 Accuracy / Macro-F1 应保持不变。
# =========================================================

def predict_with_confidence(
        model,
        dataloader,
        device,
        temperature
):

    model.eval()

    all_predictions = []
    all_confidence = []
    all_second_confidence = []
    all_margin = []

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

            # =============================================
            # Temperature Scaling
            # =============================================

            calibrated_logits = (
                logits / temperature
            )

            probabilities = (
                F.softmax(
                    calibrated_logits,
                    dim=1
                )
            )

            # =============================================
            # Top-2
            # =============================================

            top_probs, top_labels = (
                torch.topk(
                    probabilities,
                    k=2,
                    dim=1
                )
            )

            top1_prob = (
                top_probs[:, 0]
            )

            top2_prob = (
                top_probs[:, 1]
            )

            top1_label = (
                top_labels[:, 0]
            )

            margin = (
                top1_prob
                - top2_prob
            )

            all_predictions.extend(
                top1_label
                .cpu()
                .numpy()
                .tolist()
            )

            all_confidence.extend(
                top1_prob
                .cpu()
                .numpy()
                .tolist()
            )

            all_second_confidence.extend(
                top2_prob
                .cpu()
                .numpy()
                .tolist()
            )

            all_margin.extend(
                margin
                .cpu()
                .numpy()
                .tolist()
            )

    return (
        all_predictions,
        all_confidence,
        all_second_confidence,
        all_margin
    )


# =========================================================
# 5. Confidence 区间分析
# =========================================================

def analyze_confidence_bins(
        df
):

    bins = np.arange(
        0.0,
        1.1,
        0.1
    )

    rows = []

    for i in range(
            len(bins) - 1
    ):

        low = bins[i]
        high = bins[i + 1]

        if high < 1.0:

            part = df[
                (
                    df["confidence"]
                    >= low
                )
                &
                (
                    df["confidence"]
                    < high
                )
            ]

        else:

            part = df[
                (
                    df["confidence"]
                    >= low
                )
                &
                (
                    df["confidence"]
                    <= high
                )
            ]

        count = len(
            part
        )

        if count == 0:

            correct = 0
            accuracy = 0.0

        else:

            correct = int(
                part[
                    "correct"
                ].sum()
            )

            accuracy = (
                correct / count
            )

        rows.append(
            {
                "confidence_range":
                    f"{low:.1f}-{high:.1f}",

                "samples":
                    count,

                "correct":
                    correct,

                "wrong":
                    count - correct,

                "accuracy":
                    accuracy
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 6. Confidence Threshold 分析
#
# confidence >= threshold
# 认为可以自动接受。
# =========================================================

def analyze_confidence_thresholds(
        df
):

    thresholds = [
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.90
    ]

    total = len(
        df
    )

    rows = []

    for threshold in thresholds:

        accepted = df[
            df["confidence"]
            >= threshold
        ]

        accepted_count = len(
            accepted
        )

        rejected_count = (
            total
            - accepted_count
        )

        coverage = (
            accepted_count
            / total
        )

        if accepted_count == 0:

            accepted_accuracy = 0.0

        else:

            accepted_accuracy = (
                accepted[
                    "correct"
                ].mean()
            )

        rows.append(
            {
                "threshold":
                    threshold,

                "accepted":
                    accepted_count,

                "rejected":
                    rejected_count,

                "coverage":
                    coverage,

                "accepted_accuracy":
                    accepted_accuracy
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 7. Margin 区间分析
#
# Margin = Top1 Probability - Top2 Probability
# =========================================================

def analyze_margin_bins(
        df
):

    ranges = [
        (0.00, 0.05),
        (0.05, 0.10),
        (0.10, 0.15),
        (0.15, 0.20),
        (0.20, 0.25),
        (0.25, 0.30),
        (0.30, 0.40),
        (0.40, 0.50),
        (0.50, 0.60),
        (0.60, 0.70),
        (0.70, 0.80),
        (0.80, 0.90),
        (0.90, 1.01)
    ]

    rows = []

    for low, high in ranges:

        part = df[
            (
                df["margin"]
                >= low
            )
            &
            (
                df["margin"]
                < high
            )
        ]

        count = len(
            part
        )

        if count == 0:

            correct = 0
            accuracy = 0.0

        else:

            correct = int(
                part[
                    "correct"
                ].sum()
            )

            accuracy = (
                correct
                / count
            )

        rows.append(
            {
                "margin_range":
                    f"{low:.2f}-{high:.2f}",

                "samples":
                    count,

                "correct":
                    correct,

                "wrong":
                    count - correct,

                "accuracy":
                    accuracy
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 8. Confidence + Margin 联合分析
# =========================================================

def analyze_joint_thresholds(
        df
):

    confidence_thresholds = [
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60
    ]

    margin_thresholds = [
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40
    ]

    total = len(
        df
    )

    rows = []

    for confidence_threshold in (
            confidence_thresholds
    ):

        for margin_threshold in (
                margin_thresholds
        ):

            accepted = df[
                (
                    df["confidence"]
                    >= confidence_threshold
                )
                &
                (
                    df["margin"]
                    >= margin_threshold
                )
            ]

            accepted_count = len(
                accepted
            )

            rejected_count = (
                total
                - accepted_count
            )

            coverage = (
                accepted_count
                / total
            )

            if accepted_count == 0:

                accepted_accuracy = 0.0

            else:

                accepted_accuracy = (
                    accepted[
                        "correct"
                    ].mean()
                )

            rows.append(
                {
                    "confidence_threshold":
                        confidence_threshold,

                    "margin_threshold":
                        margin_threshold,

                    "accepted":
                        accepted_count,

                    "rejected":
                        rejected_count,

                    "coverage":
                        coverage,

                    "accepted_accuracy":
                        accepted_accuracy
                }
            )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 9. Correct VS Wrong
# =========================================================

def analyze_correct_vs_wrong(
        df
):

    correct_df = df[
        df["correct"]
    ]

    wrong_df = df[
        ~df["correct"]
    ]

    print(
        "\n===== Correct VS Wrong ====="
    )

    print(
        f"Correct Samples: "
        f"{len(correct_df)}"
    )

    print(
        f"Correct Avg Confidence: "
        f"{correct_df['confidence'].mean():.4f}"
    )

    print(
        f"Correct Avg Margin: "
        f"{correct_df['margin'].mean():.4f}"
    )

    print()

    print(
        f"Wrong Samples: "
        f"{len(wrong_df)}"
    )

    print(
        f"Wrong Avg Confidence: "
        f"{wrong_df['confidence'].mean():.4f}"
    )

    print(
        f"Wrong Avg Margin: "
        f"{wrong_df['margin'].mean():.4f}"
    )


# =========================================================
# 10. Main
# =========================================================

def main():

    device = (
        config.device
    )

    print(
        f"Device: {device}"
    )

    # =====================================================
    # Temperature
    # =====================================================

    temperature = (
        load_temperature()
    )

    print(
        f"Temperature: "
        f"{temperature:.4f}"
    )

    # =====================================================
    # Data
    # =====================================================

    train_df, dev_df = (
        load_data()
    )

    label_mapping = (
        build_label_mapping(
            train_df,
            dev_df
        )
    )

    num_classes = (
        max(
            train_df[
                "label"
            ].max(),

            dev_df[
                "label"
            ].max()
        )
        + 1
    )

    print(
        f"Classes: "
        f"{num_classes}"
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
    # Load Main Model
    # =====================================================

    model = (
        LabelSemanticMacBERT(
            bert_path=
                config.bert_path,

            num_classes=
                num_classes,

            temperature=
                0.05
        )
    )

    model_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    if not os.path.exists(
        model_path
    ):

        raise FileNotFoundError(
            f"找不到模型："
            f"{model_path}"
        )

    state_dict = (
        torch.load(
            model_path,
            map_location=device
        )
    )

    model.load_state_dict(
        state_dict
    )

    model = model.to(
        device
    )

    model.eval()

    # =====================================================
    # Predict
    # =====================================================

    (
        predictions,
        confidence,
        second_confidence,
        margin
    ) = predict_with_confidence(
        model=model,
        dataloader=dev_loader,
        device=device,
        temperature=temperature
    )

    # =====================================================
    # Result DataFrame
    # =====================================================

    result_df = (
        dev_df
        .copy()
        .reset_index(
            drop=True
        )
    )

    result_df[
        "pred_label"
    ] = predictions

    result_df[
        "pred_des"
    ] = (
        result_df[
            "pred_label"
        ]
        .map(
            label_mapping
        )
    )

    result_df[
        "confidence"
    ] = confidence

    result_df[
        "second_confidence"
    ] = second_confidence

    result_df[
        "margin"
    ] = margin

    result_df[
        "correct"
    ] = (
        result_df[
            "label"
        ]
        ==
        result_df[
            "pred_label"
        ]
    )

    # =====================================================
    # Overall
    # =====================================================

    accuracy = (
        accuracy_score(
            result_df[
                "label"
            ],

            result_df[
                "pred_label"
            ]
        )
    )

    macro_f1 = (
        f1_score(
            result_df[
                "label"
            ],

            result_df[
                "pred_label"
            ],

            average="macro",
            zero_division=0
        )
    )

    print(
        "\n===== Overall ====="
    )

    print(
        f"Samples  : "
        f"{len(result_df)}"
    )

    print(
        f"Accuracy : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro-F1 : "
        f"{macro_f1:.4f}"
    )

    # =====================================================
    # Sanity Check
    #
    # Temperature Scaling 不应该改变分类结果
    # =====================================================

    if abs(
        accuracy - 0.6590
    ) > 0.0001:

        print(
            "\n[WARNING] "
            "Accuracy 与预期 0.6590 不一致，"
            "请检查模型或数据。"
        )

    # =====================================================
    # Confidence Bins
    # =====================================================

    confidence_bins = (
        analyze_confidence_bins(
            result_df
        )
    )

    print(
        "\n===== Calibrated Confidence Bins ====="
    )

    print(
        confidence_bins
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Confidence Threshold
    # =====================================================

    threshold_result = (
        analyze_confidence_thresholds(
            result_df
        )
    )

    print(
        "\n===== Confidence Threshold ====="
    )

    print(
        threshold_result
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Margin
    # =====================================================

    margin_bins = (
        analyze_margin_bins(
            result_df
        )
    )

    print(
        "\n===== Top1 - Top2 Margin ====="
    )

    print(
        margin_bins
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Confidence + Margin
    # =====================================================

    joint_result = (
        analyze_joint_thresholds(
            result_df
        )
    )

    # ---------------------------------------------
    # 这里不能只看 Accuracy。
    #
    # Accuracy 很高但 Coverage 很低，
    # 对客服系统没有太大意义。
    #
    # 所以保留全部结果到 CSV，
    # 控制台先展示 Accuracy 较高的候选策略。
    # ---------------------------------------------

    joint_sorted = (
        joint_result
        .sort_values(
            [
                "accepted_accuracy",
                "coverage"
            ],
            ascending=[
                False,
                False
            ]
        )
    )

    print(
        "\n===== Confidence + Margin "
        "Top Strategies ====="
    )

    print(
        joint_sorted
        .head(30)
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 额外展示 Coverage >= 50% 的策略
    #
    # 这一块对最终工程阈值更有参考价值。
    # =====================================================

    practical_result = (
        joint_result[
            joint_result[
                "coverage"
            ] >= 0.50
        ]
        .sort_values(
            [
                "accepted_accuracy",
                "coverage"
            ],
            ascending=[
                False,
                False
            ]
        )
    )

    print(
        "\n===== Practical Strategies "
        "(Coverage >= 50%) ====="
    )

    print(
        practical_result
        .head(30)
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Correct VS Wrong
    # =====================================================

    analyze_correct_vs_wrong(
        result_df
    )

    # =====================================================
    # Save
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    result_df.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_dev_predictions.csv",

        index=False,
        encoding="utf-8-sig"
    )

    confidence_bins.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_bins.csv",

        index=False,
        encoding="utf-8-sig"
    )

    threshold_result.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_thresholds.csv",

        index=False,
        encoding="utf-8-sig"
    )

    margin_bins.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibrated_margin_bins.csv",

        index=False,
        encoding="utf-8-sig"
    )

    joint_result.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_margin_joint.csv",

        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\n===== Files Saved ====="
    )

    print(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_dev_predictions.csv"
    )

    print(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_thresholds.csv"
    )

    print(
        config.INTERIM_DATA_DIR
        + "/calibrated_margin_bins.csv"
    )

    print(
        config.INTERIM_DATA_DIR
        + "/calibrated_confidence_margin_joint.csv"
    )


if __name__ == "__main__":
    main()
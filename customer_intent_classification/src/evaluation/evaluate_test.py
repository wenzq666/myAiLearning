import json

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report
)

from src.config import Config
from src.inference.intent_classifier import IntentClassifier


config = Config()


# =========================================================
# 1. 读取 JSONL Test
# =========================================================

def load_test_data():

    data = []

    with open(
            config.test_datapath,
            "r",
            encoding="utf-8"
    ) as f:

        for line_num, line in enumerate(
                f,
                start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                item = json.loads(
                    line
                )

                data.append(
                    item
                )

            except json.JSONDecodeError as e:

                print(
                    f"第 {line_num} 行解析失败"
                )

                print(line)

                raise e

    df = pd.DataFrame(
        data
    )

    # =============================================
    # 类型统一
    # =============================================

    df["sentence"] = (
        df["sentence"]
        .fillna("")
        .astype(str)
    )

    df["label"] = (
        df["label"]
        .astype(int)
    )

    df["label_des"] = (
        df["label_des"]
        .fillna("")
        .astype(str)
    )

    return df


# =========================================================
# 2. 批量预测
# =========================================================

def predict_test(
        classifier,
        test_df
):

    rows = []

    total = len(
        test_df
    )

    for index, row in (
            test_df.iterrows()
    ):

        result = (
            classifier.predict(
                text=row["sentence"],
                top_k=3
            )
        )

        rows.append(
            {
                "id":
                    row["id"],

                "sentence":
                    row["sentence"],

                "true_label":
                    int(
                        row["label"]
                    ),

                "true_intent":
                    row["label_des"],

                "pred_label":
                    int(
                        result["label"]
                    ),

                "pred_intent":
                    result["intent"],

                "confidence":
                    result["confidence"],

                "second_intent":
                    result[
                        "second_intent"
                    ],

                "second_confidence":
                    result[
                        "second_confidence"
                    ],

                "margin":
                    result["margin"],

                "status":
                    result["status"]
            }
        )

        # 每 200 条打印一次进度
        if (
            (index + 1) % 200
            == 0
        ):

            print(
                f"Predicting: "
                f"{index + 1}/{total}"
            )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 3. Overall
# =========================================================

def evaluate_overall(
        result_df
):

    y_true = (
        result_df[
            "true_label"
        ]
    )

    y_pred = (
        result_df[
            "pred_label"
        ]
    )

    accuracy = (
        accuracy_score(
            y_true,
            y_pred
        )
    )

    macro_f1 = (
        f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        )
    )

    print(
        "\n===== Test Overall ====="
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

    return (
        accuracy,
        macro_f1
    )


# =========================================================
# 4. Router Evaluation
# =========================================================

def evaluate_router(
        result_df
):

    result_df = (
        result_df.copy()
    )

    result_df[
        "correct"
    ] = (
        result_df[
            "true_label"
        ]
        ==
        result_df[
            "pred_label"
        ]
    )

    total = len(
        result_df
    )

    print(
        "\n===== Router Evaluation ====="
    )

    for status in [
        "accepted",
        "ambiguous",
        "uncertain"
    ]:

        part = result_df[
            result_df[
                "status"
            ]
            == status
        ]

        count = len(
            part
        )

        coverage = (
            count / total
            if total > 0
            else 0.0
        )

        if count > 0:

            accuracy = (
                part[
                    "correct"
                ].mean()
            )

            avg_confidence = (
                part[
                    "confidence"
                ].mean()
            )

            avg_margin = (
                part[
                    "margin"
                ].mean()
            )

        else:

            accuracy = 0.0
            avg_confidence = 0.0
            avg_margin = 0.0

        print(
            f"\nStatus: {status}"
        )

        print(
            f"Samples        : "
            f"{count}"
        )

        print(
            f"Coverage       : "
            f"{coverage:.4f}"
        )

        print(
            f"Accuracy       : "
            f"{accuracy:.4f}"
        )

        print(
            f"Avg Confidence : "
            f"{avg_confidence:.4f}"
        )

        print(
            f"Avg Margin     : "
            f"{avg_margin:.4f}"
        )


# =========================================================
# 5. Accepted 样本单独评估
# =========================================================

def evaluate_accepted(
        result_df
):

    accepted_df = result_df[
        result_df[
            "status"
        ]
        == "accepted"
    ]

    total = len(
        result_df
    )

    accepted_count = len(
        accepted_df
    )

    if accepted_count == 0:

        print(
            "\nNo accepted samples."
        )

        return

    accuracy = (
        accuracy_score(
            accepted_df[
                "true_label"
            ],

            accepted_df[
                "pred_label"
            ]
        )
    )

    macro_f1 = (
        f1_score(
            accepted_df[
                "true_label"
            ],

            accepted_df[
                "pred_label"
            ],

            average="macro",
            zero_division=0
        )
    )

    coverage = (
        accepted_count
        / total
    )

    print(
        "\n===== Accepted Only ====="
    )

    print(
        f"Accepted : "
        f"{accepted_count}"
    )

    print(
        f"Coverage : "
        f"{coverage:.4f}"
    )

    print(
        f"Accuracy : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro-F1 : "
        f"{macro_f1:.4f}"
    )


# =========================================================
# 6. Status Distribution
# =========================================================

def show_status_distribution(
        result_df
):

    print(
        "\n===== Status Distribution ====="
    )

    status_counts = (
        result_df[
            "status"
        ]
        .value_counts()
    )

    print(
        status_counts
        .to_string()
    )


# =========================================================
# 7. 错误样本
# =========================================================

def show_error_examples(
        result_df,
        top_n=20
):

    errors = result_df[
        result_df[
            "true_label"
        ]
        !=
        result_df[
            "pred_label"
        ]
    ].copy()

    errors = (
        errors
        .sort_values(
            "confidence",
            ascending=False
        )
    )

    print(
        "\n===== High Confidence Errors ====="
    )

    columns = [
        "sentence",
        "true_intent",
        "pred_intent",
        "confidence",
        "margin",
        "status"
    ]

    print(
        errors[
            columns
        ]
        .head(
            top_n
        )
        .to_string(
            index=False
        )
    )


# =========================================================
# 8. Main
# =========================================================

def main():

    print(
        "===== Load Test Data ====="
    )

    test_df = (
        load_test_data()
    )

    print(
        f"Test Samples: "
        f"{len(test_df)}"
    )

    # =====================================================
    # IntentClassifier
    #
    # 内部已经包含：
    #
    # Label Semantic MacBERT
    # Temperature Scaling
    # confidence >= 0.50
    # margin < 0.15
    # =====================================================

    print(
        "\n===== Load Classifier ====="
    )

    classifier = (
        IntentClassifier(
            confidence_threshold=0.50,
            ambiguous_margin_threshold=0.15
        )
    )

    print(
        f"Temperature          : "
        f"{classifier.temperature:.4f}"
    )

    print(
        f"Confidence Threshold : "
        f"{classifier.confidence_threshold:.2f}"
    )

    print(
        f"Margin Threshold     : "
        f"{classifier.ambiguous_margin_threshold:.2f}"
    )

    # =====================================================
    # Predict
    # =====================================================

    print(
        "\n===== Predict Test ====="
    )

    result_df = (
        predict_test(
            classifier,
            test_df
        )
    )

    # =====================================================
    # Evaluation
    # =====================================================

    evaluate_overall(
        result_df
    )

    evaluate_router(
        result_df
    )

    evaluate_accepted(
        result_df
    )

    show_status_distribution(
        result_df
    )

    show_error_examples(
        result_df
    )

    # =====================================================
    # Save
    # =====================================================

    output_path = (
        config.INTERIM_DATA_DIR
        + "/test_predictions.csv"
    )

    result_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\n===== Saved ====="
    )

    print(
        output_path
    )


if __name__ == "__main__":
    main()
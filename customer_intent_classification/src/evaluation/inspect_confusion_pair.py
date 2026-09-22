import os

import pandas as pd

from src.config import Config


# =========================================================
# Config
# =========================================================

config = Config()


# =========================================================
# 1. 加载 Clean Train 和 Dev Prediction
# =========================================================

def load_data():

    clean_train_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    prediction_path = (
        config.INTERIM_DATA_DIR
        + "/clean_macbert_dev_predictions.csv"
    )

    if not os.path.exists(clean_train_path):

        raise FileNotFoundError(
            f"找不到 Clean Train：{clean_train_path}"
        )

    if not os.path.exists(prediction_path):

        raise FileNotFoundError(
            f"找不到 Dev Prediction：{prediction_path}"
        )

    train_df = pd.read_csv(
        clean_train_path
    )

    dev_df = pd.read_csv(
        prediction_path
    )

    return (
        train_df,
        dev_df
    )


# =========================================================
# 2. 根据 label_des 查 Label ID
# =========================================================

def find_label_info(
        train_df,
        label_des
):

    label_df = train_df[
        train_df["label_des"]
        == label_des
    ]

    if len(label_df) == 0:

        raise ValueError(
            f"找不到类别：{label_des}"
        )

    labels = (
        label_df["label"]
        .unique()
        .tolist()
    )

    return labels


# =========================================================
# 3. 检查 Label 和 Label Description 是否一一对应
# =========================================================

def check_label_mapping(
        train_df
):

    print(
        "\n===== Label Mapping Check ====="
    )

    # -----------------------------------------------------
    # 一个 label 是否对应多个 label_des
    # -----------------------------------------------------

    label_to_des = (
        train_df
        .groupby("label")["label_des"]
        .nunique()
    )

    abnormal_label = (
        label_to_des[
            label_to_des > 1
        ]
    )

    print(
        f"一个 label 对应多个 label_des : "
        f"{len(abnormal_label)}"
    )

    if len(abnormal_label) > 0:

        print(
            abnormal_label
        )

    # -----------------------------------------------------
    # 一个 label_des 是否对应多个 label
    # -----------------------------------------------------

    des_to_label = (
        train_df
        .groupby("label_des")["label"]
        .nunique()
    )

    abnormal_des = (
        des_to_label[
            des_to_label > 1
        ]
    )

    print(
        f"一个 label_des 对应多个 label : "
        f"{len(abnormal_des)}"
    )

    if len(abnormal_des) > 0:

        print(
            abnormal_des
        )


# =========================================================
# 4. 打印某个类别的 Train 样本
# =========================================================

def print_train_samples(
        train_df,
        label_des
):

    label_df = train_df[
        train_df["label_des"]
        == label_des
    ].copy()

    print(
        "\n"
        + "=" * 90
    )

    print(
        f"Train Intent: {label_des}"
    )

    print(
        "=" * 90
    )

    if len(label_df) == 0:

        print(
            "没有找到训练样本"
        )

        return

    labels = (
        label_df["label"]
        .unique()
        .tolist()
    )

    print(
        f"Label ID      : {labels}"
    )

    print(
        f"Train Samples : {len(label_df)}"
    )

    print()

    for index, (_, row) in enumerate(
            label_df.iterrows(),
            start=1
    ):

        print(
            f"{index:03d}. "
            f"[label={row['label']}] "
            f"{row['sentence']}"
        )


# =========================================================
# 5. 查看两个类别之间的 Dev 混淆
# =========================================================

def print_dev_confusion(
        dev_df,
        label_a,
        label_b,
        label_a_des,
        label_b_des
):

    # -----------------------------------------------------
    # A -> B
    # -----------------------------------------------------

    a_to_b = dev_df[
        (dev_df["label"] == label_a)
        &
        (dev_df["pred_label"] == label_b)
    ]

    # -----------------------------------------------------
    # B -> A
    # -----------------------------------------------------

    b_to_a = dev_df[
        (dev_df["label"] == label_b)
        &
        (dev_df["pred_label"] == label_a)
    ]

    print(
        "\n"
        + "=" * 90
    )

    print(
        "Dev Confusion"
    )

    print(
        "=" * 90
    )

    # -----------------------------------------------------
    # A -> B
    # -----------------------------------------------------

    print(
        f"\n{label_a_des}"
        f"  ->  "
        f"{label_b_des}"
    )

    print(
        f"Samples: {len(a_to_b)}"
    )

    for _, row in a_to_b.iterrows():

        print(
            f"  - {row['sentence']}"
        )

    # -----------------------------------------------------
    # B -> A
    # -----------------------------------------------------

    print(
        f"\n{label_b_des}"
        f"  ->  "
        f"{label_a_des}"
    )

    print(
        f"Samples: {len(b_to_a)}"
    )

    for _, row in b_to_a.iterrows():

        print(
            f"  - {row['sentence']}"
        )


# =========================================================
# 6. 检查两个 Label 在 Dev 中的整体预测去向
# =========================================================

def print_prediction_distribution(
        dev_df,
        true_label,
        true_label_des
):

    target_df = dev_df[
        dev_df["label"]
        == true_label
    ].copy()

    print(
        "\n"
        + "=" * 90
    )

    print(
        f"Prediction Distribution: "
        f"{true_label_des}"
    )

    print(
        "=" * 90
    )

    print(
        f"Dev Samples: {len(target_df)}"
    )

    if len(target_df) == 0:

        return

    # -----------------------------------------------------
    # 建立 label -> label_des
    # -----------------------------------------------------

    label_mapping = (
        dev_df[
            [
                "label",
                "label_des"
            ]
        ]
        .drop_duplicates(
            subset=["label"]
        )
        .set_index("label")["label_des"]
        .to_dict()
    )

    distribution = (
        target_df["pred_label"]
        .value_counts()
        .reset_index()
    )

    distribution.columns = [
        "pred_label",
        "count"
    ]

    distribution[
        "pred_label_des"
    ] = (
        distribution["pred_label"]
        .map(label_mapping)
    )

    distribution[
        "ratio"
    ] = (
        distribution["count"]
        /
        len(target_df)
    )

    print(
        distribution[
            [
                "pred_label",
                "pred_label_des",
                "count",
                "ratio"
            ]
        ]
        .to_string(
            index=False
        )
    )


# =========================================================
# 7. Main
# =========================================================

def main():

    # -----------------------------------------------------
    # 我们当前要检查的异常 Pair
    # -----------------------------------------------------

    INTENT_A = (
        "买家咨询商品区别"
    )

    INTENT_B = (
        "买家咨询优惠券使用规则"
    )

    # =====================================================
    # Load
    # =====================================================

    train_df, dev_df = (
        load_data()
    )

    print(
        "\n===== Dataset ====="
    )

    print(
        f"Clean Train : {len(train_df)}"
    )

    print(
        f"Dev         : {len(dev_df)}"
    )

    # =====================================================
    # Mapping Check
    # =====================================================

    check_label_mapping(
        train_df
    )

    # =====================================================
    # 找 Label ID
    # =====================================================

    labels_a = (
        find_label_info(
            train_df,
            INTENT_A
        )
    )

    labels_b = (
        find_label_info(
            train_df,
            INTENT_B
        )
    )

    print(
        "\n===== Target Labels ====="
    )

    print(
        f"{INTENT_A} : {labels_a}"
    )

    print(
        f"{INTENT_B} : {labels_b}"
    )

    # -----------------------------------------------------
    # 正常情况下应该一一对应
    # -----------------------------------------------------

    if len(labels_a) != 1:

        raise ValueError(
            f"{INTENT_A} 对应多个 Label："
            f"{labels_a}"
        )

    if len(labels_b) != 1:

        raise ValueError(
            f"{INTENT_B} 对应多个 Label："
            f"{labels_b}"
        )

    label_a = int(
        labels_a[0]
    )

    label_b = int(
        labels_b[0]
    )

    # =====================================================
    # Train Samples
    # =====================================================

    print_train_samples(
        train_df,
        INTENT_A
    )

    print_train_samples(
        train_df,
        INTENT_B
    )

    # =====================================================
    # Dev Confusion
    # =====================================================

    print_dev_confusion(
        dev_df=dev_df,

        label_a=label_a,
        label_b=label_b,

        label_a_des=INTENT_A,
        label_b_des=INTENT_B
    )

    # =====================================================
    # 查看 A 类所有 Dev 样本最终被预测到哪里
    # =====================================================

    print_prediction_distribution(
        dev_df=dev_df,
        true_label=label_a,
        true_label_des=INTENT_A
    )

    # =====================================================
    # 查看 B 类所有 Dev 样本最终被预测到哪里
    # =====================================================

    print_prediction_distribution(
        dev_df=dev_df,
        true_label=label_b,
        true_label_des=INTENT_B
    )


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    main()
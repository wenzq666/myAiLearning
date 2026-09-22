import os

import pandas as pd

from src.config import Config


# =========================================================
# Config
# =========================================================

config = Config()


# =========================================================
# 1. 加载上一阶段分析结果
# =========================================================

def load_analysis_data():

    prediction_path = (
        config.INTERIM_DATA_DIR
        + "/clean_macbert_dev_predictions.csv"
    )

    confusion_path = (
        config.INTERIM_DATA_DIR
        + "/bidirectional_confusion.csv"
    )

    if not os.path.exists(prediction_path):

        raise FileNotFoundError(
            f"找不到 Dev 预测结果：{prediction_path}"
        )

    if not os.path.exists(confusion_path):

        raise FileNotFoundError(
            f"找不到混淆分析结果：{confusion_path}"
        )

    dev_df = pd.read_csv(
        prediction_path
    )

    confusion_df = pd.read_csv(
        confusion_path
    )

    return (
        dev_df,
        confusion_df
    )


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
        .drop_duplicates(
            subset=["label"]
        )
        .set_index("label")["label_des"]
        .to_dict()
    )

    return label_mapping


# =========================================================
# 3. 提取 Top 混淆 Pair
# =========================================================

def get_top_confusion_pairs(
        confusion_df,
        top_n=20
):

    top_pairs = (
        confusion_df
        .sort_values(
            by="total_confusion",
            ascending=False
        )
        .head(top_n)
        .copy()
        .reset_index(drop=True)
    )

    return top_pairs


# =========================================================
# 4. 提取某一对类别之间的具体错误样本
# =========================================================

def extract_pair_samples(
        dev_df,
        label_a,
        label_b
):

    # -----------------------------------------------------
    # A -> B
    # -----------------------------------------------------

    a_to_b_df = dev_df[
        (dev_df["label"] == label_a)
        &
        (dev_df["pred_label"] == label_b)
    ].copy()

    a_to_b_df[
        "confusion_direction"
    ] = "A -> B"

    # -----------------------------------------------------
    # B -> A
    # -----------------------------------------------------

    b_to_a_df = dev_df[
        (dev_df["label"] == label_b)
        &
        (dev_df["pred_label"] == label_a)
    ].copy()

    b_to_a_df[
        "confusion_direction"
    ] = "B -> A"

    # -----------------------------------------------------
    # 合并
    # -----------------------------------------------------

    pair_samples = pd.concat(
        [
            a_to_b_df,
            b_to_a_df
        ],
        ignore_index=True
    )

    return pair_samples


# =========================================================
# 5. 整理所有 Top Pair 的 Hard Case
# =========================================================

def build_hard_cases(
        dev_df,
        top_pairs,
        label_mapping
):

    hard_case_list = []

    for pair_rank, row in top_pairs.iterrows():

        label_a = int(
            row["label_a"]
        )

        label_b = int(
            row["label_b"]
        )

        # -------------------------------------------------
        # 当前 Pair 的错误样本
        # -------------------------------------------------

        pair_samples = (
            extract_pair_samples(
                dev_df=dev_df,
                label_a=label_a,
                label_b=label_b
            )
        )

        if len(pair_samples) == 0:
            continue

        # -------------------------------------------------
        # Pair 基本信息
        # -------------------------------------------------

        pair_samples[
            "pair_rank"
        ] = pair_rank + 1

        pair_samples[
            "label_a"
        ] = label_a

        pair_samples[
            "label_b"
        ] = label_b

        pair_samples[
            "label_a_des"
        ] = label_mapping.get(
            label_a,
            str(label_a)
        )

        pair_samples[
            "label_b_des"
        ] = label_mapping.get(
            label_b,
            str(label_b)
        )

        pair_samples[
            "pair_total_confusion"
        ] = int(
            row["total_confusion"]
        )

        # -------------------------------------------------
        # 当前样本真实标签描述
        # -------------------------------------------------

        pair_samples[
            "true_label_des"
        ] = (
            pair_samples["label"]
            .map(label_mapping)
        )

        # -------------------------------------------------
        # 当前样本预测标签描述
        # -------------------------------------------------

        pair_samples[
            "pred_label_des"
        ] = (
            pair_samples["pred_label"]
            .map(label_mapping)
        )

        hard_case_list.append(
            pair_samples
        )

    # -----------------------------------------------------
    # 合并所有 Hard Case
    # -----------------------------------------------------

    if len(hard_case_list) == 0:

        return pd.DataFrame()

    hard_cases = pd.concat(
        hard_case_list,
        ignore_index=True
    )

    # -----------------------------------------------------
    # 调整字段顺序
    # -----------------------------------------------------

    columns = [

        "pair_rank",

        "label_a",
        "label_a_des",

        "label_b",
        "label_b_des",

        "pair_total_confusion",

        "confusion_direction",

        "id",

        "sentence",

        "label",
        "true_label_des",

        "pred_label",
        "pred_label_des"
    ]

    # 防止某些数据没有 id
    columns = [
        col
        for col in columns
        if col in hard_cases.columns
    ]

    hard_cases = hard_cases[
        columns
    ]

    return hard_cases


# =========================================================
# 6. 打印 Top Pair 具体样本
# =========================================================

def print_top_pair_samples(
        hard_cases,
        top_n=10
):

    print(
        "\n"
        "===== Top Confusion Hard Cases ====="
    )

    # -----------------------------------------------------
    # 只打印前 top_n 个 Pair
    # -----------------------------------------------------

    ranks = (
        hard_cases["pair_rank"]
        .drop_duplicates()
        .sort_values()
        .head(top_n)
        .tolist()
    )

    for rank in ranks:

        pair_df = hard_cases[
            hard_cases["pair_rank"]
            == rank
        ]

        if len(pair_df) == 0:
            continue

        first_row = (
            pair_df.iloc[0]
        )

        label_a_des = (
            first_row["label_a_des"]
        )

        label_b_des = (
            first_row["label_b_des"]
        )

        total_confusion = (
            first_row[
                "pair_total_confusion"
            ]
        )

        print(
            "\n"
            + "=" * 80
        )

        print(
            f"Pair Rank #{rank}"
        )

        print(
            f"{label_a_des}"
            f"  <->  "
            f"{label_b_des}"
        )

        print(
            f"Total Confusion: "
            f"{total_confusion}"
        )

        print(
            "=" * 80
        )

        # -------------------------------------------------
        # A -> B
        # -------------------------------------------------

        a_to_b_df = pair_df[
            pair_df[
                "confusion_direction"
            ]
            == "A -> B"
        ]

        print(
            f"\n[A -> B] "
            f"{label_a_des}"
            f"  ->  "
            f"{label_b_des}"
        )

        print(
            f"Samples: {len(a_to_b_df)}"
        )

        if len(a_to_b_df) == 0:

            print(
                "无"
            )

        else:

            for _, row in (
                a_to_b_df.iterrows()
            ):

                print(
                    f"  - {row['sentence']}"
                )

        # -------------------------------------------------
        # B -> A
        # -------------------------------------------------

        b_to_a_df = pair_df[
            pair_df[
                "confusion_direction"
            ]
            == "B -> A"
        ]

        print(
            f"\n[B -> A] "
            f"{label_b_des}"
            f"  ->  "
            f"{label_a_des}"
        )

        print(
            f"Samples: {len(b_to_a_df)}"
        )

        if len(b_to_a_df) == 0:

            print(
                "无"
            )

        else:

            for _, row in (
                b_to_a_df.iterrows()
            ):

                print(
                    f"  - {row['sentence']}"
                )


# =========================================================
# 7. 生成 Pair Summary
# =========================================================

def build_pair_summary(
        top_pairs
):

    summary_df = (
        top_pairs[
            [
                "label_a",
                "label_a_des",
                "label_b",
                "label_b_des",
                "a_to_b",
                "b_to_a",
                "total_confusion"
            ]
        ]
        .copy()
    )

    # -----------------------------------------------------
    # 判断混淆方向
    #
    # 这里只是辅助分析，不是模型结论
    # -----------------------------------------------------

    def get_direction_type(row):

        a_to_b = int(
            row["a_to_b"]
        )

        b_to_a = int(
            row["b_to_a"]
        )

        total = (
            a_to_b
            +
            b_to_a
        )

        if total == 0:

            return "none"

        max_direction = max(
            a_to_b,
            b_to_a
        )

        ratio = (
            max_direction
            /
            total
        )

        # 大部分错误集中在一个方向
        if ratio >= 0.8:

            return "mostly_one_way"

        return "two_way"

    summary_df[
        "confusion_type"
    ] = (
        summary_df.apply(
            get_direction_type,
            axis=1
        )
    )

    return summary_df


# =========================================================
# 8. Main
# =========================================================

def main():

    print(
        "\n正在分析细粒度意图 Hard Cases..."
    )

    # =====================================================
    # 加载数据
    # =====================================================

    (
        dev_df,
        confusion_df
    ) = load_analysis_data()

    # =====================================================
    # Label Mapping
    # =====================================================

    label_mapping = (
        build_label_mapping(
            dev_df
        )
    )

    # =====================================================
    # Top 20 Pair
    # =====================================================

    top_pairs = (
        get_top_confusion_pairs(
            confusion_df,
            top_n=20
        )
    )

    # =====================================================
    # Hard Cases
    # =====================================================

    hard_cases = (
        build_hard_cases(
            dev_df=dev_df,
            top_pairs=top_pairs,
            label_mapping=label_mapping
        )
    )

    # =====================================================
    # Pair Summary
    # =====================================================

    pair_summary = (
        build_pair_summary(
            top_pairs
        )
    )

    # =====================================================
    # 输出目录
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    # =====================================================
    # 保存 Hard Cases
    # =====================================================

    hard_case_path = (
        config.INTERIM_DATA_DIR
        + "/confusion_hard_cases.csv"
    )

    hard_cases.to_csv(
        hard_case_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 保存 Pair Summary
    # =====================================================

    summary_path = (
        config.INTERIM_DATA_DIR
        + "/confusion_pair_summary.csv"
    )

    pair_summary.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 打印 Top 10 Pair 的具体错误句子
    # =====================================================

    print_top_pair_samples(
        hard_cases,
        top_n=10
    )

    # =====================================================
    # 打印 Pair Summary
    # =====================================================

    print(
        "\n"
        "===== Confusion Pair Summary ====="
    )

    print(
        pair_summary[
            [
                "label_a_des",
                "label_b_des",
                "a_to_b",
                "b_to_a",
                "total_confusion",
                "confusion_type"
            ]
        ]
        .head(20)
        .to_string(
            index=False
        )
    )

    # =====================================================
    # Saved
    # =====================================================

    print(
        "\n===== Saved ====="
    )

    print(
        hard_case_path
    )

    print(
        summary_path
    )


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    main()
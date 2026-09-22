import pandas as pd

from src.config import Config
from src.data_process.data_loader import load_cic_dataset


config = Config()

REVIEW_FILE = (
    config.INTERIM_DATA_DIR
    + "/strong_noise_candidates_reviewed.csv"
)

OUTPUT_FILE = (
    config.PROCESSED_DATA_DIR
    + "/train_clean.csv"
)


def main():

    # =====================================================
    # 1. 读取原始 Train
    # =====================================================

    train_df, _, _ = load_cic_dataset()

    train_df = (
        train_df
        .copy()
        .reset_index(drop=True)
    )

    # 保留原始标签，方便追踪
    train_df["original_label"] = train_df["label"]

    print(
        "Original Train Samples:",
        len(train_df)
    )

    # =====================================================
    # 2. 读取人工审核结果
    # =====================================================

    review_df = pd.read_csv(
        REVIEW_FILE
    )

    review_df["review_status"] = (
        review_df["review_status"]
        .fillna("")
        .astype(str)
    )

    # =====================================================
    # 3. 查看人工审核统计
    # =====================================================

    print(
        "\n===== Review Summary ====="
    )

    print(
        review_df["review_status"]
        .value_counts(dropna=False)
        .to_string()
    )

    # =====================================================
    # 4. 只获取人工确认的 wrong
    # =====================================================

    wrong_df = review_df[
        review_df["review_status"] == "wrong"
    ].copy()

    print(
        "\nConfirmed Wrong Labels:",
        len(wrong_df)
    )

    # =====================================================
    # 5. 检查 review_label
    # =====================================================

    if wrong_df["review_label"].isna().any():

        raise ValueError(
            "存在 review_status=wrong "
            "但 review_label 为空的数据。"
        )

    wrong_df["review_label"] = (
        wrong_df["review_label"]
        .astype(int)
    )

    # =====================================================
    # 6. 建立 label -> label_des
    # =====================================================

    label_mapping = (
        train_df[
            ["label", "label_des"]
        ]
        .drop_duplicates()
        .set_index("label")["label_des"]
        .to_dict()
    )

    # =====================================================
    # 7. 修改标签
    #
    # 优先使用原始数据中的 id 定位。
    # =====================================================

    changed_count = 0

    change_records = []

    for _, row in wrong_df.iterrows():

        sample_id = row["id"]

        new_label = int(
            row["review_label"]
        )

        matched_index = train_df.index[
            train_df["id"] == sample_id
        ]

        if len(matched_index) == 0:

            print(
                f"[WARNING] 找不到 id={sample_id}"
            )

            continue

        if len(matched_index) > 1:

            raise ValueError(
                f"id={sample_id} 在 Train 中出现多次。"
            )

        index = matched_index[0]

        old_label = int(
            train_df.at[index, "label"]
        )

        # ---------------------------------------------
        # 如果人工审核标签与原标签相同，不修改
        # ---------------------------------------------

        if old_label == new_label:
            continue

        old_label_des = (
            label_mapping.get(
                old_label,
                str(old_label)
            )
        )

        new_label_des = (
            label_mapping.get(
                new_label,
                str(new_label)
            )
        )

        sentence = train_df.at[
            index,
            "sentence"
        ]

        # ---------------------------------------------
        # 修改 label
        # ---------------------------------------------

        train_df.at[
            index,
            "label"
        ] = new_label

        train_df.at[
            index,
            "label_des"
        ] = new_label_des

        changed_count += 1

        change_records.append(
            {
                "id": sample_id,
                "sentence": sentence,

                "old_label": old_label,
                "old_label_des": old_label_des,

                "new_label": new_label,
                "new_label_des": new_label_des
            }
        )

    # =====================================================
    # 8. 保存修改日志
    # =====================================================

    change_df = pd.DataFrame(
        change_records
    )

    change_log_path = (
        config.INTERIM_DATA_DIR
        + "/clean_train_changes.csv"
    )

    change_df.to_csv(
        change_log_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 9. 最终检查
    # =====================================================

    if len(train_df) != 10000:

        raise ValueError(
            "Clean Train 样本数量发生异常变化。"
        )

    if train_df["label"].isna().any():

        raise ValueError(
            "Clean Train 出现空标签。"
        )

    # =====================================================
    # 10. 保存 Clean Train
    # =====================================================


    train_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # 11. Report
    # =====================================================

    print(
        "\n===== Clean Train Result ====="
    )

    print(
        f"Original Samples : {len(train_df)}"
    )

    print(
        f"Reviewed Samples : {len(review_df)}"
    )

    print(
        f"Confirmed Wrong  : {len(wrong_df)}"
    )

    print(
        f"Labels Changed   : {changed_count}"
    )

    print(
        "\nClean Train:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        "\nChange Log:"
    )

    print(
        change_log_path
    )


if __name__ == "__main__":
    main()
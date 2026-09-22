import os

import pandas as pd

from src.config import Config



config = Config()
# =========================================================
# 文件路径
# =========================================================

SOURCE_FILE = (
    config.INTERIM_DATA_DIR
    + "/strong_noise_candidates.csv"
)

REVIEW_FILE = (
    config.INTERIM_DATA_DIR
    + "/strong_noise_candidates_reviewed.csv"
)


# =========================================================
# Review Status
# =========================================================

STATUS_CORRECT = "correct"
STATUS_WRONG = "wrong"
STATUS_AMBIGUOUS = "ambiguous"
STATUS_MULTI_INTENT = "multi_intent"
STATUS_SKIPPED = "skipped"


# =========================================================
# 1. 加载审核数据
# =========================================================

def load_review_data():
    """
    如果已经存在审核文件：
        继续上次审核。

    否则：
        从 strong_noise_candidates.csv 开始。
    """

    if os.path.exists(REVIEW_FILE):

        print(
            "发现历史审核记录，继续审核："
        )

        print(REVIEW_FILE)

        df = pd.read_csv(
            REVIEW_FILE
        )

    else:

        if not os.path.exists(SOURCE_FILE):

            raise FileNotFoundError(
                f"找不到文件：{SOURCE_FILE}"
            )

        print(
            "开始新的人工审核："
        )

        print(SOURCE_FILE)

        df = pd.read_csv(
            SOURCE_FILE
        )

    # =====================================================
    # 确保审核字段存在
    # =====================================================

    required_columns = [
        "review_status",
        "review_label",
        "review_note"
    ]

    for column in required_columns:

        if column not in df.columns:
            df[column] = ""

    # NaN -> ""
    df[required_columns] = (
        df[required_columns]
        .fillna("")
    )

    return df


# =========================================================
# 2. 保存
# =========================================================

def save_review_data(df):
    """
    保存审核进度。
    """

    df.to_csv(
        REVIEW_FILE,
        index=False,
        encoding="utf-8-sig"
    )


# =========================================================
# 3. Label Mapping
# =========================================================

def build_label_mapping(df):
    """
    构建：

        label -> label_des
        label_des -> label
    """

    mapping_df = pd.concat(
        [
            df[
                [
                    "true_label",
                    "true_label_des"
                ]
            ].rename(
                columns={
                    "true_label": "label",
                    "true_label_des": "label_des"
                }
            ),

            df[
                [
                    "pred_label",
                    "pred_label_des"
                ]
            ].rename(
                columns={
                    "pred_label": "label",
                    "pred_label_des": "label_des"
                }
            )
        ],
        ignore_index=True
    )

    mapping_df = (
        mapping_df
        .dropna()
        .drop_duplicates(
            subset=["label"]
        )
    )

    label_to_des = dict(
        zip(
            mapping_df["label"].astype(int),
            mapping_df["label_des"]
        )
    )

    des_to_label = {
        value: key
        for key, value
        in label_to_des.items()
    }

    return (
        label_to_des,
        des_to_label
    )


# =========================================================
# 4. 打印当前样本
# =========================================================

def print_sample(
        row,
        current,
        total
):

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"[{current} / {total}]"
    )

    print(
        "=" * 70
    )

    print(
        "\n文本："
    )

    print(
        row["sentence"]
    )

    print(
        "\n原标签："
    )

    print(
        f'{int(row["true_label"])} | '
        f'{row["true_label_des"]}'
    )

    print(
        "\n模型建议："
    )

    print(
        f'{int(row["pred_label"])} | '
        f'{row["pred_label_des"]}'
    )

    print(
        "\n概率："
    )

    print(
        f'P(true) = '
        f'{row["true_prob"]:.4f}'
    )

    print(
        f'P(pred) = '
        f'{row["pred_prob"]:.4f}'
    )

    print(
        f'Gap     = '
        f'{row["prob_gap"]:.4f}'
    )

    print(
        "\n请选择："
    )

    print(
        "1 = 原标签正确"
    )

    print(
        "2 = 原标签错误，采用模型建议标签"
    )

    print(
        "3 = 原标签错误，但模型建议也不对"
    )

    print(
        "4 = 标签存在歧义"
    )

    print(
        "5 = 多意图文本"
    )

    print(
        "s = 暂时跳过"
    )

    print(
        "q = 保存并退出"
    )


# =========================================================
# 5. 查看标签列表
# =========================================================

def show_label_list(
        label_to_des
):

    print(
        "\n===== Label List ====="
    )

    for label in sorted(
        label_to_des.keys()
    ):

        print(
            f"{label:3d} | "
            f"{label_to_des[label]}"
        )


# =========================================================
# 6. 手动选择正确标签
# =========================================================

def select_manual_label(
        label_to_des
):
    """
    当：

        原标签错误
        模型预测也错误

    时手动输入正确 label。
    """

    while True:

        print(
            "\n输入正确的 label 数字。"
        )

        print(
            "输入 l 查看标签列表。"
        )

        print(
            "输入 c 取消。"
        )

        value = input(
            "label > "
        ).strip()

        if value.lower() == "l":

            show_label_list(
                label_to_des
            )

            continue

        if value.lower() == "c":

            return None

        try:

            label = int(value)

        except ValueError:

            print(
                "请输入合法的数字 label。"
            )

            continue

        if label not in label_to_des:

            print(
                f"不存在 label={label}"
            )

            continue

        print(
            "\n你选择的是："
        )

        print(
            f"{label} | "
            f"{label_to_des[label]}"
        )

        confirm = input(
            "确认？(y/n) > "
        ).strip().lower()

        if confirm == "y":

            return label


# =========================================================
# 7. 输入备注
# =========================================================

def input_note():
    """
    备注允许为空。
    """

    note = input(
        "备注（可直接回车跳过）> "
    ).strip()

    return note


# =========================================================
# 8. 显示审核进度
# =========================================================

def print_progress(df):

    reviewed_mask = (
        df["review_status"]
        .isin(
            [
                STATUS_CORRECT,
                STATUS_WRONG,
                STATUS_AMBIGUOUS,
                STATUS_MULTI_INTENT
            ]
        )
    )

    reviewed = reviewed_mask.sum()

    skipped = (
        df["review_status"]
        == STATUS_SKIPPED
    ).sum()

    remaining = (
        len(df)
        - reviewed
        - skipped
    )

    print(
        "\n===== Review Progress ====="
    )

    print(
        f"Total     : {len(df)}"
    )

    print(
        f"Reviewed  : {reviewed}"
    )

    print(
        f"Skipped   : {skipped}"
    )

    print(
        f"Remaining : {remaining}"
    )


# =========================================================
# 9. 审核
# =========================================================

def review():

    df = load_review_data()

    (
        label_to_des,
        _
    ) = build_label_mapping(
        df
    )

    print_progress(
        df
    )

    total = len(df)

    # =====================================================
    # 找尚未正式审核的数据
    #
    # skipped 下次也重新出现。
    # =====================================================

    reviewed_status = {
        STATUS_CORRECT,
        STATUS_WRONG,
        STATUS_AMBIGUOUS,
        STATUS_MULTI_INTENT
    }

    pending_indices = [
        index
        for index in df.index
        if df.at[
            index,
            "review_status"
        ] not in reviewed_status
    ]

    if len(pending_indices) == 0:

        print(
            "\n所有候选样本已经审核完成。"
        )

        return

    # =====================================================
    # 开始逐条审核
    # =====================================================

    for position, index in enumerate(
            pending_indices,
            start=1
    ):

        row = df.loc[index]

        completed = (
            total
            - len(pending_indices)
            + position
        )

        print_sample(
            row=row,
            current=completed,
            total=total
        )

        while True:

            choice = input(
                "\n选择 > "
            ).strip().lower()

            # =============================================
            # 1. 原标签正确
            # =============================================

            if choice == "1":

                df.at[
                    index,
                    "review_status"
                ] = STATUS_CORRECT

                df.at[
                    index,
                    "review_label"
                ] = int(
                    row["true_label"]
                )

                df.at[
                    index,
                    "review_note"
                ] = input_note()

                break

            # =============================================
            # 2. 模型预测正确
            # =============================================

            elif choice == "2":

                df.at[
                    index,
                    "review_status"
                ] = STATUS_WRONG

                df.at[
                    index,
                    "review_label"
                ] = int(
                    row["pred_label"]
                )

                df.at[
                    index,
                    "review_note"
                ] = input_note()

                break

            # =============================================
            # 3. 两个标签都不对
            # =============================================

            elif choice == "3":

                manual_label = (
                    select_manual_label(
                        label_to_des
                    )
                )

                if manual_label is None:

                    continue

                df.at[
                    index,
                    "review_status"
                ] = STATUS_WRONG

                df.at[
                    index,
                    "review_label"
                ] = manual_label

                df.at[
                    index,
                    "review_note"
                ] = input_note()

                break

            # =============================================
            # 4. 标签歧义
            # =============================================

            elif choice == "4":

                df.at[
                    index,
                    "review_status"
                ] = STATUS_AMBIGUOUS

                # 歧义样本暂时保持原标签
                df.at[
                    index,
                    "review_label"
                ] = int(
                    row["true_label"]
                )

                df.at[
                    index,
                    "review_note"
                ] = input_note()

                break

            # =============================================
            # 5. 多意图
            # =============================================

            elif choice == "5":

                df.at[
                    index,
                    "review_status"
                ] = STATUS_MULTI_INTENT

                # 第一轮先保留原标签
                df.at[
                    index,
                    "review_label"
                ] = int(
                    row["true_label"]
                )

                df.at[
                    index,
                    "review_note"
                ] = input_note()

                break

            # =============================================
            # Skip
            # =============================================

            elif choice == "s":

                df.at[
                    index,
                    "review_status"
                ] = STATUS_SKIPPED

                save_review_data(
                    df
                )

                print(
                    "已跳过。"
                )

                break

            # =============================================
            # Quit
            # =============================================

            elif choice == "q":

                save_review_data(
                    df
                )

                print(
                    "\n审核进度已保存。"
                )

                print_progress(
                    df
                )

                return

            else:

                print(
                    "无效选项，请重新输入。"
                )

        # =================================================
        # 每审核一条立即保存
        #
        # 即使程序意外退出，
        # 最多只损失当前这一条。
        # =================================================

        save_review_data(
            df
        )

    # =====================================================
    # 完成
    # =====================================================

    print(
        "\n所有候选样本审核完成。"
    )

    print_progress(
        df
    )

    print(
        "\n审核结果："
    )

    print(
        REVIEW_FILE
    )


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    review()
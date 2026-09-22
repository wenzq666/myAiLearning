"""
噪声处理
"""


from pathlib import Path
import pandas as pd

from src.config import Config
from src.data_process.data_loader import load_cic_dataset

config = Config()


def clean_text_basic(text):
    """
    最基础的文本标准化。

    当前只处理：
    1. 转字符串
    2. 去除首尾空白
    3. 连续空白合并成一个空格

    不做：
    - 去标点
    - 去停用词
    - 分词
    - 繁简转换
    """

    if pd.isna(text):
        return ""

    text = str(text).strip()

    # 处理连续空格、Tab、换行
    text = " ".join(text.split())

    return text


def analyze_data_quality(df):
    """
    分析训练集数据质量。
    """

    df = df.copy()

    # =========================
    # 1. 基础统计
    # =========================

    total_samples = len(df)

    missing_text = df["sentence"].isna().sum()

    df["clean_sentence"] = df["sentence"].apply(
        clean_text_basic
    )

    empty_text = (
        df["clean_sentence"] == ""
    ).sum()

    # =========================
    # 2. 完全重复
    # sentence + label 完全相同
    # =========================

    duplicate_mask = df.duplicated(
        subset=["clean_sentence", "label"],
        keep=False
    )

    duplicate_samples = (
        df[duplicate_mask]
        .sort_values(
            ["clean_sentence", "label"]
        )
        .copy()
    )

    # =========================
    # 3. 相同文本，不同标签
    # =========================

    label_count = (
        df.groupby("clean_sentence")["label"]
        .nunique()
    )

    conflict_sentences = label_count[
        label_count > 1
    ].index

    label_conflicts = (
        df[
            df["clean_sentence"].isin(
                conflict_sentences
            )
        ]
        .sort_values(
            ["clean_sentence", "label"]
        )
        .copy()
    )

    # =========================
    # 4. 类别统计
    # =========================

    class_stats = (
        df.groupby(["label", "label_des"])
        .size()
        .reset_index(name="count")
        .sort_values("count")
    )

    rare_classes = class_stats[
        class_stats["count"] < 20
    ].copy()

    # =========================
    # 5. 输出报告
    # =========================

    print("\n===== Data Quality Report =====")

    print(f"Total Samples              : {total_samples}")
    print(f"Missing Text               : {missing_text}")
    print(f"Empty Text                 : {empty_text}")

    print(
        f"Duplicate Sample Rows       : "
        f"{len(duplicate_samples)}"
    )

    print(
        f"Duplicate Text Groups       : "
        f"{duplicate_samples['clean_sentence'].nunique()}"
    )

    print(
        f"Conflicting Text Groups     : "
        f"{len(conflict_sentences)}"
    )

    print(
        f"Conflict Sample Rows        : "
        f"{len(label_conflicts)}"
    )

    print(
        f"Number of Classes           : "
        f"{df['label'].nunique()}"
    )

    print(
        f"Classes < 10 Samples        : "
        f"{(class_stats['count'] < 10).sum()}"
    )

    print(
        f"Classes < 20 Samples        : "
        f"{(class_stats['count'] < 20).sum()}"
    )

    return {
        "data": df,
        "duplicates": duplicate_samples,
        "conflicts": label_conflicts,
        "class_stats": class_stats,
        "rare_classes": rare_classes
    }


def save_quality_report(result):
    """
    保存数据质量分析结果。
    """

    output_dir = Path(config.INTERIM_DATA_DIR)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    result["duplicates"].to_csv(
        output_dir / "duplicate_samples.csv",
        index=False,
        encoding="utf-8-sig"
    )

    result["conflicts"].to_csv(
        output_dir / "label_conflicts.csv",
        index=False,
        encoding="utf-8-sig"
    )

    result["class_stats"].to_csv(
        output_dir / "class_stats.csv",
        index=False,
        encoding="utf-8-sig"
    )

    result["rare_classes"].to_csv(
        output_dir / "rare_classes.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"\nQuality reports saved to: "
        f"{output_dir}"
    )


if __name__ == "__main__":

    train_df, _, _ = load_cic_dataset()

    result = analyze_data_quality(
        train_df
    )

    save_quality_report(
        result
    )
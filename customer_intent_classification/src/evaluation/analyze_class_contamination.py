import os

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import Config


config = Config()


# =========================================================
# 1. 加载数据
# =========================================================

def load_data():

    train_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    confusion_path = (
        config.INTERIM_DATA_DIR
        + "/bidirectional_confusion.csv"
    )

    if not os.path.exists(train_path):
        raise FileNotFoundError(
            f"找不到 Clean Train：{train_path}"
        )

    if not os.path.exists(confusion_path):
        raise FileNotFoundError(
            f"找不到混淆文件：{confusion_path}"
        )

    train_df = pd.read_csv(train_path)

    confusion_df = pd.read_csv(
        confusion_path
    )

    train_df["sentence"] = (
        train_df["sentence"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    return train_df, confusion_df


# =========================================================
# 2. 构建全局 TF-IDF
# =========================================================

def build_tfidf(train_df):

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )

    matrix = vectorizer.fit_transform(
        train_df["sentence"]
    )

    return vectorizer, matrix


# =========================================================
# 3. 找某个 Label 的训练索引
# =========================================================

def get_label_indices(
        train_df,
        label
):

    return np.where(
        train_df["label"].values
        == label
    )[0]


# =========================================================
# 4. 计算两个类别之间的跨类最近邻
# =========================================================

def analyze_pair_similarity(
        train_df,
        tfidf_matrix,
        label_a,
        label_b,
        top_k=20
):

    index_a = get_label_indices(
        train_df,
        label_a
    )

    index_b = get_label_indices(
        train_df,
        label_b
    )

    if (
        len(index_a) == 0
        or len(index_b) == 0
    ):
        return None, None

    matrix_a = tfidf_matrix[
        index_a
    ]

    matrix_b = tfidf_matrix[
        index_b
    ]

    # A × B
    similarity_matrix = (
        cosine_similarity(
            matrix_a,
            matrix_b
        )
    )

    # =====================================================
    # 每个 A 样本，在 B 中找最相似样本
    # =====================================================

    best_b_position = (
        similarity_matrix.argmax(
            axis=1
        )
    )

    best_a_similarity = (
        similarity_matrix.max(
            axis=1
        )
    )

    # =====================================================
    # 每个 B 样本，在 A 中找最相似样本
    # =====================================================

    best_a_position = (
        similarity_matrix.argmax(
            axis=0
        )
    )

    best_b_similarity = (
        similarity_matrix.max(
            axis=0
        )
    )

    # =====================================================
    # 类别级统计
    # =====================================================

    all_best_similarity = np.concatenate(
        [
            best_a_similarity,
            best_b_similarity
        ]
    )

    summary = {

        "label_a": label_a,
        "label_b": label_b,

        "train_a": len(index_a),
        "train_b": len(index_b),

        "mean_nn_similarity":
            float(
                np.mean(
                    all_best_similarity
                )
            ),

        "median_nn_similarity":
            float(
                np.median(
                    all_best_similarity
                )
            ),

        "p90_nn_similarity":
            float(
                np.percentile(
                    all_best_similarity,
                    90
                )
            ),

        "ratio_ge_070":
            float(
                np.mean(
                    all_best_similarity
                    >= 0.70
                )
            ),

        "ratio_ge_080":
            float(
                np.mean(
                    all_best_similarity
                    >= 0.80
                )
            ),

        "ratio_ge_090":
            float(
                np.mean(
                    all_best_similarity
                    >= 0.90
                )
            )
    }

    # =====================================================
    # 保存具体的跨类相似样本
    # =====================================================

    detail_rows = []

    # -----------------------------------------------------
    # A -> B 最近邻
    # -----------------------------------------------------

    for local_a, local_b in enumerate(
            best_b_position
    ):

        global_a = (
            index_a[local_a]
        )

        global_b = (
            index_b[local_b]
        )

        detail_rows.append({

            "source_label":
                label_a,

            "target_label":
                label_b,

            "source_sentence":
                train_df.iloc[
                    global_a
                ]["sentence"],

            "target_sentence":
                train_df.iloc[
                    global_b
                ]["sentence"],

            "similarity":
                float(
                    best_a_similarity[
                        local_a
                    ]
                )
        })

    # -----------------------------------------------------
    # B -> A 最近邻
    # -----------------------------------------------------

    for local_b, local_a in enumerate(
            best_a_position
    ):

        global_b = (
            index_b[local_b]
        )

        global_a = (
            index_a[local_a]
        )

        detail_rows.append({

            "source_label":
                label_b,

            "target_label":
                label_a,

            "source_sentence":
                train_df.iloc[
                    global_b
                ]["sentence"],

            "target_sentence":
                train_df.iloc[
                    global_a
                ]["sentence"],

            "similarity":
                float(
                    best_b_similarity[
                        local_b
                    ]
                )
        })

    detail_df = pd.DataFrame(
        detail_rows
    )

    detail_df = (
        detail_df
        .sort_values(
            "similarity",
            ascending=False
        )
        .head(top_k)
        .reset_index(drop=True)
    )

    return summary, detail_df


# =========================================================
# 5. 分析 Top Confusion Pairs
# =========================================================

def analyze_top_pairs(
        train_df,
        confusion_df,
        tfidf_matrix,
        top_n=20
):

    top_pairs = (
        confusion_df
        .sort_values(
            "total_confusion",
            ascending=False
        )
        .head(top_n)
        .copy()
    )

    summary_rows = []
    detail_list = []

    for pair_rank, (_, row) in enumerate(
            top_pairs.iterrows(),
            start=1
    ):

        label_a = int(
            row["label_a"]
        )

        label_b = int(
            row["label_b"]
        )

        label_a_des = (
            row["label_a_des"]
        )

        label_b_des = (
            row["label_b_des"]
        )

        summary, detail_df = (
            analyze_pair_similarity(
                train_df=train_df,
                tfidf_matrix=tfidf_matrix,
                label_a=label_a,
                label_b=label_b,
                top_k=20
            )
        )

        if summary is None:
            continue

        summary[
            "pair_rank"
        ] = pair_rank

        summary[
            "label_a_des"
        ] = label_a_des

        summary[
            "label_b_des"
        ] = label_b_des

        summary[
            "dev_confusion"
        ] = int(
            row["total_confusion"]
        )

        summary[
            "a_to_b"
        ] = int(
            row["a_to_b"]
        )

        summary[
            "b_to_a"
        ] = int(
            row["b_to_a"]
        )

        summary_rows.append(
            summary
        )

        if detail_df is not None:

            detail_df[
                "pair_rank"
            ] = pair_rank

            detail_df[
                "label_a_des"
            ] = label_a_des

            detail_df[
                "label_b_des"
            ] = label_b_des

            detail_list.append(
                detail_df
            )

    summary_df = pd.DataFrame(
        summary_rows
    )

    if len(detail_list) > 0:

        detail_df = pd.concat(
            detail_list,
            ignore_index=True
        )

    else:

        detail_df = pd.DataFrame()

    return summary_df, detail_df


# =========================================================
# 6. 给类别对增加辅助风险等级
# =========================================================

def add_risk_signal(
        summary_df
):

    def classify(row):

        ratio_08 = (
            row["ratio_ge_080"]
        )

        median_sim = (
            row[
                "median_nn_similarity"
            ]
        )

        # 注意：
        # 这里只是数据排查优先级，
        # 不是自动判定“标签错误”。

        if (
            ratio_08 >= 0.20
            or median_sim >= 0.60
        ):
            return "high"

        if (
            ratio_08 >= 0.08
            or median_sim >= 0.45
        ):
            return "medium"

        return "low"

    summary_df = (
        summary_df.copy()
    )

    summary_df[
        "contamination_signal"
    ] = summary_df.apply(
        classify,
        axis=1
    )

    return summary_df


# =========================================================
# 7. 打印最相似训练样本
# =========================================================

def print_pair_details(
        summary_df,
        detail_df,
        top_pairs=5,
        samples_per_pair=10
):

    ranks = (
        summary_df[
            "pair_rank"
        ]
        .head(top_pairs)
        .tolist()
    )

    for rank in ranks:

        summary_row = (
            summary_df[
                summary_df[
                    "pair_rank"
                ]
                == rank
            ]
            .iloc[0]
        )

        print(
            "\n"
            + "=" * 90
        )

        print(
            f"Pair #{rank}"
        )

        print(
            f"{summary_row['label_a_des']}"
            f"  <->  "
            f"{summary_row['label_b_des']}"
        )

        print(
            f"Dev Confusion : "
            f"{summary_row['dev_confusion']}"
        )

        print(
            f"Median NN Sim : "
            f"{summary_row['median_nn_similarity']:.4f}"
        )

        print(
            f"Ratio >= 0.8 : "
            f"{summary_row['ratio_ge_080']:.4f}"
        )

        print(
            f"Signal        : "
            f"{summary_row['contamination_signal']}"
        )

        print(
            "=" * 90
        )

        pair_detail = (
            detail_df[
                detail_df[
                    "pair_rank"
                ]
                == rank
            ]
            .sort_values(
                "similarity",
                ascending=False
            )
            .head(
                samples_per_pair
            )
        )

        for _, row in (
            pair_detail.iterrows()
        ):

            print(
                f"\nSimilarity: "
                f"{row['similarity']:.4f}"
            )

            print(
                f"A: "
                f"{row['source_sentence']}"
            )

            print(
                f"B: "
                f"{row['target_sentence']}"
            )


# =========================================================
# 8. Main
# =========================================================

def main():

    train_df, confusion_df = (
        load_data()
    )

    print(
        f"\nClean Train: "
        f"{len(train_df)}"
    )

    # =====================================================
    # TF-IDF
    # =====================================================

    print(
        "\n正在构建 Train TF-IDF..."
    )

    _, tfidf_matrix = (
        build_tfidf(
            train_df
        )
    )

    print(
        f"TF-IDF Shape: "
        f"{tfidf_matrix.shape}"
    )

    # =====================================================
    # 分析 Top 20 Dev Confusion Pair
    # =====================================================

    summary_df, detail_df = (
        analyze_top_pairs(
            train_df=train_df,
            confusion_df=confusion_df,
            tfidf_matrix=tfidf_matrix,
            top_n=20
        )
    )

    summary_df = (
        add_risk_signal(
            summary_df
        )
    )

    # =====================================================
    # 调整列顺序
    # =====================================================

    summary_columns = [

        "pair_rank",

        "label_a",
        "label_a_des",

        "label_b",
        "label_b_des",

        "train_a",
        "train_b",

        "a_to_b",
        "b_to_a",
        "dev_confusion",

        "mean_nn_similarity",
        "median_nn_similarity",
        "p90_nn_similarity",

        "ratio_ge_070",
        "ratio_ge_080",
        "ratio_ge_090",

        "contamination_signal"
    ]

    summary_df = summary_df[
        summary_columns
    ]

    # =====================================================
    # 保存
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    summary_path = (
        config.INTERIM_DATA_DIR
        + "/class_contamination_summary.csv"
    )

    detail_path = (
        config.INTERIM_DATA_DIR
        + "/class_contamination_details.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8-sig"
    )

    detail_df.to_csv(
        detail_path,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================================
    # Summary
    # =====================================================

    print(
        "\n"
        "===== Class Contamination Summary ====="
    )

    print(
        summary_df[
            [
                "pair_rank",
                "label_a_des",
                "label_b_des",
                "train_a",
                "train_b",
                "dev_confusion",
                "median_nn_similarity",
                "ratio_ge_080",
                "contamination_signal"
            ]
        ]
        .to_string(
            index=False
        )
    )

    # =====================================================
    # 具体案例
    # =====================================================

    print_pair_details(
        summary_df=summary_df,
        detail_df=detail_df,
        top_pairs=5,
        samples_per_pair=10
    )

    print(
        "\n===== Saved ====="
    )

    print(
        summary_path
    )

    print(
        detail_path
    )


if __name__ == "__main__":
    main()
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score

from src.config import Config
from src.data_process.data_loader import load_cic_dataset


config = Config()
# =========================================================
# 1. 生成 OOF 预测
# =========================================================

def generate_oof_predictions(
        train_df,
        n_splits=5,
        random_state=42
):
    """
    使用 Stratified K-Fold 生成 OOF 预测。

    每一条训练数据的预测结果，
    都来自一个没有见过该样本的模型。
    """

    texts = (
        train_df["sentence"]
        .fillna("")
        .astype(str)
        .values
    )

    labels = (
        train_df["label"]
        .astype(int)
        .values
    )

    num_samples = len(train_df)
    num_classes = train_df["label"].nunique()

    print("\n===== OOF Configuration =====")
    print(f"Samples   : {num_samples}")
    print(f"Classes   : {num_classes}")
    print(f"OOF Folds : {n_splits}")

    # -----------------------------------------------------
    # 用于保存每一条样本的 OOF 结果
    # -----------------------------------------------------

    oof_pred = np.zeros(
        num_samples,
        dtype=np.int64
    )

    oof_true_prob = np.zeros(
        num_samples,
        dtype=np.float32
    )

    oof_pred_prob = np.zeros(
        num_samples,
        dtype=np.float32
    )

    oof_fold = np.zeros(
        num_samples,
        dtype=np.int64
    )

    # -----------------------------------------------------
    # Stratified K-Fold
    # -----------------------------------------------------

    skf = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state
    )

    # =====================================================
    # 开始 Fold
    # =====================================================

    for fold, (train_idx, val_idx) in enumerate(
            skf.split(texts, labels),
            start=1
    ):

        print(
            f"\n========== Fold {fold}/{n_splits} =========="
        )

        x_train = texts[train_idx]
        y_train = labels[train_idx]

        x_val = texts[val_idx]
        y_val = labels[val_idx]

        print(
            f"Train Samples : {len(train_idx)}"
        )

        print(
            f"Val Samples   : {len(val_idx)}"
        )

        # =================================================
        # TF-IDF
        #
        # 注意：
        # 必须每个 Fold 单独 fit。
        #
        # 不能提前对整个 Train fit，
        # 否则会产生数据泄漏。
        # =================================================

        vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(1, 2)
        )

        x_train_tfidf = (
            vectorizer.fit_transform(
                x_train
            )
        )

        x_val_tfidf = (
            vectorizer.transform(
                x_val
            )
        )

        print(
            "TF-IDF Shape:",
            x_train_tfidf.shape
        )

        # =================================================
        # Logistic Regression
        # =================================================

        model = LogisticRegression(
            max_iter=1000
        )

        model.fit(
            x_train_tfidf,
            y_train
        )

        # =================================================
        # 获取预测概率
        # =================================================

        probabilities = (
            model.predict_proba(
                x_val_tfidf
            )
        )

        # -------------------------------------------------
        # 预测类别对应的 probability column
        # -------------------------------------------------

        pred_column = np.argmax(
            probabilities,
            axis=1
        )

        # -------------------------------------------------
        # column -> 实际 label
        # -------------------------------------------------

        predictions = (
            model.classes_[
                pred_column
            ]
        )

        # -------------------------------------------------
        # P(pred)
        # -------------------------------------------------

        pred_probability = np.max(
            probabilities,
            axis=1
        )

        # =================================================
        # P(true)
        #
        # model.classes_ 例如：
        #
        # [0, 1, 2, 3, ...]
        #
        # 为了避免假设 label 一定连续，
        # 建立 label -> probability column 映射。
        # =================================================

        class_to_column = {
            label: column
            for column, label
            in enumerate(model.classes_)
        }

        true_probability = np.array(
            [
                probabilities[
                    row_index,
                    class_to_column[true_label]
                ]
                for row_index, true_label
                in enumerate(y_val)
            ],
            dtype=np.float32
        )

        # =================================================
        # 保存 OOF
        # =================================================

        oof_pred[val_idx] = (
            predictions
        )

        oof_true_prob[val_idx] = (
            true_probability
        )

        oof_pred_prob[val_idx] = (
            pred_probability
        )

        oof_fold[val_idx] = fold

        # =================================================
        # 当前 Fold 指标
        # =================================================

        fold_accuracy = accuracy_score(
            y_val,
            predictions
        )

        fold_macro_f1 = f1_score(
            y_val,
            predictions,
            average="macro",
            zero_division=0
        )

        print(
            f"Accuracy : {fold_accuracy:.4f}"
        )

        print(
            f"Macro-F1 : {fold_macro_f1:.4f}"
        )

    return (
        labels,
        oof_pred,
        oof_true_prob,
        oof_pred_prob,
        oof_fold
    )


# =========================================================
# 2. 构建完整 OOF DataFrame
# =========================================================

def build_oof_dataframe(
        train_df,
        true_labels,
        pred_labels,
        true_probs,
        pred_probs,
        folds
):
    """
    将原始训练数据与 OOF 预测结果合并。
    """

    result_df = (
        train_df
        .copy()
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # label -> label_des
    # -----------------------------------------------------

    label_mapping = (
        train_df[
            [
                "label",
                "label_des"
            ]
        ]
        .drop_duplicates()
        .set_index("label")["label_des"]
        .to_dict()
    )

    # -----------------------------------------------------
    # OOF label
    # -----------------------------------------------------

    result_df["true_label"] = (
        true_labels
    )

    result_df["pred_label"] = (
        pred_labels
    )

    # -----------------------------------------------------
    # 中文类别名称
    # -----------------------------------------------------

    result_df["true_label_des"] = (
        result_df["true_label"]
        .map(label_mapping)
    )

    result_df["pred_label_des"] = (
        result_df["pred_label"]
        .map(label_mapping)
    )

    # -----------------------------------------------------
    # Probability
    # -----------------------------------------------------

    result_df["true_prob"] = (
        true_probs
    )

    result_df["pred_prob"] = (
        pred_probs
    )

    # -----------------------------------------------------
    # Probability Gap
    #
    # P(pred) - P(true)
    # -----------------------------------------------------

    result_df["prob_gap"] = (
        result_df["pred_prob"]
        - result_df["true_prob"]
    )

    # -----------------------------------------------------
    # 是否预测正确
    # -----------------------------------------------------

    result_df["is_correct"] = (
        result_df["true_label"]
        == result_df["pred_label"]
    )

    # -----------------------------------------------------
    # Fold
    # -----------------------------------------------------

    result_df["fold"] = folds

    return result_df


# =========================================================
# 3. 获取所有预测错误
# =========================================================

def get_all_errors(result_df):
    """
    获取所有 OOF 预测错误样本。

    注意：
    预测错误 != 标签错误。
    """

    error_df = (
        result_df[
            result_df["is_correct"] == False
        ]
        .copy()
        .sort_values(
            "prob_gap",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return error_df


# =========================================================
# 4. 筛选 Strong Noise Candidates
# =========================================================

def get_strong_noise_candidates(
        result_df,
        min_pred_prob=0.70,
        max_true_prob=0.10,
        min_prob_gap=0.60
):
    """
    筛选强分歧样本。

    默认条件：

        prediction != true label

        P(pred) >= 0.70

        P(true) <= 0.10

        P(pred) - P(true) >= 0.60

    注意：

    这里得到的是：
        疑似标签噪声候选

    不是：
        已确认标签错误
    """

    candidates = result_df[
        (result_df["is_correct"] == False)
        &
        (result_df["pred_prob"] >= min_pred_prob)
        &
        (result_df["true_prob"] <= max_true_prob)
        &
        (result_df["prob_gap"] >= min_prob_gap)
    ].copy()

    candidates = (
        candidates
        .sort_values(
            "prob_gap",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # =====================================================
    # 人工审核字段
    #
    # review_status 推荐填写：
    #
    # correct
    # wrong
    # ambiguous
    # multi_intent
    #
    # review_label:
    # 如果确认错标，可以填写正确 label
    #
    # review_note:
    # 人工备注
    # =====================================================

    candidates["review_status"] = ""

    candidates["review_label"] = ""

    candidates["review_note"] = ""

    return candidates


# =========================================================
# 5. 输出总体报告
# =========================================================

def print_oof_report(
        result_df,
        error_df
):
    """
    输出 OOF 总体结果。
    """

    accuracy = accuracy_score(
        result_df["true_label"],
        result_df["pred_label"]
    )

    macro_f1 = f1_score(
        result_df["true_label"],
        result_df["pred_label"],
        average="macro",
        zero_division=0
    )

    print(
        "\n===== 5-Fold OOF Result ====="
    )

    print(
        f"Samples           : "
        f"{len(result_df)}"
    )

    print(
        f"Accuracy          : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro-F1          : "
        f"{macro_f1:.4f}"
    )

    print(
        f"Wrong Predictions : "
        f"{len(error_df)}"
    )

    print(
        f"Error Rate        : "
        f"{len(error_df) / len(result_df):.4f}"
    )


# =========================================================
# 6. 输出 Strong Noise Candidates
# =========================================================

def print_strong_candidates(
        strong_candidates
):
    """
    输出强疑似噪声候选。
    """

    print(
        "\n===== Strong Noise Candidates ====="
    )

    print(
        f"Candidate Samples : "
        f"{len(strong_candidates)}"
    )

    if len(strong_candidates) == 0:

        print(
            "No strong noise candidates."
        )

        return

    print(
        "\n===== Top 30 Strong Noise Candidates ====="
    )

    columns = [
        "sentence",
        "true_label_des",
        "pred_label_des",
        "true_prob",
        "pred_prob",
        "prob_gap",
        "fold"
    ]

    print(
        strong_candidates[
            columns
        ]
        .head(30)
        .to_string(
            index=False
        )
    )


# =========================================================
# 7. 输出概率分布，辅助后续调整阈值
# =========================================================

def print_gap_statistics(
        error_df
):
    """
    查看 OOF 错误样本的 prob_gap 分布。

    后续可以根据真实分布调整阈值，
    而不是一直拍脑袋设置 0.6 / 0.7。
    """

    print(
        "\n===== Error Probability Statistics ====="
    )

    statistics = (
        error_df[
            [
                "true_prob",
                "pred_prob",
                "prob_gap"
            ]
        ]
        .describe(
            percentiles=[
                0.50,
                0.75,
                0.90,
                0.95,
                0.99
            ]
        )
    )

    print(
        statistics.to_string()
    )


# =========================================================
# 8. 保存结果
# =========================================================

def save_results(
        result_df,
        error_df,
        strong_candidates
):
    """
    保存分析结果。
    """


    # -----------------------------------------------------
    # 全部 10000 条 OOF 预测
    # -----------------------------------------------------

    oof_path = (
        config.INTERIM_DATA_DIR
        + "/tfidf_oof_predictions.csv"
    )

    result_df.to_csv(
        oof_path,
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------------------------------
    # 所有 OOF 错误
    # -----------------------------------------------------

    error_path = (
        config.INTERIM_DATA_DIR
        + "/tfidf_oof_errors.csv"
    )

    error_df.to_csv(
        error_path,
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------------------------------
    # Strong Noise Candidates
    # -----------------------------------------------------

    strong_path = (
        config.INTERIM_DATA_DIR
        + "/strong_noise_candidates.csv"
    )

    strong_candidates.to_csv(
        strong_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\n===== Saved Files ====="
    )

    print(oof_path)

    print(error_path)

    print(strong_path)


# =========================================================
# 9. Main
# =========================================================

def main():

    # =====================================================
    # Load Data
    # =====================================================

    train_df, _, _ = (
        load_cic_dataset()
    )

    print(
        "Train Samples:",
        len(train_df)
    )

    # =====================================================
    # 检查最小类别数量
    # =====================================================

    class_counts = (
        train_df["label"]
        .value_counts()
    )

    min_class_count = (
        class_counts.min()
    )

    print(
        "Minimum Class Samples:",
        min_class_count
    )

    # =====================================================
    # Fold 设置
    # =====================================================

    n_splits = 5

    if min_class_count < n_splits:

        raise ValueError(
            f"最小类别只有 {min_class_count} 条样本，"
            f"无法执行 {n_splits}-Fold StratifiedKFold。"
        )

    # =====================================================
    # 生成 OOF
    # =====================================================

    (
        true_labels,
        pred_labels,
        true_probs,
        pred_probs,
        folds
    ) = generate_oof_predictions(
        train_df=train_df,
        n_splits=n_splits,
        random_state=42
    )

    # =====================================================
    # 构建结果 DataFrame
    # =====================================================

    result_df = (
        build_oof_dataframe(
            train_df=train_df,
            true_labels=true_labels,
            pred_labels=pred_labels,
            true_probs=true_probs,
            pred_probs=pred_probs,
            folds=folds
        )
    )

    # =====================================================
    # 获取所有错误
    # =====================================================

    error_df = (
        get_all_errors(
            result_df
        )
    )

    # =====================================================
    # Strong Noise Candidate
    #
    # 第一轮先使用比较严格的阈值。
    # =====================================================

    strong_candidates = (
        get_strong_noise_candidates(
            result_df=result_df,

            min_pred_prob=0.70,

            max_true_prob=0.10,

            min_prob_gap=0.60
        )
    )

    # =====================================================
    # 打印结果
    # =====================================================

    print_oof_report(
        result_df=result_df,
        error_df=error_df
    )

    print_gap_statistics(
        error_df=error_df
    )

    print_strong_candidates(
        strong_candidates=strong_candidates
    )

    # =====================================================
    # 保存结果
    # =====================================================

    save_results(
        result_df=result_df,
        error_df=error_df,
        strong_candidates=strong_candidates
    )


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":
    main()
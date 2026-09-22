from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import classification_report
from src.data_process.data_loader import load_cic_dataset
import pandas as pd


def train_tfidf_lr(train_df, dev_df):
    """
    使用 Char TF-IDF + Logistic Regression
    完成 CIC 电商客服意图分类 Baseline
    """

    # =========================================================
    # 1. 准备数据
    # =========================================================
    x_train = train_df["sentence"]
    y_train = train_df["label"]

    x_dev = dev_df["sentence"]
    y_dev = dev_df["label"]

    # =========================================================
    # 2. TF-IDF 特征提取
    # =========================================================
    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(1, 2)
    )

    x_train_tfidf = vectorizer.fit_transform(x_train)
    x_dev_tfidf = vectorizer.transform(x_dev)

    print("训练集 TF-IDF:", x_train_tfidf.shape)
    print("验证集 TF-IDF:", x_dev_tfidf.shape)

    # =========================================================
    # 3. Logistic Regression
    # =========================================================
    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(x_train_tfidf, y_train)

    # =========================================================
    # 4. 验证集预测
    # =========================================================
    y_pred = model.predict(x_dev_tfidf)

    # =========================================================
    # 5. 整体指标
    # =========================================================
    accuracy = accuracy_score(y_dev, y_pred)

    macro_f1 = f1_score(
        y_dev,
        y_pred,
        average="macro"
    )

    print("\n===== Baseline Result =====")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Macro-F1 : {macro_f1:.4f}")

    # =========================================================
    # 6. 获取每个类别的 Precision / Recall / F1
    # =========================================================
    report = classification_report(
        y_dev,
        y_pred,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).T

    # 只保留真实的类别
    # classification_report 最后还包含：
    # accuracy / macro avg / weighted avg
    class_report = report_df.loc[
        [str(label) for label in sorted(y_dev.unique())]
    ].copy()

    # =========================================================
    # 7. label -> 中文标签名称
    # =========================================================
    label_map = (
        dev_df[["label", "label_des"]]
        .drop_duplicates("label")
        .set_index("label")["label_des"]
        .to_dict()
    )

    class_report["label"] = class_report.index.astype(int)

    class_report["label_des"] = class_report["label"].map(
        label_map
    )

    # =========================================================
    # 8. 按 F1 从低到高排序
    # =========================================================
    class_report = class_report.sort_values(
        "f1-score"
    )

    columns = [
        "label",
        "label_des",
        "precision",
        "recall",
        "f1-score",
        "support"
    ]

    # =========================================================
    # 9. 查看表现最差的类别
    # =========================================================
    print("\n===== F1 最低的 10 个类别 =====")

    print(
        class_report[columns]
        .head(10)
        .to_string(index=False)
    )

    # =========================================================
    # 10. 查看表现最好的类别
    # =========================================================
    print("\n===== F1 最高的 10 个类别 =====")

    print(
        class_report[columns]
        .tail(10)
        .sort_values("f1-score", ascending=False)
        .to_string(index=False)
    )

    # =========================================================
    # 11. 错误样本分析
    # =========================================================

    error_df = dev_df[
        y_dev.values != y_pred
    ].copy()

    error_df["pred_label"] = y_pred[
        y_dev.values != y_pred
    ]

    error_df["pred_label_des"] = error_df["pred_label"].map(
        label_map
    )

    print("\n===== 错误样本示例 =====")

    print(
        error_df[
            [
                "sentence",
                "label_des",
                "pred_label_des"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    return model, vectorizer


if __name__ == "__main__":

    train_df, dev_df, _ = load_cic_dataset()

    train_tfidf_lr(
        train_df,
        dev_df
    )
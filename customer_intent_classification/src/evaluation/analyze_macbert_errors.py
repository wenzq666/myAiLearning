import torch
import pandas as pd

from collections import Counter
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders


config = Config()


# =========================================================
# 1. 模型预测
# =========================================================

def predict(model, data_loader, device):
    """
    在验证集上进行预测。

    返回：
        true_labels : 真实标签
        pred_labels : 预测标签
        true_probs  : 模型分配给真实标签的概率
        pred_probs  : 模型预测标签的最大概率
    """

    model.eval()

    all_true = []
    all_pred = []

    all_true_prob = []
    all_pred_prob = []

    with torch.no_grad():

        for batch in data_loader:

            input_ids = batch["input_ids"].to(device)

            attention_mask = batch[
                "attention_mask"
            ].to(device)

            labels = batch["label"].to(device)

            # -----------------------------
            # Forward
            # -----------------------------

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = outputs.logits

            # -----------------------------
            # logits -> probability
            # -----------------------------

            probabilities = torch.softmax(
                logits,
                dim=1
            )

            # -----------------------------
            # 预测类别及其概率
            # -----------------------------

            pred_prob, predictions = torch.max(
                probabilities,
                dim=1
            )

            # -----------------------------
            # 获取真实标签对应的概率
            #
            # probabilities:
            # [batch_size, num_classes]
            #
            # labels:
            # [batch_size]
            #
            # gather 后：
            # 每个样本只取真实类别对应的概率
            # -----------------------------

            true_prob = probabilities.gather(
                dim=1,
                index=labels.unsqueeze(1)
            ).squeeze(1)

            # -----------------------------
            # 保存结果
            # -----------------------------

            all_true.extend(
                labels.cpu().tolist()
            )

            all_pred.extend(
                predictions.cpu().tolist()
            )

            all_true_prob.extend(
                true_prob.cpu().tolist()
            )

            all_pred_prob.extend(
                pred_prob.cpu().tolist()
            )

    return (
        all_true,
        all_pred,
        all_true_prob,
        all_pred_prob
    )


# =========================================================
# 2. 构建 label -> label_des 映射
# =========================================================

def build_label_mapping(train_df):
    """
    构建：

        label -> label_des

    例如：

        0 -> 买家咨询商品价格
        1 -> 买家咨询发货时间
    """

    label_mapping = (
        train_df[
            ["label", "label_des"]
        ]
        .drop_duplicates()
        .set_index("label")["label_des"]
        .to_dict()
    )

    return label_mapping


# =========================================================
# 3. 构建完整预测结果
# =========================================================

def build_prediction_dataframe(
    dev_df,
    true_labels,
    pred_labels,
    true_probs,
    pred_probs,
    label_mapping
):
    """
    将预测结果与原始 Dev 数据合并。
    """

    result_df = (
        dev_df
        .copy()
        .reset_index(drop=True)
    )

    # 防止 DataLoader 和 DataFrame 数量不一致
    assert len(result_df) == len(true_labels), (
        "Dev 数据数量和预测结果数量不一致"
    )

    # -----------------------------
    # 标签
    # -----------------------------

    result_df["true_label"] = true_labels

    result_df["pred_label"] = pred_labels

    # -----------------------------
    # 标签中文名称
    # -----------------------------

    result_df["true_label_des"] = (
        result_df["true_label"]
        .map(label_mapping)
    )

    result_df["pred_label_des"] = (
        result_df["pred_label"]
        .map(label_mapping)
    )

    # -----------------------------
    # Probability
    # -----------------------------

    result_df["true_prob"] = true_probs

    result_df["pred_prob"] = pred_probs

    # -----------------------------
    # Probability Gap
    #
    # pred_prob - true_prob
    #
    # Gap 越大：
    #
    # 模型越倾向于预测标签，
    # 而不是数据中的真实标签。
    # -----------------------------

    result_df["prob_gap"] = (
        result_df["pred_prob"]
        - result_df["true_prob"]
    )

    # -----------------------------
    # 是否预测正确
    # -----------------------------

    result_df["is_correct"] = (
        result_df["true_label"]
        == result_df["pred_label"]
    )

    return result_df


# =========================================================
# 4. 错误样本
# =========================================================

def get_error_samples(result_df):
    """
    获取预测错误的样本。
    """

    error_df = result_df[
        result_df["is_correct"] == False
    ].copy()

    return error_df


# =========================================================
# 5. 类别混淆统计
# =========================================================

def analyze_confusion(
    error_df,
    label_mapping
):
    """
    统计：

        True Label -> Pred Label

    出现的次数。
    """

    confusion_counter = Counter(
        zip(
            error_df["true_label"],
            error_df["pred_label"]
        )
    )

    confusion_rows = []

    for (
        true_label,
        pred_label
    ), count in confusion_counter.most_common():

        confusion_rows.append(
            {
                "true_label": true_label,

                "true_label_des":
                    label_mapping.get(
                        true_label,
                        str(true_label)
                    ),

                "pred_label": pred_label,

                "pred_label_des":
                    label_mapping.get(
                        pred_label,
                        str(pred_label)
                    ),

                "count": count
            }
        )

    confusion_df = pd.DataFrame(
        confusion_rows
    )

    return confusion_df


# =========================================================
# 6. 疑似标签问题排序
# =========================================================

def get_suspected_label_errors(
    error_df
):
    """
    根据 Probability Gap 对错误样本排序。

    Gap 越大：

        P(pred_label) >> P(true_label)

    说明模型更强烈地认为：

        pred_label

    比：

        true_label

    更合理。

    注意：
    这里只能叫“疑似标签问题”，
    不能直接认为原标签错误。
    """

    suspected_df = (
        error_df
        .sort_values(
            by="prob_gap",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return suspected_df


# =========================================================
# 7. 保存结果
# =========================================================

def save_results(
    result_df,
    error_df,
    confusion_df,
    suspected_df
):
    """
    保存所有分析结果。
    """

    # -----------------------------
    # 全部 Dev 预测结果
    # -----------------------------

    result_df.to_csv(
        config.INTERIM_DATA_DIR
        + "/macbert_dev_predictions.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------
    # 所有错误样本
    # -----------------------------

    error_df.to_csv(
        config.INTERIM_DATA_DIR
        + "/macbert_error_samples.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------
    # 类别混淆统计
    # -----------------------------

    confusion_df.to_csv(
        config.INTERIM_DATA_DIR
        + "/macbert_confusion_pairs.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------
    # 疑似标签问题
    # -----------------------------

    suspected_df.to_csv(
        config.INTERIM_DATA_DIR
        + "/macbert_suspected_label_errors.csv",
        index=False,
        encoding="utf-8-sig"
    )


# =========================================================
# 8. 打印评估结果
# =========================================================

def print_report(
    result_df,
    error_df,
    confusion_df,
    suspected_df
):

    # -----------------------------
    # Accuracy
    # -----------------------------

    accuracy = accuracy_score(
        result_df["true_label"],
        result_df["pred_label"]
    )

    # -----------------------------
    # Macro-F1
    # -----------------------------

    macro_f1 = f1_score(
        result_df["true_label"],
        result_df["pred_label"],
        average="macro",
        zero_division=0
    )

    # =====================================================
    # 总体结果
    # =====================================================

    print(
        "\n===== Model Evaluation ====="
    )

    print(
        f"Dev Samples     : "
        f"{len(result_df)}"
    )

    print(
        f"Correct Samples : "
        f"{len(result_df) - len(error_df)}"
    )

    print(
        f"Error Samples   : "
        f"{len(error_df)}"
    )

    print(
        f"Error Rate      : "
        f"{len(error_df) / len(result_df):.4f}"
    )

    print(
        f"Accuracy        : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro-F1        : "
        f"{macro_f1:.4f}"
    )

    # =====================================================
    # Top Confusion Pairs
    # =====================================================

    print(
        "\n===== Top 20 Confusion Pairs ====="
    )

    if len(confusion_df) > 0:

        print(
            confusion_df[
                [
                    "true_label_des",
                    "pred_label_des",
                    "count"
                ]
            ]
            .head(20)
            .to_string(index=False)
        )

    else:

        print(
            "No confusion samples."
        )

    # =====================================================
    # Top Suspected Label Errors
    # =====================================================

    print(
        "\n===== Top 30 Suspected Label Errors ====="
    )

    if len(suspected_df) > 0:

        print(
            suspected_df[
                [
                    "sentence",
                    "true_label_des",
                    "pred_label_des",
                    "true_prob",
                    "pred_prob",
                    "prob_gap"
                ]
            ]
            .head(30)
            .to_string(
                index=False
            )
        )

    else:

        print(
            "No error samples."
        )


# =========================================================
# 9. Main
# =========================================================

def main():

    # =====================================================
    # Device
    # =====================================================

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(
        "Device:",
        device
    )

    # =====================================================
    # Load Data
    # =====================================================

    train_df, dev_df, _ = (
        load_cic_dataset()
    )

    print(
        "Train Samples:",
        len(train_df)
    )

    print(
        "Dev Samples:",
        len(dev_df)
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
    # Label Mapping
    # =====================================================

    label_mapping = (
        build_label_mapping(
            train_df
        )
    )

    num_classes = (
        train_df["label"]
        .nunique()
    )

    print(
        "Num Classes:",
        num_classes
    )

    # =====================================================
    # Load Model
    # =====================================================

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            config.bert_path,
            num_labels=num_classes
        )
    )

    model_path = (
        config.bert_save_model
        + "/macbert_weighted_best.pt"
    )

    print(
        "Loading Model:",
        model_path
    )

    state_dict = torch.load(
        model_path,
        map_location=device
    )

    model.load_state_dict(
        state_dict
    )

    model.to(device)

    # =====================================================
    # Prediction
    # =====================================================

    (
        true_labels,
        pred_labels,
        true_probs,
        pred_probs
    ) = predict(
        model=model,
        data_loader=dev_loader,
        device=device
    )

    # =====================================================
    # Build Prediction DataFrame
    # =====================================================

    result_df = (
        build_prediction_dataframe(
            dev_df=dev_df,
            true_labels=true_labels,
            pred_labels=pred_labels,
            true_probs=true_probs,
            pred_probs=pred_probs,
            label_mapping=label_mapping
        )
    )

    # =====================================================
    # Error Samples
    # =====================================================

    error_df = (
        get_error_samples(
            result_df
        )
    )

    # =====================================================
    # Confusion Analysis
    # =====================================================

    confusion_df = (
        analyze_confusion(
            error_df=error_df,
            label_mapping=label_mapping
        )
    )

    # =====================================================
    # Suspected Label Errors
    # =====================================================

    suspected_df = (
        get_suspected_label_errors(
            error_df
        )
    )

    # =====================================================
    # Save
    # =====================================================

    save_results(
        result_df=result_df,
        error_df=error_df,
        confusion_df=confusion_df,
        suspected_df=suspected_df
    )

    # =====================================================
    # Print
    # =====================================================

    print_report(
        result_df=result_df,
        error_df=error_df,
        confusion_df=confusion_df,
        suspected_df=suspected_df
    )

    print(
        "\nResults saved to:",
        config.INTERIM_DATA_DIR
    )


if __name__ == "__main__":
    main()
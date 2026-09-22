import os

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn.metrics import accuracy_score, f1_score

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()


# =========================================================
# 1. 加载数据
# =========================================================

def load_data():

    train_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    train_df = pd.read_csv(
        train_path
    )

    _, dev_df, _ = (
        load_cic_dataset()
    )

    train_df["sentence"] = (
        train_df["sentence"]
        .fillna("")
        .astype(str)
    )

    dev_df["sentence"] = (
        dev_df["sentence"]
        .fillna("")
        .astype(str)
    )

    train_df["label"] = (
        train_df["label"]
        .astype(int)
    )

    dev_df["label"] = (
        dev_df["label"]
        .astype(int)
    )

    return train_df, dev_df


# =========================================================
# 2. 收集 Dev Logits
# =========================================================

def collect_logits(
        model,
        dataloader,
        device
):

    model.eval()

    all_logits = []
    all_labels = []

    with torch.no_grad():

        for batch in dataloader:

            input_ids = (
                batch["input_ids"]
                .to(device)
            )

            attention_mask = (
                batch["attention_mask"]
                .to(device)
            )

            labels = (
                batch["label"]
                .to(device)
            )

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = (
                outputs[
                    "classification_logits"
                ]
            )

            all_logits.append(
                logits.cpu()
            )

            all_labels.append(
                labels.cpu()
            )

    all_logits = torch.cat(
        all_logits,
        dim=0
    )

    all_labels = torch.cat(
        all_labels,
        dim=0
    )

    return (
        all_logits,
        all_labels
    )


# =========================================================
# 3. ECE
#
# Expected Calibration Error
# =========================================================

def calculate_ece(
        probabilities,
        labels,
        n_bins=15
):

    confidence, predictions = (
        torch.max(
            probabilities,
            dim=1
        )
    )

    correct = (
        predictions == labels
    ).float()

    bin_boundaries = torch.linspace(
        0,
        1,
        n_bins + 1
    )

    ece = torch.zeros(1)

    for i in range(n_bins):

        lower = (
            bin_boundaries[i]
        )

        upper = (
            bin_boundaries[i + 1]
        )

        if i == 0:

            mask = (
                (confidence >= lower)
                &
                (confidence <= upper)
            )

        else:

            mask = (
                (confidence > lower)
                &
                (confidence <= upper)
            )

        proportion = (
            mask.float().mean()
        )

        if proportion.item() > 0:

            bin_accuracy = (
                correct[mask]
                .mean()
            )

            bin_confidence = (
                confidence[mask]
                .mean()
            )

            ece += (
                torch.abs(
                    bin_accuracy
                    - bin_confidence
                )
                * proportion
            )

    return ece.item()


# =========================================================
# 4. Temperature Scaling
# =========================================================

class TemperatureScaler(
        nn.Module
):

    def __init__(self):

        super().__init__()

        # 用 log_temperature 保证 T 始终 > 0
        self.log_temperature = (
            nn.Parameter(
                torch.zeros(1)
            )
        )

    def forward(self, logits):

        temperature = torch.exp(
            self.log_temperature
        )

        return (
            logits / temperature
        )

    def get_temperature(self):

        return (
            torch.exp(
                self.log_temperature
            ).item()
        )


# =========================================================
# 5. 拟合 Temperature
# =========================================================

def fit_temperature(
        logits,
        labels
):

    scaler = (
        TemperatureScaler()
    )

    criterion = (
        nn.CrossEntropyLoss()
    )

    # Temperature Scaling 只有一个参数
    optimizer = torch.optim.LBFGS(
        scaler.parameters(),
        lr=0.01,
        max_iter=100
    )

    def closure():

        optimizer.zero_grad()

        scaled_logits = (
            scaler(logits)
        )

        loss = criterion(
            scaled_logits,
            labels
        )

        loss.backward()

        return loss

    optimizer.step(
        closure
    )

    return scaler


# =========================================================
# 6. Reliability Bins
# =========================================================

def build_reliability_bins(
        probabilities,
        labels,
        n_bins=10
):

    confidence, predictions = (
        torch.max(
            probabilities,
            dim=1
        )
    )

    correct = (
        predictions == labels
    ).float()

    confidence = (
        confidence.numpy()
    )

    correct = (
        correct.numpy()
    )

    bins = np.linspace(
        0.0,
        1.0,
        n_bins + 1
    )

    rows = []

    for i in range(n_bins):

        low = bins[i]
        high = bins[i + 1]

        if i == 0:

            mask = (
                (confidence >= low)
                &
                (confidence <= high)
            )

        else:

            mask = (
                (confidence > low)
                &
                (confidence <= high)
            )

        count = int(
            mask.sum()
        )

        if count == 0:

            avg_confidence = 0.0
            accuracy = 0.0

        else:

            avg_confidence = float(
                confidence[mask]
                .mean()
            )

            accuracy = float(
                correct[mask]
                .mean()
            )

        rows.append(
            {
                "range":
                    f"{low:.1f}-{high:.1f}",

                "samples":
                    count,

                "avg_confidence":
                    avg_confidence,

                "accuracy":
                    accuracy,

                "gap":
                    abs(
                        accuracy
                        - avg_confidence
                    )
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 7. Main
# =========================================================

def main():

    device = config.device

    print(
        f"Device: {device}"
    )

    train_df, dev_df = (
        load_data()
    )

    num_classes = (
        max(
            train_df["label"].max(),
            dev_df["label"].max()
        )
        + 1
    )

    # =====================================================
    # Dev Loader
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
    # 主模型
    # =====================================================

    model = (
        LabelSemanticMacBERT(
            bert_path=
                config.bert_path,

            num_classes=
                num_classes,

            temperature=0.05
        )
    )

    model_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    model.load_state_dict(
        torch.load(
            model_path,
            map_location=device
        )
    )

    model = model.to(
        device
    )

    # =====================================================
    # Collect logits
    # =====================================================

    logits, labels = (
        collect_logits(
            model,
            dev_loader,
            device
        )
    )

    # 后面只有 2000 x 118，
    # 直接 CPU 做校准即可
    logits = logits.float()
    labels = labels.long()

    # =====================================================
    # Before Calibration
    # =====================================================

    original_probabilities = (
        F.softmax(
            logits,
            dim=1
        )
    )

    original_predictions = (
        torch.argmax(
            original_probabilities,
            dim=1
        )
    )

    original_accuracy = (
        accuracy_score(
            labels.numpy(),
            original_predictions.numpy()
        )
    )

    original_f1 = (
        f1_score(
            labels.numpy(),
            original_predictions.numpy(),
            average="macro",
            zero_division=0
        )
    )

    original_nll = (
        F.cross_entropy(
            logits,
            labels
        ).item()
    )

    original_ece = (
        calculate_ece(
            original_probabilities,
            labels
        )
    )

    # =====================================================
    # Fit Temperature
    # =====================================================

    scaler = fit_temperature(
        logits,
        labels
    )

    temperature = (
        scaler.get_temperature()
    )

    # =====================================================
    # After Calibration
    # =====================================================

    with torch.no_grad():

        calibrated_logits = (
            scaler(logits)
        )

        calibrated_probabilities = (
            F.softmax(
                calibrated_logits,
                dim=1
            )
        )

    calibrated_predictions = (
        torch.argmax(
            calibrated_probabilities,
            dim=1
        )
    )

    calibrated_accuracy = (
        accuracy_score(
            labels.numpy(),
            calibrated_predictions.numpy()
        )
    )

    calibrated_f1 = (
        f1_score(
            labels.numpy(),
            calibrated_predictions.numpy(),
            average="macro",
            zero_division=0
        )
    )

    calibrated_nll = (
        F.cross_entropy(
            calibrated_logits,
            labels
        ).item()
    )

    calibrated_ece = (
        calculate_ece(
            calibrated_probabilities,
            labels
        )
    )

    # =====================================================
    # Result
    # =====================================================

    print(
        "\n===== Temperature Scaling ====="
    )

    print(
        f"Temperature : "
        f"{temperature:.4f}"
    )

    print(
        "\n===== Before Calibration ====="
    )

    print(
        f"Accuracy : "
        f"{original_accuracy:.4f}"
    )

    print(
        f"Macro-F1 : "
        f"{original_f1:.4f}"
    )

    print(
        f"NLL      : "
        f"{original_nll:.4f}"
    )

    print(
        f"ECE      : "
        f"{original_ece:.4f}"
    )

    print(
        "\n===== After Calibration ====="
    )

    print(
        f"Accuracy : "
        f"{calibrated_accuracy:.4f}"
    )

    print(
        f"Macro-F1 : "
        f"{calibrated_f1:.4f}"
    )

    print(
        f"NLL      : "
        f"{calibrated_nll:.4f}"
    )

    print(
        f"ECE      : "
        f"{calibrated_ece:.4f}"
    )

    # =====================================================
    # Reliability
    # =====================================================

    before_bins = (
        build_reliability_bins(
            original_probabilities,
            labels
        )
    )

    after_bins = (
        build_reliability_bins(
            calibrated_probabilities,
            labels
        )
    )

    comparison = pd.merge(
        before_bins,
        after_bins,
        on="range",
        suffixes=(
            "_before",
            "_after"
        )
    )

    print(
        "\n===== Reliability Comparison ====="
    )

    print(
        comparison[
            [
                "range",
                "samples_before",
                "avg_confidence_before",
                "accuracy_before",
                "samples_after",
                "avg_confidence_after",
                "accuracy_after"
            ]
        ].to_string(
            index=False
        )
    )

    # =====================================================
    # 保存 Temperature
    # =====================================================

    os.makedirs(
        config.INTERIM_DATA_DIR,
        exist_ok=True
    )

    temperature_path = (
        config.INTERIM_DATA_DIR
        + "/temperature.txt"
    )

    with open(
        temperature_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            str(temperature)
        )

    comparison.to_csv(
        config.INTERIM_DATA_DIR
        + "/calibration_reliability.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\nTemperature saved:"
    )

    print(
        temperature_path
    )


if __name__ == "__main__":
    main()
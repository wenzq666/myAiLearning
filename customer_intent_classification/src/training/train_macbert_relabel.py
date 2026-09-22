import argparse
import os

import numpy as np
import pandas as pd
import torch

from sklearn.metrics import accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
from transformers import AutoModelForSequenceClassification

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders


config = Config()
# =========================================================
# 1. 随机种子
# =========================================================

def set_seed(seed=42):
    """
    固定随机种子，尽量保证实验可复现。
    """

    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


# =========================================================
# 2. 加载 Raw / Clean Train
# =========================================================

def load_training_data(train_type):
    """
    train_type:

        raw   -> 原始 Train
        clean -> 人工审核后的 Train

    Dev 始终使用原始 Dev。
    """

    raw_train_df, dev_df, test_df = (
        load_cic_dataset()
    )

    if train_type == "raw":

        train_df = raw_train_df

    elif train_type == "clean":

        clean_path = (
            config.PROCESSED_DATA_DIR
            + "/train_clean.csv"
        )

        if not os.path.exists(clean_path):

            raise FileNotFoundError(
                f"找不到 Clean Train：{clean_path}"
            )

        train_df = pd.read_csv(
            clean_path
        )

    else:

        raise ValueError(
            f"不支持 train_type={train_type}"
        )

    return (
        train_df,
        dev_df,
        test_df
    )


# =========================================================
# 3. Class Weight
# =========================================================

def get_class_weights(
        train_df,
        num_classes,
        device
):
    """
    根据当前 Train 的类别分布计算 Weighted CE 权重。

    注意：
    Clean Train 修改了部分标签，
    所以必须重新计算 class weight。
    """

    labels = (
        train_df["label"]
        .astype(int)
        .values
    )

    present_classes = np.sort(
        np.unique(labels)
    )

    weights = compute_class_weight(
        class_weight="balanced",
        classes=present_classes,
        y=labels
    )

    # -----------------------------------------------------
    # 构造完整 num_classes 权重
    #
    # 防止未来某个类别缺失导致权重索引错位。
    # -----------------------------------------------------

    full_weights = np.ones(
        num_classes,
        dtype=np.float32
    )

    for label, weight in zip(
            present_classes,
            weights
    ):
        full_weights[int(label)] = weight

    return torch.tensor(
        full_weights,
        dtype=torch.float,
        device=device
    )


# =========================================================
# 4. Train One Epoch
# =========================================================

def train_one_epoch(
        model,
        data_loader,
        optimizer,
        criterion,
        device
):

    model.train()

    total_loss = 0.0

    for batch in data_loader:

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

        optimizer.zero_grad()

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        logits = outputs.logits

        loss = criterion(
            logits,
            labels
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    return (
        total_loss
        / len(data_loader)
    )


# =========================================================
# 5. Evaluate
# =========================================================

def evaluate(
        model,
        data_loader,
        criterion,
        device
):

    model.eval()

    total_loss = 0.0

    all_labels = []
    all_predictions = []

    with torch.no_grad():

        for batch in data_loader:

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

            logits = outputs.logits

            loss = criterion(
                logits,
                labels
            )

            total_loss += (
                loss.item()
            )

            predictions = torch.argmax(
                logits,
                dim=1
            )

            all_labels.extend(
                labels.cpu().tolist()
            )

            all_predictions.extend(
                predictions.cpu().tolist()
            )

    dev_loss = (
        total_loss
        / len(data_loader)
    )

    accuracy = accuracy_score(
        all_labels,
        all_predictions
    )

    macro_f1 = f1_score(
        all_labels,
        all_predictions,
        average="macro",
        zero_division=0
    )

    return (
        dev_loss,
        accuracy,
        macro_f1
    )


# =========================================================
# 6. Train MacBERT
# =========================================================

def train_macbert(
        train_type="raw",
        batch_size=16,
        max_length=64,
        learning_rate=2e-5,
        epochs=10,
        patience=2,
        seed=42
):

    # =====================================================
    # Seed
    # =====================================================

    set_seed(seed)

    # =====================================================
    # Device
    # =====================================================

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(
        "\n===== Experiment Configuration ====="
    )

    print(
        f"Device        : {device}"
    )

    print(
        f"Train Type    : {train_type}"
    )

    print(
        f"Batch Size    : {batch_size}"
    )

    print(
        f"Max Length    : {max_length}"
    )

    print(
        f"Learning Rate : {learning_rate}"
    )

    print(
        f"Max Epochs    : {epochs}"
    )

    print(
        f"Patience      : {patience}"
    )

    print(
        f"Seed          : {seed}"
    )

    # =====================================================
    # Data
    # =====================================================

    train_df, dev_df, _ = (
        load_training_data(
            train_type
        )
    )

    print(
        f"\nTrain Samples : {len(train_df)}"
    )

    print(
        f"Dev Samples   : {len(dev_df)}"
    )

    # =====================================================
    # Classes
    # =====================================================

    # 使用 Raw + Dev 能观察到的最大 label。
    # 当前 CIC label 为整数类别。
    num_classes = max(
        int(train_df["label"].max()),
        int(dev_df["label"].max())
    ) + 1

    print(
        f"Num Classes   : {num_classes}"
    )

    # =====================================================
    # DataLoader
    # =====================================================

    train_loader, dev_loader, _ = (
        create_macbert_dataloaders(
            train_df=train_df,
            dev_df=dev_df,
            batch_size=batch_size,
            max_length=max_length
        )
    )

    # =====================================================
    # Model
    # =====================================================

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            config.bert_path,
            num_labels=num_classes
        )
    )

    model.to(device)

    # =====================================================
    # Weighted CrossEntropy
    # =====================================================

    class_weights = (
        get_class_weights(
            train_df=train_df,
            num_classes=num_classes,
            device=device
        )
    )

    criterion = (
        torch.nn.CrossEntropyLoss(
            weight=class_weights
        )
    )

    # =====================================================
    # Optimizer
    # =====================================================

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate
    )

    # =====================================================
    # 模型保存路径
    # =====================================================


    if train_type == "clean":

        model_path = (
            config.bert_save_model
            + "/macbert_clean_weighted_best.pt"
        )

    else:

        model_path = (
            config.bert_save_model
            + "/macbert_raw_weighted_best.pt"
        )

    # =====================================================
    # Early Stopping
    # =====================================================

    best_macro_f1 = -1.0
    best_accuracy = 0.0
    best_epoch = 0

    no_improve_count = 0

    # =====================================================
    # Training
    # =====================================================

    print(
        "\n===== Training ====="
    )

    for epoch in range(
            1,
            epochs + 1
    ):

        train_loss = (
            train_one_epoch(
                model=model,
                data_loader=train_loader,
                optimizer=optimizer,
                criterion=criterion,
                device=device
            )
        )

        (
            dev_loss,
            accuracy,
            macro_f1
        ) = evaluate(
            model=model,
            data_loader=dev_loader,
            criterion=criterion,
            device=device
        )

        print(
            f"Epoch [{epoch:02d}/{epochs}] "
            f"Train Loss: {train_loss:.4f} | "
            f"Dev Loss: {dev_loss:.4f} | "
            f"Accuracy: {accuracy:.4f} | "
            f"Macro-F1: {macro_f1:.4f}"
        )

        # =================================================
        # Best Model
        #
        # 主指标：Macro-F1
        # =================================================

        if macro_f1 > best_macro_f1:

            best_macro_f1 = (
                macro_f1
            )

            best_accuracy = (
                accuracy
            )

            best_epoch = (
                epoch
            )

            no_improve_count = 0

            torch.save(
                model.state_dict(),
                model_path
            )

            print(
                "  -> Best model saved"
            )

        else:

            no_improve_count += 1

            print(
                f"  -> No improvement "
                f"({no_improve_count}/{patience})"
            )

        # =================================================
        # Early Stop
        # =================================================

        if (
            no_improve_count
            >= patience
        ):

            print(
                "  -> Early Stopping"
            )

            break

    # =====================================================
    # Final
    # =====================================================

    print(
        "\n===== Training Result ====="
    )

    print(
        f"Train Type     : {train_type}"
    )

    print(
        f"Best Epoch     : {best_epoch}"
    )

    print(
        f"Best Accuracy  : {best_accuracy:.4f}"
    )

    print(
        f"Best Macro-F1  : {best_macro_f1:.4f}"
    )

    print(
        f"Model Saved    : {model_path}"
    )

    return {
        "train_type": train_type,
        "best_epoch": best_epoch,
        "accuracy": best_accuracy,
        "macro_f1": best_macro_f1,
        "model_path": str(model_path)
    }


# =========================================================
# 7. Command Line Arguments
# =========================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Train Weighted MacBERT "
            "on Raw or Clean CIC dataset"
        )
    )

    parser.add_argument(
        "--train",
        choices=[
            "raw",
            "clean"
        ],
        default="raw",
        help="选择训练数据：raw 或 clean"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=16
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=64
    )

    parser.add_argument(
        "--lr",
        type=float,
        default=2e-5
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=10
    )

    parser.add_argument(
        "--patience",
        type=int,
        default=2
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42
    )

    return parser.parse_args()


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    TRAIN_TYPE = "raw"
    # TRAIN_TYPE = "clean"

    train_macbert(
        train_type=TRAIN_TYPE,
        batch_size=16,
        max_length=64,
        learning_rate=2e-5,
        epochs=10,
        patience=2,
        seed=42
    )
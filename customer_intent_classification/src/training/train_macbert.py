import torch
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import (
    MODEL_NAME,
    create_macbert_dataloaders
)
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import numpy as np
from sklearn.utils.class_weight import compute_class_weight

# 然后再导入 huggingface 相关的库
from transformers import AutoModel, AutoTokenizer


config = Config()

def train_one_epoch(
    model,
    train_loader,
    optimizer,
    criterion,
    device
):
    model.train()

    total_loss = 0.0

    for batch in train_loader:

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

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

    return total_loss / len(train_loader)


def evaluate(
    model,
    dev_loader,
    criterion,
    device
):
    model.eval()

    total_loss = 0.0

    all_labels = []
    all_predictions = []

    with torch.no_grad():

        for batch in dev_loader:

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = outputs.logits

            loss = criterion(
                logits,
                labels
            )

            total_loss += loss.item()

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

    avg_loss = total_loss / len(dev_loader)

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

    return avg_loss, accuracy, macro_f1


def train_macbert(
    model,
    train_loader,
    dev_loader,
    optimizer,
    criterion,
    device,
    epochs=10,
    patience=2
):
    """MacBERT Fine-tuning"""

    best_macro_f1 = 0.0
    no_improve_count = 0

    bert_base_save_path = config.bert_save_model + "/macbert_best.pt"
    bert_weighted_save_path = config.bert_save_model + "/macbert_weighted_best.pt"


    for epoch in range(1, epochs + 1):

        # ==============================
        # Train
        # ==============================

        train_loss = train_one_epoch(
            model,
            train_loader,
            optimizer,
            criterion,
            device
        )

        # ==============================
        # Dev
        # ==============================

        dev_loss, accuracy, macro_f1 = evaluate(
            model,
            dev_loader,
            criterion,
            device
        )

        print(
            f"Epoch [{epoch:02d}/{epochs}] "
            f"Train Loss: {train_loss:.4f} | "
            f"Dev Loss: {dev_loss:.4f} | "
            f"Accuracy: {accuracy:.4f} | "
            f"Macro-F1: {macro_f1:.4f}"
        )

        # ==============================
        # 保存最佳模型
        # ==============================

        if macro_f1 > best_macro_f1:

            best_macro_f1 = macro_f1
            no_improve_count = 0

            torch.save(
                model.state_dict(),
                bert_weighted_save_path
            )

            print(
                f"  -> Best Macro-F1: "
                f"{best_macro_f1:.4f} | Model Saved"
            )

        else:

            no_improve_count += 1

            if no_improve_count >= patience:
                print("  -> Early Stopping")
                break

    return best_macro_f1


def get_class_weights(train_df, device):
    """
    根据训练集类别分布计算 balanced class weight
    """

    labels = train_df["label"].values
    classes = np.sort(train_df["label"].unique())

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=labels
    )

    return torch.tensor(
        weights,
        dtype=torch.float,
        device=device
    )



if __name__ == "__main__":

    # =========================================================
    # 1. Device
    # =========================================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Device:", device)

    # =========================================================
    # 2. 数据
    # =========================================================

    train_df, dev_df, _ = load_cic_dataset()

    train_loader, dev_loader, tokenizer = (
        create_macbert_dataloaders(
            train_df,
            dev_df,
            batch_size=16,
            max_length=64
        )
    )

    print("Train Samples:", len(train_df))
    print("Dev Samples:", len(dev_df))
    print("Num Classes:", train_df["label"].nunique())

    # =========================================================
    # 3. 加载预训练 MacBERT
    # =========================================================

    model = AutoModelForSequenceClassification.from_pretrained(
        config.bert_path,
        num_labels=train_df["label"].nunique()
    )

    model = model.to(device)

    # =========================================================
    # 4. Optimizer
    # =========================================================

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=2e-5
    )

    class_weights = get_class_weights(
        train_df,
        device
    )

    print("Class Weights Shape:", class_weights.shape)

    criterion = torch.nn.CrossEntropyLoss(
        weight=class_weights
    )

    # =========================================================
    # 5. Fine-tuning
    # =========================================================

    best_macro_f1 = train_macbert(
        model=model,
        train_loader=train_loader,
        dev_loader=dev_loader,
        optimizer=optimizer,
        criterion=criterion,
        device=device,
        epochs=10,
        patience=2
    )

    print("\n===== MacBERT Result =====")
    print(f"Best Macro-F1: {best_macro_f1:.4f}")
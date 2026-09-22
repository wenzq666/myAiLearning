import os
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.metrics import accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


# =========================================================
# Config
# =========================================================

config = Config()


# =========================================================
# 实验参数
# =========================================================

SEED = 42

BATCH_SIZE = 16
MAX_LENGTH = 64

EPOCHS = 10
LEARNING_RATE = 2e-5

SEMANTIC_LOSS_WEIGHT = 0.2

EARLY_STOPPING_PATIENCE = 2


# =========================================================
# 1. Seed
# =========================================================

def set_seed(seed=42):

    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():

        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# =========================================================
# 2. 加载 Clean Train + 原始 Dev
# =========================================================

def load_train_dev():

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

    # -----------------------------------------------------
    # Dev 继续使用原始 Dev
    # -----------------------------------------------------

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
# 3. 构建严格按照 Label ID 排序的 Label Description
# =========================================================

def build_label_descriptions(
        train_df,
        dev_df,
        num_classes
):

    # -----------------------------------------------------
    # Train + Dev 都拿来建立：
    #
    # label -> label_des
    #
    # 这里只使用标签名称，不使用 Dev 文本训练模型
    # -----------------------------------------------------

    mapping_df = pd.concat(
        [
            train_df[
                [
                    "label",
                    "label_des"
                ]
            ],
            dev_df[
                [
                    "label",
                    "label_des"
                ]
            ]
        ],
        ignore_index=True
    )

    mapping_df["label_des"] = (
        mapping_df["label_des"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # 检查：
    # 同一个 Label 是否出现多个 label_des
    # -----------------------------------------------------

    mapping_check = (
        mapping_df
        .groupby("label")["label_des"]
        .nunique()
    )

    abnormal = (
        mapping_check[
            mapping_check > 1
        ]
    )

    if len(abnormal) > 0:

        raise ValueError(
            "发现同一个 label 对应多个 label_des：\n"
            + str(abnormal)
        )

    # -----------------------------------------------------
    # label -> label_des
    # -----------------------------------------------------

    label_mapping = (
        mapping_df
        .drop_duplicates(
            subset=["label"]
        )
        .set_index("label")["label_des"]
        .to_dict()
    )

    # -----------------------------------------------------
    # 必须严格按照：
    #
    # 0, 1, 2, ..., num_classes - 1
    #
    # 构造
    # -----------------------------------------------------

    label_descriptions = []

    for label_id in range(
            num_classes
    ):

        if label_id not in label_mapping:

            raise ValueError(
                f"缺少 label={label_id} "
                f"对应的 label_des"
            )

        label_des = (
            label_mapping[
                label_id
            ]
        )

        if not label_des:

            raise ValueError(
                f"label={label_id} "
                f"的 label_des 为空"
            )

        label_descriptions.append(
            label_des
        )

    if (
        len(label_descriptions)
        != num_classes
    ):

        raise ValueError(
            "Label Description 数量异常"
        )

    return label_descriptions


# =========================================================
# 4. Tokenize 118 个 Label Description
# =========================================================

def tokenize_label_descriptions(
        label_descriptions
):

    encoded = config.tokenizer(
        label_descriptions,

        padding=True,
        truncation=True,

        max_length=32,

        return_tensors="pt"
    )

    return (
        encoded["input_ids"],
        encoded["attention_mask"]
    )


# =========================================================
# 5. Class Weight
# =========================================================

def build_class_weights(
        train_df,
        num_classes,
        device
):

    classes = np.arange(
        num_classes
    )

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=train_df["label"].values
    )

    weights = torch.tensor(
        weights,
        dtype=torch.float32,
        device=device
    )

    return weights


# =========================================================
# 6. Train One Epoch
# =========================================================

def train_one_epoch(
        model,
        train_loader,
        optimizer,
        scheduler,
        classification_criterion,
        label_input_ids,
        label_attention_mask,
        device
):

    model.train()

    total_loss = 0.0
    total_classification_loss = 0.0
    total_semantic_loss = 0.0

    for batch in train_loader:

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

        # -------------------------------------------------
        # Forward
        # -------------------------------------------------

        outputs = model(

            input_ids=input_ids,

            attention_mask=attention_mask,

            label_input_ids=label_input_ids,

            label_attention_mask=label_attention_mask
        )

        classification_logits = (
            outputs[
                "classification_logits"
            ]
        )

        semantic_logits = (
            outputs[
                "semantic_logits"
            ]
        )

        # -------------------------------------------------
        # ① Weighted Classification CE
        # -------------------------------------------------

        classification_loss = (
            classification_criterion(
                classification_logits,
                labels
            )
        )

        # -------------------------------------------------
        # ② Label Semantic CE
        #
        # 这里暂时不加 class weight。
        #
        # Classification 分支已经负责处理长尾，
        # Semantic 分支先单纯学习：
        #
        # sentence <-> correct label_des
        # -------------------------------------------------

        semantic_loss = (
            nn.functional.cross_entropy(
                semantic_logits,
                labels
            )
        )

        # -------------------------------------------------
        # Total Loss
        # -------------------------------------------------

        loss = (
            classification_loss
            +
            SEMANTIC_LOSS_WEIGHT
            * semantic_loss
        )

        # -------------------------------------------------
        # Backward
        # -------------------------------------------------

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )

        optimizer.step()

        scheduler.step()

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        total_loss += (
            loss.item()
        )

        total_classification_loss += (
            classification_loss.item()
        )

        total_semantic_loss += (
            semantic_loss.item()
        )

    num_batches = len(
        train_loader
    )

    return {

        "loss":
            total_loss
            / num_batches,

        "classification_loss":
            total_classification_loss
            / num_batches,

        "semantic_loss":
            total_semantic_loss
            / num_batches
    }


# =========================================================
# 7. Evaluate
# =========================================================

def evaluate(
        model,
        dev_loader,
        device
):

    model.eval()

    all_labels = []
    all_predictions = []

    with torch.no_grad():

        for batch in dev_loader:

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

            # ---------------------------------------------
            # 公平比较：
            #
            # Dev 最终预测仍然只使用普通分类头。
            #
            # Label Semantic 在这里是辅助训练任务。
            # ---------------------------------------------

            outputs = model(

                input_ids=input_ids,

                attention_mask=attention_mask
            )

            logits = (
                outputs[
                    "classification_logits"
                ]
            )

            predictions = (
                torch.argmax(
                    logits,
                    dim=1
                )
            )

            all_labels.extend(
                labels
                .cpu()
                .numpy()
                .tolist()
            )

            all_predictions.extend(
                predictions
                .cpu()
                .numpy()
                .tolist()
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

    return accuracy, macro_f1


# =========================================================
# 8. Main
# =========================================================

def main():

    # =====================================================
    # Seed
    # =====================================================

    set_seed(
        SEED
    )

    device = config.device

    print(
        f"\nDevice: {device}"
    )

    # =====================================================
    # Data
    # =====================================================

    train_df, dev_df = (
        load_train_dev()
    )

    num_classes = (
        max(
            train_df["label"].max(),
            dev_df["label"].max()
        )
        + 1
    )

    print(
        f"Train Samples : {len(train_df)}"
    )

    print(
        f"Dev Samples   : {len(dev_df)}"
    )

    print(
        f"Num Classes   : {num_classes}"
    )

    # =====================================================
    # DataLoader
    # =====================================================

    train_loader, dev_loader,_ = (
        create_macbert_dataloaders(

            train_df=train_df,

            dev_df=dev_df,

            batch_size=BATCH_SIZE,

            max_length=MAX_LENGTH
        )
    )

    # =====================================================
    # Label Descriptions
    # =====================================================

    label_descriptions = (
        build_label_descriptions(

            train_df=train_df,

            dev_df=dev_df,

            num_classes=num_classes
        )
    )

    print(
        f"Label Descriptions: "
        f"{len(label_descriptions)}"
    )

    # -----------------------------------------------------
    # 简单检查前几个 Label
    # -----------------------------------------------------

    print(
        "\n===== Label Description Check ====="
    )

    for label_id in range(
            min(5, num_classes)
    ):

        print(
            f"{label_id:3d} -> "
            f"{label_descriptions[label_id]}"
        )

    # =====================================================
    # Tokenize Label Descriptions
    # =====================================================

    (
        label_input_ids,
        label_attention_mask
    ) = tokenize_label_descriptions(
        label_descriptions
    )

    label_input_ids = (
        label_input_ids
        .to(device)
    )

    label_attention_mask = (
        label_attention_mask
        .to(device)
    )

    print(
        "\nLabel Input Shape:"
        f" {tuple(label_input_ids.shape)}"
    )

    # =====================================================
    # Model
    # =====================================================

    model = LabelSemanticMacBERT(

        bert_path=config.bert_path,

        num_classes=num_classes,

        temperature=0.05
    )

    model = model.to(
        device
    )

    # =====================================================
    # Class Weight
    # =====================================================

    class_weights = (
        build_class_weights(

            train_df=train_df,

            num_classes=num_classes,

            device=device
        )
    )

    classification_criterion = (
        nn.CrossEntropyLoss(
            weight=class_weights
        )
    )

    # =====================================================
    # Optimizer
    # =====================================================

    optimizer = AdamW(

        model.parameters(),

        lr=LEARNING_RATE
    )

    # =====================================================
    # Scheduler
    # =====================================================

    total_steps = (
        len(train_loader)
        * EPOCHS
    )

    warmup_steps = int(
        total_steps
        * 0.1
    )

    scheduler = (
        get_linear_schedule_with_warmup(

            optimizer,

            num_warmup_steps=warmup_steps,

            num_training_steps=total_steps
        )
    )

    # =====================================================
    # Save Path
    # =====================================================

    os.makedirs(
        config.bert_save_model,
        exist_ok=True
    )

    model_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    # =====================================================
    # Training
    # =====================================================

    best_macro_f1 = -1.0
    best_accuracy = 0.0
    best_epoch = 0

    patience_counter = 0

    print(
        "\n"
        "===== Start Label Semantic Training ====="
    )

    print(
        f"Semantic Loss Weight : "
        f"{SEMANTIC_LOSS_WEIGHT}"
    )

    for epoch in range(
            1,
            EPOCHS + 1
    ):

        # -------------------------------------------------
        # Train
        # -------------------------------------------------

        train_result = (
            train_one_epoch(

                model=model,

                train_loader=train_loader,

                optimizer=optimizer,

                scheduler=scheduler,

                classification_criterion=
                    classification_criterion,

                label_input_ids=
                    label_input_ids,

                label_attention_mask=
                    label_attention_mask,

                device=device
            )
        )

        # -------------------------------------------------
        # Dev
        # -------------------------------------------------

        accuracy, macro_f1 = (
            evaluate(

                model=model,

                dev_loader=dev_loader,

                device=device
            )
        )

        # -------------------------------------------------
        # Output
        # -------------------------------------------------

        print(
            f"\nEpoch {epoch}/{EPOCHS}"
        )

        print(
            f"Train Loss          : "
            f"{train_result['loss']:.4f}"
        )

        print(
            f"Classification Loss : "
            f"{train_result['classification_loss']:.4f}"
        )

        print(
            f"Semantic Loss       : "
            f"{train_result['semantic_loss']:.4f}"
        )

        print(
            f"Dev Accuracy        : "
            f"{accuracy:.4f}"
        )

        print(
            f"Dev Macro-F1        : "
            f"{macro_f1:.4f}"
        )

        # -------------------------------------------------
        # Best Model
        # -------------------------------------------------

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

            patience_counter = 0

            torch.save(
                model.state_dict(),
                model_path
            )

            print(
                ">>> Best model saved."
            )

        else:

            patience_counter += 1

            print(
                f"Early Stop Counter: "
                f"{patience_counter}/"
                f"{EARLY_STOPPING_PATIENCE}"
            )

        # -------------------------------------------------
        # Early Stopping
        # -------------------------------------------------

        if (
            patience_counter
            >= EARLY_STOPPING_PATIENCE
        ):

            print(
                "\nEarly stopping."
            )

            break

    # =====================================================
    # Final
    # =====================================================

    print(
        "\n"
        "===== Training Finished ====="
    )

    print(
        f"Best Epoch    : "
        f"{best_epoch}"
    )

    print(
        f"Best Accuracy : "
        f"{best_accuracy:.4f}"
    )

    print(
        f"Best Macro-F1 : "
        f"{best_macro_f1:.4f}"
    )

    print(
        f"Model Saved   : "
        f"{model_path}"
    )


if __name__ == "__main__":
    main()
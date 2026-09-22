import os
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn.metrics import accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup

from src.config import Config
from src.data_process.data_loader import load_cic_dataset
from src.dataset.macbert_dataset import create_macbert_dataloaders
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()


# =========================================================
# 实验参数
# =========================================================

SEED = 42

BATCH_SIZE = 16
MAX_LENGTH = 64

# 这是在 0.5292 模型上继续微调
EPOCHS = 3
LEARNING_RATE = 5e-6

SEMANTIC_LOSS_WEIGHT = 0.2

HARD_NEGATIVE_LOSS_WEIGHT = 0.1
HARD_NEGATIVE_MARGIN = 1.0

# =========================================================
# Targeted Hard Negative Pair
# =========================================================

MODIFY_LABEL_DES = "买家要求修改收件信息"

NO_MODIFY_LABEL_DES = (
    "买家表示收件信息不需要修改了"
)


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
# 2. Data
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

    train_df = pd.read_csv(clean_path)

    # Dev 保持原始数据，不清洗、不修改
    _, dev_df, _ = load_cic_dataset()

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
# 3. Label Description
# =========================================================

def build_label_descriptions(
        train_df,
        dev_df,
        num_classes
):

    mapping_df = pd.concat(
        [
            train_df[
                ["label", "label_des"]
            ],
            dev_df[
                ["label", "label_des"]
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

    # 检查同一个 label 是否出现多个 label_des
    check = (
        mapping_df
        .groupby("label")["label_des"]
        .nunique()
    )

    abnormal = check[
        check > 1
    ]

    if len(abnormal) > 0:

        raise ValueError(
            "同一个 label 对应多个 label_des：\n"
            + str(abnormal)
        )

    mapping = (
        mapping_df
        .drop_duplicates(
            subset=["label"]
        )
        .set_index("label")["label_des"]
        .to_dict()
    )

    label_descriptions = []

    for label_id in range(
            num_classes
    ):

        if label_id not in mapping:

            raise ValueError(
                f"缺少 label={label_id}"
            )

        label_descriptions.append(
            mapping[label_id]
        )

    return label_descriptions


# =========================================================
# 4. 根据 label_des 找 Label ID
# =========================================================

def find_label_id(
        train_df,
        label_des
):

    rows = train_df[
        train_df["label_des"]
        .astype(str)
        .str.strip()
        == label_des
    ]

    if len(rows) == 0:

        raise ValueError(
            f"Train 中找不到标签：{label_des}"
        )

    label_ids = (
        rows["label"]
        .unique()
        .tolist()
    )

    if len(label_ids) != 1:

        raise ValueError(
            f"{label_des} 对应多个 Label ID："
            f"{label_ids}"
        )

    return int(
        label_ids[0]
    )


# =========================================================
# 5. Label Description Tokenize
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
# 6. Class Weight
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

    return torch.tensor(
        weights,
        dtype=torch.float32,
        device=device
    )


# =========================================================
# 7. Targeted Hard Negative Loss
# =========================================================

def compute_hard_negative_loss(
        semantic_logits,
        labels,
        modify_label,
        no_modify_label,
        margin
):

    losses = []

    # =====================================================
    # A:
    #
    # True:
    # 买家要求修改收件信息
    #
    # Hard Negative:
    # 买家表示收件信息不需要修改了
    # =====================================================

    modify_mask = (
        labels == modify_label
    )

    if modify_mask.any():

        positive_score = (
            semantic_logits[
                modify_mask,
                modify_label
            ]
        )

        negative_score = (
            semantic_logits[
                modify_mask,
                no_modify_label
            ]
        )

        modify_loss = F.relu(
            margin
            - positive_score
            + negative_score
        )

        losses.append(
            modify_loss.mean()
        )

    # =====================================================
    # B:
    #
    # True:
    # 买家表示收件信息不需要修改了
    #
    # Hard Negative:
    # 买家要求修改收件信息
    # =====================================================

    no_modify_mask = (
        labels == no_modify_label
    )

    if no_modify_mask.any():

        positive_score = (
            semantic_logits[
                no_modify_mask,
                no_modify_label
            ]
        )

        negative_score = (
            semantic_logits[
                no_modify_mask,
                modify_label
            ]
        )

        no_modify_loss = F.relu(
            margin
            - positive_score
            + negative_score
        )

        losses.append(
            no_modify_loss.mean()
        )

    # 当前 Batch 没有目标类别
    if len(losses) == 0:

        return (
            semantic_logits.sum()
            * 0.0
        )

    return (
        torch.stack(losses)
        .mean()
    )


# =========================================================
# 8. Train
# =========================================================

def train_one_epoch(
        model,
        train_loader,
        optimizer,
        scheduler,
        classification_criterion,
        label_input_ids,
        label_attention_mask,
        modify_label,
        no_modify_label,
        device
):

    model.train()

    total_loss = 0.0
    total_cls_loss = 0.0
    total_semantic_loss = 0.0

    # Hard Negative 只统计真正包含目标类别的 batch
    hard_loss_sum = 0.0
    hard_batch_count = 0

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

        # =================================================
        # Forward
        # =================================================

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,

            label_input_ids=
                label_input_ids,

            label_attention_mask=
                label_attention_mask
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

        # =================================================
        # Loss 1:
        # Weighted Classification CE
        # =================================================

        classification_loss = (
            classification_criterion(
                classification_logits,
                labels
            )
        )

        # =================================================
        # Loss 2:
        # Label Semantic CE
        # =================================================

        semantic_loss = (
            F.cross_entropy(
                semantic_logits,
                labels
            )
        )

        # =================================================
        # Loss 3:
        # Targeted Hard Negative
        # =================================================

        hard_negative_loss = (
            compute_hard_negative_loss(

                semantic_logits=
                    semantic_logits,

                labels=labels,

                modify_label=
                    modify_label,

                no_modify_label=
                    no_modify_label,

                margin=
                    HARD_NEGATIVE_MARGIN
            )
        )

        # =================================================
        # Total
        # =================================================

        loss = (
            classification_loss
            +
            SEMANTIC_LOSS_WEIGHT
            * semantic_loss
            +
            HARD_NEGATIVE_LOSS_WEIGHT
            * hard_negative_loss
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )

        optimizer.step()
        scheduler.step()

        # =================================================
        # Statistics
        # =================================================

        total_loss += (
            loss.item()
        )

        total_cls_loss += (
            classification_loss.item()
        )

        total_semantic_loss += (
            semantic_loss.item()
        )

        # 只有 batch 内包含目标 Pair 才统计
        has_hard_sample = (
            (labels == modify_label).any()
            or
            (labels == no_modify_label).any()
        )

        if has_hard_sample:

            hard_loss_sum += (
                hard_negative_loss.item()
            )

            hard_batch_count += 1

    num_batches = len(
        train_loader
    )

    avg_hard_loss = (
        hard_loss_sum
        / hard_batch_count
        if hard_batch_count > 0
        else 0.0
    )

    return {
        "loss":
            total_loss / num_batches,

        "classification_loss":
            total_cls_loss / num_batches,

        "semantic_loss":
            total_semantic_loss / num_batches,

        "hard_negative_loss":
            avg_hard_loss,

        "hard_batches":
            hard_batch_count
    }


# =========================================================
# 9. Evaluate
# =========================================================

def evaluate(
        model,
        dev_loader,
        device,
        modify_label,
        no_modify_label
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

            # 与之前实验保持一致：
            # 最终预测仍然只用 classification head
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

    # =====================================================
    # 专门统计这个 Hard Negative Pair
    # =====================================================

    a_to_b = 0
    b_to_a = 0

    modify_support = 0
    modify_correct = 0

    no_modify_support = 0
    no_modify_correct = 0

    for true_label, pred_label in zip(
            all_labels,
            all_predictions
    ):

        if true_label == modify_label:

            modify_support += 1

            if pred_label == modify_label:
                modify_correct += 1

            if pred_label == no_modify_label:
                a_to_b += 1

        elif true_label == no_modify_label:

            no_modify_support += 1

            if pred_label == no_modify_label:
                no_modify_correct += 1

            if pred_label == modify_label:
                b_to_a += 1

    modify_accuracy = (
        modify_correct / modify_support
        if modify_support > 0
        else 0.0
    )

    no_modify_accuracy = (
        no_modify_correct / no_modify_support
        if no_modify_support > 0
        else 0.0
    )

    return {
        "accuracy":
            accuracy,

        "macro_f1":
            macro_f1,

        "modify_support":
            modify_support,

        "modify_correct":
            modify_correct,

        "modify_accuracy":
            modify_accuracy,

        "no_modify_support":
            no_modify_support,

        "no_modify_correct":
            no_modify_correct,

        "no_modify_accuracy":
            no_modify_accuracy,

        "modify_to_no_modify":
            a_to_b,

        "no_modify_to_modify":
            b_to_a,

        "pair_confusion":
            a_to_b + b_to_a
    }


# =========================================================
# 10. Main
# =========================================================

def main():

    set_seed(SEED)

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
    # 找 Hard Negative Label ID
    # =====================================================

    modify_label = find_label_id(
        train_df,
        MODIFY_LABEL_DES
    )

    no_modify_label = find_label_id(
        train_df,
        NO_MODIFY_LABEL_DES
    )

    print(
        "\n===== Hard Negative Pair ====="
    )

    print(
        f"[{modify_label}] "
        f"{MODIFY_LABEL_DES}"
    )

    print(
        "VS"
    )

    print(
        f"[{no_modify_label}] "
        f"{NO_MODIFY_LABEL_DES}"
    )

    # =====================================================
    # DataLoader
    # =====================================================

    train_loader, dev_loader, _ = (
        create_macbert_dataloaders(
            train_df=train_df,
            dev_df=dev_df,
            batch_size=BATCH_SIZE,
            max_length=MAX_LENGTH
        )
    )

    # =====================================================
    # Label Description
    # =====================================================

    label_descriptions = (
        build_label_descriptions(
            train_df=train_df,
            dev_df=dev_df,
            num_classes=num_classes
        )
    )

    (
        label_input_ids,
        label_attention_mask
    ) = tokenize_label_descriptions(
        label_descriptions
    )

    label_input_ids = (
        label_input_ids.to(device)
    )

    label_attention_mask = (
        label_attention_mask.to(device)
    )

    # =====================================================
    # Model
    # =====================================================

    model = LabelSemanticMacBERT(
        bert_path=config.bert_path,
        num_classes=num_classes,
        temperature=0.05
    )

    # =====================================================
    # 关键：
    #
    # 从已经训练好的 0.5292 Label Semantic 模型继续训练
    # =====================================================

    source_model_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_best.pt"
    )

    if not os.path.exists(
            source_model_path
    ):

        raise FileNotFoundError(
            f"找不到 Label Semantic 模型："
            f"{source_model_path}"
        )

    state_dict = torch.load(
        source_model_path,
        map_location=device
    )

    model.load_state_dict(
        state_dict
    )

    model = model.to(device)

    print(
        "\nLoaded pretrained Label Semantic model:"
    )

    print(
        source_model_path
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

    total_steps = (
        len(train_loader)
        * EPOCHS
    )

    # Fine-tuning 阶段 warmup 少一点
    warmup_steps = int(
        total_steps * 0.05
    )

    scheduler = (
        get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=
                warmup_steps,
            num_training_steps=
                total_steps
        )
    )

    # =====================================================
    # 保存新模型
    # =====================================================

    save_path = (
        config.bert_save_model
        + "/macbert_clean_label_semantic_"
          "hard_negative_best.pt"
    )

    # =====================================================
    # 微调之前先测一次
    #
    # 理论上应该复现：
    # Accuracy 0.6590
    # Macro-F1 0.5292
    # Pair Confusion 20
    # =====================================================

    print(
        "\n===== Before Hard Negative Fine-tuning ====="
    )

    before_result = evaluate(
        model=model,
        dev_loader=dev_loader,
        device=device,
        modify_label=modify_label,
        no_modify_label=no_modify_label
    )

    print(
        f"Accuracy       : "
        f"{before_result['accuracy']:.4f}"
    )

    print(
        f"Macro-F1       : "
        f"{before_result['macro_f1']:.4f}"
    )

    print(
        f"{MODIFY_LABEL_DES} Accuracy: "
        f"{before_result['modify_accuracy']:.4f} "
        f"({before_result['modify_correct']}/"
        f"{before_result['modify_support']})"
    )

    print(
        f"{NO_MODIFY_LABEL_DES} Accuracy: "
        f"{before_result['no_modify_accuracy']:.4f} "
        f"({before_result['no_modify_correct']}/"
        f"{before_result['no_modify_support']})"
    )

    print(
        "Pair Confusion : "
        f"{before_result['pair_confusion']}"
    )

    print(
        "修改 -> 不需要修改 : "
        f"{before_result['modify_to_no_modify']}"
    )

    print(
        "不需要修改 -> 修改 : "
        f"{before_result['no_modify_to_modify']}"
    )

    # =====================================================
    # Train
    # =====================================================

    best_macro_f1 = -1.0
    best_accuracy = 0.0
    best_epoch = 0

    best_pair_confusion = None

    print(
        "\n"
        "===== Start Targeted Hard Negative Fine-tuning ====="
    )

    print(
        f"Learning Rate        : "
        f"{LEARNING_RATE}"
    )

    print(
        f"Semantic Weight      : "
        f"{SEMANTIC_LOSS_WEIGHT}"
    )

    print(
        f"Hard Negative Weight : "
        f"{HARD_NEGATIVE_LOSS_WEIGHT}"
    )

    print(
        f"Hard Negative Margin : "
        f"{HARD_NEGATIVE_MARGIN}"
    )

    for epoch in range(
            1,
            EPOCHS + 1
    ):

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
                modify_label=
                    modify_label,
                no_modify_label=
                    no_modify_label,
                device=device
            )
        )

        result = evaluate(
            model=model,
            dev_loader=dev_loader,
            device=device,
            modify_label=modify_label,
            no_modify_label=no_modify_label
        )

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
            f"Hard Negative Loss  : "
            f"{train_result['hard_negative_loss']:.4f}"
        )

        print(
            f"Hard Negative Batch : "
            f"{train_result['hard_batches']}"
        )

        print(
            f"Dev Accuracy        : "
            f"{result['accuracy']:.4f}"
        )

        print(
            f"Dev Macro-F1        : "
            f"{result['macro_f1']:.4f}"
        )

        print(
            f"Modify Accuracy     : "
            f"{result['modify_accuracy']:.4f} "
            f"({result['modify_correct']}/"
            f"{result['modify_support']})"
        )

        print(
            f"No Modify Accuracy  : "
            f"{result['no_modify_accuracy']:.4f} "
            f"({result['no_modify_correct']}/"
            f"{result['no_modify_support']})"
        )

        print(
            f"Pair Confusion      : "
            f"{result['pair_confusion']}"
        )

        print(
            "Modify -> No Modify : "
            f"{result['modify_to_no_modify']}"
        )

        print(
            "No Modify -> Modify : "
            f"{result['no_modify_to_modify']}"
        )

        # =================================================
        # 仍然以整体 Macro-F1 作为 Best Model 标准
        #
        # 不能为了修一个 Pair，
        # 牺牲整个 118 类模型。
        # =================================================

        if (
            result["macro_f1"]
            > best_macro_f1
        ):

            best_macro_f1 = (
                result["macro_f1"]
            )

            best_accuracy = (
                result["accuracy"]
            )

            best_epoch = epoch

            best_pair_confusion = (
                result[
                    "pair_confusion"
                ]
            )

            torch.save(
                model.state_dict(),
                save_path
            )

            print(
                ">>> Best model saved."
            )

    # =====================================================
    # Final
    # =====================================================

    print(
        "\n"
        "===== Fine-tuning Finished ====="
    )

    print(
        f"Best Epoch          : "
        f"{best_epoch}"
    )

    print(
        f"Best Accuracy       : "
        f"{best_accuracy:.4f}"
    )

    print(
        f"Best Macro-F1       : "
        f"{best_macro_f1:.4f}"
    )

    print(
        f"Best Pair Confusion : "
        f"{best_pair_confusion}"
    )

    print(
        f"Model Saved         : "
        f"{save_path}"
    )


if __name__ == "__main__":
    main()
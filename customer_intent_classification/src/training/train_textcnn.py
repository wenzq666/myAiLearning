import torch
import torch.nn as nn

from sklearn.metrics import accuracy_score, f1_score

from src.data_process.data_loader import load_cic_dataset
from src.dataset.text_dataset import create_dataloaders
from src.models.textcnn import TextCNN

from src.config import Config


config = Config()

def train_one_epoch(model, train_loader, criterion, optimizer, device):
    """
    训练一个 epoch
    """

    model.train()

    total_loss = 0.0

    for batch in train_loader:

        input_ids = batch["input_ids"].to(device)
        labels = batch["label"].to(device)

        # 清空上一轮梯度
        optimizer.zero_grad()

        # 前向传播
        logits = model(input_ids)

        # 计算损失
        loss = criterion(logits, labels)

        # 反向传播
        loss.backward()

        # 更新参数
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


def evaluate(model, dev_loader, criterion, device):
    """
    验证模型
    """

    model.eval()

    total_loss = 0.0

    all_labels = []
    all_predictions = []

    with torch.no_grad():

        for batch in dev_loader:

            input_ids = batch["input_ids"].to(device)
            labels = batch["label"].to(device)

            # 前向传播
            logits = model(input_ids)

            # loss
            loss = criterion(logits, labels)

            total_loss += loss.item()

            # 获取预测类别
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


def train_textcnn(
    model,
    train_loader,
    dev_loader,
    device,
    epochs=30,
    learning_rate=1e-3
):
    """
    TextCNN 完整训练流程
    """

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate
    )

    best_macro_f1 = 0.0
    patience = 3
    no_improve_count = 0

    for epoch in range(1, epochs + 1):

        # ==============================
        # Train
        # ==============================

        train_loss = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
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
        # 记录最佳结果
        # ==============================

        if macro_f1 > best_macro_f1:
            best_macro_f1 = macro_f1
            no_improve_count = 0

            save_path =  config.testCNNModel +  "/textcnn_best.pt"

            torch.save(
                model.state_dict(),
                save_path
            )

            print(
                f"  -> Best Macro-F1: {best_macro_f1:.4f}"
                f" | Model Saved"
            )
        else:
            no_improve_count += 1

            if no_improve_count >= patience:
                print("\nEarly Stopping")
                break

    return model


if __name__ == "__main__":

    # =========================================================
    # 1. 设备
    # =========================================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Device:", device)

    # =========================================================
    # 2. 数据
    # =========================================================

    train_df, dev_df, _ = load_cic_dataset()

    train_loader, dev_loader, vocab = create_dataloaders(
        train_df,
        dev_df,
        batch_size=64,
        max_length=64
    )

    print("Vocab Size:", len(vocab))
    print("Train Samples:", len(train_df))
    print("Dev Samples:", len(dev_df))

    # =========================================================
    # 3. 创建模型
    # =========================================================

    model = TextCNN(
        vocab_size=len(vocab),
        num_classes=train_df["label"].nunique(),
        embedding_dim=128,
        num_filters=128,
        kernel_sizes=(2, 3, 4),
        dropout=0.5
    )

    model = model.to(device)

    # =========================================================
    # 4. 开始训练
    # =========================================================

    model = train_textcnn(
        model=model,
        train_loader=train_loader,
        dev_loader=dev_loader,
        device=device,
        epochs=30,
        learning_rate=1e-3
    )
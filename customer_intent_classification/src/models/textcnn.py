import torch
import torch.nn as nn

from src.data_process.data_loader import load_cic_dataset
from src.dataset.text_dataset import create_dataloaders


class TextCNN(nn.Module):

    def __init__(
        self,
        vocab_size,
        num_classes,
        embedding_dim=128,
        num_filters=128,
        kernel_sizes=(2, 3, 4),
        dropout=0.5
    ):
        super().__init__()

        # 1. Embedding
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0
        )

        # 2. 多尺寸卷积
        self.convs = nn.ModuleList([
            nn.Conv1d(
                in_channels=embedding_dim,
                out_channels=num_filters,
                kernel_size=k
            )
            for k in kernel_sizes
        ])

        # 3. Dropout
        self.dropout = nn.Dropout(dropout)

        # 4. 分类层
        self.fc = nn.Linear(
            num_filters * len(kernel_sizes),
            num_classes
        )

    def forward(self, input_ids):

        # [batch_size, seq_len]
        x = self.embedding(input_ids)

        # [batch_size, seq_len, embedding_dim]
        #       ↓
        # [batch_size, embedding_dim, seq_len]
        x = x.permute(0, 2, 1)

        pooled_outputs = []

        for conv in self.convs:

            # 卷积
            conv_out = torch.relu(conv(x))

            # Global Max Pooling
            pooled = torch.max(
                conv_out,
                dim=2
            ).values

            pooled_outputs.append(pooled)

        # 拼接不同卷积核提取的特征
        x = torch.cat(
            pooled_outputs,
            dim=1
        )

        x = self.dropout(x)

        # 输出118个类别的 logits
        logits = self.fc(x)

        return logits


if __name__ == "__main__":

    # ---------------------------------------------------------
    # 加载数据
    # ---------------------------------------------------------
    train_df, dev_df, _ = load_cic_dataset()

    train_loader, dev_loader, vocab = create_dataloaders(
        train_df,
        dev_df,
        batch_size=64,
        max_length=64
    )

    # ---------------------------------------------------------
    # 创建模型
    # ---------------------------------------------------------
    model = TextCNN(
        vocab_size=len(vocab),
        num_classes=train_df["label"].nunique()
    )

    print(model)

    # ---------------------------------------------------------
    # 获取一个 Batch
    # ---------------------------------------------------------
    batch = next(iter(train_loader))

    input_ids = batch["input_ids"]

    print("\ninput_ids shape:")
    print(input_ids.shape)

    # ---------------------------------------------------------
    # 前向传播
    # ---------------------------------------------------------
    logits = model(input_ids)

    print("\nlogits shape:")
    print(logits.shape)

    # ---------------------------------------------------------
    # 得到预测类别
    # ---------------------------------------------------------
    predictions = torch.argmax(
        logits,
        dim=1
    )

    print("\npredictions shape:")
    print(predictions.shape)

    print("\n前10个预测:")
    print(predictions[:10])
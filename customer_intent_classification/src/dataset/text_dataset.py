from collections import Counter

import torch
from torch.utils.data import Dataset, DataLoader

from src.data_process.data_loader import load_cic_dataset


# 特殊字符
PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"

PAD_ID = 0
UNK_ID = 1


def build_vocab(sentences, min_freq=1):
    """
    根据训练集构建字符词表

    Parameters
    ----------
    sentences : 文本列表
    min_freq : 最低字符出现次数

    Returns
    -------
    dict
        char -> id
    """

    counter = Counter()

    for sentence in sentences:
        counter.update(str(sentence))

    vocab = {
        PAD_TOKEN: PAD_ID,
        UNK_TOKEN: UNK_ID
    }

    for char, count in counter.items():
        if count >= min_freq:
            vocab[char] = len(vocab)

    return vocab


def encode_text(text, vocab, max_length):
    """
    文本转换成字符 ID，并进行截断和 Padding
    """

    token_ids = [
        vocab.get(char, UNK_ID)
        for char in str(text)
    ]

    # 截断
    token_ids = token_ids[:max_length]

    # Padding
    if len(token_ids) < max_length:
        token_ids += [PAD_ID] * (max_length - len(token_ids))

    return token_ids


class CICDataset(Dataset):

    def __init__(self, df, vocab, max_length=64):

        self.sentences = df["sentence"].tolist()
        self.labels = df["label"].tolist()

        self.vocab = vocab
        self.max_length = max_length

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, index):

        sentence = self.sentences[index]
        label = self.labels[index]

        token_ids = encode_text(
            sentence,
            self.vocab,
            self.max_length
        )

        return {
            "input_ids": torch.tensor(
                token_ids,
                dtype=torch.long
            ),
            "label": torch.tensor(
                label,
                dtype=torch.long
            )
        }


def create_dataloaders(
    train_df,
    dev_df,
    batch_size=64,
    max_length=64
):
    """
    创建训练集和验证集 DataLoader
    """

    # 只能使用训练集构建词表
    vocab = build_vocab(
        train_df["sentence"]
    )

    train_dataset = CICDataset(
        train_df,
        vocab,
        max_length
    )

    dev_dataset = CICDataset(
        dev_df,
        vocab,
        max_length
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    dev_loader = DataLoader(
        dev_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, dev_loader, vocab


if __name__ == "__main__":

    train_df, dev_df, _ = load_cic_dataset()

    train_loader, dev_loader, vocab = create_dataloaders(
        train_df,
        dev_df,
        batch_size=64,
        max_length=64
    )

    print("词表大小:", len(vocab))
    print("训练 Batch 数:", len(train_loader))
    print("验证 Batch 数:", len(dev_loader))

    # 取一个 batch 检查
    batch = next(iter(train_loader))

    print("input_ids shape:", batch["input_ids"].shape)
    print("label shape:", batch["label"].shape)

    print("\n第一条 input_ids:")
    print(batch["input_ids"][0])

    print("\n第一条 label:")
    print(batch["label"][0])
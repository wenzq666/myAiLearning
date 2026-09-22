import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer

from src.data_process.data_loader import load_cic_dataset

from src.config import Config


MODEL_NAME = "chinese-macbert-base"
config = Config()


class MacBERTDataset(Dataset):

    def __init__(
        self,
        df,
        tokenizer,
        max_length=64
    ):
        self.sentences = df["sentence"].tolist()
        self.labels = df["label"].tolist()

        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, index):

        sentence = str(self.sentences[index])
        label = self.labels[index]

        encoding = self.tokenizer(
            sentence,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),

            "attention_mask": encoding["attention_mask"].squeeze(0),

            "label": torch.tensor(
                label,
                dtype=torch.long
            )
        }


def create_macbert_dataloaders(
    train_df,
    dev_df,
    batch_size=16,
    max_length=64
):

    tokenizer = AutoTokenizer.from_pretrained(
        config.bert_path
    )

    train_dataset = MacBERTDataset(
        train_df,
        tokenizer,
        max_length
    )

    dev_dataset = MacBERTDataset(
        dev_df,
        tokenizer,
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

    return train_loader, dev_loader, tokenizer


if __name__ == "__main__":

    train_df, dev_df, _ = load_cic_dataset()

    train_loader, dev_loader, tokenizer = (
        create_macbert_dataloaders(
            train_df,
            dev_df,
            batch_size=16,
            max_length=64
        )
    )

    batch = next(iter(train_loader))

    print("input_ids:")
    print(batch["input_ids"].shape)

    print("\nattention_mask:")
    print(batch["attention_mask"].shape)

    print("\nlabel:")
    print(batch["label"].shape)

    print("\n第一条 input_ids:")
    print(batch["input_ids"][0])

    print("\n第一条 attention_mask:")
    print(batch["attention_mask"][0])

    print("\n还原文本:")
    print(
        tokenizer.decode(
            batch["input_ids"][0]
        )
    )
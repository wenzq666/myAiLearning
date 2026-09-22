import json
import os

import pandas as pd

from src.config import Config


config = Config()


# =========================================================
# 1. 读取 Test JSONL
# =========================================================

def load_test_data():

    rows = []

    with open(
            config.test_datapath,
            "r",
            encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            rows.append(
                json.loads(line)
            )

    df = pd.DataFrame(rows)

    df["label"] = (
        df["label"]
        .astype(int)
    )

    df["sentence"] = (
        df["sentence"]
        .fillna("")
        .astype(str)
    )

    df["label_des"] = (
        df["label_des"]
        .fillna("")
        .astype(str)
    )

    return df


# =========================================================
# 2. 获取示例
# =========================================================

def get_examples(
        df,
        label,
        n=3
):

    examples = (
        df[
            df["label"] == label
        ]["sentence"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .head(n)
        .tolist()
    )

    return " | ".join(
        examples
    )


# =========================================================
# 3. 构建 Intent Catalog
# =========================================================

def build_catalog():

    # -----------------------------------------------------
    # Clean Train
    # -----------------------------------------------------

    train_path = (
        config.PROCESSED_DATA_DIR
        + "/train_clean.csv"
    )

    train_df = pd.read_csv(
        train_path
    )

    train_df["label"] = (
        train_df["label"]
        .astype(int)
    )

    train_df["sentence"] = (
        train_df["sentence"]
        .fillna("")
        .astype(str)
    )

    train_df["label_des"] = (
        train_df["label_des"]
        .fillna("")
        .astype(str)
    )

    # -----------------------------------------------------
    # Test
    # -----------------------------------------------------

    test_df = (
        load_test_data()
    )

    # -----------------------------------------------------
    # Label Mapping
    # -----------------------------------------------------

    label_df = pd.concat(
        [
            train_df[
                [
                    "label",
                    "label_des"
                ]
            ],

            test_df[
                [
                    "label",
                    "label_des"
                ]
            ]
        ],
        ignore_index=True
    )

    label_df = (
        label_df
        .drop_duplicates(
            subset=["label"]
        )
        .sort_values("label")
    )

    # -----------------------------------------------------
    # Count
    # -----------------------------------------------------

    train_counts = (
        train_df[
            "label"
        ]
        .value_counts()
        .to_dict()
    )

    test_counts = (
        test_df[
            "label"
        ]
        .value_counts()
        .to_dict()
    )

    rows = []

    for _, row in (
            label_df.iterrows()
    ):

        label = int(
            row["label"]
        )

        label_des = (
            row["label_des"]
        )

        rows.append(
            {
                "label":
                    label,

                "label_des":
                    label_des,

                "train_samples":
                    train_counts.get(
                        label,
                        0
                    ),

                "test_samples":
                    test_counts.get(
                        label,
                        0
                    ),

                "train_examples":
                    get_examples(
                        train_df,
                        label,
                        n=3
                    ),

                "test_examples":
                    get_examples(
                        test_df,
                        label,
                        n=3
                    )
            }
        )

    catalog_df = pd.DataFrame(
        rows
    )

    return catalog_df


# =========================================================
# 4. Main
# =========================================================

def main():

    catalog_df = (
        build_catalog()
    )

    print(
        "===== Intent Catalog ====="
    )

    print(
        f"Intent Count: "
        f"{len(catalog_df)}"
    )

    print()

    print(
        catalog_df[
            [
                "label",
                "label_des",
                "train_samples",
                "test_samples"
            ]
        ].to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    output_dir = (
        config.INTERIM_DATA_DIR
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_path = (
        output_dir
        + "/intent_catalog.csv"
    )

    catalog_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\n===== Saved ====="
    )

    print(
        output_path
    )


if __name__ == "__main__":
    main()
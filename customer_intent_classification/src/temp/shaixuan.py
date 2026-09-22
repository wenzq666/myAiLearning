import pandas as pd

from src.config import Config

config = Config()

path = (
    config.INTERIM_DATA_DIR
    + "/label_semantic_dev_predictions.csv"
)

df = pd.read_csv(path)

intent_a = "买家表示收件信息不需要修改了"
intent_b = "买家要求修改收件信息"

# A -> B
a_to_b = df[
    (df["label_des"] == intent_a)
    &
    (df["new_pred_des"] == intent_b)
]

# B -> A
b_to_a = df[
    (df["label_des"] == intent_b)
    &
    (df["new_pred_des"] == intent_a)
]

print("\n===== A -> B =====")
print("数量：", len(a_to_b))

print(
    a_to_b[
        ["sentence", "label_des", "new_pred_des"]
    ].to_string(index=False)
)

print("\n===== B -> A =====")
print("数量：", len(b_to_a))

print(
    b_to_a[
        ["sentence", "label_des", "new_pred_des"]
    ].to_string(index=False)
)

print("\n总混淆数量：", len(a_to_b) + len(b_to_a))
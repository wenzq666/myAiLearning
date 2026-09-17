"""
混淆矩阵 行(真实值)  列(预测值)
"""
import pandas as pd
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score

#
y_true = ["恶行","恶行","恶行","恶行","恶行","恶行","良性","良性","良性","良性"]

# 指定名称
labels = ["恶行","良性"]
df_labels = ["恶行(正例)","良性(反例)"]

# 模型A
y_pred_A = ["恶行","恶行","恶行","良性","良性","良性","良性","良性","良性","良性"]

cm = confusion_matrix(y_true,y_pred_A,labels=labels)
df = pd.DataFrame(cm,index=df_labels,columns=df_labels)
print(df)
# 预测对了 3 个恶性肿瘤样本，4 个良性肿瘤样本
#  预测结果 3 个恶性   7个 良性
# TP  3   恶行 模型预测对的
# FP  0   模型误判成恶行的
# FN  3   模型误判成良性的
# TN  4   良性 模型预测对的
# 准确率
acc_A = accuracy_score(y_true,y_pred_A)
print(acc_A)
# 精确率
prec_A = precision_score(y_true,y_pred_A,pos_label="恶行")
print(prec_A)

# 召回率
rec_A = recall_score(y_true,y_pred_A,pos_label="恶行")
print(rec_A)
# F1分数
f1_A = f1_score(y_true,y_pred_A,pos_label="恶行")
print(f1_A)

print('*'*50)
# 模型B
y_pred_B = ["恶行","恶行","恶行","恶行","恶行","恶行","恶行","恶行","恶行","良性"]
cm = confusion_matrix(y_true,y_pred_B,labels=labels)
df = pd.DataFrame(cm,index=df_labels,columns=df_labels)
print(df)

# 预测对了  6 个恶性肿瘤样本，1个良性肿瘤
# 预测结果  9个 恶性肿瘤样本 1个良性肿瘤
# TP  6   恶行 模型预测对的
# FP  3   模型误判成恶行的
# FN  0   模型误判成良性的
# TN  1   良性 模型预测对的
acc_B = accuracy_score(y_true,y_pred_B)
print(acc_B)
# 精确率
prec_B = precision_score(y_true,y_pred_B,pos_label="恶行")
print(prec_B)

# 召回率
rec_B = recall_score(y_true,y_pred_B,pos_label="恶行")
print(rec_B)
# F1分数
f1_B = f1_score(y_true,y_pred_B,pos_label="恶行")
print(f1_B)




















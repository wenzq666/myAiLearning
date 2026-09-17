import jieba.posseg as pos


# 词性标注
sentence = "小明一把把把把住了"

pos_cut_1 = pos.lcut(sentence)
print(pos_cut_1)
for word, flag in pos_cut_1:
    print(f"词:{word},词性:{flag}")




























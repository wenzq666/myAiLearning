import jieba


def word_2_idx():
    global data
    unique_list = []
    all_words = []
    # 今天天气不好
    data = ["小明一把把把把住了", "小明与把"]
    for sentence in data:
        cut_result = jieba.lcut(sentence)
        all_words.append(cut_result)
        # print(cut_result)
        for word in cut_result:
            if word not in unique_list:
                unique_list.append(word)

    word_2_id = {word: i for i, word in enumerate(unique_list)}
    print(word_2_id)




if __name__ == '__main__':
    word_2_idx()
































































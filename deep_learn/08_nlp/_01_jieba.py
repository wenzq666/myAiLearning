import jieba


sentence = "小明一把把把把住了"

# 精确模式  没有重复分词 切成唯一的分词
c1 = jieba.lcut(sentence, cut_all=False)
print(c1)

print('----')
# 全模式  同一个字符串可能分成多个词 完整性更全
c2 = jieba.lcut(sentence, cut_all=True)
print(c2)

print('----')
# 搜索引擎模式  是在精确模式基础上进一步切分
c3 = jieba.lcut_for_search(sentence)
print(c3)

print('----')
# 加载词典
jieba.load_userdict('./data/user_dict.txt')
c1 = jieba.lcut(sentence, cut_all=False)
print(c1)

















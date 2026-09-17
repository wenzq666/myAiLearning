# set
s2 = {'迪丽热巴','古力娜扎','雷霆嘎巴','迪丽热巴','迪丽热巴','尼古拉斯','JQKA'}

s2.add("AAAA")
s2.remove("迪丽热巴")

print(type(s2))
print(s2)

for name in s2:
    print(name)


l1 = ['迪丽热巴','古力娜扎','雷霆嘎巴','迪丽热巴','迪丽热巴','尼古拉斯','JQKA']
ss = set(l1)

print(list(ss))


ss1 = {1,2,3}
ss2 = {3,4,5}

# 差集
ss1.difference_update(ss2)
print(ss1)

# 并集
ss1.update(ss2)
print(ss1)

# 交集
print(ss1 & ss2)

print(len(ss1))


# for遍历
for i in ss1:
    print(i)

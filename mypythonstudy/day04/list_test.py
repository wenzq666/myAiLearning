names = ['迪丽热巴','古力娜扎','雷霆嘎巴','迪丽热巴','迪丽热巴','尼古拉斯','JQKA']

#names.insert(1,'尼古拉斯')

#names.append('赵四')

#names.extend('尼古拉斯')

#names.extend(['尼古拉斯'])

#print(names)

#del
#pop
#remove
# del names[0]
# names.pop(1)
# names.remove('古力娜扎')
# print(names)


# for name in names:
#     print(name)

new_names = []
for name in names:
    if name not in new_names:
        new_names.append(name)

print(new_names)
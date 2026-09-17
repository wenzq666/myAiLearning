# 文件操作
# f = open('1.txt','r',encoding='utf-8')
#
# # print(f.read())
#
# print(f.readline())
# f.seek(0)
# print(f.readline())
# print(f.readline())
#
# f.seek(0)
#
# print(f.readlines())
#
# f.close()
#
#
# f1 = open('./data/2.txt','r',encoding='utf-8')
#
# #print(f1.read())
#
# f1.close()

# 写内容
# f2 = open('./data/2.txt','a+',encoding='utf-8')
#
# f2.write('11111')
# f2.seek(0)
# print(f2.read())
#
# f2.close()


# 复制文件
old_name = './data/2.txt'

point = old_name.rindex('.')
first_name = old_name[:point]
print(first_name)
last_name = old_name[point:]
new_name = first_name + '-副本' + last_name
print(new_name)



f_src = open(old_name,'r',encoding='utf-8')
f_dest = open(new_name,'w',encoding='utf-8')


data = f_src.read()
f_dest.write(data)

f_src.close()
f_dest.close()



with open('1.txt','r',encoding='utf-8') as f1:
    print(f1.read())


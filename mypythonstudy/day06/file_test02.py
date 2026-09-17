# 二进制读写 -- 文件

# with open('./data/22.gif','rb') as f_src , open('./data/22-copy.png','wb') as f_desc:
#     while True:
#         data = f_src.read(2048)
#
#         if len(data) <= 0:
#             break
#
#         f_desc.write(data)


#
with open('./data/2.txt','r',encoding='utf-8') as f_old:
    str_list = f_old.readlines()
    print(str_list)
    new_list = []
    for str1 in str_list:
        new_str = str1.strip()
        print(new_str)
        new_list.append(new_str[::-1] + '\n')

print(new_list)

with open('./data/222.txt','w',encoding='utf-8') as f_dest:
    f_dest.writelines(new_list)
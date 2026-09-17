# 推导式
# list: 1-10
list1 = [i for i in range(1,11)]
print(list1)


#set
set1 = {i for i in range(1,11)}
print(set1)


# k : v
dict1 = {i : i+1 for i in range(1,11)}
print(dict1)




list2 = [i for i in range(1,11) if i % 2 == 0]
print(list2)


#set
set2 = {i for i in range(1,11) if i % 2 == 0}
print(set2)


# k : v
dict2 = {i : i+1 for i in range(1,11) if i % 2 == 0}
print(dict2)
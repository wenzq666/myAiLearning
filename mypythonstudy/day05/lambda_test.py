# lambda
fn1 = lambda x,y,z=10: x+y+z
print(fn1(4, 6))


# 三目运算  if  else
fn2 = lambda a , b : a if a > b else b
print(fn2(4, 6))



list1 = [5,9,5,6,3,2,4,7]
list1.sort()
print(list1)
list1.sort(reverse=True)
print(list1)

students = [
    {'name': 'Tom', 'age': 20},
    {'name': 'Rose', 'age': 19},
    {'name': 'Jack', 'age': 22}
]

students.sort(key=lambda x:x['age'],reverse=True)

print(students)























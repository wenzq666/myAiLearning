import pymysql

#  创建lianjie
conn = pymysql.Connection(
    host='192.168.88.128',
    port=3306,
    user='root',
    password='123456',
    database='my_tes_db'
)

# 实例化游标对象
cur = conn.cursor()


rows = cur.execute("select name from products")

print("影响行数 ",rows)

datas = cur.fetchall()
print(datas)

cur.close()
conn.close()






















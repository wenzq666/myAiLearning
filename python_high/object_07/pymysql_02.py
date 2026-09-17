"""
事务是一组不可分割的 SQL 操作集合，要么全部成功，要么全部失败回滚。
增删改操作一定要手动设置事务, 一般为了方便记忆, 增删改查都开启事务
开始事务: conn.begin()
提交事务: conn.commit()  事务一旦提交不能回滚
回滚事务: conn.rollback()  执行的sql一旦报错, 会将缓存区的sql清空
事务应用场景: 转账 订单数据
"""
import pymysql

conn = pymysql.Connection(
    host='192.168.88.128',
    port=3306,
    user='root',
    password='123456',
    database='my_tes_db'
)

cur = conn.cursor()

try:
    # todo:1-开始事务
    conn.begin()
    # 增加数据
    # sql = """insert into goods values (null,'iphone17','手机','苹果',6999,1,0);"""
    # cur.execute(query=sql)
    # 删除数据
    # cur.execute(query="delete from goods where id=28;")
    # 更新数据
    cur.execute(query="update goods set price=6888 where id=24;")
    # todo:2-提交事务
    conn.commit()

except Exception as e:
    print(e)
    # todo:3-回滚事务
    conn.rollback()

############## 以下代码是演示事务的作用 ##############
# cur.execute('insert into goods(name, cate_name, brand_name) values ("测试222", "测试222", "测试222");')
# conn.commit()
############## 以上代码是演示事务的作用 ##############


cur.close()
conn.close()
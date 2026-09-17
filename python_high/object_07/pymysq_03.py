"""
需求: 获取登录界面(input)用户输入的账号和密码, 和数据库用户表真实的账号和密码进行匹配, 匹配成功显示登录成功, 否则显示登录失败
① 获取用户前端界面输入的账号和密码
② 将获取的账号和密码 传入到 sql语句中  where user=账号 and pwd=密码
③ 基于查询结果 row 进行判断 是否登录成功

sql注入: 攻击者将恶意sql代码插入应用程序的输入中, 使数据库执行非预期的操作
如何解决sql注入问题:
1.%s进行占位
2.cur.execute(query=, args=(变量1, 变量2, ...))
"""
import pymysql

print(True and False or True or False)  # 返回True

# ① 获取用户前端界面输入的账号和密码
username = input('请输入账号: ')
password = input('请输入密码: ')

with pymysql.connect(host='192.168.88.128',
                    port=3306,
                    user='root',
                    password='123456',
                    database='my_tes_db') as conn:
    with conn.cursor() as cur:
        # ② 将获取的账号和密码 传入到 sql语句中  where user=账号 and pwd=密码
        # 密码输入: ' or 1=1 or '  拼接到  and pwd = '' 中 -> '' or 1=1 or ''
        # select * from user where user = 'root' and pwd = '' or 1=1 or '';
        # print(True and False or True or False)  # 返回True
        # sql注入:
        # sql = f"""
        # select *
        # from
        #     user
        # where
        #     user = '{username}'
        # and pwd = '{password}';
        # """

        # 防止sql注入问题
        # 当前%s不是字符串的格式化输出字符串类型占位符, 是MySQL中的占位符(不限制数据类型)
        sql = """
                select *
                from
                    user
                where
                    user = %s
                and pwd = %s;
                """
        # row = cur.execute(query=sql, args=(username, password))
        row = cur.execute(query=sql, args=[username, password])
        print(f'影响行数: {row}')


# ③ 基于查询结果 row 进行判断 是否登录成功
if row == 1:
    print('登录成功')
else:
    print('登录失败')

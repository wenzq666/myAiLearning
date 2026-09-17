"""
装饰器
"""


def outer_login(func):
    def inner_login():
        print("登录....")
        func()
    return inner_login



def comment():
    print("开始评论...")


comment = outer_login(comment)
comment()




# 装饰器

def check_login(fn_name):

    def fn_inner():
        print('装饰增强功能')

        fn_name()

    return fn_inner



def comment():
    print('发表评论')

def payment():
    print('充值')

# 测试调用
comment = check_login(comment)
comment()





def chek_factory(phone, password):
    def check_phone(func):
        print(check_phone.__closure__[0].cell_contents)
        print(check_phone.__closure__[1].cell_contents)
        print(check_phone.__closure__[2].cell_contents)
        def inner_check(comt):
            print(inner_check.__closure__)
            if phone == 111 and password == 222:
                print("登录....")
                func(comt)
            else:
                print('登录失败')
        return inner_check
    return check_phone

def check_code(func):
    def inner_check_code(comt):
        print("验证码....")
        func(comt)
    return inner_check_code


@chek_factory(phone=111, password=222)
@check_code
def comment(comt):
    print(comt)


#comment = check_code(comment)
#comment = check_phone(comment,111,222)
comment("我在评论...")










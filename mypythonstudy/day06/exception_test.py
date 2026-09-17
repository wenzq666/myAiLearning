# 异常
try:
    # 尝试执行有可能出问题的代码
    print(1)

except Exception as e:
    # 捕获到异常执行的
    print('有异常')
    print(e)
else:
    print('pass')
finally:
    print('finally')












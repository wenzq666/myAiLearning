# 开发程序：购物车功能。
# 已知A网站苹果和橘子两种水果单价(具体如下)，用户根据自己的需求输入斤数， 系统计算总价并打印结果。
# 水果单价
apple_price = 6.6
orange_price = 5

apple_weight = input(f"苹果的单价是{apple_price}元/Kg,请输入要购买的苹果斤数：")
orange_weight = input(f"橘子的单价是{orange_price}元/Kg,请输入要购买的橘子斤数：")

try:
    apple_weight = float(apple_weight)
    orange_weight = float(orange_weight)
    # 计算苹果的总价
    if apple_weight > 0 and orange_weight > 0:
        apple_total_price = apple_weight * apple_price
        orange_total_price = orange_weight * orange_price
        print(f"苹果的单价是{apple_price}元/Kg,"
              f"购买的斤数是{apple_weight}Kg,总价是{apple_total_price:.2f}元")
        print(f"橘子的单价是{orange_price}元/Kg,"
              f"购买的斤数是{orange_weight}Kg,总价是{orange_total_price:.2f}元")
        print(f'购买的总价是：{apple_total_price + orange_total_price:.2f}元')
    else:
        print("输入的斤数有误!")
except ValueError:
    print("输入的斤数有误!!")

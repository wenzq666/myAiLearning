class SweetPotato():

    # 初始化定义
    def __init__(self,cooked_state,cooking_time,seasoning):
        self.cooked_state = cooked_state
        self.cooking_time = cooking_time
        self.seasoning = seasoning

    # 烤地瓜
    def cooking(self,cooking_time):
        self.cooking_time += cooking_time
        if 0 < self.cooking_time <= 3:
            self.cooked_state = '生的'
        elif 3 < self.cooking_time <= 7:
            self.cooked_state = '半生不熟'
        elif 7 < self.cooking_time <= 12:
            self.cooked_state = '熟了'
        elif 12 < self.cooking_time:
            self.cooked_state = '烤糊了'

    # 添加调料
    def add_seasoning(self,*seasoning):
        for i in seasoning:
            self.seasoning.append(i)


    def __str__(self):
        return f"地瓜烤了{self.cooking_time}分钟,状态{self.cooked_state},当前添加了{self.seasoning}"

# 烤地瓜
sp = SweetPotato("生的",0,['糖精','蜂蜜'])
sp.cooking(5)
print(sp)

sp.cooking(3)
sp.add_seasoning('爆米花','1')
print(sp)






















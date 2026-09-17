# 定义手机类
class Phone:

    # 开机
    def turn_on(self):
        print("手机开机")

    # 关机
    def turn_off(self):
        print("手机关机")

    # 拍照
    def take_photo(self):
        print("手机拍照")

# 定义对象
phone = Phone()
phone.turn_on()
phone.take_photo()
phone.turn_off()
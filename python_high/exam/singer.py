#定义一个singer类(歌手类)，
# 包含初始化init方法：
# 成员属性: 歌曲名 歌手名字
# 成员方法：fans()：打印“XXX歌手的YYY歌曲持续打榜，粉丝为喜欢的歌手打call” XXX为对象的歌手名字，YYY为对象的歌曲名。
class Singer:
    def __init__(self, song_name, singer_name):
        self.song_name = song_name
        self.singer_name = singer_name

    def fans(self):
        print(f"{self.singer_name}的{self.song_name}歌曲持续打榜，粉丝为喜欢的歌手打call")


#1）通过程序逐行读取singer.txt文件内容，根据每行数据创建对应歌手对象并赋值，依次将歌手对象存入列表。
with open("singer.txt", "r", encoding="utf-8") as f:
    singer_list = []
    for line in f:
        line = line.strip()
        song_name, singer_name = line.split("，")
        singer = Singer(song_name, singer_name)
        singer_list.append(singer)

#2）遍历列表，获取元素并调用对象的fans方法
for singer in singer_list:
    singer.fans()




















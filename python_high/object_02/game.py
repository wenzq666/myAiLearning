class Game:
    top_score = 0

    @classmethod
    def show_all_score(cls):
        print(cls.top_score)


    def __init__(self,name):
        self.name = name

    @staticmethod
    def show_help():
        print("游戏帮助")


    def start_game(self):
        print(f"玩家{self.name}:游戏开始")
        Game.top_score += 10



if __name__ == '__main__':

    Game.show_help()
    Game.show_all_score()
    game = Game("player1")
    game.start_game()
    Game.show_all_score()
class Tool:
    count = 0

    @classmethod
    def show_total(cls):
        print(cls.count)

    def __init__(self):
        Tool.count += 1

if __name__ == '__main__':
    tool1 = Tool()
    tool2 = Tool()
    tool3 = Tool()

    Tool.show_total()
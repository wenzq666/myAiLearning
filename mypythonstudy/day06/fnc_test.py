a = 2

__all__ = ['fun1']

def fun1(b):
    print(f'fun1{b}{a}')


def fun2():
    print('fun2')


def fun3():
    print('fun3')

fun2()
print(__name__)

if __name__ == '__main__':
    fun1()
def say_hello(country):
    def wrapper(func):
        def deco(*args, **kwargs):
            if country == 'china':
                print('你好！')
            elif country == 'america':
                print('hello')
            else:
                return
            func(*args, **kwargs)
        return deco
    return wrapper

def say(func):
    def deco(*args, **kwargs):
        func(*args, **kwargs)
        return
    return deco

@say_hello('china')
def chinese(str):
    print(str)


@say_hello('america')
def america(str):
    print(str)

@say
def earth(str):
    print(str)

america('I am from America.')
print('-'*20)
chinese('我来自中国。')
print('-'*20)
earth("我来自地球")
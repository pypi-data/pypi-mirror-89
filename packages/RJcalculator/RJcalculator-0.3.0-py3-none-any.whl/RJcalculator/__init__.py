# class Operations:

def add(*x):
    result = 0
    for i in x:
        result = result + i
    return result

def subtract(x, y):
    return x - y

def multiply(*x):
    result = 1
    for i in x:
        result = result * i
    return result

def divide(x, y):
    return x / y

def power(x, y):
    return x // y

def remainder(x, y):
    return x % y

def percent(x, y):
    return x/100 * y




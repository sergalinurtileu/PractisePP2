#1 
def square(x):
    return x * x

#2 
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

#3
def format_name(first, last):
    return f"{last}, {first}"

#4
def is_even(n):
    return n % 2 == 0

#5 
def multiples(n, count):
    return [n * i for i in range(1, count + 1)]
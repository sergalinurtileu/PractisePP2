def square_gen(N):
    for i in range(N + 1):
        yield i * i

for x in square_gen(5):
    print(x)

def even_gen(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())

print(",".join(str(x) for x in even_gen(n)))

def div_gen(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

for x in div_gen(100):
    print(x)

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for x in squares(3, 7):
    print(x)


def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for x in countdown(5):
    print(x)
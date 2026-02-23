import math

degree = float(input())
radian = degree * math.pi / 180

print(radian)



height = float(input())
a = float(input())
b = float(input())

area = (a + b) / 2 * height
print(area)


import math

n = int(input())
a = float(input())

area = (n * a * a) / (4 * math.tan(math.pi / n))
print(round(area, 2))


base = float(input())
height = float(input())

area = base * height
print(float(area))
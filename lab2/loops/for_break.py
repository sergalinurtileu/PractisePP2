#1 
i = 1
while True:
    if i == 5:
        break
    print(i)
    i += 1

#2 
while True:
    word = input("Enter word: ")
    if word == "stop":
        break

#3 
i = 0
while True:
    if i % 2 == 0:
        print("First even:", i)
        break
    i += 2

#4 
s = 0
i = 1
while True:
    s += i
    if s >= 100:
        break
    i += 1
print("Sum =", s)

#5 
while True:
    n = int(input("Enter number: "))
    if n < 0:
        break
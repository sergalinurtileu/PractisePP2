#1 Skip even numbers
for i in range(1, 8):
    if i % 2 == 0:
        continue
    print(i)

#2 Skip empty strings
for s in ["hi", " ", "hello", ""]:
    if s == " ":
        continue
    print(s)

#3 Skip numbers less than 3
for i in range(5):
    if i < 3:
        continue
    print(i)

#4 Skip negative numbers
nums = [3, 0, 5, -2, 10]
for n in nums:
    if n < 0:
        continue
    print(n)

#5 Skip short words
for word in ["mers", "house", "bmw", "school"]:
    if len(word) < 4:
        continue
    print(word)
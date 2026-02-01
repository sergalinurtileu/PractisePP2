#1 
for i in range(1, 9):
    if i % 2 == 0:
        continue
    print(i)

#2 
for i in ["hi", "", "hello", ""]:
    if i == "":
        continue
    print(i)

#3 
for i in range(10):
    if i < 3:
        continue
    print(i)

#4 
nums = [3, 0, 4, -2, 8]
for n in nums:
    if n < 0:
        continue
    print(n)

#5 
for word in ["dog", "Abai", "Kbtu", "school"]:
    if len(word) < 4:
        continue
    print(word)
#1
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  

#2
words = ["Kazakh", "lit", "education", "AI"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)  

#3
nums = [-3, -1, 0, 2, 5]
positives = list(filter(lambda x: x > 0, nums))
print(positives)  

#4 
names = ["Bekzat", "Aruzhan", "Bota", "Dias"]
b_names = list(filter(lambda n: n.startswith("B"), names))
print(b_names)  

#5 
nums = [3, 6, 7, 9, 10, 12]
div_by_three = list(filter(lambda x: x % 3 == 0, nums))
print(div_by_three)  
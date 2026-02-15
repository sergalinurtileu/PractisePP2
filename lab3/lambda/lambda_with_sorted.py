#1 
words = ["Kazakh", "literature", "AI", "global"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words) 

#2
nums = [-10, 5, -3, 2, -1]
sorted_abs = sorted(nums, key=lambda x: abs(x))
print(sorted_abs)  

#3 
pairs = [(1, 3), (2, 1), (4, 2)]
sorted_pairs = sorted(pairs, key=lambda p: p[1])
print(sorted_pairs) 

#4 
names = ["Bekzat", "Aruzhan", "Dias", "Bota"]
sorted_names = sorted(names, key=lambda n: n[-1])
print(sorted_names)  

#5 
scores = {"Bekzat": 90, "Aruzhan": 75, "Dias": 85}
sorted_scores = sorted(scores.items(), key=lambda item: item[1])
print(sorted_scores) 
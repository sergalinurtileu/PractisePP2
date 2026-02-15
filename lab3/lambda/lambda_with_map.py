#1 
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))
print(squares)  

#2 
words = ["kazakh", "literature", "globalisation"]
upper_words = list(map(lambda w: w.upper(), words))
print(upper_words)  

#3 
nums = [5, 10, 15]
plus_ten = list(map(lambda x: x + 10, nums))
print(plus_ten)  

#4 
words = ["Bekzat", "Akhmetov", "Python"]
lengths = list(map(lambda w: len(w), words))
print(lengths)  

#5 
nums = [2, 4, 6]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)  
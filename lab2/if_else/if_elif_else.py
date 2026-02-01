#1 
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")

#2 
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

#3 
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")

#4 
score = int(input("Enter your score: "))

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")


#5
day=input("Enter a day of the week:")
if day.lower=="monday":
   print("Start of the week")
elif day.lower=="wednesday":
   print("midweek day")
elif day.lower=="thursday":
   print("midweek day")
elif day.lower=="tuesday":
   print("midweek day")
elif day.lower=="friday":
   print("midweek day")
elif day.lower=="saturday":
   print("midweek day")
elif day.lower=="sunday":
   print("midweek day")
else:
   print("Error")
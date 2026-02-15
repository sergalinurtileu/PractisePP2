#1 
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    pass

d = Dog()
d.speak()

#2
class Bird(Animal):
    def fly(self):
        print("Bird flies")

b = Bird()
b.speak()
b.fly()

#3 
class Vehicle:
    wheels = 4

class Bike(Vehicle):
    wheels = 2

print(Bike().wheels)

#4 
class Person:
    def greet(self):
        print("Hello!")

class Student(Person):
    def study(self):
        print("Studying...")

s = Student()
s.greet()
s.study()

#5 
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    pass

c = Child("Aya")
print(c.name)
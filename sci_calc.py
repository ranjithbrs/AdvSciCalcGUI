import math

def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b    

def multiplication(a, b):
    return a * b    

def division(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a / b

def power(a, b):
    return a ** b

def square_root(a):
    if a < 0:
        return "Error: Negative value."
    return round(math.sqrt(a), 6)

def modulus(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a % b

def logarithm(a, base):
    if a <= 0 or base <= 1:
        return "Error: Invalid input."
    return round(math.log(a, base), 6)

def factorial(n):
    if n < 0:
        return "Error: Negative value."
    return math.factorial(n)   

def floor_division(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a // b   

def sine(angle):
    return round(math.sin(math.radians(angle)), 6)    

def cosine(angle):
    return round(math.cos(math.radians(angle)), 6)

def tangent(angle):
    if angle % 180 == 90:
        return "Error: Undefined."
    return round(math.tan(math.radians(angle)), 6)

def exponential(a):
    try:
        return round(math.exp(a), 6)
    except OverflowError:
        return "Error: Overflow."

def sec(angle):
    cos_value = cosine(angle)
    if abs(cos_value) < 1e-15:
        return "Error: Undefined."
    return round(1 / cos_value, 6)

def cosec(angle):
    sin_value = sine(angle)
    if abs(sin_value) < 1e-15:
        return "Error: Undefined."
    return round(1 / sin_value, 6)

def cot(angle):   
    tan_value = tangent(angle)
    if tan_value == "Error: Undefined." or abs(tan_value) < 1e-15:
        return "Error: Undefined."
    return round(1 / tan_value, 6)

print("\nWelcome to the Advanced Calculator!")
print("Select operation:")
print("+. Addition")
print("-. Subtraction")
print("*. Multiplication")
print("/. Division")
print("**. Power")
print("sqrt. Square Root")
print("%. Modulus") 
print("log. Logarithm")
print("!. Factorial")
print("//. Floor Division") 
print("sin. Sine")
print("cos. Cosine")
print("tan. Tangent")
print("exp. Exponential")
print("sec. Secant")
print("cosec. Cosecant")
print("cot. Cotangent")
print("exit. Exit")

while True:
    choice = input("\nEnter choice: ").strip().lower()
    if choice == "exit":
        print("Exiting the calculator. Goodbye!")
        break   

    if choice == "sqrt":
        num = float(input("Enter number: "))
        print("Result:", square_root(num))

    elif choice == "!":
        num = int(input("Enter non-negative integer: "))
        print("Result:", factorial(num))

    elif choice in ["sin", "cos", "tan", "sec", "cosec", "cot"]:
        angle = float(input("Enter angle in degrees: "))
        if choice == "sin":
            print("Result:", sine(angle))
        elif choice == "cos":
            print("Result:", cosine(angle))
        elif choice == "tan":
            print("Result:", tangent(angle))
        elif choice == "sec":
            print("Result:", sec(angle))
        elif choice == "cosec":
            print("Result:", cosec(angle))
        elif choice == "cot":
            print("Result:", cot(angle))

    elif choice == "exp":
        num = float(input("Enter number: "))
        print("Result:", exponential(num))

    else:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if choice == "+":
            print("Result:", addition(num1, num2))
        elif choice == "-":
            print("Result:", subtraction(num1, num2))
        elif choice == "*":
            print("Result:", multiplication(num1, num2))
        elif choice == "/":
            print("Result:", division(num1, num2))
        elif choice == "**":
            print("Result:", power(num1, num2))
        elif choice == "%":
            print("Result:", modulus(num1, num2))
        elif choice == "log":
            print("Result:", logarithm(num1, num2))
        elif choice == "//":
            print("Result:", floor_division(num1, num2))
        else:
            print("Error: Invalid input.")
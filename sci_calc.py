import math
from typing import Union

def addition(a: float, b: float) -> float:
    """Returns sum of a and b."""
    return a + b

def subtraction(a: float, b: float) -> float:
    """Returns difference of a and b."""
    return a - b    

def multiplication(a: float, b: float) -> float:
    """Returns product of a and b."""
    return a * b    

def division(a: float, b: float) -> Union[float, str]:
    """Returns division of a by b."""
    if b == 0:
        return "Error: Division by zero."
    return a / b

def power(a: float, b: float) -> Union[float, str]:
    """Returns a raised to power b."""
    try:
        res = a ** b
        if isinstance(res, complex):
            return "Error: Complex result."
        return res
    except OverflowError:
        return "Error: Overflow."
    except ValueError:
        return "Error: Invalid operation."

def square_root(a: float) -> Union[float, str]:
    """Returns square root of a."""
    if a < 0:
        return "Error: Negative value."
    return round(math.sqrt(a), 6)

def modulus(a: float, b: float) -> Union[float, str]:
    """Returns modulus of a by b."""
    if b == 0:
        return "Error: Division by zero."
    return a % b

def logarithm(a: float, base: float = 10) -> Union[float, str]:
    """Returns log of a with given base (default 10)."""
    if a <= 0 or base <= 0 or base == 1:
        return "Error: Invalid input."
    return round(math.log(a, base), 6)

def natural_log(a: float) -> Union[float, str]:
    """Returns natural logarithm (ln) of a."""
    if a <= 0:
        return "Error: Invalid input."
    return round(math.log(a), 6)

def factorial(n: Union[int, float]) -> Union[int, str]:
    """Returns factorial of non-negative integer n."""
    if n < 0 or not float(n).is_integer():
        return "Error: Invalid input."
    return math.factorial(int(n))   

def floor_division(a: float, b: float) -> Union[float, str]:
    """Returns floor division of a by b."""
    if b == 0:
        return "Error: Division by zero."
    return a // b   

def sine(angle: float, mode: str = "deg") -> float:
    """Returns sine of angle in degrees or radians."""
    rad = angle if mode == "rad" else math.radians(angle)
    return round(math.sin(rad), 6)    

def cosine(angle: float, mode: str = "deg") -> float:
    """Returns cosine of angle in degrees or radians."""
    rad = angle if mode == "rad" else math.radians(angle)
    return round(math.cos(rad), 6)

def tangent(angle: float, mode: str = "deg") -> Union[float, str]:
    """Returns tangent of angle in degrees or radians."""
    rad = angle if mode == "rad" else math.radians(angle)
    cos_val = math.cos(rad)
    if abs(cos_val) < 1e-12:
        return "Error: Undefined."
    return round(math.tan(rad), 6)

def sec(angle: float, mode: str = "deg") -> Union[float, str]:
    """Returns secant of angle in degrees or radians."""
    cos_value = cosine(angle, mode)
    if cos_value == 0 or abs(cos_value) < 1e-12:
        return "Error: Undefined."
    return round(1 / cos_value, 6)

def cosec(angle: float, mode: str = "deg") -> Union[float, str]:
    """Returns cosecant of angle in degrees or radians."""
    sin_value = sine(angle, mode)
    if sin_value == 0 or abs(sin_value) < 1e-12:
        return "Error: Undefined."
    return round(1 / sin_value, 6)

def cot(angle: float, mode: str = "deg") -> Union[float, str]:
    """Returns cotangent of angle in degrees or radians."""
    tan_value = tangent(angle, mode)
    if tan_value == 0 or tan_value == "Error: Undefined." or isinstance(tan_value, str):
        return "Error: Undefined."
    return round(1 / tan_value, 6)

def arcsin(val: float, mode: str = "deg") -> Union[float, str]:
    """Returns arcsine of value in degrees or radians."""
    if val < -1 or val > 1:
        return "Error: Invalid input."
    res_rad = math.asin(val)
    return round(math.degrees(res_rad) if mode == "deg" else res_rad, 6)

def arccos(val: float, mode: str = "deg") -> Union[float, str]:
    """Returns arccosine of value in degrees or radians."""
    if val < -1 or val > 1:
        return "Error: Invalid input."
    res_rad = math.acos(val)
    return round(math.degrees(res_rad) if mode == "deg" else res_rad, 6)

def arctan(val: float, mode: str = "deg") -> Union[float, str]:
    """Returns arctangent of value in degrees or radians."""
    res_rad = math.atan(val)
    return round(math.degrees(res_rad) if mode == "deg" else res_rad, 6)

def exponential(a: float) -> Union[float, str]:
    """Returns e^a."""
    try:
        return round(math.exp(a), 6)
    except OverflowError:
        return "Error: Overflow."

def get_float_input(prompt: str) -> float:
    """Safely prompts the user for a floating point number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Invalid number. Please try again.")

def main():
    print("\nWelcome to the Advanced Calculator CLI!")
    print("Select operation:")
    print("+. Addition")
    print("-. Subtraction")
    print("*. Multiplication")
    print("/. Division")
    print("**. Power")
    print("sqrt. Square Root")
    print("%. Modulus") 
    print("log. Logarithm")
    print("ln. Natural Logarithm")
    print("!. Factorial")
    print("//. Floor Division") 
    print("sin. Sine")
    print("cos. Cosine")
    print("tan. Tangent")
    print("exp. Exponential")
    print("sec. Secant")
    print("cosec. Cosecant")
    print("cot. Cotangent")
    print("asin. Arcsine")
    print("acos. Arccosine")
    print("atan. Arctangent")
    print("exit. Exit")

    single_num_ops = {"sqrt", "exp", "ln"}
    trig_ops = {"sin", "cos", "tan", "sec", "cosec", "cot", "asin", "acos", "atan"}
    two_num_ops = {"+", "-", "*", "/", "**", "%", "log", "//"}

    while True:
        choice = input("\nEnter choice: ").strip().lower()
        if choice == "exit":
            print("Exiting the calculator. Goodbye!")
            break   

        if choice in single_num_ops:
            num = get_float_input("Enter number: ")
            if choice == "sqrt":
                print("Result:", square_root(num))
            elif choice == "exp":
                print("Result:", exponential(num))
            elif choice == "ln":
                print("Result:", natural_log(num))

        elif choice == "!":
            num = get_float_input("Enter non-negative integer: ")
            print("Result:", factorial(num))

        elif choice in trig_ops:
            val = get_float_input("Enter value/angle (in degrees for trig): ")
            if choice == "sin":
                print("Result:", sine(val))
            elif choice == "cos":
                print("Result:", cosine(val))
            elif choice == "tan":
                print("Result:", tangent(val))
            elif choice == "sec":
                print("Result:", sec(val))
            elif choice == "cosec":
                print("Result:", cosec(val))
            elif choice == "cot":
                print("Result:", cot(val))
            elif choice == "asin":
                print("Result:", arcsin(val))
            elif choice == "acos":
                print("Result:", arccos(val))
            elif choice == "atan":
                print("Result:", arctan(val))

        elif choice in two_num_ops:
            num1 = get_float_input("Enter first number: ")
            num2 = get_float_input("Enter second number: ")
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

if __name__ == "__main__":
    main()
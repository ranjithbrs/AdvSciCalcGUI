import unittest
import math
import re
import tkinter as tk
import sci_calc
from sci_calc_gui import ScientificCalculatorGUI, transform_factorials, add_implicit_multiplication

class TestMathematicalOperations(unittest.TestCase):
    """Tests all scientific, arithmetic, and domain operations."""

    def test_basic_arithmetic(self):
        self.assertEqual(sci_calc.addition(5, 3), 8)
        self.assertEqual(sci_calc.subtraction(10, 4), 6)
        self.assertEqual(sci_calc.multiplication(6, 7), 42)
        self.assertEqual(sci_calc.division(20, 5), 4)
        self.assertEqual(sci_calc.power(2, 3), 8)
        self.assertEqual(sci_calc.modulus(10, 3), 1)
        self.assertEqual(sci_calc.floor_division(10, 3), 3)

    def test_arithmetic_invalid_inputs(self):
        self.assertEqual(sci_calc.division(5, 0), "Error: Division by zero.")
        self.assertEqual(sci_calc.modulus(5, 0), "Error: Division by zero.")
        self.assertEqual(sci_calc.floor_division(5, 0), "Error: Division by zero.")
        # Zero to negative power is division by zero
        self.assertEqual(sci_calc.power(0, -1), "Error: Division by zero.")
        self.assertEqual(sci_calc.power(0, -5), "Error: Division by zero.")

    def test_powers_and_roots(self):
        self.assertEqual(sci_calc.power(2, 3), 8)
        self.assertEqual(sci_calc.power(5, 0), 1)
        self.assertEqual(sci_calc.power(0, 5), 0)
        self.assertEqual(sci_calc.square_root(16), 4)
        self.assertEqual(sci_calc.square_root(0), 0)
        self.assertEqual(sci_calc.square_root(-9), "Error: Negative value.")
        self.assertEqual(sci_calc.power(-4, 0.5), "Error: Complex result.")
        self.assertEqual(sci_calc.power(10.0, 1000), "Error: Overflow.")

    def test_logarithms(self):
        self.assertEqual(sci_calc.logarithm(100, 10), 2)
        self.assertEqual(sci_calc.logarithm(8, 2), 3)
        self.assertEqual(sci_calc.logarithm(0.25, 0.5), 2)
        self.assertEqual(sci_calc.natural_log(math.e), 1)
        # Invalid log inputs
        self.assertEqual(sci_calc.logarithm(-5, 10), "Error: Invalid input.")
        self.assertEqual(sci_calc.logarithm(0, 10), "Error: Invalid input.")
        self.assertEqual(sci_calc.logarithm(10, 1), "Error: Invalid input.")
        self.assertEqual(sci_calc.logarithm(10, 0), "Error: Invalid input.")
        self.assertEqual(sci_calc.logarithm(10, -2), "Error: Invalid input.")
        self.assertEqual(sci_calc.natural_log(-1), "Error: Invalid input.")
        self.assertEqual(sci_calc.natural_log(0), "Error: Invalid input.")

    def test_factorial(self):
        self.assertEqual(sci_calc.factorial(5), 120)
        self.assertEqual(sci_calc.factorial(0), 1)
        self.assertEqual(sci_calc.factorial(1), 1)
        # Invalid factorial inputs and limits
        self.assertEqual(sci_calc.factorial(-3), "Error: Invalid input.")
        self.assertEqual(sci_calc.factorial(3.5), "Error: Invalid input.")
        self.assertEqual(sci_calc.factorial(5000), "Error: Overflow.")

    def test_trigonometry_deg(self):
        self.assertEqual(sci_calc.sine(0, mode="deg"), 0)
        self.assertEqual(sci_calc.sine(90, mode="deg"), 1)
        self.assertEqual(sci_calc.cosine(0, mode="deg"), 1)
        self.assertEqual(sci_calc.cosine(90, mode="deg"), 0)
        self.assertEqual(sci_calc.tangent(45, mode="deg"), 1)
        self.assertEqual(sci_calc.tangent(90, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.tangent(270, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.sec(0, mode="deg"), 1)
        self.assertEqual(sci_calc.sec(90, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.cosec(90, mode="deg"), 1)
        self.assertEqual(sci_calc.cosec(0, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.cot(45, mode="deg"), 1)
        self.assertEqual(sci_calc.cot(0, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.cot(90, mode="deg"), 0)

    def test_trigonometry_rad(self):
        self.assertEqual(sci_calc.sine(math.pi / 2, mode="rad"), 1)
        self.assertEqual(sci_calc.cosine(0, mode="rad"), 1)
        self.assertEqual(sci_calc.tangent(math.pi / 4, mode="rad"), 1)

    def test_inverse_trig(self):
        self.assertEqual(sci_calc.arcsin(0, mode="deg"), 0)
        self.assertEqual(sci_calc.arcsin(1, mode="deg"), 90)
        self.assertEqual(sci_calc.arccos(1, mode="deg"), 0)
        self.assertEqual(sci_calc.arccos(0, mode="deg"), 90)
        self.assertEqual(sci_calc.arctan(1, mode="deg"), 45)
        # Domain errors outside [-1, 1]
        self.assertEqual(sci_calc.arcsin(2, mode="deg"), "Error: Invalid input.")
        self.assertEqual(sci_calc.arcsin(-1.5, mode="deg"), "Error: Invalid input.")
        self.assertEqual(sci_calc.arccos(1.01, mode="deg"), "Error: Invalid input.")

    def test_exponential(self):
        self.assertEqual(sci_calc.exponential(0), 1)
        self.assertEqual(sci_calc.exponential(1), round(math.e, 6))
        self.assertEqual(sci_calc.exponential(1000), "Error: Overflow.")

    def test_factorial_parsing_and_nested_parens(self):
        self.assertEqual(transform_factorials("5!"), "fact(5)")
        self.assertEqual(transform_factorials("(3+2)!"), "fact((3+2))")
        self.assertEqual(transform_factorials("((3))!"), "fact(((3)))")
        self.assertEqual(transform_factorials("(sin(90)+1)!"), "fact((sin(90)+1))")
        self.assertEqual(transform_factorials("3! + 4!"), "fact(3) + fact(4)")

    def test_implicit_multiplication(self):
        self.assertEqual(add_implicit_multiplication("2pi"), "2*pi")
        self.assertEqual(add_implicit_multiplication("2(5)"), "2*(5)")
        self.assertEqual(add_implicit_multiplication("(2+3)(4+5)"), "(2+3)*(4+5)")


class TestCLIGUIAgreement(unittest.TestCase):
    """Verifies CLI functions and GUI evaluation engine compute the exact same results."""

    def setUp(self):
        self.root = tk.Tk()
        self.app = ScientificCalculatorGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_arithmetic_agreement(self):
        self.app.set_display_text("15 + 25")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.addition(15, 25))

        self.app.set_display_text("50 - 18")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.subtraction(50, 18))

        self.app.set_display_text("7 * 8")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.multiplication(7, 8))

        self.app.set_display_text("84 / 4")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.division(84, 4))

        self.app.set_display_text("17 % 5")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.modulus(17, 5))

        self.app.set_display_text("2 ^ 5")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.power(2, 5))

    def test_scientific_agreement(self):
        self.app.set_display_text("sqrt(144)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.square_root(144))

        self.app.set_display_text("5!")
        self.app.evaluate()
        self.assertEqual(int(self.app.get_display_text()), sci_calc.factorial(5))

        self.app.set_display_text("log(100)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.logarithm(100, 10))

        self.app.set_display_text("ln(e)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.natural_log(math.e))

        self.app.set_angle_mode("deg")
        self.app.set_display_text("sin(90)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.sine(90, mode="deg"))

        self.app.set_display_text("cos(0)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.cosine(0, mode="deg"))

        self.app.set_display_text("tan(45)")
        self.app.evaluate()
        self.assertEqual(float(self.app.get_display_text()), sci_calc.tangent(45, mode="deg"))

    def test_gui_specific_features(self):
        # x^2 button from default "0" should produce 0, not SyntaxError
        self.app.all_clear()
        self.app.add_symbol("^2")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), "0")

        # Nested factorial
        self.app.set_display_text("((3))!")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), "6")

        # Implicit multiplication
        self.app.set_display_text("2(5)")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), "10")

        # Fresh calculation starting with digit replaces previous result
        self.app.set_display_text("4 + 6")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), "10")
        self.app.add_symbol("5")
        self.assertEqual(self.app.get_display_text(), "5")

        # Chaining operator retains previous result
        self.app.set_display_text("4 + 6")
        self.app.evaluate()
        self.app.add_symbol("+")
        self.assertEqual(self.app.get_display_text(), "10+")

    def test_error_handling_agreement(self):
        self.app.set_display_text("10 / 0")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), sci_calc.division(10, 0))

        self.app.set_display_text("sqrt(-9)")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), sci_calc.square_root(-9))

        self.app.set_display_text("(-5)!")
        self.app.evaluate()
        self.assertEqual(self.app.get_display_text(), sci_calc.factorial(-5))

if __name__ == "__main__":
    unittest.main()

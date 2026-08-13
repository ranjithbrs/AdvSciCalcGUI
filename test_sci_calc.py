import unittest
import math
import sci_calc

class TestSciCalc(unittest.TestCase):

    def test_basic_arithmetic(self):
        self.assertEqual(sci_calc.addition(5, 3), 8)
        self.assertEqual(sci_calc.subtraction(10, 4), 6)
        self.assertEqual(sci_calc.multiplication(6, 7), 42)
        self.assertEqual(sci_calc.division(20, 5), 4)
        self.assertEqual(sci_calc.division(5, 0), "Error: Division by zero.")

    def test_powers_and_roots(self):
        self.assertEqual(sci_calc.power(2, 3), 8)
        self.assertEqual(sci_calc.square_root(16), 4)
        self.assertEqual(sci_calc.square_root(-9), "Error: Negative value.")

    def test_modulus_and_floor_div(self):
        self.assertEqual(sci_calc.modulus(10, 3), 1)
        self.assertEqual(sci_calc.modulus(5, 0), "Error: Division by zero.")
        self.assertEqual(sci_calc.floor_division(10, 3), 3)
        self.assertEqual(sci_calc.floor_division(5, 0), "Error: Division by zero.")

    def test_logarithms(self):
        self.assertEqual(sci_calc.logarithm(100, 10), 2)
        self.assertEqual(sci_calc.natural_log(math.e), 1)
        self.assertEqual(sci_calc.logarithm(-5, 10), "Error: Invalid input.")
        self.assertEqual(sci_calc.logarithm(10, 1), "Error: Invalid input.")

    def test_factorial(self):
        self.assertEqual(sci_calc.factorial(5), 120)
        self.assertEqual(sci_calc.factorial(0), 1)
        self.assertEqual(sci_calc.factorial(-3), "Error: Invalid input.")

    def test_trigonometry_deg(self):
        self.assertEqual(sci_calc.sine(90, mode="deg"), 1)
        self.assertEqual(sci_calc.cosine(0, mode="deg"), 1)
        self.assertEqual(sci_calc.tangent(45, mode="deg"), 1)
        self.assertEqual(sci_calc.tangent(90, mode="deg"), "Error: Undefined.")
        self.assertEqual(sci_calc.sec(0, mode="deg"), 1)
        self.assertEqual(sci_calc.cosec(90, mode="deg"), 1)
        self.assertEqual(sci_calc.cot(45, mode="deg"), 1)

    def test_inverse_trig(self):
        self.assertEqual(sci_calc.arcsin(1, mode="deg"), 90)
        self.assertEqual(sci_calc.arccos(1, mode="deg"), 0)
        self.assertEqual(sci_calc.arctan(1, mode="deg"), 45)
        self.assertEqual(sci_calc.arcsin(2, mode="deg"), "Error: Invalid input.")

if __name__ == "__main__":
    unittest.main()

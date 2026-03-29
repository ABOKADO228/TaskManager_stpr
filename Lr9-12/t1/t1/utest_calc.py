import unittest
from calc import Calculator 

class CalcTest(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        result = self.calculator.makeOperation(self.calculator._add, 1, 2)
        self.assertEqual(result, 3)
         
    def test_sub(self):
        result = self.calculator.makeOperation(self.calculator._sub, 4, 2)
        self.assertEqual(result, 2)

    def test_mul(self):
        result = self.calculator.makeOperation(self.calculator._mul, 2, 5)
        self.assertEqual(result, 10)

    def test_div(self):
        result = self.calculator.makeOperation(self.calculator._div, 8, 4)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()

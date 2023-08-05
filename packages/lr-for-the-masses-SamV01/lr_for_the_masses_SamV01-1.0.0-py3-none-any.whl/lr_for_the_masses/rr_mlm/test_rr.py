import unittest
import rr
class Testrr(unittest.TestCase):

# Each test class should have at least two test cases and each test case should contain at least four assertion statements.

    def test_summarylin(self):
        A3 = [[0, 0], [1, 1], [2, 2]]
        A4 = [0, 1, 2]
        self.assertEqual(str( type(rr.ridgelinreg(A3,A4, alpha1 = 0)) ), "<class 'rr.ridgelinreg'>")
        self.assertEqual(str( type(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin()) ), "<class 'NoneType'>")
        self.assertEqual(str( type(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_fit())), "<class 'sklearn.linear_model._ridge.Ridge'>")
        self.assertEqual(str( type(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_alpha())), "<class 'sklearn.linear_model._ridge.Ridge'>")

unittest.main(argv=[''], verbosity=2, exit=False)

class Testrr_2(unittest.TestCase):

# Each test class should have at least two test cases and each test case should contain at least four assertion statements.

    def test_summarylin(self):
        A3 = [[0, 0], [1, 1], [2, 2]]
        A4 = [0, 1, 2]
        self.assertAlmostEqual(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_fit().coef_[0], 0.4,2)
        self.assertAlmostEqual(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_fit().coef_[1], 0.4,2)
        self.assertAlmostEqual(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_fit().intercept_, 0.2,2)
        self.assertEqual(rr.ridgelinreg(A3,A4, alpha1 = 0).testridgelin_fit().n_iter_, None)

unittest.main(argv=[''], verbosity=2, exit=False)
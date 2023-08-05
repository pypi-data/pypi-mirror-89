import unittest
import mlm
class Testmlm(unittest.TestCase):

# Each test class should have at least two test cases and each test case should contain at least four assertion statements.

    def test_summarylin(self):
        A = [1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10]
        B = [5, 6, 8, 9, 16, 29, 14, 16, 19, 25]
        C = ["1","1","1","1","1","1","2","2","2","2"]
        self.assertEqual(str( type(mlm.linearmixedeffects(A,B,C)) ), "<class 'mlm.linearmixedeffects'>")
        self.assertEqual(str( type(mlm.linearmixedeffects(A,B,C).summarymlm()) ), "<class 'statsmodels.iolib.summary2.Summary'>")
        self.assertEqual(mlm.linearmixedeffects(A,B,C).fitmlm().fe_params[0], 0.2)
        self.assertEqual(str( type(mlm.linearmixedeffects(A,B,C).fitmlm().model) ), "<class 'statsmodels.regression.mixed_linear_model.MixedLM'>")

unittest.main(argv=[''], verbosity=2, exit=False)

class Testmlm_2(unittest.TestCase):

# Each test class should have at least two test cases and each test case should contain at least four assertion statements.

    def test_summarylin(self):
        A = [1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10]
        B = [5, 6, 8, 9, 16, 29, 14, 16, 19, 25]
        C = ["1","1","1","1","1","1","2","2","2","2"]
        self.assertTrue(mlm.linearmixedeffects(A,B,C).fitmlm().cov_re["Group Var"][0] == 0)
        self.assertTrue(pd.isnull(mlm.linearmixedeffects(A,B,C).fitmlm().normalized_cov_params[0][0]))
        self.assertTrue(pd.isnull(mlm.linearmixedeffects(A,B,C).fitmlm().bse_fe[0]))
        self.assertTrue(pd.isnull(mlm.linearmixedeffects(A,B,C).fitmlm().bse_re[0]))

unittest.main(argv=[''], verbosity=2, exit=False)
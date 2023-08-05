import scipy
import matplotlib
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sklearn as skl
from sklearn import linear_model


class mullin:
    A3 = [[0, 0], [1, 1], [2, 2]]
    A4 = [0, 1, 2]

    def __init__(self, predictor_vec = A3, response = A4):
        self.predictor_vec = predictor_vec
        self.response= response 
        
    def summary_mullin(self):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        regr.fit(self.predictor_vec, self.response)
        print("The coefficients for multiple linear regression are: ")
        print(regr.coef_)
        print("The intercept for multiple linear regression is: ")
        print(round(regr.intercept_))
        print('The fitted model is of the form Y = "{:2f}" + "{:2f}"*x1 + "{:2f}"*x2'.format(regr.intercept_,regr.coef_[0], regr.coef_[1], ))
    
    def summary_mul1(self):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        regr.fit(self.predictor_vec, self.response)
        return regr.coef_
    
    def summary_mul2(self):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        regr.fit(self.predictor_vec, self.response)
        return regr.intercept_
    
    def diag_Rval(self):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        regr.fit(self.predictor_vec, self.response)
        regr1 = regr.score(self.predictor_vec, self.response)
        print('The R2 value of the model is "{}" '.format(regr1))
        print('The current model explains "{}" % of the data: '.format(regr1*100))
        return regr1*100
    
    def test_diag1(self):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        regr.fit(self.predictor_vec, self.response)
        regr1 = regr.score(self.predictor_vec, self.response)
        return regr1*100
    
    def test_diag2(self):
        from sklearn import linear_model
        return regr


# # +
# A3 = [[0, 0], [1, 1], [2, 2]]
# A4 = [0, 1, 2]

# P3 = mullin(A3,A4)
# print(P3.summary_mul1()[0])
# print(P3.summary_mul1()[1])
# print(P3.summary_mul2())
# print(str(type(P3.summary_mul1())))
# # print(str(type(P3.summary_mul1[0]())))
# # print(str(type(P3.summary_mul1[1]())))
# # print(str(type(P3.summary_mul2())))

# P4 = mullin(A3,A4)

# print(P4.test_diag1())


# import unittest



# class Testmlr(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         print('setupClass')

    
#     def setUp(self):
#         self.p4 = mullin(A3,A4)
#         self.p5 = mullin(A3,A4)

#         print('set Up')

#     def test_setlin(self): # test routine
#         p4 = mullin(A3,A4)
#         self.assertEqual(round(p4.summary_mul1()[0],2),0.5)
#         self.assertEqual(str(type(p4.summary_mul1())),str("""<class 'numpy.ndarray'>"""))
#         self.assertEqual(round(p4.summary_mul1()[1],2),0.5)
#         self.assertEqual(str(type(p4.summary_mul1()[1])),str("""<class 'numpy.float64'>"""))

#     def test_setlin2(self): # test routine
#         p5 = mullin(A3,A4)
#         self.assertEqual(round(p5.summary_mul2(),2),0)
#         self.assertEqual(str(type(p5.summary_mul2())),str("""<class 'numpy.float64'>"""))
#         self.assertEqual(round(p5.test_diag1(),2),100)
#         self.assertEqual(str(type(p5.test_diag1())),str("""<class 'numpy.float64'>"""))
        

#     def tearDown(self): # Setting up for the test
#         print('Tear Down')
        
#     @classmethod
#     def tearDownClass(cls):
#         print('teardownClass')
        
# unittest.main(argv=[''], verbosity=2, exit=False)


# -



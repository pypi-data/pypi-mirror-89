# +
import uncertainties.unumpy as unp
import uncertainties as unc
import scipy
import matplotlib
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sklearn as skl
from sklearn import linear_model


class simlin:
    def __init__(self, predictor, response, slope =0 , intercept =0, r_val =0, p_val =0, std_err =0):
        self.predictor= predictor
        self.response= response
        self.slope = slope
        self.intercept = intercept
        self.r_val = r_val
        self.p_val = p_val
        self.std_err = std_err
        
    def summarylin(self):
        self.slope, self.intercept, self.r_val, self.p_val, self.std_err = stats.linregress(self.predictor, self.response)
        print(" ")
        print("The summary of the linear regression model is given below:")
        print("Slope: " + "{:.2f}".format(self.slope) + " Intercept: " + "{:.2f}".format(self.intercept))
        
    def diagnoselin(self):
        self.slope, self.intercept, self.r_val, self.p_val, self.std_err = stats.linregress(self.predictor, self.response)
        print(" ")
        print("The diagnosis of the simple Linear Regression model for the R value, P-value and Std. error is given below:")
        print(" r_val: " + "{:.2f}".format(self.r_val) + " p_val: " + "{:.2f}".format(self.p_val) + " std_err: " + "{:.2f}".format(self.std_err))
        
    def summarylin_test_slope(self):
        self.slope, self.intercept, self.r_val, self.p_val, self.std_err = stats.linregress(self.predictor, self.response)
        return self.slope
    
    def summarylin_test_inctercept(self):
        self.slope, self.intercept, self.r_val, self.p_val, self.std_err = stats.linregress(self.predictor, self.response)
        return self.intercept
    
    def summarylin_test_rval(self):
        self.slope, self.intercept, self.r_val, self.p_val, self.std_err = stats.linregress(self.predictor, self.response)
        return self.r_val
    
    def summarylin_test_pval(self):
        self.slope, self.intercept, self.r_val, self.p_val, std_err = stats.linregress(self.predictor, self.response)
        return self.p_val

# +
class plotlin(simlin): #child class for all regression
    def __init__(self, predictor, response):
        simlin.__init__(self, predictor, response)  #calling super function to inherit all methods of the parent class
    
    def plotoriginaldata(self):
        print(" ")
        print("The following is the original data")
        plt.scatter(self.predictor, self.response, s=3, label='Data')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.legend(loc='best')
        plt.show()
        
    def plotfittedline(self):
        print(" ")
        print("The following is a visual representation of the regression analysis")
        x = np.linspace(max(self.predictor),min(self.predictor))
        plt.scatter(self.predictor, self.response, s=3, label='Data')
        plt.plot(x, self.intercept + self.slope*(x), 'r', label='fitted line')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.legend(loc='best')
        plt.show()
        
    def plottest(self):
        x = np.linspace(max(self.predictor),min(self.predictor))
        return x

    def plotconfidence_intervals(self):
        print(" ")
        print("The following is a visual representation of the regression analysis with confidence intervals")
        sns.set_theme(color_codes=True)
        sns.regplot(x=A, y=B)
        


# +
A = [1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10]
B = [5, 6, 8, 9, 16, 29, 14, 16, 19, 25]
# P1 = simlin(A,B)
# print(round(P1.summarylin_test_slope(),2))
# print(round(P1.summarylin_test_inctercept(),2))
# print(round(P1.summarylin_test_rval(),2))
# print(round(P1.summarylin_test_pval(),2))

P2 = plotlin(A,B)
print(str(type(P2.plotoriginaldata)))
x = np.linspace(10,5)
print(str(type(x)))
        
import unittest



class TestPerson(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('setupClass')

    
    def setUp(self):
        self.p1 = simlin(A,B)
        self.p2 = plotlin(A,B)
        print('set Up')

    def test_set_lin(self): # test routine
        p1 = simlin(A,B)
        self.assertEqual(round(p1.summarylin_test_slope(),2),2.05)
        self.assertEqual(round(p1.summarylin_test_inctercept(),2), 3.4)
        self.assertEqual(round(p1.summarylin_test_rval(),2), 0.77)
        self.assertEqual(round(p1.summarylin_test_pval(),2), 0.01)
        
    def test_plot_lin(self): # test routine
        p2 = plotlin(A,B)
        self.assertEqual(str(type(p2.plotoriginaldata)),str("""<class 'method'>"""))
        self.assertEqual(str(type(p2.plotfittedline)),str("""<class 'method'>"""))
        self.assertEqual(str(type(p2.plotconfidence_intervals)),str("""<class 'method'>"""))
        self.assertNotEqual(str(type(p2.plottest)),str("""<class 'method'>"""))

        
               

    def tearDown(self): # Setting up for the test
        print('Tear Down')
        
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')
        
unittest.main(argv=[''], verbosity=2, exit=False)




# -



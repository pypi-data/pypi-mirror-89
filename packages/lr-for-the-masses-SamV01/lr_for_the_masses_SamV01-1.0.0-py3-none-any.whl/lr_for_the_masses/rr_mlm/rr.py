class ridgelinreg():
    from sklearn import linear_model
    
    def __init__(self, predictor_vec = [0], response = [0], alpha1 = 0):
        self.predictor_vec = predictor_vec
        self.response= response
        self.alpha1 = alpha1

    def ridgelin_fit(self):
        from sklearn import linear_model
        self.alpha1 = float(input("Enter an alpha value for regularization:"))
        reg = linear_model.Ridge(alpha=self.alpha1)
        return reg.fit(self.predictor_vec, self.response)

    def ridgelin_alpha(self):
        from sklearn import linear_model
        self.alpha1 = float(input("Enter an alpha value for regularization:"))
        return linear_model.Ridge(alpha=self.alpha1)

    def testridgelin_alpha(self):
        from sklearn import linear_model
        self.alpha1 = 1
        return linear_model.Ridge(alpha=self.alpha1)

    def testridgelin_fit(self):
        from sklearn import linear_model
        self.alpha1 = 1
        reg = linear_model.Ridge(alpha=self.alpha1)
        return reg.fit(self.predictor_vec, self.response)

    def ridgelin(self):
        from sklearn import linear_model
        self.alpha1 = float(input("Enter an alpha value for regularization:"))
        reg = linear_model.Ridge(alpha=self.alpha1)
        reg.fit(self.predictor_vec, self.response)
        print('The coefficents for ridge regression or a value of alpha: "{:.2f}" are "{:.2f}" and "{:.2f}"'.format(self.alpha1, reg.coef_[0], reg.coef_[1]))
        print('The intercept for ridge regression or a value of alpha: "{:.2f}" is "{:.2f}"'.format(self.alpha1, reg.intercept_))

    def testridgelin(self):
        from sklearn import linear_model
        self.alpha1 = 1
        reg = linear_model.Ridge(alpha=self.alpha1)
        reg.fit(self.predictor_vec, self.response)
        print('The coefficents for ridge regression or a value of alpha: "{:.2f}" are "{:.2f}" and "{:.2f}"'.format(self.alpha1, reg.coef_[0], reg.coef_[1]))
        print('The intercept for ridge regression or a value of alpha: "{:.2f}" is "{:.2f}"'.format(self.alpha1, reg.intercept_))
        
class vislinridge(ridgelinreg):
    def __init__(self, predictor_vec = [0], response = [0], alpha1 = 0, n_alpha = 100):
        ridgelinreg.__init__(self,predictor_vec = [0], response = [0], alpha1 = 0)
        self.n_alpha = n_alpha
    
    def visridgealpha(self):
        ridgelinreg.ridgelin(self)
        alphas = np.logspace(-10, -2, self.n_alpha)
        coefs = []
        for a in alphas:
            ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
            ridge.fit(self.predictor_vec, self.response)
            coefs.append(ridge.coef_)
        
        v1 = plt.gca()
        v1.plot(alphas, coefs)
        v1.set_xscale('log')
        v1.set_xlim(v1.get_xlim()[::-1])  # reverse axis
        plt.xlabel('alpha')
        plt.ylabel('weights')
        plt.show()

class testvislinridge(ridgelinreg):
    def __init__(self, predictor_vec = [0], response = [0], alpha1 = 0, n_alpha = 100):
        ridgelinreg.__init__(self,predictor_vec = [0], response = [0], alpha1 = 0)
        self.n_alpha = n_alpha
    
    def visridgealpha(self):
        ridgelinreg.testridgelin(self)
        alphas = np.logspace(-10, -2, self.n_alpha)
        coefs = []
        for a in alphas:
            ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
            ridge.fit(self.predictor_vec, self.response)
            coefs.append(ridge.coef_)
        
        v1 = plt.gca()
        v1.plot(alphas, coefs)
        v1.set_xscale('log')
        v1.set_xlim(v1.get_xlim()[::-1])  # reverse axis
        plt.xlabel('alpha')
        plt.ylabel('weights')
        plt.show()
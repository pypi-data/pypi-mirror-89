class linearmixedeffects():
    import seaborn as sns; sns.set()
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from statsmodels.regression import mixed_linear_model
    import sklearn as sk
    from math import sqrt
    import statsmodels.api as sm
    def __init__(self, response, fixed, random, predict = 0, mlmf = 0):
        self.response = response
        self.fixed = fixed
        self.random = random

    def fitmlm(self):
        import pandas as pd
        from statsmodels.regression import mixed_linear_model
        mlm = mixed_linear_model.MixedLM(endog = pd.DataFrame(self.response), exog = pd.DataFrame(self.fixed), groups = pd.DataFrame(self.random), formula = 'response ~ fixed')
        mlmf = mlm.fit()
        return mlmf

    def summarymlm(self):
        import pandas as pd
        from statsmodels.regression import mixed_linear_model
        mlm = mixed_linear_model.MixedLM(endog = pd.DataFrame(self.response), exog = pd.DataFrame(self.fixed), groups = pd.DataFrame(self.random), formula = 'response ~ fixed')
        mlmf = mlm.fit()
        print(" ")
        print("The summary of the linear mixed effects model is given below:")
        return mlmf.summary()

    def plotmlm(self):
        import seaborn as sns; sns.set()
        import pandas as pd
        from statsmodels.regression import mixed_linear_model
        mlm = mixed_linear_model.MixedLM(endog = pd.DataFrame(self.response), exog = pd.DataFrame(self.fixed), groups = pd.DataFrame(self.random), formula = 'response ~ fixed')
        mlmf = mlm.fit()
        db_plot = pd.DataFrame()
        db_plot["residuals"] = mlmf.resid.values
        db_plot["fixed"] = fixed
        db_plot["predicted"] = mlmf.fittedvalues
        
        sns.lmplot(x = "predicted", y = "residuals", data = dbplot)
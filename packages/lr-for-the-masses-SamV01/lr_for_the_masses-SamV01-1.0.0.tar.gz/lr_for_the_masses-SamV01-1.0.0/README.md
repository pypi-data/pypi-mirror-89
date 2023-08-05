# lr_for_the_masses
## Linear Regression as an Educational Tool
### By Samuel Vélez and Mandar Kathe 
[![Build Status](https://travis-ci.org/samuel-velez/533_lab_4_KatheVelez.svg?branch=master)](https://travis-ci.org/samuel-velez/533_lab_4_KatheVelez)


The purpose of this package is to provide simplified tools to apply several different linear regression models.
The main package has tools to load custom data from a .csv, Excel, or the practice sets available in the Seaborn package and visualize it, while the remainder of the package is stored in its subpackages and modules, each dedicated to a different type of linear regression: simple linear regression, multiple linear regression, linear mixed effects regression and ridge regression.
These modules hold functions to summarize, diagnose and plot these different implementations.
The team members have followed the required structural formats for the class.
Overall, we have two sub-packahes each containing two modules. The modules also have inheritance as required by the assignment

The following is the structure and explanation on each function's function:

1. Subpackage 1: Linear regression

1.1. Module 1: Simple Linear Regression
    This module aims to provide a simplified tool to fit and diagnose linear regression models after it is provided with a predictor and a response variable.

    1.1.1 Linear regression summary: summarylin()
        This function prints the slope and intercept of the fitted linear regression model.

    1.1.2 Linear regression diagnosis: diagnoselin()
        Prints the R-squared, p-value and standard error of the fitted linear regression model.

    1.1.3 Original data plot: plotoriginaldata()
        Plots a scatterplot showing the predictor and the response.

    1.1.4 Fitted line plot: plotfittedline()
        Plots the fitted line created by the linear regression model.

    1.1.5 Confidence interval plot: plotconfidence_intervals()
        Plots the confidence intervals with a 95% confidence for the fitted linear regression.

1.2 Module 2: Multiple Linear Regression
    Simplified application of multiple linear regression asking the user to provide a response variables and predictors.

    1.2.1 Multiple linear regression summary: summary_mullin()
        This function prints the coefficients, intercept and form of the fitted multiple linear regression model.

    1.2.2 Multiple linear regression diagnosis: diag_Rval()
        Prints the R-squared of the fitted model.

2. Subpackage 2: Linear Mixed Effects and Ridge Regression

2.1 Module 1: Linear mixed effects
Provides an easy application of linear mixed effects, asking the user to choose a response variable, a fixed variable and a random variable.

    2.1.1 Summary of the linear mixed effects model: summarymlm()
        Provides information such as coefficients, number of groups, number of observations and other general information on this application.

    2.1.2 Linear mixed effects plot: plotmlm()
        Plot of the residuals of the fit linear mixed effects model.

2.2 Module 2: Ridge Linear regression
    Implementation of ridge linear regression asking the user to provide a predictor, response and a regularization alpha.

    2.2.1 Ridge regression summary: ridgelin()
        Requests the input of a regularization alpha and provides the coefficients and intercept of the model.
        
    2.2.2 Regularization alpha plot: visridgealpha()
        Plots the ridge regression implementation against its regularization alpha.
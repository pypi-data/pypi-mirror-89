# Main package
## Upload your own data or choose a practice dataset from Seaborn.
import sklearn as skl
import scipy
import matplotlib
import pandas as pd
import seaborn as sns

def load_csv(file_path):
    data = pd.read_csv(file_path)
    return "Data loaded"

def load_excel(file_path):
    data = pd.read_excel(file_path)
    return "Data loaded"

def load_practice_db(file_name):
#https://github.com/mwaskom/seaborn-data don't add .csv
    data = sns.load_dataset('iris')
    return "Data loaded"

def show_data(x,y):
    return data.head()

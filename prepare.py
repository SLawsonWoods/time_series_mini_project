
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import env

from datetime import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns

from pandas.plotting import register_matplotlib_converters

import statsmodels.api as sm
from statsmodels.tsa.api import Holt


def formatting(df):
    '''
    This function converts the sale_date column to a datetime index, then sorts it, makes a total sales column, a month and a day     column
    '''
    # converting sale_date to datetime format using to_datetime()
    df.sale_date = pd.to_datetime(df.sale_date)
    # this gives you a df resetting the index to date which has to
    df = df.set_index('sale_date').sort_index()
    # making a total sales column
    df['sales_total'] = df.sale_amount * df.item_price
    # adding a month column
    df['month'] = df.index.strftime('%B')
    # adding a day of the week column
    df['day'] = df.index.strftime('%w')
    return df

def prep_data(df):
    return df.assign(ds= pd.to_datetime(df.sale_date)).sort_values('ds').\
                assign(dollars_sold = df.sale_amount * df.item_price).\
                assign(item_sold = df.sale_amount* df.item_price).\
                df.groupby(['ds'])[['dollars_sold', 'items_sold']].sum()

# define evaluation function to compute rmse
def evaluate(target_var):
    '''
    the evaluate function will take in the actual values in the validate and the predicted values
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

# plot and evaluate
def plot_and_eval(target_var):
    '''
    a function to evaluate forecasts by computing the rmse and plot train and validate along with predictions
    '''
    plot_samples(target_var)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '--RMSE:  {: 0f}'.format(rmse))
    plt.show()
    
    
# Define function to store rmse for comparison purposes
def append_eval_df(model_type, target_var):
    '''
    this function is going to take in the model_type as a string, the target variable as a string,
    and run the evaluate() function to compute the rmse,
    and append to the dataframe a row with the model_type, target_var, and rmse. 
    It will return the new dataframe.
    '''
    rmse = evaluate(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)
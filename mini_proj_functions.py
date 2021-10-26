import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from math import sqrt
from sklearn.metrics import mean_squared_error


def get_temp_data():
    '''
    bring in global land temperatures by major city
    '''
    df = pd.read_csv('GlobalLandTemperaturesByCity.csv')
    return df
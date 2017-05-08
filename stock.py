
# coding: utf-8

# In[28]:

from matplotlib import pyplot as plt
get_ipython().magic('matplotlib inline')

import numpy as np

import pandas as pd

import seaborn as sb
sb.set_style("dark")

from pandas_datareader import data, wb

from datetime import datetime

from __future__ import division

start = datetime(2014,1,1)
end = datetime(2017,1,1)

#obtain the shang hai stock exchange data
globals()["SH"] = data.DataReader('000001.SS','yahoo',start,end)

SH.describe()

#plot and save the pictures of open price in SSE.PNG file
SH["Open"].plot(legend = True, figsize=(20,10), title = 'SSE Historical Index')

"""
plot the moving average of SSE.
MA is a widely used indicator in technical analysis that helps smooth out price action by filtering out the “noise” from random price fluctuations.
A moving average (MA) is a trend-following or lagging indicator because it is based on past prices.
The two basic and commonly used MAs are the simple moving average (SMA), which is the simple average of a security over a defined number of time periods, 
and the exponential moving average (EMA), which gives bigger weight to more recent prices. 
"""
ma = [15, 30, 60]

for days in ma:
    col_name = "{} days MA".format(days)
    SH[col_name] = pd.rolling_mean(SH["Open"],days)
    SH[col_name].plot(legend = True, figsize = (20,10), title = "SSE Moving Average")
 


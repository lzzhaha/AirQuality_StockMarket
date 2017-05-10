
# coding: utf-8

# In[110]:

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
end = datetime(2017,5,2)

#obtain the shang hai stock exchange data
globals()["SH"] = data.DataReader('000001.SS','yahoo',start,end)

SH.describe()

#plot and save the pictures of open price in SSE.PNG file
#SH["Open"].plot(legend = True, figsize=(20,10), title = 'SSE Historical Index')

"""
plot the moving average of SSE.
MA is a widely used indicator in technical analysis that helps smooth out price action by filtering out the “noise” from random price fluctuations.
A moving average (MA) is a trend-following or lagging indicator because it is based on past prices.
The two basic and commonly used MAs are the simple moving average (SMA), which is the simple average of a security over a defined number of time periods, 
and the exponential moving average (EMA), which gives bigger weight to more recent prices. 
"""
ma = [15, 30, 60]
"""
for days in ma:
    col_name = "{} days MA".format(days)
    SH[col_name] = pd.rolling_mean(SH["Open"],days)
    SH[col_name].plot(legend = True, figsize = (20,10), title = "SSE Moving Average")
"""
plt.figure()

# plot histogram
#SH["Open"].plot.hist(bins = 100)

# Now we begin to analyze the interrelationship between air quality in Beijing, Shanghai, Guangzhou and SSE index

#read csv file.

import csv


def create_frame(filename):
    with open(filename,'r',encoding = 'utf-8-sig') as file:
        reader = csv.DictReader(file)
        date_index = []
        content = []
        for row in reader:
            date_index.append(datetime.strptime(row["Date"], '%Y-%m-%d'))
            content.append([float(row["AQI"]),float(row["PM25"]),float(row["PM10"])])
        df = pd.DataFrame(data = content,index = date_index,columns = ['AQI', 'PM25','PM10'])
    monthly_price = []
    with open('000001.SS.csv','r', encoding = 'utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            monthly_price.append(float(row["Adj Close"]))
    df['stock_price'] = monthly_price
    return df



bj_df = create_frame('bj.csv')
sh_df = create_frame('sh.csv')
gz_df = create_frame('gz.csv')

#draw and find the relationship between the AQI and stock price
#store the plotted picture in BJ_AQI_and_stock.png.
#the correlation coefficient is -0.13 and p-value (significance level) is 0.43
sb.jointplot(x= "AQI", y = "stock_price", data = bj_df,kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\BJ_AQI_and_stock.png")

#store the plotted picture in BJ_PM25_and_stock.png.
#the correlation coefficient is -0.12 and p-value (significance level) is 0.45
sb.jointplot(x="PM25", y = "stock_price",data = bj_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\BJ_PM25_and_stock.png")

#store the plotted picture in BJ_PM10_and_stock.png.
#the correlation coefficient is -0.14 and p-value (significance level) is 0.39
sb.jointplot(x="PM10", y = "stock_price",data = bj_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\BJ_PM10_and_stock.png")


#similarly for another cities, the pictures are saved into corresponding files 
sb.jointplot(x="AQI", y = "stock_price",data = sh_df, kind = 'reg').savefig("C:\\Users\\HAHA\Desktop\\AirQuality_StockMarket\\SH_AQI_and_stock.png")
sb.jointplot(x="PM25", y = "stock_price",data = sh_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\SH_PM25_and_stock.png")
sb.jointplot(x="PM10", y = "stock_price",data = sh_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\SH_PM10_and_stock.png")
sb.jointplot(x="AQI", y = "stock_price",data = gz_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\GZ_AQI_and_stock.png")
sb.jointplot(x="PM25", y = "stock_price",data = gz_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\GZ_PM25_and_stock.png")
sb.jointplot(x="PM10", y = "stock_price",data = gz_df, kind = 'reg').savefig("C:\\Users\\HAHA\\Desktop\\AirQuality_StockMarket\\GZ_PM10_and_stock.png")




# In[ ]:




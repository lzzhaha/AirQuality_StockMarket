'''
Data of air quality is provided in https://www.aqistudy.cn/historydata/
'''
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import csv
#import panda as pa
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#get the web page and parse it to beautifulsoup object

target_city=['北京','上海','广州']

bj_page = requests.get('https://www.aqistudy.cn/historydata/monthdata.php?city='+target_city[0])
sh_page = requests.get('https://www.aqistudy.cn/historydata/monthdata.php?city='+target_city[1])
gz_page = requests.get('https://www.aqistudy.cn/historydata/monthdata.php?city='+target_city[2])


bj_soup = BeautifulSoup(bj_page.text,'html5lib')
sh_soup = BeautifulSoup(sh_page.content,'html5lib')
gz_soup = BeautifulSoup(gz_page.content,'html5lib')

bj_soup.prettify();
sh_soup.prettify();
gz_soup.prettify();


#Get the table 
bj_table = bj_soup.find('table',attrs={'class':'table table-condensed table-bordered table-striped table-hover table-responsive'})
sh_table = sh_soup.find('table',attrs={'class':'table table-condensed table-bordered table-striped table-hover table-responsive'})
gz_table = gz_soup.find('table',attrs={'class':'table table-condensed table-bordered table-striped table-hover table-responsive'})




bj_data = bj_table.find_all('tr')
del bj_data[0:2]
sh_data = sh_table.find_all('tr')
del sh_data[0:2]
gz_data = gz_table.find_all('tr')
del gz_data[0:2]

#define a class City to hold the data

class City_history:
    Name=''
    Date = date(2014,1,1)
    AQI = 0
    AQI_range = dict({'min':0, 'max':0})
    Quality_level = '' 
    PM25 = 0.0
    PM10 = 0.0
    SO2 = 0.0
    Rank = 0
    def __init__(self,Name,Date,AQI,AQI_range,Quality_level,PM25,PM10,SO2,Rank):
        self.Name=Name
        self.Date =Date
        self.AQI=AQI
        self.AQI_range=AQI_range
        self.Quality_level=Quality_level
        self.PM25=PM25
        self.PM10=PM10
        self.SO2=SO2
        self.Rank=Rank

bj_history=[]
sh_history=[]
gz_history=[]

#define a function to populate city history
        

def populate_city(city_data,city_history_list=[],city_name=''):
    for tr in city_data:
        td =tr.find_all('td')
        date_string = td[0].text.split('-')
        Date = date(int(date_string[0]),int(date_string[1]),1)
        AQI=td[1].text
        AQI_range= td[2].text
        Quality_level=td[3].text
        PM25=td[4].text
        PM10=td[5].text
        SO2=td[6].text
        Rank=td[10].text
        city_history_list.append(City_history(city_name,Date,AQI,AQI_range,Quality_level,PM25,PM10,SO2,Rank))
    return

#Populate the data to each City object

populate_city(bj_data,bj_history,city_name='Beijing')
populate_city(sh_data,sh_history,city_name='Shanghai')
populate_city(gz_data,gz_history,city_name='Guangzhou')


#writing data to bj.csv, sh.csv, gz.csv files
fields = ['City','Date','AQI','AQI_range','Quality_level','PM25','PM10','SO2','Rank']

with open('bj.csv','w',encoding='utf-8-sig') as bj_csv:
    bj_writer = csv.DictWriter(bj_csv,fieldnames = fields)
    bj_writer.writeheader()
    for record in bj_history:
        bj_writer.writerow({fields[0]:record.Name, fields[1]:record.Date,\
                            fields[2]:record.AQI, fields[3]:record.AQI_range,\
                            fields[4]:record.Quality_level, fields[5]:record.PM25,\
                            fields[6]:record.PM10, fields[7]: record.SO2,\
                            fields[8]:record.Rank,
                            })

bj_csv.close()

with open('sh.csv','w',encoding='utf-8-sig') as sh_csv:
    sh_writer = csv.DictWriter(sh_csv,fieldnames = fields)
    sh_writer.writeheader()
    for record in sh_history:
         sh_writer.writerow({fields[0]:record.Name, fields[1]:record.Date,\
                            fields[2]:record.AQI, fields[3]:record.AQI_range,\
                            fields[4]:record.Quality_level, fields[5]:record.PM25,\
                            fields[6]:record.PM10, fields[7]: record.SO2,\
                            fields[8]:record.Rank,
                            })

sh_csv.close()

with open('gz.csv','w',encoding='utf-8-sig') as gz_csv:
    gz_writer = csv.DictWriter(gz_csv,fieldnames = fields)
    gz_writer.writeheader()
    for record in gz_history:
        gz_writer.writerow({fields[0]:record.Name, fields[1]:record.Date,\
                            fields[2]:record.AQI, fields[3]:record.AQI_range,\
                            fields[4]:record.Quality_level, fields[5]:record.PM25,\
                            fields[6]:record.PM10, fields[7]: record.SO2,\
                            fields[8]:record.Rank,
                            })
gz_csv.close()


#Perform some statistics analysis using panda, numpy, matplotlib library

bj_df = pa.DataFrame(data = bj_history, columns = fields)

sh_df = pa.DataFrame(data = sh_history, columns = fields)

gz_df = pa.DataFrame(data = gz_hisotry, columns = fileds)

bj_df.describe()
sh_df.describe()
gz_df.describe()

bj_air_histories = []
for history in bj_history:
    bj_air_histories.append(history.Quality_level)

# get the frequencies of the air level for each cities

air_levels = ['优','良','轻度污染','重度污染','中度污染','严重污染']

plt.hist(bj_air_histories,bins = air_levels)

plot.show()

'''
Data of air quality is provided in https://www.aqistudy.cn/historydata/
'''
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import csv

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
    _Name=''
    _Date = date(2014,1,1)
    _AQI = 0
    _AQI_range = dict({'min':0, 'max':0})
    _Quality_level = '' 
    _PM25 = 0.0
    _PM10 = 0.0
    _SO2 = 0.0
    _Rank = 0
    def __init__(self,Name,Date,AQI,AQI_range,Quality_level,PM25,PM10,SO2,Rank):
        self._Name=Name
        self._Date =Date
        self._AQI=AQI
        self._AQI_range=AQI_range
        self._Quality_level=Quality_level
        self._PM25=PM25
        self._PM10=PM10
        self._SO2=SO2
        self._Rank=Rank

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
        bj_writer.writerow({fields[0]:record._Name, fields[1]:record._Date,\
                            fields[2]:record._AQI, fields[3]:record._AQI_range,\
                            fields[4]:record._Quality_level, fields[5]:record._PM25,\
                            fields[6]:record._PM10, fields[7]: record._SO2,\
                            fields[8]:record._Rank,
                            })

bj_csv.close()

with open('sh.csv','w',encoding='utf-8-sig') as sh_csv:
    sh_writer = csv.DictWriter(sh_csv,fieldnames = fields)
    sh_writer.writeheader()
    for record in sh_history:
        sh_writer.writerow({fields[0]:record._Name, fields[1]:record._Date,\
                            fields[2]:record._AQI, fields[3]:record._AQI_range,\
                            fields[4]:record._Quality_level, fields[5]:record._PM25,\
                            fields[6]:record._PM10, fields[7]: record._SO2,\
                            fields[8]:record._Rank,
                            })

sh_csv.close()

with open('gz.csv','w',encoding='utf-8-sig') as gz_csv:
    gz_writer = csv.DictWriter(gz_csv,fieldnames = fields)
    gz_writer.writeheader()
    for record in gz_history:
        gz_writer.writerow({fields[0]:record._Name, fields[1]:record._Date,\
                            fields[2]:record._AQI, fields[3]:record._AQI_range,\
                            fields[4]:record._Quality_level, fields[5]:record._PM25,\
                            fields[6]:record._PM10, fields[7]: record._SO2,\
                            fields[8]:record._Rank,
                            })

gz_csv.close()

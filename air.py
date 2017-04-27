'''
Data of air quality is provided in https://www.aqistudy.cn/historydata/
'''
import requests
from bs4 import BeautifulSoup
import json
from datetime import date

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
print(bj_data)
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
        slef._SO2=SO2
        self._Rank=Rank

bj_history=[]
sh_history=[]
gz_history=[]

#define a function to populate city history
        

def populate_city(city_data,city_history_list=[],city_name=''):
    for tr in city_data:
        td =tr.find_all('td')
        date_string = td[0].text.split('-')
        Date = datetime.date(date_string[0],date_string[1],1)
        AQI=td[1]
        AQI_range= td[2]
        Qulaity_level=td[3]
        PM25=td[4]
        PM10=td[5]
        SO2=td[6]
        Rank=td[10]
        city_history.append(City_history(city_name,Date,AQI,AQI_range,Quality_level,PM25,PM10,SO2,Rank))
    return
#Populate the data to each City object


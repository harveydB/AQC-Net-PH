from cgitb import text
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re 
import csv

def getAQI(city,filename):
    pm_array = []
    ctr = 0
    queryURL = 'https://www.iqair.com/philippines/ncr/' + city
    while ctr<17:
        page = requests.get(queryURL)
        soup = BeautifulSoup(page.text, "lxml")
        results = soup.find(class_="aqi-overview-detail__other-pollution-table")
        textdata = str(results.text)
        textdata = re.sub('[^a-zA-Z0-9 \n\.]', ' ', textdata)
        pm_value = float(textdata.split()[2])
        pm_array.append(pm_value)
        time.sleep(1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        ctr+=1

    columns = ['IQAir PM Value'] 
    with open('C:/Users/Kaldra/Desktop/School/A2ndSem21-22/CoE 199/Datasets/'+ filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for val in pm_array:
            writer.writerow([val])

#getAQI('caloocan', 'caloocan.csv' )

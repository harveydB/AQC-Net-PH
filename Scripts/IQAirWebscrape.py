from cgitb import text
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re 
import csv


def get_PM(queryURL):
    pm_array = []
    ctr = 0

    while ctr<17: 
        page = requests.get(queryURL)
        soup = BeautifulSoup(page.text, "lxml")
        results = soup.find(class_="aqi-overview-detail__other-pollution-table")
        textdata = str(results.text)
        textdata = re.sub('[^a-zA-Z0-9 \n\.]', ' ', textdata)
        pm_value = float(textdata.split()[2])
        pm_array.append(pm_value)
        time.sleep(1800)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        ctr+=1
    return pm_array

def write_PM(filename,pm_array):
    columns = ['IQAir PM Value'] 

    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for val in pm_array:
            writer.writerow([val])

queryURL = 'https://www.iqair.com/philippines/ncr/caloocan'
pm_array = get_PM(queryURL)
write_PM("D:/GitHub/EEE-199/PM_data/04-02-2022_Caloocan_IQAir",pm_array)
from cgitb import text
from itertools import count
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re 
import csv
import pickle

def getAQI(city,filename):
    pm_array = []
    ctr = 0
    queryURL = 'https://www.iqair.com/philippines/ncr/' + city
    temp_list = pickle.load(open("temp.pkl","rb"))
    print("opening pickle", temp_list)
    pickle_counter = 17 - len(temp_list)
    pm_array.extend(temp_list)
    while ctr< pickle_counter:
        page = requests.get(queryURL)
        soup = BeautifulSoup(page.text, "lxml")
        results = soup.find(class_="aqi-overview-detail__other-pollution-table")
        textdata = str(results.text)
        textdata = re.sub('[^a-zA-Z0-9 \n\.]', ' ', textdata)
        pm_value = float(textdata.split()[2])
        pm_array.append(pm_value)
        print("writing pickle", pm_array)
        pickle.dump(pm_array,open("temp.pkl","wb"))
        ctr+=1
        if ctr >= pickle_counter:
            break
        time.sleep(1800)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        
    pickle_to_csv(filename)

def pickle_to_csv(filename):
    pm_array = pickle.load(open("temp.pkl","rb"))
    columns = ['IQAir PM Value'] 
    with open('D:/GitHub/EEE-199/PM_Data/Raw_Data/'+ filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for val in pm_array:
            writer.writerow([val])
    pickle.dump([],open("temp.pkl","wb"))
    print(pm_array)


#getAQI('caloocan', '04-27_Caloocan_IQAir.csv' )
pickle_to_csv('04-27_Caloocan_IQAir.csv')


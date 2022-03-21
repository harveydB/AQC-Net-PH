from cgitb import text
import requests
from bs4 import BeautifulSoup
import pandas as pd

queryURL = 'https://www.iqair.com/philippines/ncr/caloocan'
page = requests.get(queryURL)
soup = BeautifulSoup(page.text, "lxml")
results = soup.find(class_="aqi-overview-detail__other-pollution-table")
textdata = results.text
textdata = textdata.split()
pm_value = float(textdata[2])
print(pm_value)

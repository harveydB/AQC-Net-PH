import requests
import json

URL = "http://api.airvisual.com/v2"

City = 'Caloocan'
State = 'NCR'
Country = 'Philippines'
APIKEY = '75735f79-9de0-4104-a595-e555e240f4c9'

queryURL = URL + '/city?city=' + City + '&state=' + State + '&country=' + Country + '&key=' +APIKEY

def getAQI():
    response = requests.get(queryURL)
    userdata = json.loads(response.text)
    return userdata.get('data').get('current').get('pollution').get('aqius')

print("AQI Value: " + str(getAQI()))

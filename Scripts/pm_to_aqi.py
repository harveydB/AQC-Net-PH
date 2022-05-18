import pandas as pd

def calc_aqi(pm,bp_hi,bp_lo,i_hi,i_lo):
    aqi = ((i_hi - i_lo) / (bp_hi-bp_lo)) * (pm - bp_lo) + i_lo
    return aqi

def get_aqi(pm10,pm25):
    pm10_bphi_list = [54,154,254,354,424,504,604]
    pm10_bplo_list = [0,55,155,255,355,425,505]
    pm25_bphi_list = [12.0,35.4,55.4,150.4,250.4,350.4,500.4]
    pm25_bplo_list = [0,12.1,35.5,55.5,150.5,250.5,350.5]
    aqi_bphi_list = [50,100,150,200,300,400,500]
    aqi_bplo_list = [0,51,101,151,201,301,401]
    for i in range(7):
        if pm10 < pm10_bphi_list[i] and pm10 > pm10_bplo_list[i]:
            pm10_bphi =  pm10_bphi_list[i]
            pm10_bplo =  pm10_bplo_list[i]
            pm10_aqi_bphi = aqi_bphi_list[i]
            pm10_aqi_bplo = aqi_bplo_list[i]
        if pm25 < pm25_bphi_list[i] and pm25 > pm25_bplo_list[i]:
            pm25_bphi =  pm25_bphi_list[i]
            pm25_bplo =  pm25_bplo_list[i]
            pm25_aqi_bphi = aqi_bphi_list[i]
            pm25_aqi_bplo = aqi_bplo_list[i]
    pm10_aqi = calc_aqi(pm10,pm10_bphi,pm10_bplo,pm10_aqi_bphi,pm10_aqi_bplo)
    pm25_aqi = calc_aqi(pm25,pm25_bphi,pm25_bplo,pm25_aqi_bphi,pm25_aqi_bplo)

    if pm10_aqi > pm25_aqi:
        main_pollutant = "PM10"
        calculated_aqi = pm10_aqi
    else:
        main_pollutant = "PM2.5"
        calculated_aqi = pm25_aqi
    for i in range(7):
        print(calculated_aqi)
        if calculated_aqi < aqi_bphi_list[i] and calculated_aqi > aqi_bplo_list[i]:
            label = i
            print(label)
            break
    return label,main_pollutant,calculated_aqi
    
            
date = "05-13"
location = "UP"
new_file = date + "_" + location + "_AQI"
proc_dir  = 'D:/Github/EEE-199/PM_Data/Processed_Data/'
date_dir = proc_dir + date + "/"
df = pd.read_csv(date_dir+date+"_"+location+"_P.csv")
df["Calibrated PM10"] = df["PM10"] * 0.88
df["Calibrated PM2.5"] = df["PM2.5"] * 0.88
df["Main Pollutant"] = ""
df["AQI"] = 0
df["AQI Label"] = 99

for i in range(len(df.index)):
    df["AQI Label"][i],df["Main Pollutant"][i],df["AQI"][i] = get_aqi(df.iloc[i]["PM10"],df.iloc[i]["PM2.5"])
print(df)
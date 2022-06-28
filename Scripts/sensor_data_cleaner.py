from posixpath import split
from tracemalloc import start
import pandas as pd
from datetime import datetime
import numpy as np
import os
import image_organizer


#locate starting point (8am)
def set_start_time(start_time,df):
    starting_index = df.index[df['Timestamp']==datetime.strptime(start_time,"%H:%M").time()].tolist()[0]
    return starting_index

#get values within 30mins
def ave_30_min(df,stop_index,starting_index):
    df = df.replace('',np.nan).astype({"PM10 1-min":"float","PM2.5 1-min":"float"})
    df_30min = df[stop_index:starting_index]
    ave_pm10 = df_30min[["PM10 1-min","PM2.5 1-min"]].mean(axis = 'index')[0]
    ave_pm25 = df_30min[["PM10 1-min","PM2.5 1-min"]].mean(axis = 'index')[1]
    return ave_pm10 , ave_pm25

#move time
def move_time(start_time,min_to_move):
    split_time = start_time.split(":")
    hours = split_time[0]
    mins = split_time[1]
    total_mins = int(hours) * 60 + int(mins)
    moved_time = total_mins + min_to_move
    moved_hours = moved_time//60
    moved_mins = moved_time%60
    moved_hours = 0 if moved_hours >= 24 else moved_hours
    moved_hours = "0" + str(moved_hours) if moved_hours < 10 else str(moved_hours)
    moved_mins = "0" + str(moved_mins) if moved_mins < 10 else str(moved_mins)
    moved_time = moved_hours + ":" + moved_mins
    return moved_time



def clean_data(interval,date,loc,start_time = "08:00",raw_dir = "D:/GitHub/EEE-199/PM_Data/Raw_Data/",proc_dir = 'D:/Github/EEE-199/PM_Data/Processed_Data/', pic_dir = "D:/Github/EEE-199/Pictures/"):
    #import data
    file_name = date+"_"+loc
    df = pd.read_csv(raw_dir+file_name + ".csv")
    #clean data
    column_names = df.columns.str.split(";")[0]
    df.columns = [column_names[0]]
    df = df[df.columns.str.split(";")[0][0]].str.split(";",expand=True)
    df.columns = column_names

    #change to timestamp data type
    for index in df.index:
        df.loc[index,"Timestamp"] = datetime.strptime(df.loc[index,"Timestamp"][11:-3],"%H:%M").time()

    #set start time
    ave_pm10_list = []
    ave_pm25_list = []
    valid_time = []
    stop_index = 0

    while(True):
        print(start_time)
        if start_time == "16:30":
            break
        try:
            start_index = set_start_time(start_time,df)
        except:
            #if start time is not available move 1-min
            print("start time not available")
            try:
                start_time = move_time(start_time,1)
                start_index = set_start_time(start_time,df)
            except:
            #will break if all time are already covered
                print("ending")
                break
        #get 30-min ave
        hold_pm10,holdpm25 = ave_30_min(df,stop_index,start_index)
        #store in list
        valid_time.append(start_time)
        ave_pm10_list.append(hold_pm10)
        ave_pm25_list.append(holdpm25)
        #set stop index
        stop_index = start_index + 1
        #move start time
        start_time = move_time(start_time,interval)

    image_names = image_organizer.get_image_data(pic_dir+date)
    print("PM10", ave_pm10_list)
    print("PM2.5",ave_pm25_list)
    new_df = pd.DataFrame({"Timestamp":valid_time,"PM10":ave_pm10_list,"PM2.5":ave_pm25_list})
    new_df.loc[:, 'Image name'] = pd.Series(image_names)
    print(new_df)
    os.makedirs(proc_dir+date, exist_ok=True)
    new_df.to_csv(proc_dir+date+"/"+ file_name +'_P.csv', index = False)

#sample date - "03-31"
#sample loc - "Caloocan"
#clean_data("04-02","Caloocan")
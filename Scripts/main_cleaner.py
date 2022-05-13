import sensor_data_cleaner
import CSVMerger



date = "" # sample date "04-22"
location = "" # location "Caloocan_H" / "UP_H" for harvey
#manual input for each user 
raw_dir= "D:/GitHub/EEE-199/PM_Data/Raw_Data/" 
proc_dir  = 'D:/Github/EEE-199/PM_Data/Processed_Data/'
pic_dir = "D:/Github/EEE-199/Pictures/"
merge_dir = "D:/GitHub/EEE-199/PM_Data/Merged_Data/" 
start_time = "10:00"
sensor_data_cleaner.clean_data(date,location,start_time,raw_dir ,proc_dir, pic_dir)
CSVMerger.merge_csv(date,proc_dir,location,merge_dir )
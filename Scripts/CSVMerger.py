import os
import glob
import pandas as pd

def merge_csv(date,proc_dir,location,merge_dir = "D:/GitHub/EEE-199/PM_Data/Merged_Data/"):
    os.chdir(proc_dir+date)
    filename = date+"_"+location+"_Merged"
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], axis=1)
    #export to csv
    combined_csv.to_csv(merge_dir+filename, index=False, encoding='utf-8-sig')

merge_csv("04-02",'D:/Github/EEE-199/PM_Data/Processed_Data/',"Caloocan")
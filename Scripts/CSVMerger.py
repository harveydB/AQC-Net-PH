import os
import glob
import pandas as pd


os.chdir("C:/Users/Kaldra/Desktop/School/A2ndSem21-22/CoE 199/Datasets")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], axis=1)
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
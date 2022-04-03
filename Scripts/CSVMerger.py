import os
import glob
import pandas as pd

def merge_csv(directory,file_name):
    os.chdir(directory)

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], axis=1)
    #export to csv
    combined_csv.to_csv(file_name, index=False, encoding='utf-8-sig')
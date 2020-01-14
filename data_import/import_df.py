import os
import pandas as pd
import numpy as np
import glob                                    # find file names in the folders
from matplotlib.pyplot import cm               # create colours automatically
from matplotlib import colors as mcolors       # create colours automatically


def import_polar (df_polar, subjects, base_dir):
    
    for subject in subjects: 
        # Directory for dog i folder
        #print(subject)
        folder_dir = os.path.join(base_dir, subject, 'Polar')
    
        file_name = glob.glob('%s\\*_RR_%s-%s.csv' % (folder_dir, 'Polar', subject))
        # Open each RR file and store in an array of df (df_polar)

        df_polar[subject] = pd.read_csv(file_name[0])
        
        df_polar[subject].loc[:,'date'] = pd.to_datetime(df_polar[subject].loc[:,'date'])
        df_polar[subject] = df_polar[subject].set_index('date', drop= True)
                
        df_polar[subject].rename(columns = {' rr': 'rr'}, inplace = True)
        df_polar[subject].rename(columns = {' since start': 'ss'}, inplace = True)


def import_bio (df_bio, subjects, base_dir):
    folder_dir = os.path.list(base_dir)


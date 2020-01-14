# -*- coding: utf-8 -*-
"""
Created on Tue May 21 12:34:24 2019

@author: marinara.marcato
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------------------------------------------------- #
#                               Parametes                                   #    
# ------------------------------------------------------------------------- #
date = '23/05/2019'
subjects = ['Elf', 'Dugg', 'Zeb']
timestamps = {'start': ['15:27:46', '14:15:47', '14:51:33'],
              'finish': ['15:43:25', '15:07:11']}
dir_org = "Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study"
dir_new = "Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study"

# ------------------------------------------------------------------------- #
#                               Importing data                              #    
# ------------------------------------------------------------------------- #
df_times = pd.DataFrame(timestamps, index = subjects) 

file_name = glob.glob('%s\\*BB_RR.csv*' % (dir_org))
df_org = pd.read_csv(file_name[0], index_col = 'Timestamp', parse_dates=True)

# ------------------------------------------------------------------------- #
#           Plotting Rto R in the current DF and slicing times              #    
# ------------------------------------------------------------------------- #
plt.plot(df_org.index.time, df_org['RtoR'])
for x in df_times.values.flatten(): 
    plt.axvline(x = x, color ='r')

# ------------------------------------------------------------------------- #
#                      Saving slices in new directory                       #    
# ------------------------------------------------------------------------- #
for subject in subjects:
    file_dir = os.path.join(dir_new, subject, 'Bioharness')
    file_name = datetime.strftime(datetime.strptime((date + df_times['start'][subject]), '%d/%m/%Y%H:%M:%S'),"%Y_%m_%d-%H_%M_%S_BB_RR.csv")
    df_org.between_time(df_times['start'][subject], df_times['finish'][subject]).to_csv('%s\\%s' % (file_dir,file_name))


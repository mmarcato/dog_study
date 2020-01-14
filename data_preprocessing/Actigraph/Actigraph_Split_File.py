# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:18:58 2019

@author: marinara.marcato

Retrieve Actigraph data organised by Date in 'dir_raw' and save it to the appropriate Dog folder in 'dir_new'
It takes into account the start and finish time for each dog in Data Collection - Summary.csv whose path is 'dir_sum'

:param dir_sum: path to file Data Collection - Summary.csv 
:param dir_raw: path to directory Actigraph where data are organised in folders by Date that contain 'Back', 'Chest' and 'Neck' files
:param dir_new: path to directory where Actigraph data for each dog will be saved
"""

# ------------------------------------------------------------------------- #
#                                Imports                                    #    
# ------------------------------------------------------------------------- #

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ------------------------------------------------------------------------- #
#                               Parametes                                   #    
# ------------------------------------------------------------------------- #

dir_sum = "Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study\\Data Collection - Summary.csv"
dir_raw = "Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study\\Actigraph\\"
dir_new = "Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study\\Subjects\\"

# dates when the Actigraph data was collected
# dates = os.listdir(dir_raw)
dates = ['2020-01-08']

# ------------------------------------------------------------------------- #
#                               Importing data                              #    
# ------------------------------------------------------------------------- #
df_sum = {}

# combine Date column with Time columns
parse_dict = { 'DT-Pre-Saliva': [5,6],'DT-BT Start': [5,7], 'DT-BT Finish': [5,9],'DT-Post-Saliva': [5,10], 'DT-Date': [5]} 

df_sum['dc1'] = pd.read_csv(dir_sum, skiprows = 1, index_col = 'Name', usecols = [1,*range(4,14)], parse_dates = parse_dict, dayfirst = True)
df_sum['dc2'] = pd.read_csv(dir_sum, skiprows = 1, index_col = 'Name', usecols = [1, *range(15,25)], parse_dates = parse_dict, dayfirst = True)
# setting columns names to be the same because it added '.1' because they are in the same dictionary
df_sum['dc2'].columns = df_sum['dc1'].columns

# ------------------------------------------------------------------------- #
#                              Data processing                              #    
# ------------------------------------------------------------------------- #
""" Converting DataFrame columns to correct datatype """

for dc in ['dc1', 'dc2']:
    for col in ['BT Duration']:
        df_sum[dc][col] = pd.to_timedelta(df_sum[dc][col])
    for col in ['DT-Pre-Saliva','DT-BT Start', 'DT-BT Finish','DT-Post-Saliva']: 
        df_sum[dc][col] = pd.to_datetime(df_sum[dc][col], format = '%d/%m/%Y %H:%M:%S',dayfirst= True, errors='coerce')
    # this was already transformed to datetime when read_csv
    df_sum[dc]['DT-Date'] = pd.to_datetime(df_sum[dc]['DT-Date'], format =  '%d/%m/%Y', dayfirst= True, errors='coerce')

""" Given a data collection day, get the name of the dogs, upload the Artigraph files (back, chest and neck)
                the start and finish time for their BT slice the original dataframes 
"""

df_raw = {}
for date in dates:
    for dc in ['dc1', 'dc2']:
        subjects = list(df_sum[dc].index[df_sum[dc]['DT-Date'] == date].values)
        if subjects == []:
            print('No data found on', date, 'in file ', dir_sum)
        else:
            print(subjects, date)
            for subj in subjects:
                start = df_sum[dc]['DT-BT Start'][subj].time()
                finish = df_sum[dc]['DT-BT Finish'][subj].time()
                print(subj, '\nRetrieving data from ', dc, date, 'start', start, 'finish', finish)
                for sensor in ['Back','Chest','Neck']:
                    file_raw = glob.glob ('%s//%s*-IMU.csv' % (dir_raw + date, sensor))
                    if file_raw == []:
                        print('No Raw Actigraph file found for ', sensor, 'on ', date, 'in ', dir_raw)
                    else:
                        print(sensor, '\n\t Retrieving Raw Actigraph data from \n', dir_raw)
                       # df_raw[sensor] = pd.read_csv(file_raw[0], skiprows = 10, index_col = 'Timestamp', parse_dates = [0], infer_datetime_format = True) 
                        print('\n\t Saving Raw Actigraph data to file in ', dir_new)
                       # dir_acti = '%s\\%s_Actigraph' % (dir_new + subj,  dc[-1])
                        if not os.path.exists(dir_acti):
                            os.makedirs(dir_acti)    
                       # df_raw[sensor].between_time(start,finish).to_csv('%s\\%s_Actigraph\\%s_%s.csv' % \
                                                                                (dir_new + subj, dc[-1], date, sensor))

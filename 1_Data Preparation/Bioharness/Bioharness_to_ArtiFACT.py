# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:32:56 2019

    Convert Bioharness BB_RR to RR text file that can be read by ArtiiFACT

@author: marinara.marcato
"""
import pandas as pd
import glob
import os
import numpy as np

# Subject Directory
base_dir = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study'
subjects = os.listdir(base_dir)

# Data Collection Summary Directory
info_path = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study-Info\\Summary - Study.csv'
df_info = pd.read_csv(info_path, index_col = 'Subject')
df_info['Date'] = pd.to_datetime(df_info['Date'])

# Saving file with IBI for Artifact from start to finish according to df_info
for subject in subjects: 
    print(subject)
    # Bioharness Directory for each subject
    folder_dir = ('Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study\\%s\\Bioharness' % subject) 
    # List of files in subject folder that have 'BB_RR.csv' in it        
    file_name = glob.glob('%s\*BB_RR.csv' % (folder_dir))
    # Reading csv file, converting timestamps to date
    df = pd.read_csv(file_name[0], usecols = ['RtoR', 'Timestamp'], index_col = 'Timestamp', parse_dates = True)
    # Dropping duplicate numbers
    df.drop_duplicates(['RtoR'], keep = 'first', inplace = True)
    
    df.between_time(df_info['BT Start'][subject], df_info['BT Finish'][subject])
    # Taking the absolute number and multiplying by 1000, so now the RtoR are in ms
    ibi = df['RtoR'].abs()*1000
    np.savetxt("%s\\%s-RR_ArtiFACT.txt" % (folder_dir, subject), ibi , fmt = '%d', delimiter=' ')
    arti_dir = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Artifact\\Study\\Bioharness'
    np.savetxt("%s\\%s\\%s.txt" % (arti_dir, df_info['Date'][subject].strftime('%Y_%m_%d'), subject), ibi, fmt = '%d', delimiter=' ' )

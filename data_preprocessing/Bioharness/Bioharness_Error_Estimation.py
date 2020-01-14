# -*- coding: utf-8 -*-
"""
Created on Wed May 22 08:23:56 2019

@author: marinara.marcato
"""
import os
import glob
import numpy as np
import pandas as pd
from glob import glob as gb 

arti_dir  = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Artifact\\Study\\Bioharness'
arti_file = 'Summary_artifactCorrection_Results.xls'
arti_path = gb('%s\\*\\%s' % (arti_dir, arti_file))

# Importing original df to extract timestamp and IBI
df_dir  = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study'
subjects = os.listdir(df_dir)
df_file = '*BB_RR.csv'

# Reading results from ArtiFACT
df_list= []
for path in arti_path: 
    df_list.append(pd.read_excel(path, index_col = 'FileName', usecols = ['FileName','NumberOfArtifacts','NumberofDataPoints']))
df_arti = pd.concat(df_list)
df_arti['PercentageError'] = df_arti['NumberOfArtifacts']/df_arti['NumberofDataPoints']
df_arti.index = df_arti.index.map(lambda x: str(x)[:-4])

df_bio = {}
df_arti['Rec_dur'], df_arti ['IBI_dur'] = np.nan, np.nan

# Reading Bioharness RR df 
for subject in subjects:
    # Finding file names
    df_path = glob.glob('%s\\%s\\Bioharness\\%s' % (df_dir, subject, df_file))
    # Import bioharness df
    df_bio[subject] = pd.read_csv(df_path[0], index_col ='Timestamp' , usecols = ['Timestamp', 'RtoR'], parse_dates = True)
    # Renamin column from RtoR to IBI
    df_bio[subject].columns = ['IBI']
    # Dropping duplicate numbers
    df_bio[subject].drop_duplicates(['IBI'], keep = 'first', inplace = True)
    # Taking the absolute number and multiplying by 1000, so now the RtoR are in ms
    df_bio[subject]['IBI'] = df_bio[subject]['IBI'].abs()*1000
    
    # Calculate duration
    rec_duration = df_bio[subject].index[-1] - df_bio[subject].index[0]
    ibi_duration = df_bio[subject].IBI.values.sum()/1000
    
    # Fill in duration columns in df_arti    
    df_arti['Rec_dur'][subject], df_arti['IBI_dur'][subject] = [rec_duration.total_seconds(), ibi_duration]
    print(subject, rec_duration.total_seconds(), ibi_duration)

print(df_arti)    
df_arti['Missing'] = df_arti['Rec_dur'] - df_arti['IBI_dur']
df_arti['PercentageMissing'] = df_arti['Missing'] / df_arti['Rec_dur']
    

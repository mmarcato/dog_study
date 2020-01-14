# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:24:55 2019

@author: marinara.marcato
"""

import os
import glob
import numpy as np
import pandas as pd
from glob import glob as gb 
from matplotlib import pyplot as plt

arti_dir  = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Artifact\\Study\\Polar'
arti_file = 'Summary_artifactCorrection_Results.xls'
cor_file = 'ArtifactCorrectedWithMethod_1.csv'
arti_path = gb('%s\\*\\%s' % (arti_dir, arti_file))

# Importing original df to extract timestamp and IBI
df_dir  = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Study'
subjects = os.listdir(df_dir)
df_file = '*_RR_*.csv' 

# Reading results from ArtiFACT
df_list= []
for path in arti_path: 
    df_list.append(pd.read_excel(path, index_col = 'FileName', usecols = ['FileName','NumberOfArtifacts','NumberofDataPoints']))
df_arti = pd.concat(df_list)
df_arti['PercentageError'] = df_arti['NumberOfArtifacts']/df_arti['NumberofDataPoints']*100
df_arti.index = df_arti.index.map(lambda x: str(x)[:-4].rsplit('_')[-1])

df_polar = {}
df_arti['Rec_dur'], df_arti ['IBI_dur'] = np.nan, np.nan

# Reading Bioharness RR df 
for subject in subjects:
    # Finding file names
    df_path = glob.glob('%s\\%s\\Polar\\%s' % (df_dir, subject, df_file))
    print (df_path)
    # Import bioharness df
    df_polar[subject] = pd.read_csv(df_path[0], index_col ='date' , usecols = ['date', ' rr'], parse_dates = True)
    # Renaming column from RtoR to IBI
    df_polar[subject].columns = ['IBI']


    # Calculate duration
    rec_duration = df_polar[subject].index[-1] - df_polar[subject].index[0]
    ibi_duration = df_polar[subject].IBI.values.sum()/1000
    
    # Fill in duration columns in df_arti    
    df_arti['Rec_dur'][subject], df_arti['IBI_dur'][subject] = [rec_duration.total_seconds(), ibi_duration]
    print(subject, rec_duration.total_seconds(), ibi_duration)


df_arti['Missing'] = df_arti['Rec_dur'] - df_arti['IBI_dur']
df_arti['PercentageMissing'] = df_arti['Missing'] / df_arti['Rec_dur']*100


arti_dir  = 'Z:\\Tyndall\\IGDB\\Observational Study\\Data Collection\\Artifact\\Study\\Polar'
arti_file = 'Summary_artifactCorrection_Results.xls'
cor_file = 'ArtifactCorrectedWithMethod_1'
arti_path = gb('%s\\*\\%s' % (arti_dir, arti_file))
df_cor = {}
for subject in subjects:    
    print(subject)
    cor_path = gb('%s\\*\\*%s_%s.xls' % (arti_dir, subject, cor_file))
    print(cor_path)
    df_cor[subject] = pd.read_excel(cor_path[0], header = None)
    df_cor[subject].columns = ['IBI']
    
    bins = np.linspace(200, 1200,50)

    plt.hist(df_polar[subject], bins, alpha=0.5, label='x')
    plt.hist(df_cor[subject], bins, alpha=0.5, label='y')
    plt.legend(loc='upper right')
    plt.show()

for subject in subjects:
    plt.figure()
    plt.plot(df_polar[subject]['IBI'].values, '-rx' ,label='polar')
    plt.plot(df_cor[subject]['IBI'].values, '-bo',label='corrected')
    plt.legend(loc='upper right')
    plt.title('%s' % (subject))
    plt.show()
    
print(df_arti.index, df_arti.PercentageError)

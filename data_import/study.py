import os
import pandas as pd
import numpy as np
import glob as gb                #find file names in the folders
import import_df 
import datetime as dt
import matplotlib.pyplot as plt


def import_summary(dir):
    dfs = pd.read_excel('%s\\Data Collection.xlsx' % dir, header = [0,1], sheet_name= ['Summary', 'Data', 'Measurements'])
    for key in list(dfs.keys()):
        dfs.get(key).set_index([('Info','Name')], inplace = True, drop = False)
        dfs.get(key).loc[: , ('Info', 'Intake')].fillna(method = 'ffill', inplace = True)
        dfs.get(key).rename(columns = {'Data Collection 1' : 'DC1', 'Data Collection 2' : 'DC2' }, inplace = True)
    
    # return Measurements 
    return pd.concat({'Info': dfs['Summary']['Info'],
                'DC1': dfs['Summary']['DC1'].join(dfs['Data']['DC1'].drop(['Date'], axis = 1)),
                'DC2': dfs['Summary']['DC2'].join(dfs['Data']['DC2'].drop(['Date'], axis = 1)),
                'Quest':dfs['Summary']['Questionnaire']},
                 axis = 1 )
        	
class Data_BT:

    def add_actigraph(self):
        if(self.info.Actigraph != 'Done'):
            print('%s: %s No Actigraph data ' % self.info.name, self.info.Date.strftime(format = '%Y-%m-%d'))
            return(np.NaN)
        else:
            df_actigraph = []
            p_name = os.path.join(base_dir, 'Actigraph', '%s' % self.info.Date.date())
            for bp in ['Back', 'Neck', 'Chest']:
                df_actigraph.append(pd.read_csv('%s\\%s (%s)-IMU.csv' % ( p_name, bp, self.info.Date.date() ),\
                    index_col = ['Timestamp'], skiprows = 10, parse_dates = [0],\
                    date_parser = lambda x: pd.to_datetime(x, format = '%Y-%m-%d %H:%M:%S.%f'))\
                    .drop(['Temperature'], axis = 1).between_time(self.info['BT Start'], self.info['BT Finish'])) 

            return (pd.concat(df_actigraph, axis = 1, keys = ['Back', 'Neck', 'Chest'], \
                        names = ['Body Parts', 'Sensor Axis']))

    def add_bioharness(self):    
        if(self.info.Bioharness != 'Done'):
            print('No Bioharness data for %s' % self.info.name)
            return(np.NaN)
        else: 
            p_name = os.path.join(base_dir , 'Bioharness', '%s' % self.info.Date.date())
            df_bioharness = []
            ts = dt.datetime(2019,1,1,0,0)
            # loop through the files for the data collection day
            for p in pd.to_datetime(os.listdir(p_name), format = '%Y_%m_%d-%H_%M_%S'): 
                # Import df if first ts is smaller than the BT finish time
                if p.time() < self.info['BT Finish']:
                    df = pd.read_csv( gb.glob('%s\\%s\\*_BB_RR.csv' % (p_name, p.strftime(format = '%Y_%m_%d-%H_%M_%S')))[0], index_col = 'Timestamp', parse_dates = True) 
                    # Append df if it is the first one to be appended
                    # after that Append if (last ts of previous df) is smaller than (first ts of the current df)
                    if (df_bioharness == []) | (ts < df.index[0]): 
                        df_bioharness.append(df) 
                        ts = df.index[-1]
                    else: 
                        print('%s:%s Bioharness files have duplicate information' % (self.info.name , self.info.Date.strftime(format = '%Y-%m-%d')))
            
            df_bioharness = pd.concat(df_bioharness)
            # select rows that are between BT start and finish time
            return (df_bioharness.between_time(self.info['BT Start'], self.info['BT Finish']))

    def add_polar (self): 
        if self.info.Polar != 'Done':
            self.polar = np.NaN
        else:
            print (self.info.name, self.info.Date.date())
            p_name = os.path.join(base_dir , 'Polar', '%s' % self.info.Date.date(), self.info.name)
            f_name = gb.glob('%s\\*_RR_%s*.csv' % (p_name, self.info.name))
            # Open each RR file and store in an array of df 
            df_polar = pd.concat([pd.read_csv(f) for f in f_name])               
            df_polar.loc[:,'date'] = pd.to_datetime(df_polar.loc[:,'date'])
            df_polar = df_polar.set_index('date', drop= True)                 
            df_polar.rename(columns = {' rr': 'RtoR'}, inplace = True)
            df_polar.rename(columns = {' since start': 'ss'}, inplace = True)
            #Check for duplicate files/timestamps
            return df_polar.between_time(self.info['BT Start'], self.info['BT Finish'])
 
    def __init__(self, info):
        # Error Check: No Date or BT status not Done
        if ((pd.isnull(info['Date'])) | (info['BT'] != 'Done')): 
            print('%s: %s BT not found' % (info.name , info['Date'].strftime(format = '%Y-%m-%d')) ) 
            self.info = np.NaN
        
        if info['BT Finish'] < info['BT Start']:
            print ('%s: %s BT Finish time before BT Start time' % (info.name, info['Date'].strftime(format = '%Y-%m-%d')))
            self.info = np.NaN

        else:
            self.info = info
            self.actigraph = self.add_actigraph()
            #self.bioharness = self.add_bioharness()
            #self.polar = self.add_polar()

class Data_Study:
    def __init__(self, summary):
        self.name = summary['Info']['Name']
        self.code = summary['Info']['Code']
        self.intake = summary['Info']['Intake']
        self.quest = summary['Quest']
        #self.meas = Data_Measurements()
        self.dc = {}
        self.dc['DC1'] = Data_BT(summary['DC1'])
        self.dc['DC2'] = Data_BT(summary['DC2'])

data = {}
base_dir = "D:\\Marinara\\Tyndall\\Study"
study = import_summary(base_dir)
for dog in ['Zeb', 'Eldin']:
    data[dog] = Data_Study(study.loc[dog])

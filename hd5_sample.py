##########################################################################
#Script to illustrate the use of HDF to store and retrieve data in python
# Read more about HDF at https://www.hdfgroup.org/
# Download free viewer after registering at the same website
# All the imports are not needed
# You may have to do pip install or conda install for some of these modules
##########################################################################


import sys
from collections import OrderedDict
import numpy as np
import pandas as pd
import re
from itertools import *
import h5py
import os
import shutil
import datetime
import csv


#df = pd.read_excel ('C:\Users\aruna\Downloads\anushree_prj\justice40dac_mapping_tool\DOE_J40_DACs_with_territories_March2022.xlsx')
#Wrting and reading from hdf is quite straigt forward
file_name = 'DOE_J40_DACs_with_territories_March2022.csv'
file_name = 'NHPD_Subsidy_Level.csv'
file_name_no_ext = file_name.rsplit( ".", 1 )[ 0 ]
file_name_hdf = f'{file_name_no_ext}.hdf5'
file_name_csv = file_name_no_ext+'.csv'
file_name_xls = file_name_no_ext+'.xlsx'
try:
    df = pd.read_csv(file_name)
    
except:
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if(line_count == 0):
                header = row
                df = pd.DataFrame(columns = header)
            else:
                d = dict(zip(header,row))
                #print(d)
                df = df.append(d, ignore_index=True, sort=False)
            line_count = line_count+1
            if(line_count == 4):
                print( type(row), len(row))
                break

df.to_hdf(file_name_hdf, key =file_name_no_ext, mode = 'w') 

df2 = pd.read_hdf(file_name_hdf)

print(df2)

##########################################################################
# Now some additional data verification in the  the sql_lit and the QCT_2022 files
#########################################################################
import sqlite3
from sqlite3 import Error

try:
    con = sqlite3.connect(r'C:\Users\aruna\Downloads\anushree_prj\justice40dac_mapping_tool\Data\gis_data.sqlite')
except Error as e:
   print(f'Error {e} while opening sql file')
df3 = pd.read_sql_query("SELECT * from DAC_percentiles_data", con)
df4 = pd.read_sql_query("SELECT * from Justice40DACIndices", con)
con.close()
print(df3.head(), df3.shape)
print(df4.head(), df4.shape)
try:
    df1 = pd.read_csv(r'C:\Users\aruna\Downloads\anushree_prj\QCT2022.CSV')
except:
    print('Cannot read csv file')
print(df1.head(), df1.shape)

df3_list = df3["GEOID"].values.tolist()
df4_list = df4["GEOID"].values.tolist()
df1_list = df1["fips"].values.astype(str).tolist()
df4_state_list = list(set(df4["state_code"].values.tolist()))


common_geo_ids = list(set(df3_list) & set(df4_list))
commmon_geo_ids2 = list(set(common_geo_ids) & set(df1_list))


print(len(df3_list),len(df4_list), len(df1_list), len(common_geo_ids), len(commmon_geo_ids2))
print(df3_list[:5])
print(df4_list[:5])
print(df1_list[:5])

#Now find the interesecting data frame for all 3 data sets
df5 = df4[df4['GEOID'].isin(commmon_geo_ids2)]
df5_list = df5["state_code"].values.tolist()
common_state_list = list(set(df5_list))
print(len(df4_state_list), df4_state_list)
print(len(common_state_list), common_state_list)
missing_states = list(set(df4_state_list) - set(common_state_list))
print(len(missing_states), missing_states)



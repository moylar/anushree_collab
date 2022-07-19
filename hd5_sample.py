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


          

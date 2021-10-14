# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:49:26 2021

@author: Mohammad Eslami 
Massachusetts Eye and Ear
Harvard Medical School
"""

#from PyVisualFields.RvisualFields import *
from PyVisualFields import RvisualFields
from PyVisualFields import Rvfprogression

import pandas 
import numpy as np
from matplotlib import pyplot as plt 

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri as rpyn

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

#import pandas as pd
#from rpy2.robjects.packages import importr
# import R's "base" package
#base = importr('base')

# import R's "utils" package
#utils = importr('utils')

# lib_vf = importr('visualFields')
lib_vfprogression = importr('vfprogression')


# Notice: for our df make sure to have date format as dateformat = "%Y-%m-%d"




################ Get samples
###### Get sample dataset as pandas dataframe 
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
RvisualFields.vfdesc(df_VFs_py)
# df_VFs_p = vfctrSunyiu24d2()
# df_VFs_p = vfpwgSunyiu24d2()
# df_VFs_p = vfctrSunyiu10d2()
# df_VFs_p = vfctrIowaPC26()
# df_VFs_p = vfctrIowaPeri()

df_VFs_py = Rvfprogression.data_vfseries()
df_VFs_py = Rvfprogression.data_vfi()
df_VFs_py = Rvfprogression.data_cigts()
df_VFs_py = Rvfprogression.data_plrnouri2012()
df_VFs_py = Rvfprogression.data_schell2014()




################################
# Get all normalized computations
td, tdp, gi, gip, pd, pdp, gh = RvisualFields.getallvalues(df_VFs_py) 

# another way individually:
td = RvisualFields.gettd(df_VFs_py) # get TD values
gi = RvisualFields.getgl(df_VFs_py) # get global indices
tdp = RvisualFields.gettdp(td) # get TD probability values
pd = RvisualFields.getpd(td) # get PD values
gh = RvisualFields.getgh(td) # get the general height
pdp = RvisualFields.getpdp(pd) # get PD probability values
gip = RvisualFields.getglp(gi) # get global indices probability values



######
###### Get sample dataset as R dataframe 
df_VFs_r= robjects.r['vfctrSunyiu24d2']
# lib_vf.vfwrite(df_VFs_r,'tmp1.csv', dateformat = "%Y-%m-%d")
# s = lib_vf.gettd(df_VFs_r)
# lib_vf.vfdesc(df_VFs_r)



######
###### plots 

# 
# vector=rpyn.ri2numpy(vector_R)
# R_float_vec = rpyn.numpy2rpy(td_single)

ind_td_start=df_VFs_py.columns.get_loc("l1")
ind_td_end=df_VFs_py.columns.get_loc("l54") 

td = td.fillna(0)
tdp = tdp.fillna(0)


td_values_single = td.iloc[0,ind_td_start:ind_td_end+1].to_numpy().astype(np.int8())
Rvfprogression.plotValues(td_values_single, title= 'Total Deviation',
                                 save=True, filename='td', fmt='png')

tdp_values_single = tdp.iloc[0,ind_td_start:ind_td_end+1].to_numpy().astype(np.float16())
Rvfprogression.plotProbabilities(tdp_values_single, title= 'Total Deviation Probablity',
                                 save=True, filename='tdp', fmt='png')



######
###### Analysis

df_VFs_py = Rvfprogression.data_cigts()
results = Rvfprogression.progression_cigts(df_VFs_py)
print(results)

df_VFs_py = Rvfprogression.data_plrnouri2012()
results = Rvfprogression.progression_plrnouri2012(df_VFs_py)
print(results)

df_VFs_py = Rvfprogression.data_vfi()
results = Rvfprogression.progression_vfi(df_VFs_py)
print(results)

df_VFs_py = Rvfprogression.data_schell2014()
results = Rvfprogression.progression_schell2014(df_VFs_py)
print(results)



################ Get the locmaps information
###### 
LocMaps=RvisualFields.locmaps()
X = LocMaps['p24d2']['coord']['x']
Y = LocMaps['p24d2']['coord']['y']


################ Get the normalization values
###### 
NormValues=RvisualFields.normvals()


# robjects.r('''
#            library(visualFields)
#            print(typeof(vfctrSunyiu24d2))
#            ''')
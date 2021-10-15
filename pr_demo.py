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
import os

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

lib_vf = importr('visualFields')
# lib_vfprogression = importr('vfprogression')
# lib_grdevices = importr('grDevices')


# Notice: for our df make sure to have date format as dateformat = "%Y-%m-%d"


################ Get samples
###### Get sample dataset as pandas dataframe 
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
RvisualFields.vfdesc(df_VFs_py)
df_VFs_p = RvisualFields.data_vfctrSunyiu24d2()
df_VFs_p = RvisualFields.data_vfpwgSunyiu24d2()
df_VFs_p = RvisualFields.data_vfctrSunyiu10d2()
df_VFs_p = RvisualFields.data_vfctrIowaPC26()
df_VFs_p = RvisualFields.data_vfctrIowaPeri()

df_VFs_py = Rvfprogression.data_vfseries()
df_VFs_py = Rvfprogression.data_vfi()
df_VFs_py = Rvfprogression.data_cigts()
df_VFs_py = Rvfprogression.data_plrnouri2012()
df_VFs_py = Rvfprogression.data_schell2014()




################################
# Get all normalized computations
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
df_td, df_tdp, df_gi, df_gip, df_pd, df_pdp, gh = RvisualFields.getallvalues(df_VFs_py) 

# another way individually:
df_td = RvisualFields.gettd(df_VFs_py) # get TD values
df_gi = RvisualFields.getgl(df_VFs_py) # get global indices
df_tdp = RvisualFields.gettdp(df_td) # get TD probability values
df_pd = RvisualFields.getpd(df_td) # get PD values
gh = RvisualFields.getgh(df_td) # get the general height
df_pdp = RvisualFields.getpdp(df_pd) # get PD probability values
df_gip = RvisualFields.getglp(df_gi) # get global indices probability values


######
###### Get sample dataset as R dataframe 
df_VFs_r= robjects.r['vfctrSunyiu24d2']
# lib_vf.vfwrite(df_VFs_r,'tmp1.csv', dateformat = "%Y-%m-%d")
# s = lib_vf.gettd(df_VFs_r)
# lib_vf.vfdesc(df_VFs_r)



##################
###### plots 

#################




td = np.random.randint(low=-35, high=5, size=(54,))
Rvfprogression.plotValues(td, title= 'Total Deviation',
                                 save=True, filename='td', fmt='png')
tdp = np.float16(np.random.rand(54)/10)
Rvfprogression.plotProbabilities(tdp, title= 'Total Deviation Probablity',
                                 save=True, filename='tdp', fmt='png')

# more realistic example:
ind_td_start=df_VFs_py.columns.get_loc("l1")
ind_td_end=df_VFs_py.columns.get_loc("l54") 

df_td = df_td.fillna(0)
df_tdp = df_tdp.fillna(0)

td = df_td.iloc[0,ind_td_start:ind_td_end+1].to_numpy().astype(np.int8())
print(td.shape)
print(type(td.shape))
tdp = df_tdp.iloc[0,ind_td_start:ind_td_end+1].to_numpy().astype(np.float16())
Rvfprogression.plotProbabilities(tdp, title= 'Total Deviation Probablity',
                                 save=True, filename='tdp', fmt='png')


#################

df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
vf = df_VFs_py.iloc[[0]] 

RvisualFields.vfplot(vf, type='s', save=True, filename='file', fmt='png')

##################
###### report generation

df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
vf = df_VFs_py.iloc[[0]] 
RvisualFields.vfsfa(vf, 'report.pdf')

# TODO: vfspa

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



# linear regression with global indices
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
df_VFs_py = df_VFs_py.loc[(df_VFs_py.id==1) & (df_VFs_py.eye=='OD')]
df_gi = RvisualFields.getgl(df_VFs_py) # get global indices
res = RvisualFields.glr(df_gi) #linear regression with global indices
print(res.keys())
intercept = res['int']
slope = res['sl']
se = res['se']
tval = res['tval']
pval = res['pval']


# pointwise linear regression (PLR) with TD values
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
df_VFs_py = df_VFs_py.loc[(df_VFs_py.id==1) & (df_VFs_py.eye=='OD')]
res = RvisualFields.plr(df_VFs_py) # pointwise linear regression (PLR) with TD values
print(res.keys())
intercept = res['int']
slope = res['sl']
se = res['se']
tval = res['tval']
pval = res['pval']
print(slope.keys())
arrObejct = np.array(list(slope.items()))
slope_numpy = np.float16(arrObejct[:,1])
print(slope_numpy)


# Permutation of PLR with TD values
df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
df_VFs_py = df_VFs_py.loc[(df_VFs_py.id==1) & (df_VFs_py.eye=='OD')]
res = RvisualFields.poplr(df_VFs_py) # Permutation of PLR with TD values
print(res.keys())


# TODO: pred is missed in conversion (not critical)

################ Get the locmaps information
###### 
LocMaps=RvisualFields.locmaps()
X = LocMaps['p24d2']['coord']['x']
Y = LocMaps['p24d2']['coord']['y']


################ Get the normalization values
###### 
NormValues=RvisualFields.normvals()
# TODO

################ calculate new normalization values and set it as default
###### 

# TODO
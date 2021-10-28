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

# lib_vf = importr('visualFields')
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





# another example to show required fields
df_VFs_py = Rvfprogression.data_vfseries()
columns2preserve = ['eyeid','righteye','age', 'duration', 
                     's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',
                      's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16',
                       's17', 's18', 's19', 's20', 's21', 's22', 's23', 's24',
                        's25', 's26', 's27', 's28', 's29', 's30', 's31', 's32',
                         's33', 's34', 's35', 's36', 's37', 's38', 's39', 's40',
                         's41',  's42', 's43', 's44', 's45', 's46', 's47', 's48',
                          's49', 's50', 's51', 's52', 's53', 's54']
df_VFs_py = df_VFs_py[columns2preserve]
df_VFs_py.rename(columns={'s1':'l1', 's2':'l2', 's3':'l3', 
                                      's4':'l4', 's5':'l5', 's6':'l6', 's7':'l7',
                                      's8':'l8', 's9':'l9', 's10':'l10',
                                      's11':'l11', 's12':'l12', 's13':'l13',
                                      's14':'l14', 's15':'l15','s16':'l16',
                                      's17':'l17', 's18':'l18', 's19':'l19',
                      's20':'l20', 's21':'l21', 's22':'l22',
                      's23':'l23', 's24':'l24','s25':'l25', 's26':'l26', 
                      's27':'l27', 's28':'l28', 's29':'l29', 's30':'l30', 
                      's31':'l31', 's32':'l32','s33':'l33', 's34':'l34',
                      's35':'l35', 's36':'l36', 's37':'l37', 's38':'l38', 
                      's39':'l39', 's40':'l40', 's41':'l41', 
                         's42':'l42', 's43':'l43', 's44':'l44', 's45':'l45', 
                         's46':'l46', 's47':'l47', 's48':'l48',
                          's49':'l49', 's50':'l50', 's51':'l51', 's52':'l52',
                          's53':'l53', 's54':'l54'}, inplace=True)
df_VFs_py.rename(columns={"eyeid": "id"}, inplace=True)
df_VFs_py = df_VFs_py.replace({'righteye':{0:'OS', 1:'OD'}})
df_VFs_py.rename(columns={"righteye": "eye"}, inplace=True)
df_VFs_py.insert(1, "time", '00:00:00')
df_VFs_py.insert(1, 'date', 1000)
df_VFs_py['date'] = pandas.to_datetime(df_VFs_py['date'], errors='coerce')
df_VFs_py.insert(1, 'type', 'SIT')
df_VFs_py.insert(1, 'fpr', 0)
df_VFs_py.insert(1, 'fnr', 0)
df_VFs_py.insert(1, 'fl', 0)
df_td, df_tdp, df_gi, df_gip, df_pd, df_pdp, gh = RvisualFields.getallvalues(df_VFs_py)


######
###### Get sample dataset as R dataframe 
df_VFs_r= robjects.r['vfctrSunyiu24d2']
# lib_vf.vfwrite(df_VFs_r,'tmp1.csv', dateformat = "%Y-%m-%d")
# s = lib_vf.gettd(df_VFs_r)
# lib_vf.vfdesc(df_VFs_r)



##################
###### plots 

######




td = np.random.randint(low=-35, high=5, size=(54,))
Rvfprogression.plotValues(td, title= 'Total Deviation',
                                 save=True, filename='td', fmt='png')

# more realistic example:

df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
df_td, df_tdp, df_gi, df_gip, df_pd, df_pdp, gh = RvisualFields.getallvalues(df_VFs_py)     
    
ind_td_start=df_VFs_py.columns.get_loc("l1")
ind_td_end=df_VFs_py.columns.get_loc("l54") 

df_td = df_td.fillna(0)
df_tdp = df_tdp.fillna(0)

td = df_td.iloc[0,ind_td_start:ind_td_end+1].to_numpy().astype(np.int8())
print(td.shape)
print(type(td.shape))
tdp = df_tdp.iloc[0, ind_td_start:ind_td_end+1].to_numpy().astype(np.float16())
Rvfprogression.plotProbabilities(tdp, title= 'Total Deviation Probablity',
                                 save=True, filename='tdp', fmt='png')  
# make sure to use plt.close('all'), if you are using it in a loop

########

df_VFs_py = RvisualFields.data_vfpwgRetest24d2()
vf = df_VFs_py.iloc[[0]] 

RvisualFields.vfplot(vf, type='s', save=True, filename='file', fmt='png')
RvisualFields.vfplot_s(vf, save=True, filename='file', fmt='png')
RvisualFields.vfplot_td(vf, save=True, filename='file', fmt='png')
RvisualFields.vfplot_pd(vf, save=True, filename='file', fmt='png')
RvisualFields.vfplot_tds(vf, save=True, filename='file', fmt='png')
RvisualFields.vfplot_pds(vf, save=True, filename='file', fmt='png')


df_VFs_py = RvisualFields.data_vfpwgSunyiu24d2()
filter1 = df_VFs_py.id=='sample1'
filter2 = df_VFs_py.eye=='OD'
df_vf_1 = df_VFs_py.loc[ filter1 & filter2]
RvisualFields.vfplotsparklines(df_vf_1, type='s', save=True, filename='file', fmt='png')
RvisualFields.vfplotsparklines_s(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vfplotsparklines_td(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vfplotsparklines_pd(df_vf_1, save=True, filename='file', fmt='png')

RvisualFields.vfplotplr(df_vf_1, type='s', save=True, filename='file', fmt='png')
RvisualFields.vfplotplr_s(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vfplotplr_td(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vfplotplr_pd(df_vf_1, save=True, filename='file', fmt='png')

RvisualFields.vflegoplot(df_vf_1, type='s', save=True, filename='file', fmt='png')
RvisualFields.vflegoplot_s(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vflegoplot_td(df_vf_1, save=True, filename='file', fmt='png')
RvisualFields.vflegoplot_pd(df_vf_1, save=True, filename='file', fmt='png')



# TODO: add colorbar of probablies



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
# TODO: show an progression example

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

# TODO: read load pdf xml dcm files
 
################ new R package progression
######
# TODO
# https://cran.r-project.org/web/packages/spCP/index.html
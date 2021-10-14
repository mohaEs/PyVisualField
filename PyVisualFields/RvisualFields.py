# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami 
Massachusetts Eye and Ear
Harvard Medical School
"""

"""
This file contains wrappers for R package: visualFields
https://cran.r-project.org/web/packages/visualFields/index.html
"""

import sys

import rpy2
import rpy2.robjects as robjects
import os

from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

from PyVisualFields.core import FnRecurList


# import R's "base" package
lib_base = importr('base')

# import R's "utils" package
lib_utils = importr('utils')

lib_vf = importr('visualFields')


'''  ###########################
Part I: Datasets 
'''

def data_vfctrSunyiu24d2():
    vfs_r = robjects.r['vfctrSunyiu24d2']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')
    return vfs_p

def data_vfctrSunyiu10d2():
    vfs_r = robjects.r['vfctrSunyiu10d2']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')
    return vfs_p

def data_vfpwgRetest24d2():
    vfs_r = robjects.r['vfpwgRetest24d2']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')
    return vfs_p

def data_vfpwgSunyiu24d2():
    vfs_r = robjects.r['vfpwgSunyiu24d2']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')
    return vfs_p

def data_vfctrIowaPC26():
    vfs_r = robjects.r['vfctrIowaPC26']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')    
    return vfs_p

def data_vfctrIowaPeri():
    vfs_r = robjects.r['vfctrIowaPeri']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    vfs_p.date = pd.to_datetime(vfs_p.date, unit='D', origin='1970-1-1')
    return vfs_p





'''  ###########################
part II: plots
'''








'''  ###########################
part III: computations
'''

def getallvalues(dataframe_VFs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    df_vf_r = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv') 
    
    # get the values #####################################
    TotalDev = lib_vf.gettd(df_vf_r) # get TD values
    GlobalIndices = lib_vf.getgl(df_vf_r) # get global indices
    
    TotoalDevProbs = lib_vf.gettdp(TotalDev) # get TD probability values
    PatternDev =lib_vf.getpd(TotalDev) # get PD values
    GeneralHeight = lib_vf.getgh(TotalDev) # get the general height
    
    PatternDevProbs = lib_vf.getpdp(PatternDev)  # get PD probability values
    
    GlobalIndicesProbs = lib_vf.getglp(GlobalIndices) # get global indices probability values
        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        TotalDev = ro.conversion.rpy2py(TotalDev)
        TotoalDevProbs = ro.conversion.rpy2py(TotoalDevProbs)
        GlobalIndices = ro.conversion.rpy2py(GlobalIndices)
        PatternDev = ro.conversion.rpy2py(PatternDev)
        PatternDevProbs = ro.conversion.rpy2py(PatternDevProbs)
        GlobalIndicesProbs = ro.conversion.rpy2py(GlobalIndicesProbs)
        GeneralHeight = ro.conversion.rpy2py(GeneralHeight)    
    TotalDev.date = pd.to_datetime(TotalDev.date, unit='D', origin='1970-1-1')
    TotoalDevProbs.date = pd.to_datetime(TotoalDevProbs.date, unit='D', origin='1970-1-1')
    GlobalIndices.date = pd.to_datetime(GlobalIndices.date, unit='D', origin='1970-1-1')
    PatternDev.date = pd.to_datetime(PatternDev.date, unit='D', origin='1970-1-1')
    PatternDevProbs.date = pd.to_datetime(PatternDevProbs.date, unit='D', origin='1970-1-1')
    GlobalIndicesProbs.date = pd.to_datetime(GlobalIndicesProbs.date, unit='D', origin='1970-1-1')
    
    return (TotalDev, TotoalDevProbs, GlobalIndices, 
            GlobalIndicesProbs, PatternDev, PatternDevProbs, GeneralHeight)
        
       
def gettd(dataframe_VFs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    df_vf_r = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################
    TotalDev = lib_vf.gettd(df_vf_r) # get TD values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        TotalDev = ro.conversion.rpy2py(TotalDev)
    TotalDev.date = pd.to_datetime(TotalDev.date, unit='D', origin='1970-1-1')
    return (TotalDev)
        

def gettdp(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    TotalDev = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################    
    TotoalDevProbs = lib_vf.gettdp(TotalDev) # get TD probability values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        TotoalDevProbs = ro.conversion.rpy2py(TotoalDevProbs)   
    TotoalDevProbs.date = pd.to_datetime(TotoalDevProbs.date, unit='D', origin='1970-1-1')    
    return TotoalDevProbs

    
def getpd(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    TotalDev = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################
    PatternDev =lib_vf.getpd(TotalDev) # get PD values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        PatternDev = ro.conversion.rpy2py(PatternDev)  
    PatternDev.date = pd.to_datetime(PatternDev.date, unit='D', origin='1970-1-1')    
    return PatternDev


def getpdp(dataframe_PDs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_PDs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    PatternDev = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################   
    PatternDevProbs = lib_vf.getpdp(PatternDev)  # get PD probability values           
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        PatternDevProbs = ro.conversion.rpy2py(PatternDevProbs)
    PatternDevProbs.date = pd.to_datetime(PatternDevProbs.date, unit='D', origin='1970-1-1')    
    return PatternDevProbs


              
def getgh(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    TotalDev = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################
    GeneralHeight = lib_vf.getgh(TotalDev) # get the general height            
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        GeneralHeight = ro.conversion.rpy2py(GeneralHeight)        
    return GeneralHeight


def getgl(dataframe_VFs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    df_vf_r = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################
    GlobalIndices = lib_vf.getgl(df_vf_r) # get global indices           
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        GlobalIndices = ro.conversion.rpy2py(GlobalIndices)
    GlobalIndices.date = pd.to_datetime(GlobalIndices.date, unit='D', origin='1970-1-1')   
    return GlobalIndices


def getglp(dataframe_GIs_py):       
    # Convert pandas to r compatibele with package ###########
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(dataframe_GIs_py)    
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    GlobalIndices = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')     
    # get the values #####################################    
    GlobalIndicesProbs = lib_vf.getglp(GlobalIndices) # get global indices probability values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        GlobalIndicesProbs = ro.conversion.rpy2py(GlobalIndicesProbs)  
    GlobalIndicesProbs.date = pd.to_datetime(GlobalIndicesProbs.date, unit='D', origin='1970-1-1')    
    return GlobalIndicesProbs




'''  ###########################
Part IV: values and helpers
'''

def locmaps():
    locs = robjects.r['locmaps']
    locs = FnRecurList(locs)
    return locs

def normvals():
    nvals = robjects.r['normvals']
    nvals = FnRecurList(nvals)
    return nvals


# def vfdesc(dataframe_VFs_R):
#     # print("Hello from a function") 
#     print(lib_vf.vfdesc(dataframe_VFs_R))


def vfdesc(dataframe_VFs_py):
    # print("Hello from a function") 
    print(dataframe_VFs_py.describe())    
    
    
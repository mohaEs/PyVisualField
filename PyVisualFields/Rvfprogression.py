# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami 
Massachusetts Eye and Ear
Harvard Medical School
"""

"""
this file contains wrappers for R package: vfprogression
https://cran.r-project.org/web/packages/vfprogression/index.html
"""

import sys

import rpy2
import rpy2.robjects as robjects
import os
from skimage import io
import matplotlib.pyplot as plt

from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas 
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import DataFrame, FloatVector, IntVector, StrVector, ListVector

from PyVisualFields.core import FnRecurList
from PyVisualFields.core import FnGetColumns



# import R's "base" package
lib_base = importr('base')

# import R's "utils" package
lib_utils = importr('utils')

lib_vf = importr('vfprogression')
lib_grdevices = importr('grDevices')

'''  ###########################
Part I: Datasets 
'''


def data_vfi():
    vfs_r = robjects.r['vf.vfi']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    return vfs_p 
    
def data_vfseries():
    vfs_r = robjects.r['vfseries']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    return vfs_p

def data_cigts():
    vfs_r = robjects.r['vf.cigts']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    return vfs_p

def data_plrnouri2012():
    vfs_r = robjects.r['vf.plr.nouri.2012']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    return vfs_p

def data_schell2014():
    vfs_r = robjects.r['vf.schell2014']
    with localconverter(ro.default_converter + pandas2ri.converter):
        vfs_p = ro.conversion.rpy2py(vfs_r) 
    return vfs_p


'''  ###########################
part II: plots
'''

######################
###########
######################
def plotProbabilities(values, title = 'Probability', 
                      save=False, filename='tmp', fmt='pdf'):
    
    length = len(values)
    columns = FnGetColumns(length)
        
    df = pandas.DataFrame(columns = columns)    
    for i in range(0,len(values)):
        df.loc[0, columns[i]] = values[i]      
    df.to_csv("tmp.csv", index=False) 
    
    lib_grdevices.png(file='tmp.png', width=480, height=480)    
    # plotting code here 
    robjects.r('''
    df <- read.csv(file = "tmp.csv")
    plotTdProbabilities(df, cex.tds = 1)
    ''')
    rtitle=robjects.r['title']
    rtitle(main=title, line = 3)
    lib_grdevices.dev_off()
    
    if save==True:
        
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=480, height=480)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
                  # plotting code here 
        robjects.r('''
        df <- read.csv(file = "tmp.csv")
        plotTdProbabilities(df, cex = 3)
        ''')
        rtitle=robjects.r['title']
        rtitle(main=title, line = 3)
        lib_grdevices.dev_off()          
        
    
    os.remove('tmp.csv') 
    # os.remove('tmp.png')
    
    img = io.imread('tmp.png', as_gray=True)  
    plt.figure()
    plt.imshow(img, cmap='gray')# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')            

    


######################
###########
######################
            
def plotValues(values, title = 'Deviation', 
                      save=False, filename='tmp', fmt='pdf'):
    
    length = len(values)
    columns = FnGetColumns(length)
        
    df = pandas.DataFrame(columns = columns)    
    for i in range(0,len(values)):
        df.loc[0, columns[i]] = values[i]      
    df.to_csv("tmp.csv", index=False) 
    
    lib_grdevices.png(file='tmp.png', width=256, height=256)    
    # plotting code here 
    robjects.r('''
    df <- read.csv(file = "tmp.csv")
    plotTDvalues(df, cex.tds = 1)
    ''')
    rtitle=robjects.r['title']
    rtitle(main=title, line = 3)
    lib_grdevices.dev_off()
    
    if save==True:
        
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=256, height=256)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
                  # plotting code here 
        robjects.r('''
        df <- read.csv(file = "tmp.csv")
        plotTDvalues(df, cex.tds = 1)
        ''')
        rtitle=robjects.r['title']
        rtitle(main=title, line = 3)
        lib_grdevices.dev_off()          
        
    
    os.remove('tmp.csv') 
    # os.remove('tmp.png')
    
    img = io.imread('tmp.png', as_gray=True)  
    plt.figure()
    plt.imshow(img, cmap='gray')# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')            

       

'''  ###########################
part III: Analysis
'''

def progression_cigts(df_VFs_py):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_VFs_r = ro.conversion.py2rpy(df_VFs_py)    
    rtitle = robjects.r['progression.cigts']
    results = tuple(rtitle(df_VFs_r))
    return results


def progression_plrnouri2012(df_VFs_py):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_VFs_r = ro.conversion.py2rpy(df_VFs_py)    
    rtitle = robjects.r['progression.plr.nouri.2012']
    results = tuple(rtitle(df_VFs_r))
    return results


def progression_vfi(df_VFs_py):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_VFs_r = ro.conversion.py2rpy(df_VFs_py)    
    rtitle = robjects.r['progression.vfi']
    results = tuple(rtitle(df_VFs_r))
    return results


def progression_schell2014(df_VFs_py):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_VFs_r = ro.conversion.py2rpy(df_VFs_py)    
    rtitle = robjects.r['progression.schell2014']
    results = tuple(rtitle(df_VFs_r))
    return results
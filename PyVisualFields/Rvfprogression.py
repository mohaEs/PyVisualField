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

from PyVisualFields.core import FnRecurList


# import R's "base" package
lib_base = importr('base')

# import R's "utils" package
lib_utils = importr('utils')

lib_vf = importr('vfprogression')
lib_grdevices = importr('grDevices')

'''  ###########################
Part I: Datasets 
'''





'''  ###########################
part II: plots
'''

def plotTdProbabilities(values, show=True, save=False, filename='tmp.png'):

    
    # columns=['tdp1', 'tdp2', 'tdp3', 'tdp4', 'tdp5', 'tdp6', 
    #                                'tdp7', 'tdp8', 'tdp9', 'tdp10', 'tdp11', 'tdp12', 
    #                                'tdp13', 'tdp14', 'tdp15', 'tdp16', 'tdp17', 'tdp18', 
    #                                'tdp19', 'tdp20', 'tdp21', 'tdp22', 'tdp23', 'tdp24', 
    #                                'tdp25', 'tdp26', 'tdp27', 'tdp28', 'tdp29', 'tdp30', 
    #                                'tdp31', 'tdp32', 'tdp33', 'tdp34', 'tdp35', 'tdp36', 
    #                                'tdp37', 'tdp38', 'tdp39', 'tdp40', 'tdp41', 'tdp42', 
    #                                'tdp43', 'tdp44', 'tdp45', 'tdp46', 'tdp47', 'tdp48', 
    #                                'tdp49', 'tdp50', 'tdp51', 'tdp52', 'tdp53', 'tdp54' 
    #                                ]
    if len(values)==54:
        columns=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
                                       'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
                                       'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 
                                       'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 
                                       'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 
                                       'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 
                                       'p37', 'p38', 'p39', 'p40', 'p41', 'p42', 
                                       'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 
                                       'p49', 'p50', 'p51', 'p52', 'p53', 'p54' 
                                       ]
    elif len(values)==52:      
        columns=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
                                       'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
                                       'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 
                                       'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 
                                       'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 
                                       'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 
                                       'p37', 'p38', 'p39', 'p40', 'p41', 'p42', 
                                       'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 
                                       'p49', 'p50', 'p51', 'p52' ]
    elif len(values)==74:
        columns=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
                                       'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
                                       'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 
                                       'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 
                                       'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 
                                       'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 
                                       'p37', 'p38', 'p39', 'p40', 'p41', 'p42', 
                                       'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 
                                       'p49', 'p50', 'p51', 'p52', 'p53', 'p54',
                                       'p55', 'p56', 'p57', 'p58', 'p59', 'p60',
                                       'p61', 'p62', 'p63', 'p64', 'p65', 'p66',
                                       'p67', 'p68', 'p69', 'p70', 'p71', 'p72',
                                       'p73','p74'                                       
                                       ]
    elif len(values)==76:
        columns=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
                                       'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
                                       'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 
                                       'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 
                                       'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 
                                       'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 
                                       'p37', 'p38', 'p39', 'p40', 'p41', 'p42', 
                                       'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 
                                       'p49', 'p50', 'p51', 'p52', 'p53', 'p54',
                                       'p55', 'p56', 'p57', 'p58', 'p59', 'p60',
                                       'p61', 'p62', 'p63', 'p64', 'p65', 'p66',
                                       'p67', 'p68', 'p69', 'p70', 'p71', 'p72',
                                       'p73','p74' , 'p75', 'p76'                                      
                                       ]
    else:
        raise NameError('Length of the input vector should be one of: 52, 54, 74, 76')
        
    df = pandas.DataFrame(columns = columns)    
    for i in range(0,len(values)):
        df.loc[0, columns[i]] = values[i]      
    df.to_csv("tmp.csv", index=False) 
    
    
    dpi=300
    lib_grdevices.png(file=filename, width=512, height=512)
    # plotting code here
    
    robjects.r('''
    df <- read.csv(file = "tmp.csv")
    plotTdProbabilities(df)
                ''')    
    lib_grdevices.dev_off()
    
    os.remove('tmp.csv')    
    
    if show==True:
        img = io.imread(filename, as_gray=True)    
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
                
    if save==False:
        os.remove(filename)    
    




'''  ###########################
part III: computations
'''
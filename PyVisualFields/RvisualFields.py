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
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3600987/
"""

import sys

import rpy2
import rpy2.robjects as robjects
import os
from skimage import io as skio
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader

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
lib_grdevices = importr('grDevices')



'''  ###########################
Utils
'''

def FnWriteLoadTmpCSV(df_vf_py):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_vf_r = ro.conversion.py2rpy(df_vf_py)   
    lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    df_vf_r = lib_vf.vfread('tmp0.csv')
    os.remove('tmp0.csv')   
    return df_vf_r

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

def vfplot(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'):
        
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_vf_py)    
            
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')   
    
    df_vf_r = FnWriteLoadTmpCSV(df_vf_py)
    
    lib_grdevices.png(file='tmp.png', width=350, height=350)    
    # plotting code here 
    lib_vf.vfplot(df_vf_r, type=type)
    lib_grdevices.dev_off()
    
    if save==True:
        
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=350, height=350)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
            
        # plotting code here 
        lib_vf.vfplot(df_vf_r, type=type)
        lib_grdevices.dev_off()          
            
    img = skio.imread('tmp.png')  
    plt.figure(figsize=(7, 7), dpi=100)
    if type=='s':
        plt.imshow(img, cmap='gray', interpolation='none', resample=False,)# , vmin=0, vmax=255
    else:
        plt.imshow(img, interpolation='none', resample=False)# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')            


def vfplot_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplot(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)
def vfplot_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplot(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)
def vfplot_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplot(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)
def vfplot_tds(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplot(df_vf_py, type='tds', save=save, filename=filename, fmt=fmt)    
def vfplot_pds(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplot(df_vf_py, type='pds', save=save, filename=filename, fmt=fmt)
    
    
    
    
def vfplotsparklines(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'):    
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_vf_py)    
            
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    
    df_vf_r = FnWriteLoadTmpCSV(df_vf_py)
    
    lib_grdevices.png(file='tmp.png', width=500, height=500)    
    # plotting code here 
    lib_vf.vfplotsparklines(df_vf_r, type=type, thr = 2,
                 width = 4,
                 height = 2)
    lib_grdevices.dev_off()
    
    if save==True:    
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=500, height=500)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
            
        # plotting code here 
        lib_vf.vfplotsparklines(df_vf_r, type=type, thr = 2,
                 width = 4,
                 height = 2)
        lib_grdevices.dev_off()          
            
    img = skio.imread('tmp.png')  
    plt.figure(figsize=(7, 7), dpi=100)
    if type=='s':
        plt.imshow(img, cmap='gray', interpolation='none', resample=False)# , vmin=0, vmax=255
    else:
        plt.imshow(img, interpolation='none', resample=False)# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')  


def vfplotsparklines_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplotsparklines(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)
def vfplotsparklines_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplotsparklines(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)
def vfplotsparklines_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):  
    vfplotsparklines(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)



def vfplotplr(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'): 
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_vf_py)    
            
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    
    df_vf_r = FnWriteLoadTmpCSV(df_vf_py)
    lib_grdevices.png(file='tmp.png', width=500, height=500)    
    # plotting code here 
    lib_vf.vfplotplr(df_vf_r, type=type)
    lib_grdevices.dev_off()
    
    if save==True:    
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=500, height=500)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
            
        # plotting code here 
        lib_vf.vfplotplr(df_vf_r, type=type)
        lib_grdevices.dev_off()          
            
    img = skio.imread('tmp.png')  
    plt.figure(figsize=(7, 7), dpi=100)
    if type=='s':
        plt.imshow(img, cmap='gray', interpolation='none', resample=False)# , vmin=0, vmax=255
    else:
        plt.imshow(img, interpolation='none', resample=False)# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')  


def vfplotplr_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplotplr(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)
def vfplotplr_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vfplotplr(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)
def vfplotplr_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):  
    vfplotplr(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)



def vflegoplot(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'):    
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_vf_py)    
            
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    df_vf_r = FnWriteLoadTmpCSV(df_vf_py)
    
    lib_grdevices.png(file='tmp.png', width=500, height=500)    
    # plotting code here 
    lib_vf.vflegoplot(df_vf_r, type=type)
    lib_grdevices.dev_off()
    
    if save==True:    
        if fmt=='pdf':
            lib_grdevices.pdf(file=filename+'.'+fmt) 
        elif fmt=='png':
            lib_grdevices.png(file=filename+'.'+fmt, width=500, height=500)        
        elif fmt=='svg':
            lib_grdevices.svg(file=filename+'.'+fmt) 
        else:
            raise NameError('format should be one of: pdf, svg, png')
            
        # plotting code here 
        lib_vf.vflegoplot(df_vf_r, type=type)
        lib_grdevices.dev_off()          
            
    img = skio.imread('tmp.png')  
    plt.figure(figsize=(7, 7), dpi=100)
    if type=='s':
        plt.imshow(img, cmap='gray', interpolation='none', resample=False)# , vmin=0, vmax=255
    else:
        plt.imshow(img, interpolation='none', resample=False)# , vmin=0, vmax=255
    plt.axis('off')     
    os.remove('tmp.png')  

def vflegoplot_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vflegoplot(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)
def vflegoplot_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):   
    vflegoplot(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)
def vflegoplot_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):  
    vflegoplot(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)


def vfsfa(df_vf_py, filename='report.pdf'):
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_vf_py)   
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')     
    df_vf_r = FnWriteLoadTmpCSV(df_vf_py)
    # validity = bool(lib_vf.vfisvalid(df_vf_r))
    # print(validity)
    # if validity==False:
    #     raise NameError('format of dataframe is not proper for visualFields package! check the documentations and sample data.')
        
    
    lib_grdevices.png(file='tmp.png', width=350, height=350)       
    lib_vf.vfsfa(df_vf_r, file=filename)
    lib_grdevices.dev_off()
    os.remove('tmp.png')     
    
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(30, 45, "Wrapped by PyVisualFields from:")
    can.save()
    
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(filename, "wb")
    output.write(outputStream)
    outputStream.close()
    
    
    

'''  ###########################
part III: computations
'''

def getallvalues(dataframe_VFs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv') 
    df_vf_r = FnWriteLoadTmpCSV(dataframe_VFs_py)
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
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')     
    df_vf_r = FnWriteLoadTmpCSV(dataframe_VFs_py)
    # get the values #####################################
    TotalDev = lib_vf.gettd(df_vf_r) # get TD values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        TotalDev = ro.conversion.rpy2py(TotalDev)
    TotalDev.date = pd.to_datetime(TotalDev.date, unit='D', origin='1970-1-1')
    return (TotalDev)
        

def gettdp(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # TotalDev = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')   
    TotalDev = FnWriteLoadTmpCSV(dataframe_TDs_py)
    # get the values #####################################    
    TotoalDevProbs = lib_vf.gettdp(TotalDev) # get TD probability values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        TotoalDevProbs = ro.conversion.rpy2py(TotoalDevProbs)   
    TotoalDevProbs.date = pd.to_datetime(TotoalDevProbs.date, unit='D', origin='1970-1-1')    
    return TotoalDevProbs

    
def getpd(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # TotalDev = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')     
    TotalDev = FnWriteLoadTmpCSV(dataframe_TDs_py)

    # get the values #####################################
    PatternDev =lib_vf.getpd(TotalDev) # get PD values        
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        PatternDev = ro.conversion.rpy2py(PatternDev)  
    PatternDev.date = pd.to_datetime(PatternDev.date, unit='D', origin='1970-1-1')    
    return PatternDev


def getpdp(dataframe_PDs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_PDs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # PatternDev = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')    
    PatternDev = FnWriteLoadTmpCSV(dataframe_PDs_py)

    # get the values #####################################   
    PatternDevProbs = lib_vf.getpdp(PatternDev)  # get PD probability values           
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        PatternDevProbs = ro.conversion.rpy2py(PatternDevProbs)
    PatternDevProbs.date = pd.to_datetime(PatternDevProbs.date, unit='D', origin='1970-1-1')    
    return PatternDevProbs


              
def getgh(dataframe_TDs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_TDs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # TotalDev = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')     
    TotalDev = FnWriteLoadTmpCSV(dataframe_TDs_py)
    
    # get the values #####################################
    GeneralHeight = lib_vf.getgh(TotalDev) # get the general height            
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        GeneralHeight = ro.conversion.rpy2py(GeneralHeight)        
    return GeneralHeight


def getgl(dataframe_VFs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_VFs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')    
    df_vf_r = FnWriteLoadTmpCSV(dataframe_VFs_py)
    # get the values #####################################
    GlobalIndices = lib_vf.getgl(df_vf_r) # get global indices           
    # Convert r to pandas #####################################
    with localconverter(ro.default_converter + pandas2ri.converter):
        GlobalIndices = ro.conversion.rpy2py(GlobalIndices)
    GlobalIndices.date = pd.to_datetime(GlobalIndices.date, unit='D', origin='1970-1-1')   
    return GlobalIndices


def getglp(dataframe_GIs_py):       
    # Convert pandas to r compatibele with package ###########
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(dataframe_GIs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # GlobalIndices = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')     
    GlobalIndices = FnWriteLoadTmpCSV(dataframe_GIs_py)    
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

# def vfisvalid():
    

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
    



'''  ###########################
Part IV: Analyis
'''
def glr(df_gi_py):
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_gi_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    df_vf_r = FnWriteLoadTmpCSV(df_gi_py) 
    
    res=lib_vf.glr(df_vf_r)
    res_py=FnRecurList(res)
    return(res_py)

def plr(df_VFs_py):
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_VFs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    
    df_vf_r = FnWriteLoadTmpCSV(df_VFs_py) 
    res=lib_vf.plr(df_vf_r)
    res_py = FnRecurList(res)
    return(res_py)


def poplr(df_VFs_py):
    # with localconverter(ro.default_converter + pandas2ri.converter):
    #     df_vf_r = ro.conversion.py2rpy(df_VFs_py)    
    # lib_vf.vfwrite(df_vf_r,'tmp0.csv', dateformat = "%Y-%m-%d")
    # df_vf_r = lib_vf.vfread('tmp0.csv')
    # os.remove('tmp0.csv')  
    
    df_vf_r = FnWriteLoadTmpCSV(df_VFs_py) 
    res=lib_vf.poplr(df_vf_r)
    res_py = FnRecurList(res)
    return(res_py)
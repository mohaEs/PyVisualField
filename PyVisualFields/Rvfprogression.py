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


from PyVisualFields.utils import FnRecurList
from PyVisualFields.utils import FnGetColumns



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
    
    lib_grdevices.png(file='tmp.png', width=350, height=350)    
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
            lib_grdevices.png(file=filename+'.'+fmt, width=350, height=350)        
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
    
    
    img = io.imread('tmp.png', as_gray=True)  
    plt.figure(figsize=(8, 6), dpi=80)
    plt.imshow(img, cmap='gray', interpolation='none', resample=False)# , vmin=0, vmax=255
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
    
    lib_grdevices.png(file='tmp.png', width=300, height=300)    
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
            lib_grdevices.png(file=filename+'.'+fmt, width=300, height=300)        
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
    
    
    img = io.imread('tmp.png', as_gray=True)  
    plt.figure(figsize=(8, 6), dpi=80)
    plt.imshow(img, cmap='gray', interpolation='none', resample=False)# , vmin=0, vmax=255
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


def progression_agis(df_VFs_py):
    ''' total deviation are requred as input '''

    df_VFs_py.to_csv('tmp.csv')
    robjects.r(''' 
        #### AGIS VF scoring

        # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994)
        agis.vf.sectors <- c(
            rep("upper", 10),
            "nasal", rep("upper", 7),
            "nasal", "nasal", rep("upper", 5), NA, "upper",
            "nasal", "nasal", rep("lower", 5), NA, "lower",
            "nasal", rep("lower", 7),
            rep("lower", 10))

        # neighboring VF locations within each of the three VF sectors,
        # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994)
        agis.neighbors <- list(
            c(2, 5, 6, 7), c(1, 3, 6:8), c(2, 4, 7:9), c(3, 8:10),
            c(1, 6, 12, 13), c(1, 2, 5, 7, 12:14), c(1:3, 6, 8, 13:15), c(2:4, 7, 9, 14:16), c(3, 4, 8, 10, 15:17), c(4, 9, 16:18),
            c(19, 20), c(5, 6, 13, 21, 22), c(5:7, 12, 14, 21:23), c(6:8, 13, 15, 22:24), c(7:9, 14, 16, 23:25), c(8:10, 15, 17, 24, 25), c(9, 10, 16, 18, 25, 27), c(10, 17, 27),
            c(11, 20, 28, 29), c(11, 19, 28, 29), c(12, 13, 22), c(12:14, 21, 23), c(13:15, 22, 24), c(14:16, 23, 25), c(15:17, 24), NA, c(17, 18),
            c(19, 20, 29, 37), c(19, 20, 28, 37), c(31, 38, 39), c(30, 32, 38:40), c(31, 33, 39:41), c(32, 34, 40:42), c(33, 41:43), NA, c(43, 44),
            c(28, 29), c(30, 31, 39, 45, 46), c(30:32, 38, 40, 45:47), c(31:33, 39, 41, 46:48), c(32:34, 40, 42, 47:49), c(33, 34, 41, 43, 48:50), c(34, 36, 42, 44, 49, 50), c(36, 43, 50),
            c(38, 39, 46, 51), c(38:40, 45, 47, 51, 52), c(39:41, 46, 48, 51:53), c(40:42, 47, 49, 52:54), c(41:43, 48, 50, 53, 54), c(42:44, 49, 54),
            c(45:47, 52), c(46:48, 51, 53), c(47:49, 52, 54), c(48:50, 53))

        agis.is.abnormal <- function(vf)
        # returns boolean vector of VF locations; 
        # TRUE: abnormal according to  AGIS 2 (Gaasterland et al., 1994)
        {
            x = if(length(vf)<54) c(vf[1:25], NA, vf[26:33], NA, vf[34:52])  else vf
            # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994):
            criteria <- -c(
                rep(9, 4),
                rep(8, 8), rep(6, 4), 8, 8,
                9, 8, rep(6, 5), NA, 8,
                9, 7, rep(5, 5), NA, 7,
                7, 7, rep(5, 4), rep(7, 12))
            vf <= criteria
        }

        agis.clusters <- function(vf)
        # return indices of clusters seperately for upper and lower hemifields and nasal sector
        {
            abn <- agis.is.abnormal(vf)
            clusterize <- function(clusterlist, unassigned)
            {
                if(length(unassigned) == 0)
                    clusterlist
                else
                {
                    if(length(clusterlist)==0)
                        clusterize(list(unassigned[1]), unassigned[-1])
                    else
                    {
                        cc = clusterlist[[length(clusterlist)]]
                        neighbors = unique(do.call(c, agis.neighbors[cc]))
                        newindices = unassigned %in% neighbors
                        newmembers = unassigned[newindices]
                        if(length(newmembers) == 0)
                        {
                            clusterlist[[length(clusterlist)+1]] = unassigned[1]
                            clusterize(clusterlist, unassigned[-1])
                        }
                        else
                        {
                            newunassigned = unassigned[!newindices]
                            clusterlist[[length(clusterlist)]] = sort(c(cc, newmembers))
                            clusterize(clusterlist, newunassigned)
                        }
                    }
                }
            }
            upperind = which(agis.vf.sectors == "upper" & abn)
            clusters.upper = clusterize(list(), upperind) 
            lowerind = which(agis.vf.sectors == "lower" & abn)
            clusters.lower = clusterize(list(), lowerind)
            nasalind = which(agis.vf.sectors == "nasal" & abn)
            clusters.nasal = clusterize(list(), nasalind)
            list(upper = clusters.upper, lower = clusters.lower, nasal = clusters.nasal)
        }

        agis.score <- function(tds)
        # according to  AGIS 2 (Gaasterland et al., 1994), p. 1448, and
        # Katz (1999), p. 392
        {
            n = length(tds)
            if(n<52)
                stop("agis.score: too few elements in TD vector (must be 52 or 54)")
            if(n>54)
            {
                # try to extract TDs from the data structure:
                if("td1" %in% names(tds))
                    tds <- tds[grep("^td[0-9]+", names(tds))]
                else
                    stop("agis.score: too many elements in TD vector (must be 52 or 54, or a data structure that contains names td1, ..., td54)")
            }
            
            vf <- if(length(tds)<54) c(tds[1:25], NA, tds[26:33], NA, tds[34:52])  else tds
            cl <- agis.clusters(vf)
            score = 0
            # nasal:
            if(length(cl$nasal) > 0)
            {
                if(length(cl$nasal) == 1 && length(cl$nasal[[1]]) < 3) # nasal step if it's restricted to one hemifield:
                {
                    if(all(cl$nasal[[1]] %in% c(11, 19, 20)) || all(cl$nasal[[1]] %in% c(28, 29, 37)))
                        score = score+1
                } else # "nasal defect"
                    score = score+ifelse(any(sapply(cl$nasal, length) > 2), 1, 0)

                lessequal12 <- which(vf[which(agis.vf.sectors == "nasal")] <= -12)
                if(length(lessequal12)>=4) score = score+1
            }
            # hemifields:
            score.locations <- function(clusterlist)
            {
                score = 0
                number.per.cluster <- sapply(clusterlist, length)
                # only clusters >= 3:
                greatereq3 <- which(number.per.cluster>=3)
                if(length(greatereq3) > 0)
                {
                    s = sum(number.per.cluster[greatereq3])
                    if(s>=3) score = score+1
                    if(s>=6) score = score+1
                    if(s>=13) score = score+1
                    if(s>=20) score = score+1
                    # add even more if half of the locations exceed a certain value:
                    loc3 <- vf[ do.call(c, clusterlist[greatereq3]) ]
                    l3h <- length(loc3)/2
                    addone <- function(criterion)
                        ifelse(length(which(loc3<=-criterion)) >= l3h, 1, 0)
                    score = score+addone(12)
                    score = score+addone(16)
                    score = score+addone(20)
                    score = score+addone(24)
                    score = score+addone(28)
                }
                score 
            }
            score <- score + score.locations(cl$upper)
            score <- score + score.locations(cl$lower)
            score
        }


        progression.agis.base <- function(measmatrix)
        # AGIS VF progression : 
            # Rabiolo, A., Morales, E., Mohamed, L., Capistrano, V., Kim, J.H., Afifi, A., Yu, F., Coleman, A.L., Nouri-Mahdavi, K. and Caprioli, J., 2019. 
            # Comparison of methods to detect and measure glaucomatous visual field progression. 
            # Translational vision science & technology, 8(5), pp.2-2.

        # measmatrix: columns must contain the 52 TD probs and yearsfollowed,
        #    rows represent the single measurements
        # returns "stable", "worsening", or "improving"
        # note: If a VF series is temporarily improving and
        #    temporarily worsening, it is assumed to be "stable" overall
        {
            if(nrow(measmatrix)<5)
                stop("agis.progression: at least 5 VFs required")
            tds = measmatrix[, grep("^td[0-9]+", colnames(measmatrix))]
            agis.scores = apply(tds, 1, agis.score)
            baseline = agis.scores[1]
            
            tl = rev(agis.scores[-(1)] - baseline)
            results = ifelse(tl >= 4, "worsening", ifelse(tl <= -3, "improving", "stable"))
            final = unique(results[1:3])
            
            if(length(final) == 1)
            {
                inter = results[-(1:3)]
                # if ever a VF series is both "improving" and "worsening" for single VFs, we assume it to be stable overall
                ifelse(any(inter != "stable" & inter != final), "stable", final)
            } else "stable"	
        }

        progression.agis <- function(measmatrix)
        {
        if(!("eyeid" %in% colnames(measmatrix)))
        {
            warning("progression.cigts: input does not contain column named 'eyeid'. Assuming that all measurements are from the same eye.")
            measmatrix$eyeid <- 1
        }

        method = 'agis'

        do.call(
            "rbind",
            by(
            measmatrix,
            measmatrix$eyeid,
            function(eye)
                sapply(
                method,
                function(meth) do.call(paste("progression", meth, 'base', sep="."), list(eye))),  #Dian, added 'base' 5.16.2019
            simplify=F))

        }
    

        df_VF_r <- read.csv(file = 'tmp.csv')
        agis_prpgression_results = progression.agis(df_VF_r)
#       df_VF_r$AGIS_Score <- AGIS_Score
        write.csv(agis_prpgression_results, 'tmp.csv', row.names=FALSE)  

    ''')

    df_res = pandas.read_csv('tmp.csv')   
    
    try: # suppose we have two eyes of the subject
        results = tuple([df_res.agis[0], df_res.agis[1]])
    except: # we have only one eye
        results = tuple([df_res.agis[0]])

    os.remove('tmp.csv')
    return results 


def get_score_AGIS(df_VF_py):
    ''' total deviation are requred as input '''

    if type(df_VF_py.iloc[[0]])==pandas.core.series.Series:
       df_VF_py=pandas.DataFrame(df_VF_py).transpose()

    df_VF_py.to_csv('tmp.csv')
    robjects.r(''' 

        #### AGIS VF scoring

        # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994)
        agis.vf.sectors <- c(
            rep("upper", 10),
            "nasal", rep("upper", 7),
            "nasal", "nasal", rep("upper", 5), NA, "upper",
            "nasal", "nasal", rep("lower", 5), NA, "lower",
            "nasal", rep("lower", 7),
            rep("lower", 10))

        # neighboring VF locations within each of the three VF sectors,
        # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994)
        agis.neighbors <- list(
            c(2, 5, 6, 7), c(1, 3, 6:8), c(2, 4, 7:9), c(3, 8:10),
            c(1, 6, 12, 13), c(1, 2, 5, 7, 12:14), c(1:3, 6, 8, 13:15), c(2:4, 7, 9, 14:16), c(3, 4, 8, 10, 15:17), c(4, 9, 16:18),
            c(19, 20), c(5, 6, 13, 21, 22), c(5:7, 12, 14, 21:23), c(6:8, 13, 15, 22:24), c(7:9, 14, 16, 23:25), c(8:10, 15, 17, 24, 25), c(9, 10, 16, 18, 25, 27), c(10, 17, 27),
            c(11, 20, 28, 29), c(11, 19, 28, 29), c(12, 13, 22), c(12:14, 21, 23), c(13:15, 22, 24), c(14:16, 23, 25), c(15:17, 24), NA, c(17, 18),
            c(19, 20, 29, 37), c(19, 20, 28, 37), c(31, 38, 39), c(30, 32, 38:40), c(31, 33, 39:41), c(32, 34, 40:42), c(33, 41:43), NA, c(43, 44),
            c(28, 29), c(30, 31, 39, 45, 46), c(30:32, 38, 40, 45:47), c(31:33, 39, 41, 46:48), c(32:34, 40, 42, 47:49), c(33, 34, 41, 43, 48:50), c(34, 36, 42, 44, 49, 50), c(36, 43, 50),
            c(38, 39, 46, 51), c(38:40, 45, 47, 51, 52), c(39:41, 46, 48, 51:53), c(40:42, 47, 49, 52:54), c(41:43, 48, 50, 53, 54), c(42:44, 49, 54),
            c(45:47, 52), c(46:48, 51, 53), c(47:49, 52, 54), c(48:50, 53))

        agis.is.abnormal <- function(vf)
        # returns boolean vector of VF locations; 
        # TRUE: abnormal according to  AGIS 2 (Gaasterland et al., 1994)
        {
            x = if(length(vf)<54) c(vf[1:25], NA, vf[26:33], NA, vf[34:52])  else vf
            # according to Fig. 1 in AGIS 2 (Gaasterland et al., 1994):
            criteria <- -c(
                rep(9, 4),
                rep(8, 8), rep(6, 4), 8, 8,
                9, 8, rep(6, 5), NA, 8,
                9, 7, rep(5, 5), NA, 7,
                7, 7, rep(5, 4), rep(7, 12))
            vf <= criteria
        }

        agis.clusters <- function(vf)
        # return indices of clusters seperately for upper and lower hemifields and nasal sector
        {
            abn <- agis.is.abnormal(vf)
            clusterize <- function(clusterlist, unassigned)
            {
                if(length(unassigned) == 0)
                    clusterlist
                else
                {
                    if(length(clusterlist)==0)
                        clusterize(list(unassigned[1]), unassigned[-1])
                    else
                    {
                        cc = clusterlist[[length(clusterlist)]]
                        neighbors = unique(do.call(c, agis.neighbors[cc]))
                        newindices = unassigned %in% neighbors
                        newmembers = unassigned[newindices]
                        if(length(newmembers) == 0)
                        {
                            clusterlist[[length(clusterlist)+1]] = unassigned[1]
                            clusterize(clusterlist, unassigned[-1])
                        }
                        else
                        {
                            newunassigned = unassigned[!newindices]
                            clusterlist[[length(clusterlist)]] = sort(c(cc, newmembers))
                            clusterize(clusterlist, newunassigned)
                        }
                    }
                }
            }
            upperind = which(agis.vf.sectors == "upper" & abn)
            clusters.upper = clusterize(list(), upperind) 
            lowerind = which(agis.vf.sectors == "lower" & abn)
            clusters.lower = clusterize(list(), lowerind)
            nasalind = which(agis.vf.sectors == "nasal" & abn)
            clusters.nasal = clusterize(list(), nasalind)
            list(upper = clusters.upper, lower = clusters.lower, nasal = clusters.nasal)
        }

        agis.score <- function(tds)
        # according to  AGIS 2 (Gaasterland et al., 1994), p. 1448, and
        # Katz (1999), p. 392
        {
            n = length(tds)
            if(n<52)
                stop("agis.score: too few elements in TD vector (must be 52 or 54)")
            if(n>54)
            {
                # try to extract TDs from the data structure:
                if("td1" %in% names(tds))
                    tds <- tds[grep("^td[0-9]+", names(tds))]
                else
                    stop("agis.score: too many elements in TD vector (must be 52 or 54, or a data structure that contains names td1, ..., td54)")
            }
            
            vf <- if(length(tds)<54) c(tds[1:25], NA, tds[26:33], NA, tds[34:52])  else tds
            cl <- agis.clusters(vf)
            score = 0
            # nasal:
            if(length(cl$nasal) > 0)
            {
                if(length(cl$nasal) == 1 && length(cl$nasal[[1]]) < 3) # nasal step if it's restricted to one hemifield:
                {
                    if(all(cl$nasal[[1]] %in% c(11, 19, 20)) || all(cl$nasal[[1]] %in% c(28, 29, 37)))
                        score = score+1
                } else # "nasal defect"
                    score = score+ifelse(any(sapply(cl$nasal, length) > 2), 1, 0)

                lessequal12 <- which(vf[which(agis.vf.sectors == "nasal")] <= -12)
                if(length(lessequal12)>=4) score = score+1
            }
            # hemifields:
            score.locations <- function(clusterlist)
            {
                score = 0
                number.per.cluster <- sapply(clusterlist, length)
                # only clusters >= 3:
                greatereq3 <- which(number.per.cluster>=3)
                if(length(greatereq3) > 0)
                {
                    s = sum(number.per.cluster[greatereq3])
                    if(s>=3) score = score+1
                    if(s>=6) score = score+1
                    if(s>=13) score = score+1
                    if(s>=20) score = score+1
                    # add even more if half of the locations exceed a certain value:
                    loc3 <- vf[ do.call(c, clusterlist[greatereq3]) ]
                    l3h <- length(loc3)/2
                    addone <- function(criterion)
                        ifelse(length(which(loc3<=-criterion)) >= l3h, 1, 0)
                    score = score+addone(12)
                    score = score+addone(16)
                    score = score+addone(20)
                    score = score+addone(24)
                    score = score+addone(28)
                }
                score 
            }
            score <- score + score.locations(cl$upper)
            score <- score + score.locations(cl$lower)
            score
        }


        df_VF_r <- read.csv(file = 'tmp.csv')
        AGIS_Score = agis.score(df_VF_r)
        df_VF_r$AGIS_Score <- AGIS_Score
        write.csv(df_VF_r, 'tmp.csv', row.names=FALSE)          

    ''')

    df_res = pandas.read_csv('tmp.csv')
    score = df_res.AGIS_Score.values
    score = score[0]
    os.remove('tmp.csv')
    return score 




def get_score_CIGTS(df_VF_py):
    ''' total deviation probabilities are requred as input '''

    if type(df_VF_py.iloc[[0]])==pandas.core.series.Series:
       df_VF_py=pandas.DataFrame(df_VF_py).transpose()

    df_VF_py.to_csv('tmp.csv')
    robjects.r(''' 

            #### CIGTS VF scoring (Musch et al., 1999; Gillespie et al., 2003)

            # neighboring VF locations within each hemifield,
            # according to Gillespie et al. (2003), with 52 indices
            cigts.neighbors <- list(
                c(2, 5, 6, 7), c(1, 3, 6:8), c(2, 4, 7:9), c(3, 8:10),
                c(1, 6, 11:13), c(1, 2, 5, 7, 12:14), c(1:3, 6, 8, 13:15), c(2:4, 7, 9, 14:16), c(3, 4, 8, 10, 15:17), c(4, 9, 16:18),
                c(5, 12, 19:21), c(5, 6, 11, 13, 20:22), c(5:7, 12, 14, 21:23), c(6:8, 13, 15, 22:24), c(7:9, 14, 16, 23:25), c(8:10, 15, 17, 24, 25), c(9, 10, 16, 18, 25, 26), c(10, 17, 26),
                c(11, 20), c(11, 12, 19, 21), c(11:13, 20, 22), c(12:14, 21, 23), c(13:15, 22, 24), c(14:16, 23, 25), c(15:17, 24), c(17, 18),
                c(28, 35), c(27, 29, 35, 36), c(28, 30, 35:37), c(29, 31, 36:38), c(30, 32, 37:39), c(31, 33, 38:40), c(32, 39:41), c(41, 42),
                c(27:29, 36, 43), c(28:30, 35, 37, 43, 44), c(29:31, 36, 38, 43:45), c(30:32, 37, 39, 44:46), c(31:33, 38, 40, 45:47), c(32, 33, 39, 41, 46:48), c(33, 34, 40, 42, 47, 48), c(34, 41, 48),
                c(35:37, 44, 49), c(36:38, 43, 45, 49, 50), c(37:39, 44, 46, 49:51), c(38:40, 45, 47, 50:52), c(39:41, 46, 48, 51, 52), c(40:42, 47, 52),
                c(43:45, 50), c(44:46, 49, 51), c(45:47, 50, 52), c(46:48, 51))

            cigts.score <- function(tdprobs)
            # CIGTS VF scoring (Gillespie et al., 2003)
            # tdprobs: vector of length 52 representing the TD probabilities (between 0.005 and 1)
            # example from Gillespie: 
            #    tdprobs = c(0.05, 0.02, 0.05, rep(1,8), 0.05, 0.02, rep(1,7), 0.01, 0.005, rep(1,6), 0.02, rep(1,17), 0.01, rep(1,5))
            #    cigts.score(tdprobs) -> 0.7692308
            {
                n = length(tdprobs)
                if(n<52)
                    stop("cigts.score: too few elements in TD prob vector (must be 52 or 54)")
                if(n>54)
                {
                    # try to extract TDs from the data structure:
                    if("tdp1" %in% names(tdprobs))
                        tdprobs <- tdprobs[grep("^tdp[0-9]+", names(tdprobs))]
                    else
                        stop("cigts.score: too many elements in TD prob vector (must be 52 or 54, or a data structure that contains names td1, ..., td54)")
                }
                if(n==54)
                    tdprobs <- tdprobs[-c(26,35)]
                
                pweights <- ifelse(tdprobs==0.005, 4, ifelse(tdprobs==0.01, 3, ifelse(tdprobs==0.02, 2, ifelse(tdprobs==0.05, 1, 0))))
                # calculate the weights relevant for scoring:
                get.effective.weight <- function(weight, neighbors)
                {
                    neighborweights = sort(pweights[neighbors], decreasing=T)
                    min(neighborweights[2], weight)
                }
                effective.weights <- mapply(get.effective.weight, pweights, cigts.neighbors)
                sum(effective.weights)/10.4
            }

        df_VF_r <- read.csv(file = 'tmp.csv')
        cigts_Score = cigts.score(df_VF_r)
        df_VF_r$cigts_Score <- cigts_Score
        write.csv(df_VF_r, 'tmp.csv', row.names=FALSE)          

    ''')

    df_res = pandas.read_csv('tmp.csv')
    score = df_res.cigts_Score.values
    score = score[0]
    os.remove('tmp.csv')

    return score 


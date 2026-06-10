# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 18:00:28 2021

@author: MOhammad Eslami
"""

try: 
    import rpy2
    print('===> rpy2 version: ', rpy2.__version__)
    
    import rpy2.robjects as robjects

    from rpy2.robjects.packages import importr
    # import rpy2's package module
    import rpy2.robjects.packages as rpackages
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
    print('===> R and rpy2 work fine!')
except:
    print('===> Something is wrong: rpy2 does not work fine or is not available!')



# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 18:00:28 2021

@author: Mohammad Eslami
"""

try: 
    import rpy2
    print('===> rpy2 version: ', rpy2.__version__)
    
    from rpy2.robjects.packages import importr
    # import rpy2's package module
    import rpy2.robjects.packages as rpackages
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
except:
    print('===> Something is wrong: rpy2 is not available!')

# import R's "base" package
lib_base = importr('base')

# import R's "utils" package
lib_utils = importr('utils')

# select a mirror for R packages
lib_utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# R package names
packnames = ('visualFields', 'vfprogression')

# Selectively install what needs to be install.
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    lib_utils.install_packages(StrVector(names_to_install))

try: 
    lib_vf = importr('visualFields')
    print('===> visualFields R package is installed/loaded successfully!')
    lib_vfprogression = importr('vfprogression')
    print('===> vfprogression R package is installed/loaded successfully!')
    
except:
    print('===> Something is wrong: R packages are not available!')
    

# try:
#     import PyVisualFields
#     print('===> PyVisualFields package loaded successfully!')
# except:
#     print('===> Something is wrong: PyVisualFields is not available!')
    

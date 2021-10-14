# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami 
Massachusetts Eye and Ear
Harvard Medical School
"""

"""
this file contains wrappers for R package: visualFields
"""


from rpy2.robjects.vectors import DataFrame, FloatVector, IntVector, StrVector, ListVector
import numpy
from collections import OrderedDict




# # convert R list to python dictionaty recurssively
# def FnRecurList(data):
#     rDictTypes = [ DataFrame,ListVector]
#     rArrayTypes = [FloatVector,IntVector]
#     rListTypes=[StrVector]
#     if type(data) in rDictTypes:
#         return OrderedDict(zip(data.names, [FnRecurList(elt) for elt in data]))
#     elif type(data) in rListTypes:
#         return [FnRecurList(elt) for elt in data]
#     elif type(data) in rArrayTypes:
#         return numpy.array(data)
#     else:
#         if hasattr(data, "rclass"): # An unsupported r class
#             raise KeyError('Could not proceed, type {} is not defined'.format(type(data)))
#         else:
#             return data # We reached the end of recursion
        
        
def FnRecurList(data):
    rDictTypes = [ DataFrame,ListVector]
    rArrayTypes = [FloatVector,IntVector]
    rListTypes=[StrVector]
    if type(data) in rDictTypes:
        return OrderedDict(zip(data.names, [FnRecurList(elt) for elt in data]))
    elif type(data) in rListTypes:
        return [FnRecurList(elt) for elt in data]
    elif type(data) in rArrayTypes:
        return numpy.array(data)
    else:
        if hasattr(data, "rclass"): # An unsupported r class
            #raise KeyError('Could not proceed, type {} is not defined'.format(type(data)))
            print('WARNING: inner function ignored: ')
            # print('Could not proceed, type {} is not defined'.format(type(data)))
        else:
            return data # We reached the end of recursion
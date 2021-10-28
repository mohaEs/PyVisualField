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


from rpy2.robjects.vectors import DataFrame, FloatVector, IntVector, StrVector, ListVector, Matrix
#from rpy2_Matrix import Matrix
import numpy
from collections import OrderedDict


def FnGetColumns(length):
    
    if length==54:
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
    elif length==52:      
        columns=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
                                       'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
                                       'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 
                                       'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 
                                       'p25', 'p26', 'p27', 'p28', 'p29', 'p30', 
                                       'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 
                                       'p37', 'p38', 'p39', 'p40', 'p41', 'p42', 
                                       'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 
                                       'p49', 'p50', 'p51', 'p52' ]
    elif length==74:
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
    elif length==76:
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
        
    return columns
    

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
    rArrayTypes = [FloatVector,IntVector, Matrix]
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
        

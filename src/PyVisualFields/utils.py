# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami
Massachusetts Eye and Ear
Harvard Medical School

@contributor: Bharath Erusalagandi (Python implementation)
"""

"""
this file contains required utilities
"""
import os
import numpy

# Optional rpy2.
# If rpy2 is absent the R-type branches are simply unreachable.
try:
    from rpy2.robjects.vectors import (
        DataFrame, FloatVector, IntVector, StrVector, ListVector, Matrix
    )
    _RPY2_TYPES_AVAILABLE = True
except Exception:
    # Define stub classes so type-checks in FnRecurList don't NameError.
    class _Stub:
        pass
    DataFrame = FloatVector = IntVector = StrVector = ListVector = Matrix = _Stub
    _RPY2_TYPES_AVAILABLE = False
from collections import OrderedDict



######################3
##########################3



import re
import pandas as pd


POINT_ALIASES = {
    "sens": ["l", "s", "sen", "sens", "sensitivity", "vf"],
    "td": ["td"],
    "pd": ["pd"],
    "tdp": ["tdp"],
    "pdp": ["pdp"],
}

CANON_PREFIX = {
    "sens": "l",
    "td": "td",
    "pd": "pd",
    "tdp": "tdp",
    "pdp": "pdp",
}

META_ALIASES = {
    "patientid": ["patientid", "patient_id", "patient", "patid", "pid", "subjectid", "mrn", "id"],
    "eyeid": ["eyeid", "eye_id", "eye", "laterality"],
    "date": ["date", "examdate", "testdate", "vfdate"],
    "age": ["age"],
    "yearsfollowed": ["yearsfollowed", "years_followed", "followup", "time"],
    "md": ["md", "mtd"],
    "psd": ["psd"],
    "ght": ["ght"],
    "vfi": ["vfi"],
    "fpr": ["fpr"],
    "fnr": ["fnr"],
    "fl": ["fl"],
    "duration": ["duration"],
}


def _normalize_name(x):
    return re.sub(r"[_\-\s]+", "", str(x).lower())


def _rename_meta_cols(df):
    rename = {}
    norm_to_col = {_normalize_name(c): c for c in df.columns}

    for canon, aliases in META_ALIASES.items():
        for alias in aliases:
            key = _normalize_name(alias)
            if key in norm_to_col:
                rename[norm_to_col[key]] = canon
                break

    return df.rename(columns=rename)


def _normalize_eye(x):
    if pd.isna(x):
        return x
    x = str(x).strip().upper()

    if x in {"R", "RIGHT", "OD"}:
        return "OD"
    if x in {"L", "LEFT", "OS"}:
        return "OS"
    if x in {"B", "BOTH", "OU"}:
        return "OU"

    return x


def _cols_by_prefix(df, prefixes):
    out = []

    for c in df.columns:
        cs = str(c)

        for p in prefixes:
            pattern = rf"^{re.escape(p)}[_\-\s]?(\d+)$"
            m = re.match(pattern, cs, flags=re.IGNORECASE)

            if m:
                out.append((int(m.group(1)), c))
                break

    return [c for _, c in sorted(out)]


def canonicalize_vf_row(row, **kwargs):
    df = canonicalize_vf_df(
        pd.DataFrame([row]),
        **kwargs
    )
    return df.iloc[0]

def canonicalize_vf_df(
    df,
    include=None,
    fill_age=60.0,
    sort_by_date=True,
):
    df = _rename_meta_cols(df.copy())

    used = set()
    blocks = {}

    if include is None:
        include = tuple(POINT_ALIASES.keys())

    for block in include:
        cols = _cols_by_prefix(df, POINT_ALIASES[block])

        if len(cols) in (52, 54):
            prefix = CANON_PREFIX[block]
            new_cols = [f"{prefix}{i}" for i in range(1, len(cols) + 1)]

            blocks[block] = pd.DataFrame(
                {
                    new: pd.to_numeric(df[old], errors="coerce")
                    for old, new in zip(cols, new_cols)
                },
                index=df.index,
            )
            used.update(cols)

        elif len(cols) > 0:
            raise ValueError(
                f"{block}: found {len(cols)} columns, expected 52 or 54."
            )

    meta = df[[c for c in df.columns if c not in used]].copy()
    out = pd.concat(
        [meta] + [blocks[k] for k in include if k in blocks],
        axis=1,
    )

    if "eyeid" in out.columns:
        out["eyeid"] = out["eyeid"].apply(_normalize_eye)

    if "age" not in out.columns and "sens" in include:
        out["age"] = fill_age

    if "age" in out.columns:
        out["age"] = pd.to_numeric(out["age"], errors="coerce").fillna(fill_age)

    if sort_by_date and "date" in out.columns:
        sort_key = pd.to_datetime(out["date"], errors="coerce")
        if sort_key.notna().any():
            out = (
                out.assign(_sort_date=sort_key)
                .sort_values("_sort_date")
                .drop(columns="_sort_date")
            )

    return out.reset_index(drop=True)


######################3
##########################3





def has_block(df, prefix, min_cols=52):
    """
    Check whether dataframe contains a complete VF block.

    Examples
    --------
    has_block(df, "l")
    has_block(df, "td")
    has_block(df, "pd")
    has_block(df, "tdp")
    has_block(df, "pdp")
    """
    cols = [
        c for c in df.columns
        if c.startswith(prefix)
        and c[len(prefix):].isdigit()
    ]

    return len(cols) >= min_cols


def has_sensitivity(df):
    return has_block(df, "l")

def has_td(df):
    return has_block(df, "td")

def has_pd(df):
    return has_block(df, "pd")

def has_tdp(df):
    return has_block(df, "tdp")

def has_pdp(df):
    return has_block(df, "pdp")

def vf_blocks(df):
    return {
        "sens": has_block(df, "l"),
        "td": has_block(df, "td"),
        "pd": has_block(df, "pd"),
        "tdp": has_block(df, "tdp"),
        "pdp": has_block(df, "pdp"),
    }

def missing_blocks(df):
    return [
        name
        for name, present in vf_blocks(df).items()
        if not present
    ]


#############################
###############################3



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
    


        
        
def FnRecurList(data):
    # print('WARNING: inner R functions ignored')
    
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
            
            # print('WARNING: inner R functions ignored')
            error = 1
            
            # print('Could not proceed, type {} is not defined'.format(type(data)))
        else:
            return data # We reached the end of recursion
        

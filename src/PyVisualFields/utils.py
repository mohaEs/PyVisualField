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
    "sens": ["l", "s", "sen", "sens", "sensitivity"],
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

# META_ALIASES = {
#     "patientid": ["patientid", "patient_id", "patient", "patid", "pid", "subjectid", "mrn", "id"],
#     "eyeid": ["eyeid", "eye_id", "eye", "laterality"],
#     "date": ["date", "examdate", "testdate", "vfdate"],
#     "age": ["age"],
#     "yearsfollowed": ["yearsfollowed", "years_followed"],
#     "md": ["md", "mtd"],    
#     "psd": ["psd"],
#     "ght": ["ght"],
#     "vfi": ["vfi"],
#     "fpr": ["fpr"],
#     "fnr": ["fnr"],
#     "fl": ["fl"],
#     "duration": ["duration"],
# }


META_ALIASES = {
    "patientid": [
        "patientid", "patient_id", "patient",
        "patid", "pid", "subjectid", "mrn", "id"
    ],

    "eyeid": [
        "eyeid", "eye_id", "eye", "laterality"
    ],

    "date": [
        "date", "examdate", "testdate", "vfdate"
    ],

    "age": ["age"],

    "yearsfollowed": [
        "yearsfollowed", "years_followed"
    ],

    # Global indices
    "md": [
        "md", "mtd"
    ],
    "mdprob": [
        "mdp", "mdprob", "md_p"
    ],

    "psd": [
        "psd"
    ],
    #PSD probability
    "psdprob": [
        "psd_p", "psdprob", "psdp"
    ],

    "ght": [
        "ght"
    ],

    "vfi": [
        "vfi"
    ],

    "msens": [
        "msens", "ms", "meansensitivity"
    ],

    "ssens": [
        "ssens", "ss", "sdsensitivity"
    ],

    "tmd": [
        "tmd"
    ],

    "tsd": [
        "tsd"
    ],

    "pmd": [
        "pmd"
    ],

    "gh": [
        "gh", "generalheight"
    ],

    # Reliability
    "fpr": [
        "fpr"
    ],

    "fnr": [
        "fnr"
    ],

    "fl": [
        "fl"
    ],

    "duration": [
        "duration"
    ],
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


#################33
######################33
#####################


def investigate_vf_df(df):
    """
    Inspect a canonicalized VF dataframe and report available metadata,
    pointwise blocks, global indices, and progression fields.
    """

    from PyVisualFields.Deviation_Analysis import _get_point_cols


    info = {}

    # ---------- Metadata ----------
    meta_candidates = [
        "patientid", "eyeid", "date", "age",
        "yearsfollowed", "duration"
    ]

    info["metadata"] = {
        c: (c in df.columns)
        for c in meta_candidates
    }

    # ---------- Pointwise blocks ----------
    blocks = {
        "sensitivity": "l",
        "total_deviation": "td",
        "pattern_deviation": "pd",
        "total_deviation_probability": "tdp",
        "pattern_deviation_probability": "pdp",
    }

    info["blocks"] = {}

    for name, prefix in blocks.items():
        cols = _get_point_cols(df, prefix)

        info["blocks"][name] = {
            "present": len(cols) > 0,
            "n_locations": len(cols),
        }

    # ---------- Global indices ----------
    global_indices = [
        "md", "mdprob", "psd", "psdprob",  "ght", "vfi",
        "msens", "ssens",
        "tmd", "tsd",
        "pmd", "gh"
    ]

    info["global_indices"] = {
        c: (c in df.columns)
        for c in global_indices
    }

    # ---------- Reliability ----------
    reliability = [
        "fpr",
        "fnr",
        "fl",
    ]

    info["reliability"] = {
        c: (c in df.columns)
        for c in reliability
    }

    # ---------- Summary ----------
    info["n_rows"] = len(df)
    info["n_columns"] = len(df.columns)

    return info


def print_vf_summary(df):
    info = investigate_vf_df(df)

    print("=== VF Data Summary ===")
    print(f"Rows: {info['n_rows']}")
    print(f"Columns: {info['n_columns']}")

    print("\nPointwise blocks:")
    for k, v in info["blocks"].items():
        mark = "✓" if v["present"] else "✗"
        print(f"  {mark} {k} ({v['n_locations']} locations)")

    print("\nGlobal indices:")
    for k, v in info["global_indices"].items():
        mark = "✓" if v else "✗"
        print(f"  {mark} {k}")

    print("\nMetadata:")
    for k, v in info["metadata"].items():
        mark = "✓" if v else "✗"
        print(f"  {mark} {k}")
    
    


##########################
########################333
#######################3

import numpy as np
BLIND_SPOT_1BASED = (26, 35)
# blind spot positions if 54 elements (1-indexed 26 and 35 -> 0-indexed 25 and 34)


def _expand_52_to_54(block_df, prefix):
    """
    Expand 52 VF locations to 54 by inserting NaN blind-spot columns
    at 1-based locations 26 and 35.

    If not 52 columns, return unchanged.
    """

    if block_df.shape[1] != 52:
        return block_df

    out = pd.DataFrame(index=block_df.index)

    src_idx = 0

    for i in range(1, 55):
        col = f"{prefix}{i}"

        if i in BLIND_SPOT_1BASED:
            out[col] = np.nan
        else:
            out[col] = block_df.iloc[:, src_idx]
            src_idx += 1

    return out


def canonicalize_vf_df(
    df,
    include=None,
    fill_age=None,
    sort_byDateAge=False
):
    df = _rename_meta_cols(df.copy())

    used = set()
    blocks = {}

    if include is None:
        include = tuple(POINT_ALIASES.keys())

    for block in include:
        cols = _cols_by_prefix(df, POINT_ALIASES[block])

        if len(cols) == 0:
            continue



        prefix = CANON_PREFIX[block]

        tmp = pd.DataFrame(
            {
                f"{prefix}{i}": pd.to_numeric(df[old], errors="coerce")
                for i, old in enumerate(cols, start=1)
            },
            index=df.index,
        )

        blocks[block] = _expand_52_to_54(tmp, prefix)
        used.update(cols)


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
        out["age"] = pd.to_numeric(out["age"], errors="coerce")
        if fill_age is not None:
            out["age"] = out["age"].fillna(fill_age)

    if sort_byDateAge:

        sorted_ok = False

        if "date" in out.columns:

            sort_key = pd.to_datetime(out["date"], errors="coerce")

            if sort_key.notna().any():

                out = out.assign(_sort_date=sort_key)

                sort_cols = []

                if "patientid" in out.columns:
                    sort_cols.append("patientid")

                if "eyeid" in out.columns:
                    sort_cols.append("eyeid")

                sort_cols.append("_sort_date")

                out = (
                    out.sort_values(sort_cols)
                    .drop(columns="_sort_date")
                )

                sorted_ok = True

        if not sorted_ok and "age" in out.columns:

            sort_cols = []

            if "patientid" in out.columns:
                sort_cols.append("patientid")

            if "eyeid" in out.columns:
                sort_cols.append("eyeid")

            sort_cols.append("age")

            out = out.sort_values(sort_cols)
    
    return out.reset_index(drop=True)

######################3
##########################3


from PyVisualFields.Deviation_Analysis import (
    py_getnv, py_setnv, py_setdefaults, py_normvals, py_get_info_normvals,
    py_nvgenerate, py_setnv_custom,
    py_gettd, py_getgh, py_getpd, py_gettdp, py_getpdp,
    py_getgl, py_getglp, py_getallvalues,
)

def compute_missing_blocks(df):

    new_blocks = []

    if not has_td(df):
        df_td = py_gettd(df)
        td_cols = [c for c in df_td.columns if c.startswith("td")]
        new_blocks.append(df_td[td_cols])

    if not has_pd(df):
        df_pd = py_getpd(df if has_td(df) else pd.concat([df] + new_blocks, axis=1))
        pd_cols = [c for c in df_pd.columns if c.startswith("pd")]
        new_blocks.append(df_pd[pd_cols])

    if not has_tdp(df):
        df_tdp = py_gettdp(df if has_td(df) else pd.concat([df] + new_blocks, axis=1))
        tdp_cols = [c for c in df_tdp.columns if c.startswith("tdp")]
        new_blocks.append(df_tdp[tdp_cols])

    if not has_pdp(df):
        working_df = pd.concat([df] + new_blocks, axis=1)
        df_pdp = py_getpdp(working_df)
        pdp_cols = [c for c in df_pdp.columns if c.startswith("pdp")]
        new_blocks.append(df_pdp[pdp_cols])

    if new_blocks:
        df = pd.concat([df] + new_blocks, axis=1)

    return df


######################3
##########################3

import matplotlib.pyplot as plt
import fitz

# def Fn_report(df_vf, fName, format='pdf'):

#     from PyVisualFields import vfprogression
#     from PyVisualFields import visualFields

#     ###########
#     sensCol = _cols_by_prefix(df_vf, ['l'])
#     sens = df_vf.loc[0, sensCol].to_numpy().astype(np.float16())
#     # print(sens)
#     vfprogression.plotValues(sens, title= 'Sensitivity',
#                                  save=True, filename='s_tmp', fmt='pdf', show=False)

#     ##############
    
#     ind_tdp_start= df_vf.columns.get_loc("tdp1")
#     ind_tdp_end= df_vf.columns.get_loc("tdp54") 
#     tdp = df_vf.iloc[0, ind_tdp_start:ind_tdp_end+1].to_numpy().astype(np.float16())
#     #this function also needs values, not dataframe
#     vfprogression.plotProbabilities(tdp, title= 'Total Deviation Probablity',
#                                     save=True, filename='tdp_tmp', fmt='pdf', show=False)  

#     ##############
    
#     ind_pdp_start= df_vf.columns.get_loc("pdp1")
#     ind_pdp_end= df_vf.columns.get_loc("pdp54") 
#     pdp = df_vf.iloc[0, ind_pdp_start:ind_pdp_end+1].to_numpy().astype(np.float16())
#     #this function also needs values, not dataframe
#     vfprogression.plotProbabilities(pdp, title= 'Pattern Deviation Probablity',
#                                     save=True, filename='pdp_tmp', fmt='pdf', show=False)  


#     ###############

#     visualFields.vfplot_s(df_vf, title='Sensitivity', save=True, 
#                           filename='file', fmt='pdf', show=False) # types: s, td,pd, tds, pds
#     visualFields.vfplot_td(df_vf, title='Total Deviaton and Probability', save=True, 
#                            filename='tdtmp', fmt='pdf', show=False) # alias for vfplot(type='td')
#     visualFields.vfplot_pd(df_vf, title='Pattern Deviaton and Probability', save=True, 
#                            filename='pdtmp', fmt='pdf', show=False) # alias for vfplot(type='pd')


#     ##############

#     # 1. List of your 6 different PDF files
#     pdf_paths = [
#         'file.pdf', 'tdtmp.pdf', 'pdtmp.pdf',
#         's_tmp.pdf', 'tdp_tmp.pdf', 'pdp_tmp.pdf'
#     ]

#     out = fitz.open()
#     page = out.new_page(width=1200, height=900)

#     margin = 30
#     gap = 20
#     cell_w = (1200 - 2*margin - 2*gap) / 3
#     cell_h = (900 - 2*margin - gap) / 2

#     for i, path in enumerate(pdf_paths):
#         row = i // 3
#         col = i % 3

#         x0 = margin + col * (cell_w + gap)
#         y0 = margin + row * (cell_h + gap)
#         rect = fitz.Rect(x0, y0, x0 + cell_w, y0 + cell_h)

#         src = fitz.open(path)
#         page.show_pdf_page(rect, src, 0)  # page 0, vector-preserved
#         src.close()

    
#     out.save(fName)
#     out.close()
#     print(f"Saved report to {fName}")

#     for f in pdf_paths:
#         if os.path.exists(f):
#             os.remove(f)
#             #print(f"Deleted: {f}")
#         # else:
#         #     print(f"Not found: {f}")

def Fn_report(df_vf, fName, format='pdf'):

    import os
    import fitz
    import numpy as np

    from PyVisualFields import vfprogression
    from PyVisualFields import visualFields

    ############################################################
    # Generate component PDFs
    ############################################################

    sensCol = _cols_by_prefix(df_vf, ['l'])
    sens = df_vf.loc[0, sensCol].to_numpy().astype(np.float16)

    vfprogression.plotValues(
        sens,
        title='Sensitivity',
        save=True,
        filename='s_tmp',
        fmt='pdf',
        show=False
    )

    ind_tdp_start = df_vf.columns.get_loc("tdp1")
    ind_tdp_end   = df_vf.columns.get_loc("tdp54")

    tdp = df_vf.iloc[
        0,
        ind_tdp_start:ind_tdp_end + 1
    ].to_numpy().astype(np.float16)

    vfprogression.plotProbabilities(
        tdp,
        title='Total Deviation Probability',
        save=True,
        filename='tdp_tmp',
        fmt='pdf',
        show=False
    )

    ind_pdp_start = df_vf.columns.get_loc("pdp1")
    ind_pdp_end   = df_vf.columns.get_loc("pdp54")

    pdp = df_vf.iloc[
        0,
        ind_pdp_start:ind_pdp_end + 1
    ].to_numpy().astype(np.float16)

    vfprogression.plotProbabilities(
        pdp,
        title='Pattern Deviation Probability',
        save=True,
        filename='pdp_tmp',
        fmt='pdf',
        show=False
    )

    visualFields.vfplot_s(
        df_vf,
        title='Sensitivity',
        save=True,
        filename='file',
        fmt='pdf',
        show=False
    )

    visualFields.vfplot_td(
        df_vf,
        title='Total Deviation and Probability',
        save=True,
        filename='tdtmp',
        fmt='pdf',
        show=False
    )

    visualFields.vfplot_pd(
        df_vf,
        title='Pattern Deviation and Probability',
        save=True,
        filename='pdtmp',
        fmt='pdf',
        show=False
    )

    ############################################################
    # PDF Montage
    ############################################################

    pdf_paths = [
        'file.pdf',
        'tdtmp.pdf',
        'pdtmp.pdf',
        's_tmp.pdf',
        'tdp_tmp.pdf',
        'pdp_tmp.pdf'
    ]

    page_width = 1200
    page_height = 950

    out = fitz.open()
    page = out.new_page(width=page_width, height=page_height)

    ############################################################
    # Header information
    ############################################################

    row = df_vf.iloc[0]

    patientID = row.get("patientID", "")
    age       = row.get("age", "")
    date      = row.get("date", "")
    vfi       = row.get("vfi", np.nan)
    md        = row.get("md", np.nan)
    psd       = row.get("psd", np.nan)

    def fmt(v, n=2):
        try:
            if np.isnan(v):
                return "NA"
            return f"{float(v):.{n}f}"
        except:
            return str(v)

    page.insert_text(
        (30, 30),
        "Visual Field Report",
        fontsize=20,
        fontname="helv"
    )

    page.insert_text(
        (30, 60),
        f"Patient ID: {patientID}      Age: {age}      Date: {date}",
        fontsize=14,
        fontname="helv"
    )

    page.insert_text(
        (30, 85),
        (
            f"VFI: {fmt(vfi,1)}%      "
            f"MD: {fmt(md,2)} dB      "
            f"PSD: {fmt(psd,2)} dB"
        ),
        fontsize=14,
        fontname="helv"
    )

    page.draw_line(
        fitz.Point(30, 105),
        fitz.Point(page_width - 30, 105),
        width=1
    )

    ############################################################
    # Layout for 6 PDF panels
    ############################################################

    margin = 30
    gap = 20

    header_height = 120

    cell_w = (
        page_width
        - 2 * margin
        - 2 * gap
    ) / 3

    cell_h = (
        page_height
        - header_height
        - 2 * margin
        - gap
    ) / 2

    for i, path in enumerate(pdf_paths):

        row_idx = i // 3
        col_idx = i % 3

        x0 = margin + col_idx * (cell_w + gap)

        y0 = (
            header_height
            + margin
            + row_idx * (cell_h + gap)
        )

        rect = fitz.Rect(
            x0,
            y0,
            x0 + cell_w,
            y0 + cell_h
        )

        src = fitz.open(path)

        page.show_pdf_page(
            rect,
            src,
            0
        )

        src.close()

    ############################################################
    # Save report
    ############################################################

    out.save(fName)
    out.close()

    print(f"Saved report to {fName}")

    ############################################################
    # Cleanup temporary PDFs
    ############################################################

    for f in pdf_paths:
        if os.path.exists(f):
            os.remove(f)

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
        

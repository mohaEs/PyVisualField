# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami
Massachusetts Eye and Ear
Harvard Medical School

@contributor: Bharath Erusalagandi (Python implementation)
"""

"""
this file contains wrappers for R package: vfprogression
https://cran.r-project.org/web/packages/vfprogression/index.html
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas

from PyVisualFields.utils import canonicalize_vf_df, canonicalize_vf_row

# Optional R bridge.
try:
    import rpy2  # noqa: F401
    _R_AVAILABLE = True
except Exception:
    _R_AVAILABLE = False






'''  ###########################
Part I: Datasets 
'''

def data_vfi():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vf.vfi.pkl')
    vfs_p = pandas.read_pickle(path)
    return vfs_p
    
def data_vfseries():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfseries.pkl')
    vfs_p = pandas.read_pickle(path)
    return vfs_p

def data_cigts():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vf.cigts.pkl')
    vfs_p = pandas.read_pickle(path)
    return vfs_p

def data_plrnouri2012():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vf.plr.nouri.2012.pkl')
    vfs_p = pandas.read_pickle(path)
    return vfs_p

def data_schell2014():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vf.schell2014.pkl')
    vfs_p = pandas.read_pickle(path)
    return vfs_p





'''  ###########################
part II: plots
'''

######################
###########
######################

# Standard HFA 24-2 grid coordinates (54 locations, degree positions)
# Blind spots at indices 25 and 34 (0-indexed) are marked as None
_GRID_24D2 = [
    (-9,21),(-3,21),(3,21),(9,21),
    (-15,15),(-9,15),(-3,15),(3,15),(9,15),(15,15),
    (-21,9),(-15,9),(-9,9),(-3,9),(3,9),(9,9),(15,9),(21,9),
    (-27,3),(-21,3),(-15,3),(-9,3),(-3,3),(3,3),(9,3),None,(21,3),
    (-27,-3),(-21,-3),(-15,-3),(-9,-3),(-3,-3),(3,-3),(9,-3),None,(21,-3),
    (-21,-9),(-15,-9),(-9,-9),(-3,-9),(3,-9),(9,-9),(15,-9),(21,-9),
    (-15,-15),(-9,-15),(-3,-15),(3,-15),(9,-15),(15,-15),
    (-9,-21),(-3,-21),(3,-21),(9,-21),
]

# Dot-cluster offset patterns for each probability symbol (integer grid steps).
_P002_OFFSETS = [
    (-2, -4), (0, -4), (2, -4), (-3, -3), (-1, -3), (-2, -2), (0, -2),
    (-3, -1), (1, -1), (-2, 0), (2, 0), (-3, 1), (-1, 1), (1, 1),
    (0, 2), (2, 2), (1, 3),
]
_P001_OFFSETS = [
    (-3, -4), (-2, -4), (0, -4), (1, -4), (2, -4),
    (-3, -3), (-2, -3), (-1, -3), (1, -3), (3, -3),
    (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
    (-1, -1), (0, -1), (2, -1), (3, -1),
    (-3, 0), (-2, 0), (0, 0), (1, 0),
    (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
    (-3, 2), (-2, 2), (-1, 2), (1, 2),
    (-2, 3), (1, 3),
]
_P005_OFFSETS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

_GRID_SCALE = 6.0  # degree spacing between grid locations


def _draw_prob_symbol(ax, cx, cy, p):
    """Draw the probability symbol for value p at grid position (cx, cy).

    Midpoint thresholds handle float16 noise in discrete probability codes.
    """
    import matplotlib.patches as mpatches

    def _dot(x, y, side):
        ax.add_patch(mpatches.Rectangle((x - side / 2, y - side / 2), side, side,
                                        facecolor='black', edgecolor='none'))

    def _cluster(offsets, step, side):
        for ox, oy in offsets:
            _dot(cx + ox * step, cy + oy * step, side)

    if p <= 0.0075:
        d = 0.16 * _GRID_SCALE
        ax.add_patch(mpatches.Rectangle((cx - d, cy - d), 2 * d, 2 * d,
                                        facecolor='black', edgecolor='none'))
    elif p <= 0.015:
        _cluster(_P001_OFFSETS, step=0.04 * _GRID_SCALE, side=0.26)
    elif p <= 0.035:
        _cluster(_P002_OFFSETS, step=0.04 * _GRID_SCALE, side=0.17)
    elif p <= 0.075:
        _cluster(_P005_OFFSETS, step=0.08 * _GRID_SCALE, side=0.17)
    else:
        _dot(cx, cy, side=0.17)


def _draw_prob_legend(ax):
    """Draw a compact legend of the five probability symbols (lower-right)."""
    import matplotlib.patches as mpatches

    x0, x1, y0, y1 = 18.0, 24.0, -24.0, -16.5
    ax.add_patch(mpatches.Rectangle((x0, y0), x1 - x0, y1 - y0,
                                    facecolor='white', edgecolor='black',
                                    linewidth=0.6))
    rows = [
        (0.5, 'p ≥ 0.05'),
        (0.05, 'p < 0.05'),
        (0.02, 'p < 0.02'),
        (0.01, 'p < 0.01'),
        (0.005, 'p < 0.005'),
    ]
    sym_x, lbl_x = 19.0, 20.2
    ys = [-17.2, -18.6, -20.0, -21.4, -22.8]
    for (pval, label), y in zip(rows, ys):
        _draw_prob_symbol(ax, sym_x, y, pval)
        ax.text(lbl_x, y, label, ha='left', va='center', fontsize=6.5)


def plotProbabilities(values, title='Probability',
                      save=False, filename='tmp', fmt='pdf'):
    """Classic symbol-only probability map with graded dot-cluster stipple symbols."""
    vals = np.array(values, dtype=float)

    if len(vals) == 52:
        vals = np.concatenate([vals[:25], [np.nan], vals[25:33], [np.nan], vals[33:]])

    fig, ax = plt.subplots(figsize=(7, 7))

    for i, pos in enumerate(_GRID_24D2):
        if pos is None or i >= len(vals):
            continue
        p = vals[i]
        if np.isnan(p):
            continue
        cx, cy = pos
        _draw_prob_symbol(ax, cx, cy, p)

    # Crosshair dividers
    ax.axvline(x=0, color='black', linewidth=1.0)
    ax.axhline(y=0, color='black', linewidth=1.0)

    ax.set_xlim(-30, 24)
    ax.set_ylim(-24, 24)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, fontweight='bold')

    plt.tight_layout()
    if save:
        fig.savefig(f'{filename}.{fmt}', bbox_inches='tight', dpi=150)
    plt.show()            

    
######################
###########
######################
            
def plotValues(values, title='Deviation', save=False, filename='tmp', fmt='pdf'):
    """Plot a vector of visual-field values as a 24-2 grid.

    Parameters
    ----------
    values : array-like
        Vector of length 52, 54, 74, or 76.
    title : str
        Plot title.
    save : bool
        If True, save to *filename*.*fmt*.
    filename : str
        Output file path (without extension).
    fmt : str
        One of 'pdf', 'png', 'svg'.
    """
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    values = list(values)
    length = len(values)
    if length not in (52, 54, 74, 76):
        raise NameError('Length of the input vector should be one of: 52, 54, 74, 76')
    if save and fmt not in ('pdf', 'png', 'svg'):
        raise NameError('format should be one of: pdf, svg, png')

    vals = np.array(values, dtype=float)
    is_24d2 = length in (52, 54)
    if length == 52:
        vals = np.concatenate([vals[:25], [np.nan], vals[25:33], [np.nan], vals[33:]])

    if is_24d2:
        grid = _GRID_24D2
        xs = sorted(set(x for p in grid if p is not None for x, _ in [p]))
        ys = sorted(set(y for p in grid if p is not None for _, y in [p]), reverse=True)
    else:
        xs = list(range(-27, 28, 6))
        ys = list(range(27, -28, -6))
        grid = []
        for y in ys:
            for x in xs:
                grid.append((x, y))
        grid = grid[:length if length == 76 else 74]
        if length == 76:
            grid.insert(len(grid) // 2, None)
            grid.insert(len(grid) // 2 + 1, None)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, fontweight='bold')

    cell = 5.0

    for idx, pos in enumerate(grid):
        if pos is None or idx >= len(vals):
            continue
        cx, cy = pos
        v = vals[idx]
        
        # Blind spots get a solid gray shape in standard R visualFields if NaN
        if np.isnan(v) and is_24d2 and idx in (25, 34):
            triangle = mpatches.Polygon(
                [[cx - 2.0, cy - 2.0], [cx + 2.0, cy - 2.0], [cx, cy + 2.0]],
                facecolor='darkgray', edgecolor='none'
            )
            ax.add_patch(triangle)
            continue
            
        if not np.isnan(v):
            ax.text(cx, cy, f'{v:.0f}', ha='center', va='center',
                    fontsize=12, color='black')

    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.axhline(y=0, color='black', linewidth=0.8)

    all_x = [p[0] for p in grid if p is not None]
    all_y = [p[1] for p in grid if p is not None]
    margin = cell
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    plt.tight_layout()
    if save:
        fig.savefig(f'{filename}.{fmt}', bbox_inches='tight', dpi=150)
    plt.show()
    plt.close(fig)            

       



# OLD R-based progression_cigts 
# def progression_cigts(df_VFs_py):
#     with localconverter(ro.default_converter + pandas2ri.converter):
#         df_VFs_r = ro.conversion.py2rpy(df_VFs_py)
#     rtitle = robjects.r['progression.cigts']
#     results = tuple(rtitle(df_VFs_r))
#     return results
# END OLD R-based progression_cigts 


def _progression_cigts_base(eye_df):
    """CIGTS progression for a single eye. Returns 'stable', 'worsening', or 'improving'.

    Reference: Musch et al. (1999); Gillespie et al. (2003)
    """
    import re

    if len(eye_df) < 5:
        raise ValueError("progression_cigts: at least 5 visual field visits are required")

    tdp_cols = sorted(
        [c for c in eye_df.columns if re.match(r'^tdp\d+$', c)],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    scores = eye_df[tdp_cols].apply(lambda row: _cigts_score(row.values), axis=1).values

    baseline = (scores[0] + scores[1]) / 2.0
    diffs = list(reversed(scores[2:] - baseline))

    def classify(d):
        if d >= 3:   return 'worsening'
        if d <= -3:  return 'improving'
        return 'stable'

    labels = [classify(d) for d in diffs]

    if len(set(labels[:3])) == 1:
        final = labels[0]
        if any(v != 'stable' and v != final for v in labels[3:]):
            return 'stable'
        return final

    return 'stable'


def progression_cigts(df_VFs_py):
    """CIGTS VF progression analysis.

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Must contain columns tdp1..tdp52/tdp54 and optionally 'eyeid'.
        At least 5 visits per eye are required.

    Returns
    -------
    tuple
        Progression result ('stable', 'worsening', or 'improving') for each eye.

    Reference: Musch et al. (1999); Gillespie et al. (2003)
    """

    df_VFs_py = canonicalize_vf_df(df_VFs_py, 
                                   sort_by_date=True)

    if 'eyeid' not in df_VFs_py.columns:
        df_VFs_py = df_VFs_py.copy()
        df_VFs_py['eyeid'] = 1

    results = {}
    for eyeid, eye_df in df_VFs_py.groupby('eyeid'):
        results[eyeid] = _progression_cigts_base(eye_df)

    return tuple(results.values())


def _plr_two_omit(timepoints, tds):
    """Pointwise linear regression with two-omit criterion for a single location.

    Runs OLS twice (omitting the last visit, then the second-to-last); both must agree
    on worsening/improving (|slope| >= 1, p <= 0.01) for that classification to stand.

    Reference: Gardiner & Crabb (2002)
    """
    from scipy import stats

    n = len(timepoints)
    if n < 3:
        raise ValueError("_plr_two_omit: at least 3 measurements required")

    def _standard_crit(tpts, tdvals):
        slope, _intercept, _r, pval, _se = stats.linregress(tpts, tdvals)
        if abs(slope) >= 1 and pval <= 0.01:
            return "worsening" if slope < 0 else "improving"
        return "stable"

    # r1: drop the last visit; r2: drop the second-to-last visit
    r1 = _standard_crit(np.delete(timepoints, n - 1), np.delete(tds, n - 1))
    r2 = _standard_crit(np.delete(timepoints, n - 2), np.delete(tds, n - 2))

    return r1 if r1 == r2 else "stable"


def _progression_plrnouri2012_base(eye_df):
    """PLR Nouri-Mahdavi 2012 progression for a single eye. Returns 'stable', 'worsening', or 'improving'.

    Reference: Nouri-Mahdavi et al. (2012), doi:10.1016/j.ophtha.2011.08.033
    """
    import re

    if "yearsfollowed" not in eye_df.columns:
        raise ValueError("progression_plrnouri2012: column 'yearsfollowed' missing")

    n = len(eye_df)
    if n < 3:
        raise ValueError("progression_plrnouri2012: at least 3 visual field visits are required")

    td_cols = sorted(
        [c for c in eye_df.columns if re.match(r'^td\d+$', c)],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    if len(td_cols) < 52:
        raise ValueError("progression_plrnouri2012: too few TD columns (must be 52 or 54)")
    if len(td_cols) > 54:
        raise ValueError("progression_plrnouri2012: too many TD columns (must be 52 or 54)")

    # Drop blind-spot columns td26 and td35 if 54 locations provided
    if len(td_cols) == 54:
        td_cols = [c for c in td_cols if c not in ("td26", "td35")]

    timepoints = eye_df["yearsfollowed"].values.astype(float)
    tds_matrix = eye_df[td_cols].values.astype(float)  # shape: (n_visits, 52)

    location_results = [
        _plr_two_omit(timepoints, tds_matrix[:, j])
        for j in range(tds_matrix.shape[1])
    ]

    worsening = location_results.count("worsening")
    improving = location_results.count("improving")

    if worsening >= improving + 3:
        return "worsening"
    if improving >= worsening + 3:
        return "improving"
    return "stable"


def progression_plrnouri2012(df_VFs_py):
    """PLR Nouri-Mahdavi 2012 VF progression analysis.

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Must contain columns td1..td52/td54, 'yearsfollowed', and optionally 'eyeid'.
        At least 3 visits per eye are required.

    Returns
    -------
    tuple
        Progression result ('stable', 'worsening', or 'improving') for each eye.

    Reference: Nouri-Mahdavi et al. (2012), doi:10.1016/j.ophtha.2011.08.033
    """


    df_VFs_py = canonicalize_vf_df(
        df_VFs_py,    
        sort_by_date=True,
    )

    if "eyeid" not in df_VFs_py.columns:
        df_VFs_py = df_VFs_py.copy()
        df_VFs_py["eyeid"] = 1

    results = {}
    for eyeid, eye_df in df_VFs_py.groupby("eyeid"):
        results[eyeid] = _progression_plrnouri2012_base(eye_df)

    return tuple(results.values())


# OLD R-based progression_vfi
# def progression_vfi(df_VFs_py): #Still in R
#     with localconverter(ro.default_converter + pandas2ri.converter):
#         df_VFs_r = ro.conversion.py2rpy(df_VFs_py)
#     rtitle = robjects.r['progression.vfi']
#     results = tuple(rtitle(df_VFs_r))
#     return results
# END OLD R-based progression_vfi


def _progression_vfi_base(eye_df):
    """VFI progression for a single eye using OLS linear regression.

    Reference: Aptel et al. (2015), PMID 26095771; Bengtsson & Heijl (2008)
    """
    from scipy import stats

    if len(eye_df) < 3:
        raise ValueError("progression_vfi: at least 3 visual field visits are required")
    if "vfi" not in eye_df.columns:
        raise ValueError("progression_vfi: column 'vfi' is missing")
    if "yearsfollowed" not in eye_df.columns:
        raise ValueError("progression_vfi: column 'yearsfollowed' is missing")

    yearsfollowed = eye_df["yearsfollowed"].values.astype(float)
    vfis = eye_df["vfi"].values.astype(float)

    slope, _intercept, _r, pval, _se = stats.linregress(yearsfollowed, vfis)

    if not np.isnan(pval) and pval <= 0.05:
        return "worsening" if slope < 0 else "improving"
    return "stable"


def progression_vfi(df_VFs_py):
    """VFI progression analysis using ordinary least-squares regression.

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Must contain columns 'vfi' and 'yearsfollowed'. Optionally 'eyeid'.
        At least 3 visits per eye are required.

    Returns
    -------
    tuple
        Progression result ('stable', 'worsening', or 'improving') for each eye.

    Reference: Aptel et al. (2015), PMID 26095771; Bengtsson & Heijl (2008)
    """

    df_VFs_py = canonicalize_vf_df(
        df_VFs_py,    
        sort_by_date=True,
    )

    if "eyeid" not in df_VFs_py.columns:
        df_VFs_py = df_VFs_py.copy()
        df_VFs_py["eyeid"] = 1

    results = {}
    for eyeid, eye_df in df_VFs_py.groupby("eyeid"):
        results[eyeid] = _progression_vfi_base(eye_df)

    return tuple(results.values())


# OLD R-based progression_schell2014
# def progression_schell2014(df_VFs_py):
#     with localconverter(ro.default_converter + pandas2ri.converter):
#         df_VFs_r = ro.conversion.py2rpy(df_VFs_py)    
#     rtitle = robjects.r['progression.schell2014']
#     results = tuple(rtitle(df_VFs_r))
#     return results
# END OLD R-based progression_schell2014


def _progression_schell2014_base(eye_df):
    """Schell 2014 VF progression for a single eye. Returns 'stable', 'worsening', or 'improving'.

    Reference: Schell et al. (2014), doi:10.1016/j.ophtha.2014.02.021
    """
    if len(eye_df) < 4:
        raise ValueError("progression_schell2014: at least 4 VFs required")
    if "md" not in eye_df.columns:
        raise ValueError("progression_schell2014: Column with name 'md' missing")

    mds = eye_df["md"].values.astype(float)

    # Baseline = mean of first 2 visits
    baseline = np.mean(mds[:2])

    # Total loss for follow-ups after baseline, reversed so most recent first
    tl = mds[2:] - baseline
    tl = tl[::-1]

    def classify(val):
        if val <= -3:
            return "worsening"
        if val >= 3:
            return "improving"
        return "stable"

    results = [classify(v) for v in tl]

    # First 2 most recent follow-ups must agree
    if len(results) >= 2:
        final_candidates = set(results[:2])
        if len(final_candidates) == 1:
            final = results[0]
            # Check older visits for contradictions
            if any(v != "stable" and v != final for v in results[2:]):
                return "stable"
            return final

    return "stable"


def progression_schell2014(df_VFs_py):
    """Schell 2014 VF progression analysis.

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Must contain column 'md'. Optionally 'eyeid'.
        At least 4 visits per eye are required.

    Returns
    -------
    tuple
        Progression result ('stable', 'worsening', or 'improving') per eye.

    Reference: Schell et al. (2014), doi:10.1016/j.ophtha.2014.02.021
    """

    df_VFs_py = canonicalize_vf_df(
        df_VFs_py,        
        sort_by_date=True,
    )

    if "eyeid" not in df_VFs_py.columns:
        df_VFs_py = df_VFs_py.copy()
        df_VFs_py["eyeid"] = 1

    results = {}
    for eyeid, eye_df in df_VFs_py.groupby("eyeid"):
        results[eyeid] = _progression_schell2014_base(eye_df)

    return tuple(results.values())





def _progression_agis_base(eye_df):
    """AGIS progression for a single eye's VF series.

    Reference: Rabiolo et al. (2019), Translational Vision Science & Technology, 8(5).

    Parameters
    ----------
    eye_df : pandas.DataFrame
        Rows = visits (must have >= 5). Must contain columns td1..td52/td54.

    Returns
    -------
    str
        'stable', 'worsening', or 'improving'
    """
    import re
    if len(eye_df) < 5:
        raise ValueError("progression_agis: at least 5 VFs required")

    td_cols = sorted(
        [c for c in eye_df.columns if re.match(r'^td\d+$', c)],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    # Compute AGIS score for every visit row
    agis_scores = eye_df[td_cols].apply(lambda row: _agis_score(row.values), axis=1).values

    baseline = agis_scores[0]
    # Compare all visits after baseline to baseline, then reverse order (R's rev())
    diffs = list(reversed(agis_scores[1:] - baseline))

    visit_results = [
        'worsening' if d >= 4 else ('improving' if d <= -3 else 'stable')
        for d in diffs
    ]

    # The final classification is based on the last 3 visits (index 0:3 after rev)
    final_set = set(visit_results[:3])

    if len(final_set) == 1:
        final = visit_results[0]
        # If any earlier visit contradicts the final label, classify as stable
        earlier = visit_results[3:]
        if any(v != 'stable' and v != final for v in earlier):
            return 'stable'
        return final
    return 'stable'


def progression_agis(df_VFs_py):
    """AGIS VF progression analysis.

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Must contain columns td1..td52/td54 and 'eyeid'.
        At least 5 visits per eye are required.

    Returns
    -------
    tuple
        Progression result ('stable', 'worsening', or 'improving') for each eye.

    Reference: Rabiolo et al. (2019), Translational Vision Science & Technology, 8(5).
    """

    df_VFs_py = canonicalize_vf_df(
        df_VFs_py,
        sort_by_date=True, 
    )

    if 'eyeid' not in df_VFs_py.columns:
        df_VFs_py = df_VFs_py.copy()
        df_VFs_py['eyeid'] = 1

    results = {}
    for eyeid, eye_df in df_VFs_py.groupby('eyeid'):
        results[eyeid] = _progression_agis_base(eye_df)

    return tuple(results.values())





# =====================================================================
# AGIS constants and helper functions
# Reference: AGIS 2 (Gaasterland et al., 1994); Katz (1999)
# =====================================================================

# 54-element sector map (1-indexed positions, None = blind spot)
# Matches R's agis.vf.sectors exactly
AGIS_VF_SECTORS = (
    ["upper"] * 10 +                                   # 1-10
    ["nasal"] + ["upper"] * 7 +                         # 11-18
    ["nasal", "nasal"] + ["upper"] * 5 + [None, "upper"] +  # 19-27
    ["nasal", "nasal"] + ["lower"] * 5 + [None, "lower"] +  # 28-36
    ["nasal"] + ["lower"] * 7 +                         # 37-44
    ["lower"] * 10                                      # 45-54
)

# 54-element neighbor list (1-indexed to match R code; converted to 0-indexed at use)
# None entries correspond to blind-spot positions (26, 35 in 1-indexed)
AGIS_NEIGHBORS_1INDEXED = [
    [2, 5, 6, 7], [1, 3, 6, 7, 8], [2, 4, 7, 8, 9], [3, 8, 9, 10],
    [1, 6, 12, 13], [1, 2, 5, 7, 12, 13, 14], [1, 2, 3, 6, 8, 13, 14, 15], [2, 3, 4, 7, 9, 14, 15, 16], [3, 4, 8, 10, 15, 16, 17], [4, 9, 16, 17, 18],
    [19, 20], [5, 6, 13, 21, 22], [5, 6, 7, 12, 14, 21, 22, 23], [6, 7, 8, 13, 15, 22, 23, 24], [7, 8, 9, 14, 16, 23, 24, 25], [8, 9, 10, 15, 17, 24, 25], [9, 10, 16, 18, 25, 27], [10, 17, 27],
    [11, 20, 28, 29], [11, 19, 28, 29], [12, 13, 22], [12, 13, 14, 21, 23], [13, 14, 15, 22, 24], [14, 15, 16, 23, 25], [15, 16, 17, 24], None, [17, 18],
    [19, 20, 29, 37], [19, 20, 28, 37], [31, 38, 39], [30, 32, 38, 39, 40], [31, 33, 39, 40, 41], [32, 34, 40, 41, 42], [33, 41, 42, 43], None, [43, 44],
    [28, 29], [30, 31, 39, 45, 46], [30, 31, 32, 38, 40, 45, 46, 47], [31, 32, 33, 39, 41, 46, 47, 48], [32, 33, 34, 40, 42, 47, 48, 49], [33, 34, 41, 43, 48, 49, 50], [34, 36, 42, 44, 49, 50], [36, 43, 50],
    [38, 39, 46, 51], [38, 39, 40, 45, 47, 51, 52], [39, 40, 41, 46, 48, 51, 52, 53], [40, 41, 42, 47, 49, 52, 53, 54], [41, 42, 43, 48, 50, 53, 54], [42, 43, 44, 49, 54],
    [45, 46, 47, 52], [46, 47, 48, 51, 53], [47, 48, 49, 52, 54], [48, 49, 50, 53],
]

# Abnormality criteria (54 elements, 1-indexed; None = blind spot)
# A location is abnormal if its TD value <= the corresponding criterion
_AGIS_CRITERIA = -np.array([
    9, 9, 9, 9,
    8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 8, 8,
    9, 8, 6, 6, 6, 6, 6, np.nan, 8,
    9, 7, 5, 5, 5, 5, 5, np.nan, 7,
    7, 7, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
], dtype=float)


def _agis_pad_to_54(values):
    """Pad a 52-element vector to 54 by inserting NaN at positions 26 and 35 (1-indexed)."""
    values = list(values)
    if len(values) == 54:
        return np.array(values, dtype=float)
    elif len(values) == 52:
        # Insert NaN at 1-indexed positions 26 and 35 (0-indexed 25 and 34)
        values.insert(25, np.nan)
        values.insert(34, np.nan)
        return np.array(values, dtype=float)
    else:
        raise ValueError(f"Expected 52 or 54 TD values, got {len(values)}")


def _agis_is_abnormal(vf_54):
    """Return boolean array (length 54) - True where location is abnormal.
    Uses <= comparison against AGIS criteria. NaN positions are False."""
    with np.errstate(invalid='ignore'):
        result = vf_54 <= _AGIS_CRITERIA
    # NaN comparisons produce False in numpy, which is what we want
    return np.asarray(result, dtype=bool)


def _agis_clusterize(indices, neighbors_0idx):
    """Given a list of (0-indexed) abnormal location indices and a neighbor lookup,
    return a list of connected clusters (each cluster is a sorted list of 0-indexed indices).
    Iterative BFS replaces the recursive R version."""
    if len(indices) == 0:
        return []

    remaining = set(indices)
    clusters = []

    while remaining:
        # Start a new cluster from an arbitrary remaining index
        seed = min(remaining)
        remaining.discard(seed)
        cluster = {seed}
        queue = [seed]

        while queue:
            current = queue.pop(0)
            nbrs = neighbors_0idx.get(current, [])
            for nb in nbrs:
                if nb in remaining:
                    remaining.discard(nb)
                    cluster.add(nb)
                    queue.append(nb)

        clusters.append(sorted(cluster))

    return clusters


def _agis_clusters(vf_54):
    """Return dict with keys 'upper', 'lower', 'nasal', each holding
    a list of clusters (sorted 0-indexed location lists)."""
    abn = _agis_is_abnormal(vf_54)

    # Build 0-indexed neighbor dict (only for non-blind-spot positions)
    neighbors_0idx = {}
    for i, nbrs in enumerate(AGIS_NEIGHBORS_1INDEXED):
        if nbrs is not None:
            neighbors_0idx[i] = [n - 1 for n in nbrs]  # convert to 0-indexed

    result = {}
    for sector in ("upper", "lower", "nasal"):
        sector_indices = [i for i in range(54)
                          if AGIS_VF_SECTORS[i] == sector and abn[i]]
        result[sector] = _agis_clusterize(sector_indices, neighbors_0idx)

    return result


def _agis_score_locations(clusterlist, vf_54):
    """Score one hemifield (upper or lower) based on its clusters."""
    score = 0
    cluster_sizes = [len(c) for c in clusterlist]
    # Only consider clusters with >= 3 members
    large_clusters = [c for c, s in zip(clusterlist, cluster_sizes) if s >= 3]
    if large_clusters:
        s = sum(len(c) for c in large_clusters)
        if s >= 3:  score += 1
        if s >= 6:  score += 1
        if s >= 13: score += 1
        if s >= 20: score += 1
        # Depth scoring: collect all locations in large clusters
        loc3 = np.array([vf_54[i] for c in large_clusters for i in c])
        l3h = len(loc3) / 2.0
        for criterion in [12, 16, 20, 24, 28]:
            if np.sum(loc3 <= -criterion) >= l3h:
                score += 1
    return score


def _agis_score(tds):
    """Compute the AGIS severity score for a single VF measurement.

    Parameters
    ----------
    tds : array-like
        Total deviation values (52 or 54 elements).

    Returns
    -------
    int
        AGIS score (0–20 scale).

    Reference: AGIS 2 (Gaasterland et al., 1994), p. 1448; Katz (1999), p. 392
    """
    tds = np.asarray(tds, dtype=float)
    n = len(tds)
    if n < 52:
        raise ValueError("agis_score: too few elements in TD vector (must be 52 or 54)")
    if n > 54:
        raise ValueError("agis_score: too many elements in TD vector (must be 52 or 54)")

    vf = _agis_pad_to_54(tds)
    cl = _agis_clusters(vf)

    score = 0

    # --- Nasal scoring (uses 1-indexed references from the paper) ---
    nasal_clusters = cl["nasal"]
    if nasal_clusters:
        if len(nasal_clusters) == 1 and len(nasal_clusters[0]) < 3:
            # Nasal step - restricted to one hemifield
            # 1-indexed {11,19,20} -> 0-indexed {10,18,19}; {28,29,37} -> {27,28,36}
            cluster_set = set(nasal_clusters[0])
            if cluster_set <= {10, 18, 19} or cluster_set <= {27, 28, 36}:
                score += 1
        else:
            # "nasal defect" - any cluster with > 2 members
            if any(len(c) > 2 for c in nasal_clusters):
                score += 1

        # Check if >= 4 nasal locations have TD <= -12
        nasal_indices = [i for i in range(54) if AGIS_VF_SECTORS[i] == "nasal"]
        nasal_vals = vf[nasal_indices]
        if np.sum(nasal_vals <= -12) >= 4:
            score += 1

    # --- Hemifield scoring ---
    score += _agis_score_locations(cl["upper"], vf)
    score += _agis_score_locations(cl["lower"], vf)

    return score


def get_score_AGIS(df_VF_py):
    """Compute AGIS severity score from total deviation values.

    Parameters
    ----------
    df_VF_py : pandas.Series or pandas.DataFrame
        Must contain columns td1..td52 (or td1..td54) with total deviation values.

    Returns
    -------
    int
        AGIS score.
    """
    
    df_VF_py = canonicalize_vf_row(df_VF_py)  
    
    if isinstance(df_VF_py, pandas.core.series.Series):
        df_VF_py = pandas.DataFrame(df_VF_py).transpose()

    import re
    td_cols = sorted(
        [c for c in df_VF_py.columns if re.match(r'^td\d+$', c)],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    if not td_cols:
        raise ValueError("Input must contain columns named td1, td2, ... td52/td54")

    tds = df_VF_py[td_cols].values.flatten().astype(float)
    return _agis_score(tds)







# =====================================================================
# CIGTS constants and helper functions
# Reference: Musch et al., 1999; Gillespie et al., 2003

# 52-element neighbor list (1-indexed, matching R's cigts.neighbors)
# CIGTS uses 52 locations 
CIGTS_NEIGHBORS_1INDEXED = [
    [2, 5, 6, 7], [1, 3, 6, 7, 8], [2, 4, 7, 8, 9], [3, 8, 9, 10],
    [1, 6, 11, 12, 13], [1, 2, 5, 7, 12, 13, 14], [1, 2, 3, 6, 8, 13, 14, 15], [2, 3, 4, 7, 9, 14, 15, 16], [3, 4, 8, 10, 15, 16, 17], [4, 9, 16, 17, 18],
    [5, 12, 19, 20, 21], [5, 6, 11, 13, 20, 21, 22], [5, 6, 7, 12, 14, 21, 22, 23], [6, 7, 8, 13, 15, 22, 23, 24], [7, 8, 9, 14, 16, 23, 24, 25], [8, 9, 10, 15, 17, 24, 25], [9, 10, 16, 18, 25, 26], [10, 17, 26],
    [11, 20], [11, 12, 19, 21], [11, 12, 13, 20, 22], [12, 13, 14, 21, 23], [13, 14, 15, 22, 24], [14, 15, 16, 23, 25], [15, 16, 17, 24], [17, 18],
    [28, 35], [27, 29, 35, 36], [28, 30, 35, 36, 37], [29, 31, 36, 37, 38], [30, 32, 37, 38, 39], [31, 33, 38, 39, 40], [32, 39, 40, 41], [41, 42],
    [27, 28, 29, 36, 43], [28, 29, 30, 35, 37, 43, 44], [29, 30, 31, 36, 38, 43, 44, 45], [30, 31, 32, 37, 39, 44, 45, 46], [31, 32, 33, 38, 40, 45, 46, 47], [32, 33, 39, 41, 46, 47, 48], [33, 34, 40, 42, 47, 48], [34, 41, 48],
    [35, 36, 37, 44, 49], [36, 37, 38, 43, 45, 49, 50], [37, 38, 39, 44, 46, 49, 50, 51], [38, 39, 40, 45, 47, 50, 51, 52], [39, 40, 41, 46, 48, 51, 52], [40, 41, 42, 47, 52],
    [43, 44, 45, 50], [44, 45, 46, 49, 51], [45, 46, 47, 50, 52], [46, 47, 48, 51],
]


def _cigts_score(tdprobs):
    """Compute the CIGTS severity score for a single VF measurement.

    Parameters
    ----------
    tdprobs : array-like
        Total deviation probability values (52 or 54 elements).
        Values should be between 0.005 and 1.

    Returns
    -------
    float
        CIGTS score.

    Reference: Gillespie et al. (2003); Musch et al. (1999)
    """
    tdprobs = np.asarray(tdprobs, dtype=float)
    n = len(tdprobs)
    if n < 52:
        raise ValueError("cigts_score: too few elements in TD prob vector (must be 52 or 54)")
    if n > 54:
        raise ValueError("cigts_score: too many elements in TD prob vector (must be 52 or 54)")
    # Remove blind spot positions if 54 elements (1-indexed 26 and 35 -> 0-indexed 25 and 34)
    if n == 54:
        tdprobs = np.delete(tdprobs, [25, 34])

    # Map probabilities to weights
    pweights = np.zeros(52, dtype=float)
    pweights[tdprobs == 0.005] = 4
    pweights[tdprobs == 0.01] = 3
    pweights[tdprobs == 0.02] = 2
    pweights[tdprobs == 0.05] = 1

    # Calculate effective weights: min(own weight, 2nd-highest neighbor weight)
    effective_weights = np.zeros(52, dtype=float)
    for i in range(52):
        weight = pweights[i]
        # Get neighbor weights (convert 1-indexed to 0-indexed)
        neighbor_indices = [n - 1 for n in CIGTS_NEIGHBORS_1INDEXED[i]]
        neighbor_weights = sorted([pweights[j] for j in neighbor_indices], reverse=True)
        # 2nd highest neighbor weight (index 1)
        second_highest = neighbor_weights[1] if len(neighbor_weights) >= 2 else 0
        effective_weights[i] = min(weight, second_highest)

    return float(np.sum(effective_weights) / 10.4)


def get_score_CIGTS(df_VF_py):
    """Compute CIGTS severity score from total deviation probabilities.

    Parameters
    ----------
    df_VF_py : pandas.Series or pandas.DataFrame
        Must contain columns tdp1..tdp52 (or tdp1..tdp54) with TD probability values.

    Returns
    -------
    float
        CIGTS score.
    """

    # df_VF_py = canonicalize_vf_df(
    #     df_VF_py        
    # )

    df_VF_py = canonicalize_vf_row(df_VF_py)  # Ensure column names are standardized (e.g., tdp1, tdp2, ...)

    if isinstance(df_VF_py, pandas.core.series.Series):
        df_VF_py = pandas.DataFrame(df_VF_py).transpose()

    import re
    tdp_cols = sorted(
        [c for c in df_VF_py.columns if re.match(r'^tdp\d+$', c)],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    if not tdp_cols:
        raise ValueError("Input must contain columns named tdp1, tdp2, ... tdp52/tdp54")

    tdprobs = df_VF_py[tdp_cols].values.flatten().astype(float)
    return _cigts_score(tdprobs)


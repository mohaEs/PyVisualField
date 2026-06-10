# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:16:54 2021

@author: Mohammad Eslami
Massachusetts Eye and Ear
Harvard Medical School

@contributor: Bharath Erusalagandi (Python implementation)
"""

"""
This file contains wrappers for R package: visualFields
https://cran.r-project.org/web/packages/visualFields/index.html
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3600987/
"""

import os
import sys
from collections import OrderedDict
from math import erf, sqrt

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.stats import t as _student_t       # Student-t CDF, matches R's pt()
from scipy.stats import rankdata as _rankdata  # average-tie ranks, matches R rank()

from PyVisualFields.Deviation_Analysis import (
    py_getnv, py_setnv, py_setdefaults, py_normvals, py_get_info_normvals,
    py_nvgenerate, py_setnv_custom,
    py_gettd, py_getgh, py_getpd, py_gettdp, py_getpdp,
    py_getgl, py_getglp, py_getallvalues,
)









'''  ###########################
Utils
'''


'''  ###########################
Part I: Datasets 
'''

def data_vfctrSunyiu24d2():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfctrSunyiu24d2.pkl')
    return pd.read_pickle(path)

def data_vfctrSunyiu10d2():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfctrSunyiu10d2.pkl')
    return pd.read_pickle(path)
 
def data_vfpwgRetest24d2():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfpwgRetest24d2.pkl')
    return pd.read_pickle(path)

def data_vfpwgSunyiu24d2():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfpwgSunyiu24d2.pkl')
    return pd.read_pickle(path)

def data_vfctrIowaPC26():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfctrIowaPC26.pkl')
    return pd.read_pickle(path)

def data_vfctrIowaPeri():
    path = os.path.join(os.path.dirname(__file__), 'pkl_files', 'vfctrIowaPeri.pkl')
    return pd.read_pickle(path)








'''  ###########################
part II: plots
'''

_GRID_24D2 = [
    (3, 0), (4, 0), (5, 0), (6, 0),
    (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), None, (8, 3),
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), None, (8, 4),
    (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
    (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
    (3, 7), (4, 7), (5, 7), (6, 7),
]
_BLIND_SPOT_IDX = frozenset(i for i, pos in enumerate(_GRID_24D2) if pos is None)

_VF_PROB_SCHEME = [
    (0.005, '#800026', '#800026', 'white'),
    (0.010, '#BD0026', '#BD0026', 'white'),
    (0.020, '#FD8D3C', '#FD8D3C', 'black'),
    (0.050, '#FED976', '#FED976', 'black'),
    (0.950, '#F7F0EB', '#CCCCCC', 'black'),
    (0.980, '#41AE76', '#41AE76', 'black'),
    (0.990, '#238B45', '#238B45', 'white'),
    (0.995, '#006D2C', '#006D2C', 'white'),
    (1.001, '#00441B', '#00441B', 'white'),
]

# _R_COLMAP = [
#     (0.000, '#000000'),
#     (0.005, '#800026'),
#     (0.010, '#BD0026'),
#     (0.020, '#FD8D3C'),
#     (0.050, '#FED976'),
#     (0.950, '#F7F0EB'),
#     (0.980, '#41AE76'),
#     (0.990, '#238B45'),
#     (0.995, '#006D2C'),
#     (1.001, '#00441B'),
# ]

_R_SENS_MAX = 35.0


# def _r_prob_color(p, sensitivity=None):
#     """Probability value → hex fill color. Sensitivity < 0 forces black."""
#     color = '#F7F0EB'
#     try:
#         if not np.isnan(p):
#             for thresh, col in _R_COLMAP:
#                 if p <= thresh:
#                     color = col
#                     break
#     except (TypeError, ValueError):
#         pass
#     if sensitivity is not None and np.isfinite(float(sensitivity)) and float(sensitivity) < 0.0:
#         color = '#000000'
#     return color


# def _r_prob_color(p, sensitivity=None):

#     if sensitivity is not None:
#         if np.isfinite(float(sensitivity)) and float(sensitivity) < 0:
#             return "#111111"

#     if np.isnan(p):
#         return "#EBEBEB"

#     if p <= 0.005:
#         return "#111111"      # p<0.5%
#     elif p <= 0.01:
#         return "#8B0000"      # p<1%
#     elif p <= 0.02:
#         return "#E65F10"      # p<2%
#     elif p <= 0.05:
#         return "#E8B322"      # p<5%
#     elif p >= 0.95:
#         return "#1D8514"      # above normal
#     else:
#         return "#EBEBEB"      # normal



def _r_sens_gray(v):
    """Sensitivity dB → grayscale float [0=black, 1=white] scaled to 35 dB max."""
    if np.isnan(v):
        return 1.0
    return float(np.clip(v / _R_SENS_MAX, 0.0, 1.0))


def _gray_hex(g):
    """Grayscale float [0, 1] → '#RRGGBB'."""
    v = int(round(np.clip(float(g), 0.0, 1.0) * 255))
    return f'#{v:02X}{v:02X}{v:02X}'


def _hex_luminance(hex_col):
    """Relative luminance of a '#RRGGBB' color."""
    r = int(hex_col[1:3], 16) / 255.0
    g = int(hex_col[3:5], 16) / 255.0
    b = int(hex_col[5:7], 16) / 255.0
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _get_prob_colors(p_val):
    """Return (fill, border, text) colors for a probability value."""
    if np.isnan(p_val):
        return '#F7F0EB', '#CCCCCC', 'black'
    for thresh, fill, border, text in _VF_PROB_SCHEME:
        if p_val <= thresh:
            return fill, border, text
    return '#F7F0EB', '#CCCCCC', 'black'


def _save_plot(fig, save=False, filename='tmp', fmt='pdf'):
    """Persist a matplotlib figure when requested."""
    if save:
        fig.savefig(f'{filename}.{fmt}', bbox_inches='tight', dpi=150, transparent=True)


def _expand_24d2_values(values):
    """Expand 52-element array to 54 by inserting NaN at the two blind spot positions."""
    vals = np.array(values, dtype=float)
    if len(vals) == 52:
        vals = np.concatenate([vals[:25], [np.nan], vals[25:33], [np.nan], vals[33:]])
    return vals


def _get_sensitivity_cols(df):
    """Return ordered list of visual-field sensitivity columns."""
    for prefix in ('l', 's', 'p', 'sens', 'vf'):
        cols = sorted(
            [c for c in df.columns if c.startswith(prefix) and c[len(prefix):].isdigit()],
            key=lambda x: int(x[len(prefix):]),
        )
        if len(cols) >= 52:
            return cols
    cols = sorted(
        [
            c for c in df.columns
            if c[-1].isdigit() and c.rstrip('0123456789') not in
            ('age', 'date', 'id', 'eye', 'time', 'fpr', 'fnr', 'fl', 'duration', 'eyeid', 'patientid')
        ],
        key=lambda x: int(x.lstrip('abcdefghijklmnopqrstuvwxyz')),
    )
    return cols


def _sort_vf_dataframe(df_vf_py):
    """Return a copy sorted by date when a date column is present."""
    df_sorted = df_vf_py.copy()
    if 'date' in df_sorted.columns:
        try:
            sort_key = pd.to_datetime(df_sorted['date'], errors='coerce')
            if sort_key.notna().any():
                df_sorted = df_sorted.assign(_sort_date=sort_key)
                df_sorted = df_sorted.sort_values(['_sort_date']).drop(columns=['_sort_date'])
            else:
                df_sorted = df_sorted.sort_values('date')
        except Exception:
            df_sorted = df_sorted.sort_values('date')
    return df_sorted.reset_index(drop=True)


def _canonicalize_vf_dataframe(df_vf_py):
    """Normalize point-column names to l1..lN and ensure an age column exists."""
    df_sorted = _sort_vf_dataframe(df_vf_py)
    sens_cols = _get_sensitivity_cols(df_sorted)
    if not sens_cols:
        raise ValueError('No visual field sensitivity columns found in the input dataframe.')

    meta_cols = [c for c in df_sorted.columns if c not in sens_cols]
    df_canonical = df_sorted[meta_cols].copy().reset_index(drop=True)
    vf_cols = [f'l{i}' for i in range(1, len(sens_cols) + 1)]
    for idx, col in enumerate(sens_cols, start=1):
        df_canonical[f'l{idx}'] = pd.to_numeric(df_sorted[col], errors='coerce')

    if 'age' not in df_canonical.columns:
        df_canonical['age'] = 60.0
    df_canonical['age'] = pd.to_numeric(df_canonical['age'], errors='coerce').fillna(60.0)
    return df_canonical, vf_cols


def _row_to_array(row, cols):
    """Convert a dataframe row to a masked 24-2 point array."""
    arr = row[cols].values.astype(float)
    for i in _BLIND_SPOT_IDX:
        if i < len(arr):
            arr[i] = np.nan
    return arr


def _matrix_from_df(df_points, cols):
    """Convert a dataframe slice to a masked 2-D point matrix."""
    mat = df_points[cols].values.astype(float)
    for i in _BLIND_SPOT_IDX:
        if i < mat.shape[1]:
            mat[:, i] = np.nan
    return mat


def _nanmean_columns(data):
    """Column-wise nanmean without emitting warnings for all-NaN columns."""
    counts = np.sum(np.isfinite(data), axis=0)
    sums = np.nansum(data, axis=0)
    out = np.full(data.shape[1], np.nan, dtype=float)
    np.divide(sums, counts, out=out, where=counts > 0)
    return out


def _compute_plot_dataframes(df_vf_py):
    """Compute canonical VF and derived TD/PD/probability/global-index dataframes."""
    df_vf, vf_cols = _canonicalize_vf_dataframe(df_vf_py)
    df_td = py_gettd(df_vf)
    df_pd = py_getpd(df_td)
    df_tdp = py_gettdp(df_td)
    df_pdp = py_getpdp(df_pd)
    df_gi = py_getgl(df_vf)
    return df_vf, vf_cols, df_td, df_pd, df_tdp, df_pdp, df_gi


def _simple_slope(x, y):
    """Return the OLS slope for finite x/y values, or NaN when unavailable."""
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 2:
        return np.nan
    x_use = x[mask]
    y_use = y[mask]
    x_center = x_use - x_use.mean()
    denom = np.sum(x_center ** 2)
    if denom <= 0:
        return np.nan
    return float(np.sum(x_center * (y_use - y_use.mean())) / denom)


def _probability_cell_style(p_val, scheme="10"):
    """
    Return (facecolor, edgecolor, text_color, linewidth) for a probability value.

    scheme='10': Use 10 probability thresholds (default, matches VF_PROB_SCHEME)
    scheme='5': Collapsed 5-bracket scheme (same fills, no green border on normal)
    """
    if np.isnan(p_val):
        return "#EBEBEB", "#BBBBBB", "black", 1.0

    if scheme == "5":
        if p_val <= 0.005:
            return "#111111", "#111111", "white", 2.5
        elif p_val <= 0.01:
            return "#8B0000", "#8B0000", "white", 2.5
        elif p_val <= 0.02:
            return "#EB520B", "#EB520B", "white", 2.0
        elif p_val <= 0.05:
            return "#E8A322", "#E8A322", "black", 2.0
        elif p_val >= 0.95:
            return "#EBEBEB", "#BBBBBB", "black", 2.5  # above-normal green border
        else:
            return "#EBEBEB", "#BBBBBB", "black", 1.0  # normal — plain gray
    else:  # scheme == '10' (default)
        fc, ec, tc = _get_prob_colors(p_val)
        return fc, ec, tc, 1.0

def _draw_blind_spot(ax, cell_width=1):
    """Draw the two blind spot cells (rows 3 and 4, col 7) as hatched gray boxes."""
    half = cell_width / 2.0
    for row in (3, 4):
        y = 7 - row
        col = 7
        rect = mpatches.Rectangle(
            (col - half, y - half),
            cell_width,
            cell_width,
            facecolor="#CCCCCC",
            edgecolor="#888888",
            linewidth=1.0,
            hatch="////",
        )
        ax.add_patch(rect)


def _draw_vf_cell(
    ax, col, row, value, facecolor, edgecolor, text_color,
    fmt=".0f", cell_width=1, linewidth=0
):
    """
    Draw a single VF cell with rounded corners, a colored fill, and bold text.

    Parameters:
    - ax: matplotlib axis
    - col, row: grid coordinates
    - value: numeric value to display
    - facecolor, edgecolor, text_color: cell colors
    - fmt: value format string
    - cell_width: cell size
    - linewidth: border thickness
    """
    half = cell_width / 2.0
    y = 7 - row

    rect = mpatches.Rectangle(
        (col - half, y - half),
        cell_width,
        cell_width,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    ax.add_patch(rect)

    if not np.isnan(value):
        ax.text(
            col,
            y,
            _format_vf_value(value, fmt),
            ha="center",
            va="center",
            fontsize=10,
            color=text_color,
            fontweight="bold",
            fontfamily="DejaVu Sans",
        )

def _format_vf_value(value, fmt=".0f"):
    """Format a VF value and avoid displaying rounded negative zero."""
    text = format(value, fmt)
    if text.startswith("-"):
        try:
            if float(text) == 0.0:
                return text[1:]
        except ValueError:
            pass
    return text


def _draw_sensitivity_colorbar(ax, y=-1.15, vmin=0, vmax=35):
    """
    Draw continuous grayscale sensitivity legend.
    """

    gradient = np.linspace(vmin, vmax, 256).reshape(1, -1)

    ax.imshow(
        gradient,
        extent=(-0.2, 8.2, y, y + 0.35),
        cmap="gray",
        aspect="auto",
        vmin=vmin,
        vmax=vmax,
        zorder=0,
    )

    # outline
    rect = mpatches.Rectangle(
        (-0.2, y),
        8.4,
        0.35,
        fill=False,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.add_patch(rect)

    # ticks
    tick_vals = [0, 5, 10, 15, 20, 25, 30, 35]

    for t in tick_vals:
        x = -0.2 + (t - vmin) / (vmax - vmin) * 8.4

        ax.plot(
            [x, x],
            [y - 0.05, y],
            color="black",
            linewidth=0.8,
        )

        ax.text(
            x,
            y - 0.12,
            str(t),
            ha="center",
            va="top",
            fontsize=6.5,
        )

    ax.text(
        8.45,
        y + 0.175,
        "dB",
        va="center",
        fontsize=7,
        fontweight="bold",
    )


def _draw_probability_colorbar(ax, y=-1.15):
    """Draw a polished probability legend strip below a standalone cell plot."""
    # 5-bracket legend: p<0.5%, p<1%, p<2%, p<5%, normal, above-normal
    legend_items = [
        ("p<0.5%",  "#111111", "#111111", "white"),
        ("p<1%",   "#8B0000", "#8B0000", "white"),
        ("p<2%",   "#EB520B", "#EB520B", "white"),
        ("p<5%",   "#E8A322", "#E8A322", "black"),
        ("normal", "#EBEBEB", "#BBBBBB", "black"),
        ("p≥95%",  "#EBEBEB", "#BBBBBB", "black"),
    ]

    n = len(legend_items)
    total_w = 9.0
    width = total_w / n
    height = 0.38
    pad = 0.03
    start_x = -0.4
    for idx, (label, fill, border, tc) in enumerate(legend_items):
        x = start_x + idx * width
        lw = 2.5 if border not in ("#111111", "#8B0000", "#C41E1E", "#E87722", "#BBBBBB") else 1.5
        rect = mpatches.FancyBboxPatch(
            (x + pad, y + pad),
            width - 2 * pad,
            height - 2 * pad,
            boxstyle=f"round,pad={pad}",
            facecolor=fill,
            edgecolor=border,
            linewidth=lw,
        )
        ax.add_patch(rect)
        ax.text(
            x + width / 2,
            y + height / 2,
            label,
            ha="center",
            va="center",
            fontsize=6.5,
            color=tc,
            fontweight="bold",
        )

def _vf_cell_plot(
    values,
    probs=None,
    title="",
    fmt=".0f",
    ax=None,
    figsize=(7, 6),
    scheme="10",
    cell_width=1,
    show_prob_legend=None,
):
    """
    Draw a cell-based 24-2 visual field plot.

    Parameters:
    - values: numeric values to display in cells (one per VF location)
    - probs: (optional) probability values for coloring cells
    - title: plot title
    - fmt: format string for values
    - ax: existing matplotlib axis (creates new figure if None)
    - figsize: figure size if ax is None
    - scheme: '10' for 10-bracket or '5' for 5-bracket probability colors
    - cell_width: size of each cell rectangle

    If probs is None:
    - Draw cells with neutral colors and numeric values

    If probs is provided:
    - Use probability values to determine cell colors
    - Text values displayed in cells use the probability-based text color
    """
    created_axis = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()
    if show_prob_legend is None:
        show_prob_legend = created_axis and probs is not None

    vals = _expand_24d2_values(values)
    prbs = _expand_24d2_values(probs) if probs is not None else None
    drew_blind_spot = False

    # Draw all grid locations
    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            if not drew_blind_spot:
                _draw_blind_spot(ax)
                drew_blind_spot = True
            continue

        c, r = pos
        v = vals[i] if i < len(vals) else np.nan

        if not np.isnan(v):
            if probs is not None:
                p = prbs[i] if i < len(prbs) else np.nan
                if not np.isnan(p):
                    facecolor, edgecolor, text_color, lw = _probability_cell_style(
                        p, scheme=scheme
                    )
                else:
                    facecolor, edgecolor, text_color, lw = "#EBEBEB", "#BBBBBB", "black", 1.0
            else:
                facecolor, edgecolor, text_color, lw = "#EBEBEB", "#BBBBBB", "black", 1.0

            _draw_vf_cell(
                ax, c, r, v,
                facecolor, edgecolor, text_color,
                fmt=fmt,
                cell_width=cell_width,
                linewidth=lw,
            )

    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-1.55 if show_prob_legend else -0.6, 7.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
    if show_prob_legend:
        _draw_probability_colorbar(ax)

    return fig, ax

def _vf_grid_plot(values, title='', colormap=None, cbar_label='dB',
                  vmin=None, vmax=None, fmt='.0f', ax=None, figsize=(7, 6)):
    """Draw a classic, minimalist 24-2 grid plot for raw sensitivity values."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    vals = np.array(values, dtype=float)

    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            continue
        c, r = pos
        y = 7 - r
        v = vals[i] if i < len(vals) else np.nan

        # Use the module-level blind spot index if available
        bs_idx = getattr(sys.modules[__name__], '_BLIND_SPOT_IDX', [25, 34])
        if i in bs_idx and np.isnan(v):
            triangle = mpatches.Polygon(
                [[c - 0.35, y - 0.35], [c + 0.35, y - 0.35], [c, y + 0.45]],
                facecolor='darkgray', edgecolor='none'
            )
            ax.add_patch(triangle)
            continue

        if not np.isnan(v):
            ax.text(c, y, format(v, fmt), ha='center', va='center', fontsize=13, color='black')

    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-0.6, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.axvline(x=4.5, color='black', linewidth=1.0)
    ax.axhline(y=3.5, color='black', linewidth=1.0)

    return fig, ax

def _vf_prob_plot(values, probs, title="", fmt=".0f", ax=None):
    """Draw a 24-2 value grid with cell-based coloring using probability values."""
    return _vf_cell_plot(
        values,
        probs=probs,
        title=title,
        fmt=fmt,
        ax=ax,
        figsize=(7, 6),
        scheme="5",
        cell_width=1,
    )


def _draw_r_blind_spot(ax):
    """Gray ellipse at the blind spot location."""
    ax.add_patch(mpatches.Ellipse(
        (7, 3.5), width=0.65, height=1.1,
        facecolor='lightgray', edgecolor='none'
    ))


def _vf_sens_plot(
    sens_vals,
    title='',
    ax=None,
    figsize=(7, 6),
    show_sens_legend=None
):
    """Sensitivity map: grayscale cell backgrounds, <0 label for out-of-range values."""
    created_axis = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    if show_sens_legend is None:
        show_sens_legend = created_axis

    vals = _expand_24d2_values(sens_vals)
    half = 0.5
    drew_bs = False

    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            if not drew_bs:
                _draw_r_blind_spot(ax)
                drew_bs = True
            continue
        c, r = pos
        y = 7 - r
        v = vals[i] if i < len(vals) else np.nan
        if np.isnan(v):
            continue

        g = _r_sens_gray(v)
        ax.add_patch(mpatches.Rectangle(
            (c - half, y - half), 2 * half, 2 * half,
            facecolor=_gray_hex(g), edgecolor='none'
        ))
        text_col = '#4D4D4D' if g >= 0.5 else '#B3B3B3'
        txt = '<0' if v < 0 else str(int(round(v)))
        ax.text(c, y, txt, ha='center', va='center', fontsize=10, color=text_col)

    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-1.55 if show_sens_legend else -0.6, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    if show_sens_legend:
        _draw_sensitivity_colorbar(ax)
    return fig, ax


def _vf_devborder_plot(dev_vals, probs, sens_vals, title='', ax=None, figsize=(7, 6), show_prob_legend=None):
    """TD/PD map: probability-colored outer ring, white inner cell, gray deviation text."""
    created_axis = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    if show_prob_legend is None:
        show_prob_legend = created_axis

    devs = _expand_24d2_values(dev_vals)
    prbs = _expand_24d2_values(probs)
    sens = _expand_24d2_values(sens_vals)
    outer_half, inner_half = 0.5, 0.31
    drew_bs = False



    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            if not drew_bs:
                _draw_r_blind_spot(ax)
                drew_bs = True
            continue
        c, r = pos
        y = 7 - r
        if i >= len(devs) or np.isnan(devs[i]):
            continue

        p = prbs[i] if i < len(prbs) else np.nan
        s = sens[i] if i < len(sens) else np.nan
        # outer_col = _r_prob_color(p, sensitivity=s)

        # ax.add_patch(mpatches.Rectangle(
        #     (c - outer_half, y - outer_half), 2 * outer_half, 2 * outer_half,
        #     facecolor=outer_col, edgecolor='none'
        # ))

        facecolor, edgecolor, text_color, lw = _probability_cell_style(p, scheme="5")

        ax.add_patch(mpatches.Rectangle(
            (c - outer_half, y - outer_half), 2 * outer_half, 2 * outer_half,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=lw
        ))

        ax.add_patch(mpatches.Rectangle(
            (c - inner_half, y - inner_half), 2 * inner_half, 2 * inner_half,
            facecolor='#F7F0EB', edgecolor='none'
        ))
        ax.text(c, y, str(int(round(devs[i]))),
                ha='center', va='center', fontsize=9, color='#4D4D4D')

    # _draw_probability_colorbar(ax)
    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-1.55 if show_prob_legend else -0.6, 7.6)
    if show_prob_legend:
        _draw_probability_colorbar(ax)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    
    return fig, ax


def _vf_sdevborder_plot(dev_vals, probs, sens_vals, title='', ax=None, figsize=(7, 6), show_prob_legend=None):
    """TDS/PDS map: probability-colored outer ring, sensitivity-grayscale inner cell."""
    created_axis = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    if show_prob_legend is None:
        show_prob_legend = created_axis

    devs = _expand_24d2_values(dev_vals)
    prbs = _expand_24d2_values(probs)
    sens = _expand_24d2_values(sens_vals)
    outer_half, inner_half = 0.5, 0.31
    drew_bs = False

    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            if not drew_bs:
                _draw_r_blind_spot(ax)
                drew_bs = True
            continue
        c, r = pos
        y = 7 - r
        if i >= len(devs) or np.isnan(devs[i]):
            continue

        # p = prbs[i] if i < len(prbs) else np.nan
        # s = sens[i] if i < len(sens) else np.nan
        # outer_col = _r_prob_color(p, sensitivity=s)
        # g = _r_sens_gray(s)
        # inner_col = _gray_hex(g)
        # text_col = '#4D4D4D' if g >= 0.5 else '#B3B3B3'

        # ax.add_patch(mpatches.Rectangle(
        #     (c - outer_half, y - outer_half), 2 * outer_half, 2 * outer_half,
        #     facecolor=outer_col, edgecolor='none'
        # ))

        p = prbs[i] if i < len(prbs) else np.nan
        s = sens[i] if i < len(sens) else np.nan

        facecolor, edgecolor, _, lw = _probability_cell_style(
            p,
            scheme="5"
        )

        g = _r_sens_gray(s)
        inner_col = _gray_hex(g)
        text_col = '#4D4D4D' if g >= 0.5 else '#B3B3B3'

        ax.add_patch(mpatches.Rectangle(
            (c - outer_half, y - outer_half),
            2 * outer_half,
            2 * outer_half,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=lw
        ))

        ax.add_patch(mpatches.Rectangle(
            (c - inner_half, y - inner_half), 2 * inner_half, 2 * inner_half,
            facecolor=inner_col, edgecolor='none'
        ))
        ax.text(c, y, str(int(round(devs[i]))),
                ha='center', va='center', fontsize=9, color=text_col)

    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-1.55 if show_prob_legend else -0.6, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    if show_prob_legend:
        _draw_probability_colorbar(ax)
    return fig, ax


def plotProbColormap(save=False, filename="tmp", fmt="pdf"):
    """Display the standard probability color legend used by the plot helpers."""
    legend_items = [
        ("p < 0.5%",  "#111111", "#111111", "white"),
        ("p < 1%",    "#8B0000", "#8B0000", "white"),
        ("p < 2%",    "#C41E1E", "#C41E1E", "white"),
        ("p < 5%",    "#E87722", "#E87722", "black"),
        ("normal",    "#EBEBEB", "#BBBBBB", "black"),
        ("p ≥ 95%",   "#EBEBEB", "#1A7A1A", "black"),
    ]
    n = len(legend_items)
    fig, ax = plt.subplots(figsize=(9, 0.65))
    pad = 0.04
    for idx, (label, fill, border, tc) in enumerate(legend_items):
        lw = 2.5 if border == "#1A7A1A" else 1.5
        rect = mpatches.Rectangle(
            (idx + pad, pad),
            1 - 2 * pad, 1 - 2 * pad,
            facecolor=fill, edgecolor=border, linewidth=lw,
        )
        ax.add_patch(rect)
        ax.text(idx + 0.5, 0.5, label,
                ha="center", va="center", fontsize=8,
                color=tc, fontweight="bold")
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis("off")
    plt.tight_layout(pad=0.1)
    _save_plot(fig, save=save, filename=filename, fmt=fmt)
    plt.show()
    plt.close(fig)


def vfplot(df_vf_py, type="s", title="", save=False, filename="tmp", fmt="pdf", show_colorbar=True):
    """Plot a single visual field using the active Deviation_Analysis NV setting."""
    df_vf, vf_cols, df_td, df_pd, df_tdp, df_pdp, _ = _compute_plot_dataframes(
        df_vf_py.head(1)
    )
    sens = _row_to_array(df_vf.iloc[0], vf_cols)
    td = _row_to_array(df_td.iloc[0], vf_cols)
    pd_vals = _row_to_array(df_pd.iloc[0], vf_cols)
    tdp = _row_to_array(df_tdp.iloc[0], vf_cols)
    pdp = _row_to_array(df_pdp.iloc[0], vf_cols)
    

    if type == "s":
        fig, _ = _vf_sens_plot(sens, title=title, show_sens_legend=show_colorbar)
    elif type == "td":
        fig, _ = _vf_devborder_plot(td, tdp, sens, title=title, show_prob_legend=show_colorbar)
    elif type == "pd":
        fig, _ = _vf_devborder_plot(pd_vals, pdp, sens, title=title, show_prob_legend=show_colorbar)
    elif type == "tds":
        fig, _ = _vf_sdevborder_plot(td, tdp, sens, title=title, show_prob_legend=show_colorbar)
    elif type == "pds":
        fig, _ = _vf_sdevborder_plot(pd_vals, pdp, sens, title=title, show_prob_legend=show_colorbar)
    else:
        raise ValueError(f"Unknown plot type: {type}")

    _save_plot(fig, save=save, filename=filename, fmt=fmt)
    
    plt.show()
    plt.close(fig)


def vfplot_s(df_vf_py, title="", save=False, filename='tmp', fmt='pdf'):
    vfplot(df_vf_py, type='s', title=title, save=save, filename=filename, fmt=fmt)


def vfplot_td(df_vf_py, title="", save=False, filename='tmp', fmt='pdf'):
    vfplot(df_vf_py, type='td', title=title, save=save, filename=filename, fmt=fmt)


def vfplot_pd(df_vf_py, title="", save=False, filename='tmp', fmt='pdf'):
    vfplot(df_vf_py, type='pd', title=title, save=save, filename=filename, fmt=fmt)


def vfplot_tds(df_vf_py, title="", save=False, filename='tmp', fmt='pdf'):
    vfplot(df_vf_py, type='tds', title=title, save=save, filename=filename, fmt=fmt)


def vfplot_pds(df_vf_py, title="", save=False, filename='tmp', fmt='pdf'):
    vfplot(df_vf_py, type='pds', title=title, save=save, filename=filename, fmt=fmt)


def vfplotsparklines(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'):
    """Per-location trend lines ("sparklines") over the visit series.

    Each cell of the 24-2 grid shows that location's value across all visits
    (earliest to latest). A line is red where its slope is negative (declining)
    and black otherwise, so a cluster of red sparklines marks an area that is
    deteriorating over time. ``type`` selects 's' (sensitivity), 'td' or 'pd'.
    """
    df_vf, vf_cols, df_td, df_pd, _, _, _ = _compute_plot_dataframes(df_vf_py)
    if type == 's':
        data = _matrix_from_df(df_vf, vf_cols)
    elif type == 'td':
        data = _matrix_from_df(df_td, vf_cols)
    elif type == 'pd':
        data = _matrix_from_df(df_pd, vf_cols)
    else:
        raise ValueError(f'Unknown sparkline type: {type}')

    nvisits = data.shape[0]
    x = np.arange(nvisits, dtype=float)
    finite_vals = data[np.isfinite(data)]
    vmin_s = float(np.nanmin(finite_vals)) if finite_vals.size else 0.0
    vmax_s = float(np.nanmax(finite_vals)) if finite_vals.size else 1.0
    rng = max(vmax_s - vmin_s, 1e-6)

    cell_w, cell_h = 0.85, 0.85
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-0.6, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Sparklines ({type})', fontsize=10)

    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            continue
        c, r = pos
        y = 7 - r
        if i in _BLIND_SPOT_IDX:
            ellipse = mpatches.Ellipse((c, y), cell_w * 0.8, cell_h * 0.6,
                                       color='#BBBBBB', ec='#999999', lw=0.8)
            ax.add_patch(ellipse)
            continue

        rect = mpatches.FancyBboxPatch(
            (c - cell_w / 2, y - cell_h / 2), cell_w, cell_h,
            boxstyle='round,pad=0.03', facecolor='#F8F8F8', edgecolor='#CCCCCC', linewidth=0.6,
        )
        ax.add_patch(rect)

        if i >= data.shape[1]:
            continue
        series = data[:, i]
        if np.all(np.isnan(series)):
            continue

        sy = (series - vmin_s) / rng
        sx = np.linspace(0, 1, nvisits)
        px = c - cell_w / 2 + 0.05 + sx * (cell_w - 0.10)
        py = y - cell_h / 2 + 0.05 + sy * (cell_h - 0.10)
        slope = _simple_slope(x, series)
        line_color = 'red' if np.isfinite(slope) and slope < 0 else 'black'
        ax.plot(px, py, color=line_color, linewidth=0.7, solid_capstyle='round')

    ax.axvline(x=4.5, color='#AAAAAA', linewidth=0.8)
    ax.axhline(y=3.5, color='#AAAAAA', linewidth=0.8)
    plt.tight_layout()
    _save_plot(fig, save=save, filename=filename, fmt=fmt)
    plt.show()
    plt.close(fig)


def vfplotsparklines_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotsparklines(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)


def vfplotsparklines_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotsparklines(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)


def vfplotsparklines_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotsparklines(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)


def vfplotplr(df_vf_py, type='s', save=False, filename='tmp', fmt='pdf'):
    """Plot pointwise regression slopes using the active Deviation_Analysis NV setting."""
    res = plr(df_vf_py, type=type)
    slopes = np.array(list(res['sl'].values()), dtype=float)
    pvals = np.array(list(res['pval'].values()), dtype=float)

    slopes_display = np.where(np.isnan(slopes), np.nan, np.round(slopes, 1))
    probs_display = np.where(np.isnan(pvals), 0.5, pvals)
    fig, _ = _vf_prob_plot(slopes_display, probs_display, title=f'PLR slopes ({type})', fmt='.1f')
    _save_plot(fig, save=save, filename=filename, fmt=fmt)
    plt.show()
    plt.close(fig)


def vfplotplr_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotplr(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)


def vfplotplr_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotplr(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)


def vfplotplr_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vfplotplr(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)


def vflegoplot(df_vf_py, type='s', grp=3, save=False, filename='tmp', fmt='pdf'):
    """Lego plot of change between the start and end of a VF series.

    For each location on the 24-2 grid the tile is coloured by the baseline value
    (mean of the first ``grp`` visits), the circle on top by the follow-up value
    (mean of the last ``grp`` visits), and the centre text gives the change
    (follow-up minus baseline). A darker circle than its tile with a large
    negative number marks a location that has worsened. ``type`` selects 's',
    'td' or 'pd'.
    """
    df_vf, vf_cols = _canonicalize_vf_dataframe(df_vf_py)
    nvisits = len(df_vf)
    thr = min(grp, nvisits)

    sens_mat = _matrix_from_df(df_vf, vf_cols)
    sens_b_arr = _nanmean_columns(sens_mat[:thr])
    sens_l_arr = _nanmean_columns(sens_mat[-thr:])

    def _mean_df(sens_arr):
        row = {c: df_vf[c].iloc[0] for c in df_vf.columns if c not in vf_cols}
        for j, col in enumerate(vf_cols):
            row[col] = float(sens_arr[j]) if j < len(sens_arr) and np.isfinite(sens_arr[j]) else np.nan
        return pd.DataFrame([row])[list(df_vf.columns)]

    if type == 's':
        sens_b = _expand_24d2_values(sens_b_arr)
        sens_l = _expand_24d2_values(sens_l_arr)
        diff = sens_l - sens_b

        def _bg(i): return _gray_hex(_r_sens_gray(sens_b[i]))
        def _fg(i): return _gray_hex(_r_sens_gray(sens_l[i]))
        def _tc(i): return '#4D4D4D' if _r_sens_gray(sens_l[i]) >= 0.5 else '#B3B3B3'

    elif type in ('td', 'pd'):
        df_b = _mean_df(sens_b_arr)
        df_l = _mean_df(sens_l_arr)

        if type == 'td':
            dev_b_df = py_gettd(df_b)
            dev_l_df = py_gettd(df_l)
            prob_b_df = py_gettdp(dev_b_df)
            prob_l_df = py_gettdp(dev_l_df)
        else:
            dev_b_df = py_getpd(py_gettd(df_b))
            dev_l_df = py_getpd(py_gettd(df_l))
            prob_b_df = py_getpdp(dev_b_df)
            prob_l_df = py_getpdp(dev_l_df)

        dev_b  = _expand_24d2_values(_row_to_array(dev_b_df.iloc[0],  vf_cols))
        dev_l  = _expand_24d2_values(_row_to_array(dev_l_df.iloc[0],  vf_cols))
        prob_b = _expand_24d2_values(_row_to_array(prob_b_df.iloc[0], vf_cols))
        prob_l = _expand_24d2_values(_row_to_array(prob_l_df.iloc[0], vf_cols))
        sens_b = _expand_24d2_values(sens_b_arr)
        sens_l = _expand_24d2_values(sens_l_arr)
        diff = dev_l - dev_b

        def _prob_fill(p, s=None):
            if s is not None and np.isfinite(float(s)) and float(s) < 0:
                return "#111111"

            fc, ec, tc, lw = _probability_cell_style(p, scheme="5")
            return fc

        def _bg(i): return _prob_fill(prob_b[i], sens_b[i])
        def _fg(i): return _prob_fill(prob_l[i], sens_l[i])
        def _tc(i): return '#4D4D4D' if _hex_luminance(_fg(i)) >= 0.4 else '#B3B3B3'

    else:
        raise ValueError(f'Unknown lego type: {type}')

    fig, ax = plt.subplots(figsize=(7, 6))
    drew_bs = False
    half, crad = 0.43, 0.30

    for i, pos in enumerate(_GRID_24D2):
        if pos is None:
            if not drew_bs:
                _draw_r_blind_spot(ax)
                drew_bs = True
            continue
        c, r = pos
        y = 7 - r
        if i >= len(diff) or np.isnan(diff[i]):
            continue

        ax.add_patch(mpatches.Rectangle(
            (c - half, y - half), 2 * half, 2 * half,
            facecolor=_bg(i), edgecolor='none'
        ))
        ax.add_patch(mpatches.Circle(
            (c, y), radius=crad, facecolor=_fg(i), edgecolor='none', zorder=2
        ))
        d_r = round(diff[i], 1)
        txt = str(int(d_r)) if d_r == int(d_r) else f'{d_r:.1f}'
        # bold for readability on dark tiles
        ax.text(c, y, txt, ha='center', va='center', fontsize=7,
                fontweight='bold', color=_tc(i), zorder=3)

    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-0.6, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Lego plot ({type})', fontsize=10)
    plt.tight_layout()
    _save_plot(fig, save=save, filename=filename, fmt=fmt)
    plt.show()
    plt.close(fig)


def vflegoplot_s(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vflegoplot(df_vf_py, type='s', save=save, filename=filename, fmt=fmt)


def vflegoplot_td(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vflegoplot(df_vf_py, type='td', save=save, filename=filename, fmt=fmt)


def vflegoplot_pd(df_vf_py, save=False, filename='tmp', fmt='pdf'):
    vflegoplot(df_vf_py, type='pd', save=save, filename=filename, fmt=fmt)


def vfsfa(df_vf_py, filename='report.pdf'):
    """Generate a single-field analysis report with PyVisualFields-derived values."""
    df_vf, vf_cols, df_td, df_pd, df_tdp, df_pdp, df_gi = _compute_plot_dataframes(df_vf_py.head(1))
    sens = _row_to_array(df_vf.iloc[0], vf_cols)
    td = _row_to_array(df_td.iloc[0], vf_cols)
    pd_vals = _row_to_array(df_pd.iloc[0], vf_cols)
    tdp = _row_to_array(df_tdp.iloc[0], vf_cols)
    pdp = _row_to_array(df_pdp.iloc[0], vf_cols)
    gi = df_gi.iloc[0]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    _vf_grid_plot(sens, title='Sensitivity (dB)', ax=axes[0])
    _vf_grid_plot(td, title='Total Deviation (dB)', ax=axes[1])
    _vf_prob_plot(pd_vals, pdp, title='Pattern Deviation Prob', ax=axes[2])

    fig.suptitle(
        f"MD={gi['tmd']:.2f} dB   PSD={gi['psd']:.2f} dB   VFI={gi['vfi']:.1f}%",
        fontsize=11,
    )
    fig.savefig(filename, bbox_inches='tight')
    plt.show()
    plt.close(fig)
    print(f'Saved: {filename}')
    
    
    





def getallvalues(dataframe_VFs_py):
    """Compute all deviations and global indices."""
    return py_getallvalues(dataframe_VFs_py)
        
       
def gettd(dataframe_VFs_py):
    """Total Deviation values."""
    return py_gettd(dataframe_VFs_py)
        

def gettdp(dataframe_TDs_py):
    """Total Deviation probability values."""
    return py_gettdp(dataframe_TDs_py)

    
def getpd(dataframe_TDs_py):
    """Pattern Deviation values."""
    return py_getpd(dataframe_TDs_py)


def getpdp(dataframe_PDs_py):
    """Pattern Deviation probability values."""
    return py_getpdp(dataframe_PDs_py)


              
def getgh(dataframe_TDs_py):
    """General Height values."""
    return py_getgh(dataframe_TDs_py)


def getgl(dataframe_VFs_py):
    """Global Indices (MD, PSD, VFI, etc.)."""
    return py_getgl(dataframe_VFs_py)


def getglp(dataframe_GIs_py):
    """Global Indices probability values."""
    return py_getglp(dataframe_GIs_py)






# def vfisvalid():
    

def locmaps():
    """Return all location maps as a dictionary."""
    from PyVisualFields.Deviation_Analysis import _LOCMAPS
    return _LOCMAPS

def normvals():
    """Return all predefined normative value settings."""
    return py_normvals()

def get_info_normvals():
    """Print and return info for all predefined NV settings."""
    return py_get_info_normvals()



def getnv():
    """Return the current normative-value info."""
    return py_getnv()

def setdefaults():
    """Reset NV setting to package default."""
    py_setdefaults()



def setnv(inp):
    """
    Set active normative values.
    Pass a key string (e.g. 'iowa_Peri_pw') or a custom NV dict from nvgenerate.
    """
    if isinstance(inp, str):
        py_setnv(inp)
    elif isinstance(inp, dict):
        py_setnv_custom(inp)
    else:
        raise TypeError(f"setnv expects a str key or a dict from nvgenerate, got {type(inp)}")
    
    

def nvgenerate(df_py, method="pointwise",
               name="SUNY-IU pointwise NVs",
               perimetry="static automated perimetry",
               strategy="SITA standard",
               size="Size III"):
    """
    Generate normative values from a control population.
    method: 'pointwise' (per-location OLS regression on age).
    Returns: (nv_py, nv_py)  – same dict twice for API compatibility
    """
    nv_py = py_nvgenerate(df_py, method=method, name=name,
                          perimetry=perimetry, strategy=strategy, size=size)
    return nv_py, nv_py


# def vfdesc(dataframe_VFs_R):
#     # print("Hello from a function") 
#     print(lib_vf.vfdesc(dataframe_VFs_R))


def vfdesc(dataframe_VFs_py):
    # print("Hello from a function") 
    print(dataframe_VFs_py.describe())    
    




# Column map: glr type -> getgl() output column
_GLR_TYPE_COL = {
    'ms':  'msens',
    'ss':  'ssens',
    'md':  'tmd',
    'sd':  'tsd',
    'pmd': 'pmd',
    'psd': 'psd',
    'vfi': 'vfi',
    'gh':  'gh',
}


def glr(df_gi_py, type="md", testSlope=0):
    """Global linear regression.

    Parameters
    ----------
    df_gi_py : pandas.DataFrame
        Output of ``getgl()`` (global-index columns) or a raw VF dataframe
        (global indices will be computed automatically).
    type : str
        Global index to regress.  One of: 'ms', 'ss', 'md', 'sd', 'pmd', 'psd', 'vfi', 'gh'.
    testSlope : float
        Null-hypothesis slope (default 0).

    Returns
    -------
    dict
        Keys: id, eye, type, testSlope, nvisits, years, data, pred, sl, int, tval, pval.
    """
    valid_types = set(_GLR_TYPE_COL)
    if type not in valid_types:
        raise ValueError(f"glr: type must be one of {sorted(valid_types)}, got '{type}'")

    col = _GLR_TYPE_COL[type]

    # Accept getgl() output (has 'tmd') or a raw VF dataframe
    if col not in df_gi_py.columns:
        df_gi_py = py_getgl(df_gi_py)

    df_sorted = _sort_vf_dataframe(df_gi_py)
    years = _parse_years(df_sorted)
    data  = df_sorted[col].values.astype(float)

    sl, intercept, tval, pval, _se = _ols_regression(years, data, float(testSlope))

    pred = sl * years + intercept if np.isfinite(sl) else np.full_like(years, np.nan)

    result = {
        'type':      type,
        'testSlope': testSlope,
        'nvisits':   len(df_sorted),
        'years':     years,
        'data':      data,
        'pred':      pred,
        'sl':        sl,
        'int':       intercept,
        'tval':      tval,
        'pval':      pval,
        'se':        _se,
    }
    if 'id' in df_sorted.columns:
        result['id'] = df_sorted['id'].iloc[0]
    if 'eye' in df_sorted.columns:
        result['eye'] = df_sorted['eye'].iloc[0]
    return result


def _parse_years(df_vf_py):
    """Extract years-from-baseline from a dataframe date column when present."""
    if 'date' not in df_vf_py.columns:
        return np.arange(len(df_vf_py), dtype=float)

    raw = df_vf_py['date'].reset_index(drop=True)
    if pd.api.types.is_datetime64_any_dtype(raw):
        t0 = raw.iloc[0]
        return np.array([(d - t0).days / 365.25 for d in raw], dtype=float)

    dates = pd.to_datetime(raw, errors='coerce')
    if not dates.isna().all():
        t0 = dates.iloc[0]
        return np.array([(d - t0).days / 365.25 for d in dates], dtype=float)

    try:
        int_vals = pd.to_numeric(raw, errors='coerce')
        if int_vals.notna().all() and int_vals.between(0, 30000).all():
            dates = pd.to_datetime(int_vals.astype(int), unit='D', origin='1970-01-01')
            t0 = dates.iloc[0]
            return np.array([(d - t0).days / 365.25 for d in dates], dtype=float)
    except Exception:
        pass

    return np.arange(len(df_vf_py), dtype=float)


def _normal_cdf(x):
    """Normal CDF helper (no longer used for p-values; see _ols_regression)."""
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


_REG_PRECISION = 1e-06   # threshold for a flat/invariant series, as in R


def _ols_regression(x, y, test_slope):
    """OLS slope test matching R visualFields glr()/plr() (Student-t p-value, n-2 dof)."""
    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    if n < 3:
        return np.nan, np.nan, np.nan, np.nan, np.nan

    x_use = x[mask]
    y_use = y[mask]
    ssyears = (n - 1) * np.var(x_use, ddof=1)
    if ssyears <= 0:
        return np.nan, np.nan, np.nan, np.nan, np.nan
    ssvf = (n - 1) * np.var(y_use, ddof=1)

    x_mean = x_use.mean()
    y_mean = y_use.mean()
    slope = float(np.sum((x_use - x_mean) * (y_use - y_mean)) / ssyears)
    intercept = float(y_mean - slope * x_mean)

    v = (ssvf - ssyears * slope ** 2) / ((n - 2) * ssyears)
    se = float(np.sqrt(v)) if v > 0 else 0.0

    # a flat series has no trend; R forces slope 0 and se = precision
    if float(np.std(y_use, ddof=1)) <= _REG_PRECISION:
        slope = 0.0
        intercept = float(y_use[0])
        se = _REG_PRECISION

    if se > 0:
        tval = (slope - test_slope) / se
    else:
        tval = np.inf * np.sign(slope - test_slope) if slope != test_slope else 0.0
    pval = float(_student_t.cdf(tval, n - 2))
    return slope, intercept, tval, pval, se


def plr(df_VFs_py, type = "s", testSlope = 0):
    """Perform pointwise linear regression using the active Deviation_Analysis NV setting.

    The default ``type="s"`` regresses raw sensitivity, matching R visualFields
    1.0.7 (which removed the ``type`` argument and always uses sensitivity). Pass
    ``type="td"`` for the older R 1.0.1 behavior (total deviation).
    """
    df_vf, vf_cols = _canonicalize_vf_dataframe(df_VFs_py)
    years = _parse_years(df_vf)

    if type in ('td', 'tds'):
        data = _matrix_from_df(py_gettd(df_vf), vf_cols)
    elif type in ('pd', 'pds'):
        data = _matrix_from_df(py_getpd(py_gettd(df_vf)), vf_cols)
    else:
        data = _matrix_from_df(df_vf, vf_cols)

    n_pts = data.shape[1]
    if np.isscalar(testSlope):
        test_slope_arr = np.full(n_pts, float(testSlope), dtype=float)
    else:
        test_slope_arr = np.asarray(testSlope, dtype=float)
        if test_slope_arr.size != n_pts:
            raise ValueError('testSlope must be a scalar or have one value per visual-field location.')

    sl = np.full(n_pts, np.nan, dtype=float)
    intercept = np.full(n_pts, np.nan, dtype=float)
    tval = np.full(n_pts, np.nan, dtype=float)
    pval = np.full(n_pts, np.nan, dtype=float)
    se_arr = np.full(n_pts, np.nan, dtype=float)

    for idx in range(n_pts):
        sl[idx], intercept[idx], tval[idx], pval[idx], se_arr[idx] = _ols_regression(
            years, data[:, idx], test_slope_arr[idx]
        )

    pred = np.outer(years, sl) + intercept
    result = {
        'type': type,
        'testSlope': testSlope,
        'nvisits': len(df_vf),
        'years': years,
        'data': data,
        'pred': pred,
        'sl': dict(zip(vf_cols, sl)),
        'int': dict(zip(vf_cols, intercept)),
        'tval': dict(zip(vf_cols, tval)),
        'pval': dict(zip(vf_cols, pval)),
        'se': dict(zip(vf_cols, se_arr)),
    }
    if 'id' in df_vf.columns:
        result['id'] = df_vf['id'].iloc[0]
    if 'eye' in df_vf.columns:
        result['eye'] = df_vf['eye'].iloc[0]
    return result


# ---------------------------------------------------------------------------
# PoPLR helpers
# ---------------------------------------------------------------------------

_POPLR_RNG_SEED = 42       # deterministic seed for sampled permutations
_POPLR_SAMPLE_CAP = 5000   # max permutations when visits > 7


def _poplr_sstats(pval_matrix, trunc=1.0):
    """Combine permutation p-values like R visualFields poplrsstats.

    pval_matrix is (n_perm, n_loc) with the observed ordering in row 0; returns
    the observed csl/cslp/csr/csrp and the full cslall/csrall.
    """
    P = np.asarray(pval_matrix, dtype=float)
    valid = np.isfinite(P[0])          # drop blind-spot / all-NaN columns
    P = np.clip(P[:, valid], _REG_PRECISION, 1.0 - _REG_PRECISION)
    nperm = P.shape[0]

    def _combine(pv):
        tp = pv.min(axis=1)
        tp = np.where(tp < trunc, trunc, tp)
        keep = pv <= tp[:, None]
        return -np.sum(np.where(keep, np.log(pv), 0.0), axis=1)

    csl = _combine(P)
    csr = _combine(1.0 - P)
    cslp = 1.0 - _rankdata(csl, method='average') / nperm
    csrp = 1.0 - _rankdata(csr, method='average') / nperm
    return {
        'csl': float(csl[0]), 'cslp': float(cslp[0]),
        'csr': float(csr[0]), 'csrp': float(csrp[0]),
        'cslall': csl, 'csrall': csr,
    }


def _poplr_perm_regress(years, data, perm_matrix, ts_arr):
    """Per-permutation pointwise regression in one matrix product (R poplrpvals).

    Returns (sl, int, se, pval) of shape (n_perm, n_loc). Equivalent to calling
    _ols_regression per cell but vectorised, so whole-cohort PoPLR is fast.
    """
    # Used Copilot to work out the vectorised permutation algebra here.
    years = np.asarray(years, dtype=float)
    data  = np.asarray(data, dtype=float)
    n     = len(years)

    perm_years = years[perm_matrix]
    syears  = years.sum()
    myears  = years.mean()
    ssyears = (n - 1) * np.var(years, ddof=1)
    kvyears = (n - 2) * ssyears

    mvf  = data.mean(axis=0)
    ssvf = (n - 1) * data.var(axis=0, ddof=1)

    sl   = (perm_years @ data - syears * mvf[None, :]) / ssyears
    intc = mvf[None, :] - myears * sl
    varslope = (ssvf[None, :] - ssyears * sl ** 2) / kvyears
    se = np.sqrt(np.where(varslope < 0, 0.0, varslope))

    inv = data.std(axis=0, ddof=1) <= _REG_PRECISION
    if np.any(inv):
        sl[:, inv]   = 0.0
        intc[:, inv] = data[0, inv]
        se[:, inv]   = _REG_PRECISION

    with np.errstate(divide='ignore', invalid='ignore'):
        tval = (sl - np.asarray(ts_arr, dtype=float)[None, :]) / se
    pval = _student_t.cdf(tval, n - 2)
    return sl, intc, se, pval


def _poplr_permutations(n_visits, nperm_arg):
    """Return array of row-index permutations (n_perms x n_visits).

    Policy
    ------
    n_visits <= 7 : exhaustive (n_visits! rows).
    n_visits >  7 : deterministic random sample capped at _POPLR_SAMPLE_CAP
                    (or the explicit nperm_arg integer if provided).
    """
    import itertools
    import math

    n_fact = math.factorial(n_visits)

    if nperm_arg == 'default':
        if n_visits <= 7:
            return np.array(list(itertools.permutations(range(n_visits))), dtype=int)
        n_draw = min(_POPLR_SAMPLE_CAP, n_fact)
    else:
        n_draw = int(nperm_arg)
        if n_visits <= 7 and n_draw >= n_fact:
            return np.array(list(itertools.permutations(range(n_visits))), dtype=int)

    # keep the observed ordering as row 0, then sample the rest (as R does)
    identity = tuple(range(n_visits))
    rng  = np.random.default_rng(_POPLR_RNG_SEED)
    seen = {identity}
    rows = [list(identity)]
    while len(rows) < n_draw:
        p = tuple(rng.permutation(n_visits).tolist())
        if p not in seen:
            seen.add(p)
            rows.append(list(p))
    return np.array(rows, dtype=int)


def poplr(df_VFs_py, type="s", testSlope=0, nperm='default', trunc=1):
    """PoPLR analysis.

    Permutation Analyses of Pointwise Linear Regression (O'Leary et al. 2012,
    Investigative Ophthalmology and Visual Science, 53).

    Parameters
    ----------
    df_VFs_py : pandas.DataFrame
        Visual field series with sensitivity columns and optionally date/id/eye.
    type : str
        Data to analyse: 's' (sensitivity), 'td' (total deviation), 'pd' (pattern deviation).
    testSlope : float or array-like
        Null-hypothesis slope(s).  Scalar or one value per VF location.
    nperm : int or 'default'
        Number of permutations.  'default' = exhaustive for <= 7 visits, capped 5000 otherwise.
    trunc : float
        Truncation threshold for the Truncated Product Method (default 1 = no truncation).

    Returns
    -------
    dict
        Keys: id, eye, type, testSlope, nvisits, years, data, pred, sl, int, tval, pval,
              csl, cslp, csr, csrp,
              pstats (dict: sl, int, se, pval, permutations),
              cstats (dict: csl, cslp, csr, csrp, cslall, csrall).
    """
    df_vf, vf_cols = _canonicalize_vf_dataframe(df_VFs_py)
    years    = _parse_years(df_vf)
    n_visits = len(df_vf)

    if type in ('td', 'tds'):
        data = _matrix_from_df(py_gettd(df_vf), vf_cols)
    elif type in ('pd', 'pds'):
        data = _matrix_from_df(py_getpd(py_gettd(df_vf)), vf_cols)
    else:
        data = _matrix_from_df(df_vf, vf_cols)

    n_pts = data.shape[1]

    if np.isscalar(testSlope):
        ts_arr = np.full(n_pts, float(testSlope))
    else:
        ts_arr = np.asarray(testSlope, dtype=float)
        if ts_arr.size != n_pts:
            raise ValueError('testSlope must be scalar or have one value per VF location.')

    # Observed PLR
    sl        = np.full(n_pts, np.nan)
    intercept = np.full(n_pts, np.nan)
    tval      = np.full(n_pts, np.nan)
    pval      = np.full(n_pts, np.nan)
    se_arr    = np.full(n_pts, np.nan)

    for j in range(n_pts):
        sl[j], intercept[j], tval[j], pval[j], se_arr[j] = _ols_regression(
            years, data[:, j], ts_arr[j]
        )

    pred    = np.outer(years, sl) + intercept

    # Permutation loop: fill the (n_perm x n_loc) p-value matrix, then combine
    # exactly as R's poplrsstats does (see _poplr_sstats).  Row 0 is observed.
    perm_matrix = _poplr_permutations(n_visits, nperm)
    n_perms     = len(perm_matrix)

    perm_sl, perm_int, perm_se, perm_pval = _poplr_perm_regress(
        years, data, perm_matrix, ts_arr)

    _ss     = _poplr_sstats(perm_pval, trunc)
    csl_obs = _ss['csl']
    csr_obs = _ss['csr']
    cslp    = _ss['cslp']
    csrp    = _ss['csrp']
    cslall  = _ss['cslall']
    csrall  = _ss['csrall']

    pstats = {
        'sl':   sl,
        'int':  intercept,
        'se':   se_arr,
        'pval': pval,
        'permutations': {
            'sl':   perm_sl,
            'int':  perm_int,
            'se':   perm_se,
            'pval': perm_pval,
        },
    }
    cstats = {
        'csl':    csl_obs,
        'cslp':   cslp,
        'csr':    csr_obs,
        'csrp':   csrp,
        'cslall': cslall,
        'csrall': csrall,
    }

    result = {
        'type':      type,
        'testSlope': testSlope,
        'nvisits':   n_visits,
        'years':     years,
        'data':      data,
        'pred':      pred,
        'sl':        sl,
        'int':       intercept,
        'tval':      tval,
        'pval':      pval,
        'csl':       csl_obs,
        'cslp':      cslp,
        'csr':       csr_obs,
        'csrp':      csrp,
        'pstats':    pstats,
        'cstats':    cstats,
    }
    if 'id' in df_vf.columns:
        result['id'] = df_vf['id'].iloc[0]
    if 'eye' in df_vf.columns:
        result['eye'] = df_vf['eye'].iloc[0]
    return result

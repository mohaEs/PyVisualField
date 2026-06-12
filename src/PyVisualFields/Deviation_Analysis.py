# -*- coding: utf-8 -*-
"""
Normative-value computations for visual field analysis using
pandas and numpy. Loads pre-extracted JSON normative databases at import time.

@author: Mohammad Eslami
@contributor: Bharath Erusalagandi (Python implementation)
"""

import os
import json
from copy import deepcopy
import numpy as np
import pandas as pd

_PKL_DIR = os.path.join(os.path.dirname(__file__), "pkl_files")


def _load_json(fname):
    with open(os.path.join(_PKL_DIR, fname), encoding="utf-8") as fh:
        return json.load(fh)


_NORMVALS = _load_json("normvals.json")
_LOCMAPS  = _load_json("locmaps.json")
_META     = _load_json("normvals_meta.json")

_HEIJL_1987_INTERCEPT = [
    33.5, 34.2, 33.8, 33.1, 32.9, 33.0, 33.2, 32.8, 31.5, 32.0, 32.5, 32.1,
    30.8, 31.3, 31.6, 31.0, 30.1, 30.5, 30.9, 30.3, 29.5, 29.8, 30.2, 29.6,
    28.9, 29.1, 29.5, 28.8, 28.0, 28.4, 28.7, 28.1, 27.2, 27.6, 27.9, 27.3,
    26.5, 26.8, 27.1, 26.5, 25.8, 26.0, 26.3, 25.7, 25.0, 25.2, 25.5, 24.9,
    24.2, 24.4, 24.7, 24.1, 23.5, 23.7,
]
_HEIJL_1987_SLOPE = [
    -0.082, -0.082, -0.083, -0.082, -0.081, -0.081, -0.082, -0.081, -0.080, -0.081, -0.080, -0.079,
    -0.079, -0.079, -0.079, -0.078, -0.078, -0.078, -0.078, -0.077, -0.077, -0.077, -0.077, -0.076,
    -0.076, -0.076, -0.076, -0.075, -0.075, -0.075, -0.075, -0.074, -0.074, -0.074, -0.074, -0.073,
    -0.073, -0.073, -0.073, -0.072, -0.072, -0.072, -0.072, -0.071, -0.071, -0.071, -0.071, -0.070,
    -0.070, -0.070, -0.070, -0.069, -0.069, -0.069,
]


def _register_builtin_normvals() -> None:
    """Register deterministic built-in NV aliases not stored as standalone JSON blobs."""
    if 'heijl_1987' not in _NORMVALS:
        heijl_nv = deepcopy(_NORMVALS['sunyiu_24d2'])
        heijl_nv['info'] = {
            'name': 'Heijl 1987 classic NVs for 24-2',
            'perimetry': 'Static automated perimetry',
            'strategy': 'Full threshold',
            'size': 'Size III',
        }
        heijl_nv['agem_coeff'] = {
            'intercept': _HEIJL_1987_INTERCEPT,
            'slope': _HEIJL_1987_SLOPE,
        }
        _NORMVALS['heijl_1987'] = heijl_nv

    _META.setdefault('name_to_key', {})['Heijl 1987 classic NVs for 24-2'] = 'heijl_1987'


_register_builtin_normvals()

_current_nv_key: str = _META["default_nv_key"]


def _nv() -> dict:
    """Return the currently active normative-value dictionary."""
    return _NORMVALS[_current_nv_key]


def _get_vf_cols(df: pd.DataFrame, colname='l') -> list:
    """Ordered list of location columns (l1, l2, …) present in df."""
    return [c for c in df.columns if c.startswith(colname) and c[len(colname):].isdigit()]


def _info_cols(df: pd.DataFrame) -> list:
    vf = set(_get_vf_cols(df))
    return [c for c in df.columns if c not in vf]


# ---------------------------------------------------------------------------
# NV management
# ---------------------------------------------------------------------------

def py_getnv() -> dict:
    """Return the current normative-value key and info block."""
    nv = _nv()
    print(f"$name\n[1] \"{nv['info']['name']}\"\n\n"
          f"$perimetry\n[1] \"{nv['info']['perimetry']}\"\n\n"
          f"$strategy\n[1] \"{nv['info']['strategy']}\"\n\n"
          f"$size\n[1] \"{nv['info']['size']}\"")
    return [_current_nv_key, nv["info"]]


def py_setnv(key: str) -> None:
    """Set the active normative-value setting by key name."""
    global _current_nv_key
    valid = list(_NORMVALS.keys())
    if key not in valid:
        raise ValueError(f"NV key '{key}' not found. Valid: {valid}")
    _current_nv_key = key


def py_setdefaults() -> None:
    """Reset to the package default normative values (sunyiu_24d2)."""
    global _current_nv_key
    _current_nv_key = _META["default_nv_key"]
    print(f"==> default normalization setting is set: {_current_nv_key}")


def py_normvals() -> dict:
    """Return the full normvals dictionary (all predefined NV settings)."""
    return _NORMVALS


def py_get_info_normvals() -> dict:
    """Print and return info for all predefined NV settings."""
    print("==> comment: > pw: pointwise, classic: smooth")
    print("==> comment: > default is: sunyiu_24d2")
    result = {}
    for k, nv in _NORMVALS.items():
        print(f"\n==> SettingName:  {k}")
        for field, val in nv["info"].items():
            print(f"  {field}: {val}")
        result[k] = nv["info"]
    return result


def py_nvgenerate(df_vf: pd.DataFrame, method: str = "pointwise",
                  name: str = "custom_NV", perimetry: str = "",
                  strategy: str = "", size: str = "") -> dict:
    """
    Generate a new normative-value set from a control population using
    pointwise linear regression (age vs sensitivity per location).
    """
    if method != "pointwise":
        raise NotImplementedError("Only 'pointwise' method is currently supported.")

    vf_cols = _get_vf_cols(df_vf)
    ages    = df_vf["age"].values.astype(float)
    n_locs  = len(vf_cols)

    intercept = np.zeros(n_locs)
    slope     = np.zeros(n_locs)
    sd_vf     = np.zeros(n_locs)

    for j, col in enumerate(vf_cols):
        y    = df_vf[col].values.astype(float)
        mask = ~np.isnan(y) & ~np.isnan(ages)
        if mask.sum() < 2:
            continue
        coeffs       = np.polyfit(ages[mask], y[mask], 1)
        slope[j]     = coeffs[0]
        intercept[j] = coeffs[1]
        residuals    = y[mask] - (coeffs[0] * ages[mask] + coeffs[1])
        sd_vf[j]     = residuals.std(ddof=1)

    nv_py = {
        "info": {"name": name, "perimetry": perimetry,
                 "strategy": strategy, "size": size},
        "agem_coeff": {"intercept": intercept.tolist(),
                       "slope": slope.tolist()},
        "sd": {"vf": sd_vf.tolist(), "td": sd_vf.tolist(), "pd": sd_vf.tolist()},
        "gh_perc":   _nv().get("gh_perc",   0.85),
        "td_lut":    _nv().get("td_lut",    {}),
        "td_probs":  _nv().get("td_probs",  []),
        "pd_lut":    _nv().get("pd_lut",    {}),
        "pd_probs":  _nv().get("pd_probs",  []),
        "gl_bs":     _nv().get("gl_bs",     []),
        "gl_wtd":    _nv().get("gl_wtd",    []),
        "gl_wpd":    _nv().get("gl_wpd",    []),
        "gl_coord":  _nv().get("gl_coord",  {}),
        "glp_lut":   _nv().get("glp_lut",   {}),
        "glp_probs": _nv().get("glp_probs", []),
        "glp_idxm":  _nv().get("glp_idxm",  []),
        "glp_idxs":  _nv().get("glp_idxs",  []),
    }
    return nv_py


def py_setnv_custom(nv_py: dict) -> None:
    """Register a custom NV dict and activate it."""
    global _current_nv_key
    key = nv_py["info"]["name"].replace(" ", "_")
    _NORMVALS[key] = nv_py
    _current_nv_key = key


# ---------------------------------------------------------------------------
# Deviation computations
# ---------------------------------------------------------------------------

def py_gettd(df_vf: pd.DataFrame) -> pd.DataFrame:
    """Total Deviation = measured sensitivity − age-expected normal."""

    nv = _nv()
    coeff = nv["agem_coeff"]

    intercept = np.array(
        [float(v) if str(v) != "NA" else np.nan
         for v in coeff["intercept"]],
        dtype=float,
    )

    slope_arr = np.array(
        [float(v) if str(v) != "NA" else np.nan
         for v in coeff["slope"]],
        dtype=float,
    )

    vf_cols = _get_vf_cols(df_vf, colname='l')

    ages = df_vf["age"].values.astype(float)
    sens = df_vf[vf_cols].values.astype(float)

    expected = intercept + slope_arr * ages[:, np.newaxis]
    td_vals = sens - expected

    meta_cols = [c for c in df_vf.columns if c not in vf_cols]

    df_td = df_vf[meta_cols].copy()

    td_cols = [f"td{i}" for i in range(1, len(vf_cols) + 1)]

    df_td[td_cols] = td_vals

    return df_td


def py_getgh(df_td: pd.DataFrame) -> np.ndarray:
    """General Height (85th percentile of TD, excluding blind-spot locations)."""
    nv      = _nv()
    gh_perc = float(nv["gh_perc"])
    bs_1idx = nv.get("gl_bs", []) or []
    bs_cols = {f"l{i}" for i in bs_1idx if i is not None}

    td_cols  = _get_vf_cols(df_td, colname='td')
    use_cols = [c for c in td_cols if c not in bs_cols]

    vals = df_td[use_cols].values.astype(float)
    n    = vals.shape[1]
    # R's ghfun: pos = floor((1 - perc) * ncol), then the pos-th largest TD.
    pos  = max(int(np.floor((1.0 - gh_perc) * n)), 1)

    sorted_desc = np.sort(vals, axis=1)[:, ::-1]
    return sorted_desc[:, pos - 1]


def py_getpd(df_td: pd.DataFrame) -> pd.DataFrame:
    """Pattern Deviation = Total Deviation − General Height."""
    td_cols = _get_vf_cols(df_td, colname='td')
    gh      = py_getgh(df_td)

    meta_cols = [c for c in df_td.columns if c not in td_cols]

    pd_vals = df_td[td_cols].values.astype(float) - gh[:, np.newaxis]

    df_pd = df_td[meta_cols].copy()

    pd_cols = [f"pd{i}" for i in range(1, len(td_cols) + 1)]

    df_pd[pd_cols] = pd_vals

    return df_pd



# ---------------------------------------------------------------------------
# Probability lookup tables
# ---------------------------------------------------------------------------

def _parse_lut_value(v) -> float:
    """Convert R-style Inf / -Inf / NA strings to float."""
    if v == "Inf":   return np.inf
    if v == "-Inf":  return -np.inf
    if v is None or str(v) == "NA": return np.nan
    return float(v)


def _get_point_cols(df, prefix):
    return sorted(
        [
            c for c in df.columns
            if c.startswith(prefix) and c[len(prefix):].isdigit()
        ],
        key=lambda x: int(x[len(prefix):])
    )

def _apply_prob_lut(
    df: pd.DataFrame,
    lut_dict: dict,
    probs: list,
    input_prefix: str,
    output_prefix: str,
) -> pd.DataFrame:
    """Assign probability levels per location using a cutoff table."""

    in_cols = _get_point_cols(df, input_prefix)

    n_probs = len(probs)
    vals = df[in_cols].values.astype(float)
    R, N = vals.shape
    valsp = np.full((R, N), np.nan)

    lut_arr = np.zeros((n_probs, N), dtype=float)

    for j, col in enumerate(in_cols):
        # LUT keys are usually l1...l54, even when input is td1...td54
        loc_num = int(col[len(input_prefix):])
        lut_key = f"l{loc_num}"

        raw = lut_dict.get(lut_key) or [np.nan] * n_probs

        for i, v in enumerate(raw):
            lut_arr[i, j] = _parse_lut_value(v)

    prob_vals = np.array([
        _parse_lut_value(p) if isinstance(p, str) else float(p)
        for p in probs
    ])

    for i in range(n_probs - 1, 0, -1):
        mask = vals < lut_arr[i, :]
        valsp[mask] = prob_vals[i]

    meta_cols = [c for c in df.columns if c not in in_cols]
    out = df[meta_cols].copy()

    out_cols = [f"{output_prefix}{i}" for i in range(1, N + 1)]
    out[out_cols] = valsp

    return out


def py_gettdp(df_td: pd.DataFrame) -> pd.DataFrame:
    """Total Deviation probability values."""
    nv = _nv()
    return _apply_prob_lut(
        df_td,
        nv["td_lut"],
        nv["td_probs"],
        input_prefix="td",
        output_prefix="tdp",
    )


def py_getpdp(df_pd: pd.DataFrame) -> pd.DataFrame:
    """Pattern Deviation probability values."""
    nv = _nv()
    return _apply_prob_lut(
        df_pd,
        nv["pd_lut"],
        nv["pd_probs"],
        input_prefix="pd",
        output_prefix="pdp",
    )


# ---------------------------------------------------------------------------
# VFI computation (port of R's vfcomputevfi)
# ---------------------------------------------------------------------------

def _compute_vfi(vf_mat, td_mat, pd_mat, tdp_mat, pdp_mat,
                 tmd, mnsens, coord_x, coord_y):
    """Compute Visual Field Index per row."""
    d = np.sqrt(coord_x ** 2 + coord_y ** 2)
    w = 1.0 / (0.08 * (d + 0.8))

    denom  = np.where(mnsens > 0, mnsens, np.nan)
    vfiloc = 100.0 * (1.0 - np.abs(td_mat) / denom)

    use_pd = (tmd >= -20)[:, np.newaxis]
    vfiloc = np.where(use_pd  & (pdp_mat > 0.05), 100.0, vfiloc)
    vfiloc = np.where(~use_pd & (tdp_mat > 0.05), 100.0, vfiloc)
    vfiloc = np.where(vf_mat < 0, 0.0, vfiloc)

    w_broadcast = np.where(np.isnan(vfiloc), 0.0, w)
    w_sum = w_broadcast.sum(axis=1)
    return np.nansum(vfiloc * w_broadcast, axis=1) / w_sum


def _wtd_mean(mat, w):
    """Row-wise weighted mean."""
    return (mat * w).sum(axis=1) / w.sum()


def _wtd_var(mat, w):
    """Row-wise unbiased weighted variance (divides by sum(w) - 1, as Hmisc::wtd.var)."""
    mu   = _wtd_mean(mat, w)
    diff = (mat - mu[:, np.newaxis]) ** 2
    return (diff * w).sum(axis=1) / (w.sum() - 1.0)


# ---------------------------------------------------------------------------
# Global indices
# ---------------------------------------------------------------------------

# def py_getgl(df_vf: pd.DataFrame) -> pd.DataFrame:
#     """Compute global indices: msens, ssens, tmd, tsd, pmd, psd, gh, vfi."""
#     nv      = _nv()
#     bs_1idx = nv.get("gl_bs", []) or []
#     bs_cols = {f"l{i}" for i in bs_1idx if i is not None}

#     vf_cols  = _get_vf_cols(df_vf)
#     use_cols = [c for c in vf_cols if c not in bs_cols]

#     df_td  = py_gettd(df_vf)
#     df_pd  = py_getpd(df_td)
#     df_tdp = py_gettdp(df_td)
#     df_pdp = py_getpdp(df_pd)

#     vf_mat  = df_vf[use_cols].values.astype(float)
#     td_mat  = df_td[use_cols].values.astype(float)
#     pd_mat  = df_pd[use_cols].values.astype(float)
#     tdp_mat = df_tdp[use_cols].values.astype(float)
#     pdp_mat = df_pdp[use_cols].values.astype(float)

#     wtd = np.asarray(nv["gl_wtd"], dtype=float)[:len(use_cols)]
#     wpd = np.asarray(nv["gl_wpd"], dtype=float)[:len(use_cols)]

#     msens = vf_mat.mean(axis=1)
#     ssens = vf_mat.std(axis=1, ddof=1)
#     tmd   = _wtd_mean(td_mat, wtd)
#     tsd   = np.sqrt(_wtd_var(td_mat, wtd))
#     pmd   = _wtd_mean(pd_mat, wpd)
#     psd   = np.sqrt(_wtd_var(pd_mat, wpd))
#     gh    = py_getgh(df_td)

#     # VFI
#     coord     = nv.get("gl_coord", {})
#     coeff     = nv["agem_coeff"]
#     intercept = np.array([float(v) if str(v) != "NA" else np.nan
#                           for v in coeff["intercept"]], dtype=float)
#     slope_arr = np.array([float(v) if str(v) != "NA" else np.nan
#                           for v in coeff["slope"]], dtype=float)

#     all_l_cols  = _get_vf_cols(df_vf)
#     use_idx     = [all_l_cols.index(c) for c in use_cols]
#     intercept_u = intercept[use_idx]
#     slope_u     = slope_arr[use_idx]
#     ages        = df_vf["age"].values.astype(float)
#     mnsens_mat  = intercept_u + slope_u * ages[:, np.newaxis]

#     coord_x = np.asarray(coord.get("x", []), dtype=float)[:len(use_cols)]
#     coord_y = np.asarray(coord.get("y", []), dtype=float)[:len(use_cols)]

#     vfi = _compute_vfi(vf_mat, td_mat, pd_mat, tdp_mat, pdp_mat,
#                        tmd, mnsens_mat, coord_x, coord_y)

#     info   = df_vf[_info_cols(df_vf)].copy().reset_index(drop=True)
#     result = info.assign(msens=msens, ssens=ssens,
#                          tmd=tmd, tsd=tsd, pmd=pmd, psd=psd,
#                          gh=gh, vfi=vfi)
#     return result


# def py_getgl(df_vf: pd.DataFrame) -> pd.DataFrame:
#     """
#     Compute global indices: msens, ssens, tmd, tsd, pmd, psd, gh, vfi.

#     Assumes df_vf is already canonicalized and contains:
#         l1-l54, td1-td54, pd1-pd54, tdp1-tdp54, pdp1-pdp54
#     """

#     nv = _nv()

#     l_cols   = _get_point_cols(df_vf, "l")
#     td_cols  = _get_point_cols(df_vf, "td")
#     pd_cols  = _get_point_cols(df_vf, "pd")
#     tdp_cols = _get_point_cols(df_vf, "tdp")
#     pdp_cols = _get_point_cols(df_vf, "pdp")

#     n_locs = len(l_cols)

#     if not all(len(x) == n_locs for x in [td_cols, pd_cols, tdp_cols, pdp_cols]):
#         raise ValueError(
#             "py_getgl requires matching complete blocks: "
#             "l, td, pd, tdp, and pdp."
#         )

#     bs_1idx = set(nv.get("gl_bs", []) or [])

#     use_idx = [
#         i for i in range(n_locs)
#         if (i + 1) not in bs_1idx
#     ]

#     l_use   = [l_cols[i] for i in use_idx]
#     td_use  = [td_cols[i] for i in use_idx]
#     pd_use  = [pd_cols[i] for i in use_idx]
#     tdp_use = [tdp_cols[i] for i in use_idx]
#     pdp_use = [pdp_cols[i] for i in use_idx]

#     vf_mat  = df_vf[l_use].values.astype(float)
#     td_mat  = df_vf[td_use].values.astype(float)
#     pd_mat  = df_vf[pd_use].values.astype(float)
#     tdp_mat = df_vf[tdp_use].values.astype(float)
#     pdp_mat = df_vf[pdp_use].values.astype(float)

#     wtd = np.asarray(nv["gl_wtd"], dtype=float)
#     wpd = np.asarray(nv["gl_wpd"], dtype=float)

#     if len(wtd) != len(use_idx):
#         raise ValueError(
#         f"Weight length mismatch: gl_wtd has {len(wtd)} weights, "
#         f"but {len(use_idx)} non-blind-spot locations were found."
#         )

#     if len(wpd) != len(use_idx):
#         raise ValueError(
#         f"Weight length mismatch: gl_wpd has {len(wpd)} weights, "
#         f"but {len(use_idx)} non-blind-spot locations were found."
#         )

#     msens = np.nanmean(vf_mat, axis=1)
#     ssens = np.nanstd(vf_mat, axis=1, ddof=1)

#     tmd = _wtd_mean(td_mat, wtd)
#     tsd = np.sqrt(_wtd_var(td_mat, wtd))

#     pmd = _wtd_mean(pd_mat, wpd)
#     psd = np.sqrt(_wtd_var(pd_mat, wpd))

#     gh = py_getgh(df_vf)

#     # VFI
#     coord = nv.get("gl_coord", {})
#     coeff = nv["agem_coeff"]

#     intercept = np.array(
#         [float(v) if str(v) != "NA" else np.nan for v in coeff["intercept"]],
#         dtype=float,
#     )

#     slope_arr = np.array(
#         [float(v) if str(v) != "NA" else np.nan for v in coeff["slope"]],
#         dtype=float,
#     )

#     intercept_u = intercept[use_idx]
#     slope_u = slope_arr[use_idx]

#     ages = df_vf["age"].values.astype(float)
#     mnsens_mat = intercept_u + slope_u * ages[:, np.newaxis]

#     coord_x = np.asarray(coord.get("x", []), dtype=float)
#     coord_y = np.asarray(coord.get("y", []), dtype=float)


#     if len(coord_x) != len(use_idx):
#         coord_x = coord_x[use_idx]

#     if len(coord_y) != len(use_idx):
#         coord_y = coord_y[use_idx]

#     vfi = _compute_vfi(
#         vf_mat,
#         td_mat,
#         pd_mat,
#         tdp_mat,
#         pdp_mat,
#         tmd,
#         mnsens_mat,
#         coord_x,
#         coord_y,
#     )

#     point_cols = set(l_cols + td_cols + pd_cols + tdp_cols + pdp_cols)
#     info_cols = [c for c in df_vf.columns if c not in point_cols]

#     result = df_vf[info_cols].copy().reset_index(drop=True)

#     result = result.assign(
#         msens=msens,
#         ssens=ssens,
#         tmd=tmd,
#         tsd=tsd,
#         pmd=pmd,
#         psd=psd,
#         gh=gh,
#         vfi=vfi,
#     )

#     return result


def py_getgl(df_vf: pd.DataFrame) -> pd.DataFrame:
    """
    Compute missing global indices only.

    Assumes df_vf is canonicalized and contains:
        l1-l54, td1-td54, pd1-pd54, tdp1-tdp54, pdp1-pdp54
    """

    target_cols = ["msens", "ssens", "tmd", "tsd", "pmd", "psd", "gh", "vfi"]
    missing = [c for c in target_cols if c not in df_vf.columns]
    print(f"==> py_getgl: missing global indices to compute: {missing}")

    point_prefixes = ("l", "td", "pd", "tdp", "pdp")
    point_cols = []
    for p in point_prefixes:
        point_cols.extend(_get_point_cols(df_vf, p))

    info_cols = [c for c in df_vf.columns if c not in set(point_cols)]
    result = df_vf[info_cols].copy().reset_index(drop=True)

    if not missing:
        return result

    nv = _nv()

    l_cols   = _get_point_cols(df_vf, "l")
    td_cols  = _get_point_cols(df_vf, "td")
    pd_cols  = _get_point_cols(df_vf, "pd")
    tdp_cols = _get_point_cols(df_vf, "tdp")
    pdp_cols = _get_point_cols(df_vf, "pdp")

    n_locs = len(l_cols)

    if not all(len(x) == n_locs for x in [td_cols, pd_cols, tdp_cols, pdp_cols]):
        raise ValueError(
            "py_getgl requires matching complete blocks: "
            "l, td, pd, tdp, and pdp."
        )

    bs_1idx = set(nv.get("gl_bs", []) or [])
    use_idx = [i for i in range(n_locs) if (i + 1) not in bs_1idx]

    l_use   = [l_cols[i] for i in use_idx]
    td_use  = [td_cols[i] for i in use_idx]
    pd_use  = [pd_cols[i] for i in use_idx]
    tdp_use = [tdp_cols[i] for i in use_idx]
    pdp_use = [pdp_cols[i] for i in use_idx]

    vf_mat = td_mat = pd_mat = tdp_mat = pdp_mat = None

    if any(c in missing for c in ["msens", "ssens", "vfi"]):
        vf_mat = df_vf[l_use].values.astype(float)

    if any(c in missing for c in ["tmd", "tsd", "vfi"]):
        td_mat = df_vf[td_use].values.astype(float)

    if any(c in missing for c in ["pmd", "psd", "vfi"]):
        pd_mat = df_vf[pd_use].values.astype(float)

    if "vfi" in missing:
        tdp_mat = df_vf[tdp_use].values.astype(float)
        pdp_mat = df_vf[pdp_use].values.astype(float)

    wtd = np.asarray(nv["gl_wtd"], dtype=float)
    wpd = np.asarray(nv["gl_wpd"], dtype=float)

    if len(wtd) != len(use_idx):
        raise ValueError(
            f"Weight length mismatch: gl_wtd has {len(wtd)} weights, "
            f"but {len(use_idx)} non-blind-spot locations were found."
        )

    if len(wpd) != len(use_idx):
        raise ValueError(
            f"Weight length mismatch: gl_wpd has {len(wpd)} weights, "
            f"but {len(use_idx)} non-blind-spot locations were found."
        )

    computed = {}

    if "msens" in missing:
        computed["msens"] = np.nanmean(vf_mat, axis=1)

    if "ssens" in missing:
        computed["ssens"] = np.nanstd(vf_mat, axis=1, ddof=1)

    if "tmd" in missing:
        computed["tmd"] = _wtd_mean(td_mat, wtd)

    if "tsd" in missing:
        if td_mat is None:
            td_mat = df_vf[td_use].values.astype(float)
        computed["tsd"] = np.sqrt(_wtd_var(td_mat, wtd))

    if "pmd" in missing:
        computed["pmd"] = _wtd_mean(pd_mat, wpd)

    if "psd" in missing:
        if pd_mat is None:
            pd_mat = df_vf[pd_use].values.astype(float)
        computed["psd"] = np.sqrt(_wtd_var(pd_mat, wpd))

    if "gh" in missing:
        computed["gh"] = py_getgh(df_vf)

    if "vfi" in missing:
        if vf_mat is None:
            vf_mat = df_vf[l_use].values.astype(float)
        if td_mat is None:
            td_mat = df_vf[td_use].values.astype(float)
        if pd_mat is None:
            pd_mat = df_vf[pd_use].values.astype(float)

        coord = nv.get("gl_coord", {})
        coeff = nv["agem_coeff"]

        intercept = np.array(
            [float(v) if str(v) != "NA" else np.nan for v in coeff["intercept"]],
            dtype=float,
        )

        slope_arr = np.array(
            [float(v) if str(v) != "NA" else np.nan for v in coeff["slope"]],
            dtype=float,
        )

        intercept_u = intercept[use_idx]
        slope_u = slope_arr[use_idx]

        ages = df_vf["age"].values.astype(float)
        mnsens_mat = intercept_u + slope_u * ages[:, np.newaxis]

        coord_x = np.asarray(coord.get("x", []), dtype=float)
        coord_y = np.asarray(coord.get("y", []), dtype=float)

        if len(coord_x) != len(use_idx):
            coord_x = coord_x[use_idx]
        if len(coord_y) != len(use_idx):
            coord_y = coord_y[use_idx]

        tmd_for_vfi = (
            result["tmd"].values.astype(float)
            if "tmd" in result.columns
            else computed.get("tmd")
        )

        if tmd_for_vfi is None:
            tmd_for_vfi = _wtd_mean(td_mat, wtd)

        computed["vfi"] = _compute_vfi(
            vf_mat,
            td_mat,
            pd_mat,
            tdp_mat,
            pdp_mat,
            tmd_for_vfi,
            mnsens_mat,
            coord_x,
            coord_y,
        )

    if computed:
        result = pd.concat(
            [result, pd.DataFrame(computed, index=result.index)],
            axis=1,
        )

    return result

def py_getglp(df_gi: pd.DataFrame) -> pd.DataFrame:
    """Global indices probability values (left-tailed for means, right for SDs)."""
    nv       = _nv()
    lut_dict = nv["glp_lut"]
    probs    = nv["glp_probs"]
    idxm_0   = [i - 1 for i in (nv["glp_idxm"] or [])]
    idxs_0   = [i - 1 for i in (nv["glp_idxs"] or [])]

    gl_cols   = ["msens", "ssens", "tmd", "tsd", "pmd", "psd", "gh", "vfi"]
    mean_cols = [gl_cols[i] for i in idxm_0 if i < len(gl_cols)]
    std_cols  = [gl_cols[i] for i in idxs_0  if i < len(gl_cols)]
    n_probs   = len(probs)

    prob_vals = np.array([_parse_lut_value(p) if isinstance(p, str) else float(p)
                          for p in probs])
    df_gp = df_gi.copy()

    def _build_col_lut(col):
        raw = lut_dict.get(col, [np.nan] * n_probs)
        return np.array([_parse_lut_value(v) if isinstance(v, str) else float(v)
                         for v in raw])

    for col in mean_cols:
        if col not in df_gi.columns:
            continue
        cutoffs = _build_col_lut(col)
        vals = df_gi[col].values.astype(float)
        vp   = np.full(len(vals), np.nan)
        for i in range(n_probs - 1, 0, -1):
            vp[vals < cutoffs[i]] = prob_vals[i]
        df_gp[col] = vp

    for col in std_cols:
        if col not in df_gi.columns:
            continue
        cutoffs = _build_col_lut(col)
        vals = df_gi[col].values.astype(float)
        vp   = np.full(len(vals), np.nan)
        for i in range(n_probs - 1, 0, -1):
            vp[vals > cutoffs[i]] = prob_vals[i]
        df_gp[col] = vp

    return df_gp


def py_getallvalues(df_vf: pd.DataFrame):
    """Compute all deviations and global indices in one call.

    Returns: df_td, df_tdp, df_gi, df_gip, df_pd, df_pdp, gh
    """
    df_td  = py_gettd(df_vf)
    df_tdp = py_gettdp(df_td)
    df_pd  = py_getpd(df_td)
    df_pdp = py_getpdp(df_pd)
    df_gi  = np.nan # py_getgl(df_vf)
    df_gip = np.nan # py_getglp(df_gi)
    gh     = py_getgh(df_td)
    return df_td, df_tdp, df_gi, df_gip, df_pd, df_pdp, gh





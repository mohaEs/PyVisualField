
import numpy as np
import pandas as pd

import numpy as np
import pandas as pd

from PyVisualFields.Deviation_Analysis import _get_point_cols, _get_vf_cols

# def _normalise_eye(val):
#     """Return 'OD' or 'OS' regardless of input format."""
#     v = str(val).strip().lower()
#     if v in ('od', 'right', 'r', '1', 'righteye', 're'):
#         return 'OD'
#     if v in ('os', 'left', 'l', '0', 'lefteye', 'le'):
#         return 'OS'
#     return None   # unknown — caller returns Non-GL


# def _pt_cols_from_row(row):
#     """Return sorted point column names (s* or l*) from a row's index."""
#     cols = sorted(
#         [c for c in row.index if len(c) >= 2 and c[0] in ('s', 'l') and c[1:].isdigit()],
#         key=lambda x: int(x[1:])
#     )
#     return cols


# def _pt_cols_from_df(df, listCols=None):
#     """Return sorted point column names (s* or l*) from a dataframe."""
#     cols = sorted(
#         [c for c in df.columns if len(c) >= 2 and c[0] in (listCols) and c[1:].isdigit()],
#         key=lambda x: int(x[1:])
#     )
#     return cols


# def _eye_col(row):
#     """Return the eye value from whichever column name exists (Eye/eye/EYE)."""
#     for name in ('Eye', 'eye', 'EYE'):
#         if name in row.index:
#             return row[name]
#     return None


# def _col(prefix, n, pt_cols):
#     """
#     Return the column name for point n (1-indexed) using whatever prefix
#     is present in pt_cols (s or l).
#     """
#     actual_prefix = pt_cols[0][0] if pt_cols else 's'
#     return f'{actual_prefix}{n}'


def convertVF_to_2D(VF):
    VF_2D = np.full((8,9), np.nan)

    VF_2D[0,3:7] = VF[0:4]
    VF_2D[1,2:8] = VF[4:10]
    VF_2D[2,1:9] = VF[10:18]
    VF_2D[3,0:9] = VF[18:27]
    VF_2D[4,0:9] = VF[27:36]
    VF_2D[5,1:9] = VF[36:44]
    VF_2D[6,2:8] = VF[44:50]
    VF_2D[7,3:7] = VF[50:54]

    return VF_2D

##########################################################
###################################################


# def Fn_HAP2(df_PDP):
#     pt_cols  = _pt_cols_from_df(df_PDP)
#     data     = df_PDP[pt_cols]

#     counts_05 = (data <= 0.05).sum(axis=1)
#     counts_01 = (data <= 0.01).sum(axis=1)

#     df_PDP['HAP2_p1_clf'] = np.where(
#         (counts_05 >= 3) & (counts_01 >= 1), 'GL', 'Non-GL')

#     df_GL = df_PDP[df_PDP['HAP2_p1_clf'] == 'GL'].copy()

#     # find MD column case-insensitively
#     md_col = next((c for c in df_PDP.columns if c.lower() in ('md', 'tmd')), None)
#     if md_col:
#         md = df_GL[md_col]
#         c05 = counts_05[df_GL.index]
#         c01 = counts_01[df_GL.index]
#         cond1 = (md > -6.0)   & c05.between(1, 12)  & c01.between(1, 4)
#         cond2 = (md.between(-12.0, -6.01)) | (c05.between(13, 26) & c01.between(5, 13))
#         cond3 = (md < -12.0)  | (c05 >= 27)
#         df_GL['HAP2_p2_clf'] = np.select(
#             [cond1, cond2, cond3],
#             ['Stage 1', 'Stage 2', 'Stage 3'],
#             default='GL')
#     else:
#         df_GL['HAP2_p2_clf'] = 'GL'

#     df_PDP.loc[df_GL.index, 'HAP2_p2_clf'] = df_GL['HAP2_p2_clf']
#     df_PDP['HAP2_p2_clf'] = df_PDP['HAP2_p2_clf'].fillna('Non-GL')
#     return df_PDP



def has_pd_cluster_3_with_1_at_1pct(pdp_values):
    """
    Criterion:
    cluster of 3 points at P < 5%,
    with at least 1 of those points at P < 1%.
    """
    pd_grid = convertVF_to_2D(pdp_values)

    mask_5 = pd_grid < 0.05
    mask_1 = pd_grid < 0.01

    mask_5 = np.nan_to_num(mask_5, nan=False).astype(bool)
    mask_1 = np.nan_to_num(mask_1, nan=False).astype(bool)

    visited = np.zeros(mask_5.shape, dtype=bool)

    neighbors = [(-1,-1), (-1,0), (-1,1),
                 (0,-1),           (0,1),
                 (1,-1),  (1,0),   (1,1)]

    for r in range(mask_5.shape[0]):
        for c in range(mask_5.shape[1]):
            if not mask_5[r, c] or visited[r, c]:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            component = []

            while stack:
                rr, cc = stack.pop()
                component.append((rr, cc))

                for dr, dc in neighbors:
                    nr, nc = rr + dr, cc + dc
                    if (
                        0 <= nr < mask_5.shape[0]
                        and 0 <= nc < mask_5.shape[1]
                        and mask_5[nr, nc]
                        and not visited[nr, nc]
                    ):
                        visited[nr, nc] = True
                        stack.append((nr, nc))

            if len(component) >= 3:
                has_1pct_point = any(mask_1[rr, cc] for rr, cc in component)
                if has_1pct_point:
                    return True

    return False


GHT_CODES = {
    1: "within normal limits",
    2: "borderline",
    3: "outside normal limits",
    4: "general reduction of sensitivity",
    5: "abnormally high sensitivity",
    6: "borderline/general reduction",
}

def _is_ght_outside_normal_limits(x):

    if pd.isna(x):
        return False

    try:
        return int(x) == 3
    except (TypeError, ValueError):
        pass

    x = str(x).strip().lower()

    return (
        "outside normal limits" in x
        or x in {"outside", "onl", "abnormal"}
    )


def _is_psd_p_less_5(row):
    """
    Handles possible column names:
    If only PSD is present as a p-value, it checks PSD < 0.05.
    """

    if "psdp" not in row.index:
        return False

    val = pd.to_numeric(row["psdp"], errors="coerce")

    if pd.isna(val):
        return False

    # coded Humphrey probability categories
    # integer coded
    if val in {0, 1, 2, 3, 4, 5}:
        return val > 2

    # actual probability
    if 0 <= val <= 1:
        return val < 0.05

    return False


def HAP2_clf(row):
    """
    Criteria:
    1. GHT outside normal limits
    OR
    2. cluster of 3 PD probability points at P < 5%,
       with at least 1 at P < 1%
    OR
    3. PSD at P < 5%
    """
    pt_cols = _get_vf_cols(pd.DataFrame([row]), colname='pdp')    
    pd_values = pd.to_numeric(row[pt_cols], errors="coerce").values

    # Criterion 1: GHT outside normal limits
    # canonicalized dataframe should use lowercase ght
    if "ght" in row.index and _is_ght_outside_normal_limits(row["ght"]):
        return "GL"

    # Criterion 2: PD cluster
    if has_pd_cluster_3_with_1_at_1pct(pd_values):
        return "GL"

    # Criterion 3: PSD P < 5%
    if _is_psd_p_less_5(row):
        return "GL"

    return "Non-GL"


def HAP2_clf_reason(row):
    pt_cols = _get_vf_cols(pd.DataFrame([row]), colname="pdp")
    pdp_values = pd.to_numeric(row[pt_cols], errors="coerce").values

    reasons = []

    if "ght" in row.index and _is_ght_outside_normal_limits(row["ght"]):
        reasons.append("GHT outside")

    if has_pd_cluster_3_with_1_at_1pct(pdp_values):
        reasons.append("cluster of 3 PDP points < 5% with ≥1 points < 1%")

    if _is_psd_p_less_5(row):
        reasons.append("PSD p < 0.05")

    if reasons:
        return "GL", "; ".join(reasons)

    return "Non-GL", ""

def Fn_HAP2(df_PDP):
    out = df_PDP.copy()
    #out["HAP2_clf"] = out.apply(HAP2_clf, axis=1)

    res = out.apply(HAP2_clf_reason, axis=1)

    out["HAP2_clf"] = res.apply(lambda x: x[0])
    out["HAP2_reason"] = res.apply(lambda x: x[1])

    return out


###################

def _central_5_indices_24d2():
    """
    Approximate central 5-degree locations in 24-2.
    Uses 1-based VF indices.
    """
    return [23, 24, 32, 33]


def _hemifield_indices_24d2():
    """
    Superior/inferior hemifields using 1-based 24-2 indices.
    Blind spots are included safely; NaNs are ignored later.
    """
    superior = list(range(1, 28))      # rows above/including horizontal midline
    inferior = list(range(28, 55))     # rows below horizontal midline
    return superior, inferior


def _get_cols_by_indices(prefix, indices, row):
    return [
        f"{prefix}{i}"
        for i in indices
        if f"{prefix}{i}" in row.index
    ]


def HAP2_part2_severity(row):
    """
    HAP2 Part II severity classification:
        Early / Moderate / Severe

    Assumes canonicalized row with:
        l1-l54, pdp1-pdp54, md
    """

    # Required columns
    l_cols = [f"l{i}" for i in range(1, 55) if f"l{i}" in row.index]
    pdp_cols = [f"pdp{i}" for i in range(1, 55) if f"pdp{i}" in row.index]

    # if "md" not in row.index:
    #     return "Unknown"

    if "md" in row.index and pd.notna(row["md"]):
        md = pd.to_numeric(row["md"], errors="coerce")
    elif "tmd" in row.index and pd.notna(row["tmd"]):
        md = pd.to_numeric(row["tmd"], errors="coerce")
    else:
        return "Unknown"

    sens = pd.to_numeric(row[l_cols], errors="coerce")
    pdp = pd.to_numeric(row[pdp_cols], errors="coerce")

    central_idx = _central_5_indices_24d2()
    central_cols = _get_cols_by_indices("l", central_idx, row)
    central_sens = pd.to_numeric(row[central_cols], errors="coerce")

    # PD probability counts
    n_pdp_5 = int((pdp < 0.05).sum())
    n_pdp_1 = int((pdp < 0.01).sum())

    # central 5-degree sensitivity
    any_central_0 = bool((central_sens == 0).any())
    any_central_lt15 = bool((central_sens < 15).any())

    # hemifield central <15
    sup_idx, inf_idx = _hemifield_indices_24d2()
    sup_central_cols = _get_cols_by_indices("l", [i for i in central_idx if i in sup_idx], row)
    inf_central_cols = _get_cols_by_indices("l", [i for i in central_idx if i in inf_idx], row)

    sup_lt15 = bool((pd.to_numeric(row[sup_central_cols], errors="coerce") < 15).any())
    inf_lt15 = bool((pd.to_numeric(row[inf_central_cols], errors="coerce") < 15).any())

    # -------------------------
    # Severe defect
    # Any criterion is enough
    # -------------------------
    severe = (
        md < -12
        or any_central_0
        or (sup_lt15 and inf_lt15)
        or n_pdp_5 >= 27
        or n_pdp_1 >= 14
    )

    if severe:
        return "Severe"

    # -------------------------
    # Early defect
    # All criteria required
    # -------------------------
    early = (
        md > -6
        and not any_central_lt15
        and n_pdp_5 <= 12
        and n_pdp_1 <= 4
    )

    if early:
        return "Early"

    # -------------------------
    # Moderate defect
    # At least one criterion
    # -------------------------
    only_one_hemifield_central_lt15 = (
        (sup_lt15 and not inf_lt15)
        or (inf_lt15 and not sup_lt15)
    )

    moderate = (
        (-12 <= md <= -6)
        or (only_one_hemifield_central_lt15 and not any_central_0)
        or (13 <= n_pdp_5 <= 26)
        or (5 <= n_pdp_1 <= 13)
    )

    if moderate:
        return "Moderate"

    return ""


# def Fn_HAP2_part2(df):
#     df
#     out = df.copy()
#     severity = out.apply(HAP2_part2_severity, axis=1)
#     return pd.concat([out, severity.rename("severity(HAP2_part2)")], axis=1).copy()


def Fn_HAP2_part2(df):
    out = df.copy()

    severity = pd.Series("", index=out.index, dtype=object)

    mask = out["HAP2_clf"] == "GL"

    severity.loc[mask] = out.loc[mask].apply(
        HAP2_part2_severity,
        axis=1
    )

    return pd.concat(
        [out, severity.rename("severity(HAP2_part2)")],
        axis=1
    ).copy()


########################################################
########################################################

# def check_gl_condition(row, threshold=0.01, consecutive_reductions=2):
#     numeric_values = pd.to_numeric(row.values, errors='coerce')
#     below = (numeric_values <= threshold).astype(float)
#     below = np.nan_to_num(below, nan=0.0)
#     counts = np.convolve(below, np.ones(consecutive_reductions), mode='valid')
#     return np.any(counts >= consecutive_reductions)


# def Fn_UKGTS(df_TDP, threshold=0.01, consecutive_reductions=2):
#     pt_cols = _pt_cols_from_df(df_TDP)
#     df_TDP['UKGTS_clf'] = np.where(
#         df_TDP[pt_cols].apply(
#             check_gl_condition, axis=1,
#             threshold=threshold,
#             consecutive_reductions=consecutive_reductions),
#         'GL', 'Non-GL')
#     return df_TDP



def has_cluster(mask, min_size=2, connectivity=8):
    mask = np.nan_to_num(mask, nan=False).astype(bool)
    visited = np.zeros(mask.shape, dtype=bool)

    if connectivity == 8:
        neighbors = [(-1,-1), (-1,0), (-1,1),
                     (0,-1),           (0,1),
                     (1,-1),  (1,0),   (1,1)]
    else:
        neighbors = [(-1,0), (1,0), (0,-1), (0,1)]

    for r in range(mask.shape[0]):
        for c in range(mask.shape[1]):
            if not mask[r, c] or visited[r, c]:
                continue

            stack = [(r, c)]
            visited[r, c] = True
            size = 0

            while stack:
                rr, cc = stack.pop()
                size += 1

                for dr, dc in neighbors:
                    nr, nc = rr + dr, cc + dc
                    if (
                        0 <= nr < mask.shape[0]
                        and 0 <= nc < mask.shape[1]
                        and mask[nr, nc]
                        and not visited[nr, nc]
                    ):
                        visited[nr, nc] = True
                        stack.append((nr, nc))

            if size >= min_size:
                return True

    return False

def has_nasal_step_10db(td_grid, nasal_cols=(0, 1, 2, 3, 4)):
    """
    Assumes right eye.
    Nasal field is assumed to be the left side of the VF grid.
    Checks adjacent superior/inferior pairs across the horizontal midline.
    """
    diffs = []

    for c in nasal_cols:
        sup = td_grid[3, c]
        inf = td_grid[4, c]

        if not np.isnan(sup) and not np.isnan(inf):
            diffs.append(abs(sup - inf) >= 10)
        else:
            diffs.append(False)

    # cluster of 2 adjacent nasal step points
    for i in range(len(diffs) - 1):
        if diffs[i] and diffs[i + 1]:
            return True

    return False



# def UKGTS_clf(row_prob, row_db):
#     prob_values = pd.to_numeric(row_prob, errors="coerce").values
#     db_values = pd.to_numeric(row_db, errors="coerce").values

#     prob_grid = convertVF_to_2D(prob_values)
#     db_grid = convertVF_to_2D(db_values)

#     # Criterion 1: cluster of 2 points at P < 1%
#     if has_cluster(prob_grid < 0.01, min_size=2):
#         return "GL"

#     # Criterion 2: cluster of 3 points at P < 5%
#     if has_cluster(prob_grid < 0.05, min_size=3):
#         return "GL"

#     # Criterion 3: cluster of 2 points with 10 dB difference across nasal horizontal midline
#     if has_nasal_step_10db(db_grid):
#         return "GL"

#     return "Non-GL"


# def Fn_UKGTS(df):

#     prob_cols = _get_vf_cols(df, colname='tdp') 
#     db_cols = _get_vf_cols(df, colname='td') 

#     # prob_cols = _pt_cols_from_df(df_TDP)
#     # db_cols = _pt_cols_from_df(df_TD)

#     if len(prob_cols) != 54 or len(db_cols) != 54:
#         raise ValueError("Expected 54 VF point columns in both probability and dB dataframes.")

#     out = df.copy()

#     out["UKGTS_clf"] = [
#         UKGTS_clf(df.loc[i, prob_cols], df.loc[i, db_cols])
#         for i in df.index
#     ]

#     return out


def UKGTS_clf_reason(row_prob, row_db):
    prob_values = pd.to_numeric(row_prob, errors="coerce").values
    db_values = pd.to_numeric(row_db, errors="coerce").values

    prob_grid = convertVF_to_2D(prob_values)
    db_grid = convertVF_to_2D(db_values)

    reasons = []

    if has_cluster(prob_grid < 0.01, min_size=2):
        reasons.append("Cluster of 2 TDP points < 1%")

    if has_cluster(prob_grid < 0.05, min_size=3):
        reasons.append("Cluster of 3 TDP points < 5%")

    if has_nasal_step_10db(db_grid):
        reasons.append("Nasal step ≥ 10 dB")

    if reasons:
        return "GL", "; ".join(reasons)

    return "Non-GL", ""

def Fn_UKGTS(df):

    prob_cols = _get_vf_cols(df, colname="tdp")
    db_cols = _get_vf_cols(df, colname="td")

    if len(prob_cols) != 54 or len(db_cols) != 54:
        raise ValueError(
            "Expected 54 VF point columns in both probability and dB data."
        )

    out = df.copy()

    res = [
        UKGTS_clf_reason(out.loc[i, prob_cols], out.loc[i, db_cols])
        for i in out.index
    ]

    out["UKGTS_clf"] = [r[0] for r in res]
    out["UKGTS_reason"] = [r[1] for r in res]

    return out

########################################################
########################################################


# def Fn_LoGTS(df):
#     pt_cols = _get_vf_cols(df, colname='td')
#     out = df.copy()
#     out['LoGTS_clf'] = out[pt_cols].apply(LoGTS_clf, axis=1)
#     return out


# def LoGTS_clf(row):
#     values = pd.to_numeric(row, errors='coerce').values
#     VF_2D = convertVF_to_2D(values)   # ← use the result

#     # criterion 1: cluster of 2 points with TD < -10 dB
#     if has_cluster(VF_2D < -10, min_size=2):
#         return "GL"

#     # criterion 2: cluster of 3 points with TD < -8 dB
#     if has_cluster(VF_2D < -8, min_size=3):
#         return "GL"

#     return "Non-GL"

def LoGTS_clf_reason(row):

    values = pd.to_numeric(row, errors="coerce").values
    vf_2d = convertVF_to_2D(values)

    reasons = []

    if has_cluster(vf_2d < -10, min_size=2):
        reasons.append("Cluster of 2 TD points < -10 dB")

    if has_cluster(vf_2d < -8, min_size=3):
        reasons.append("Cluster of 3 TDP points < -8 dB")

    if reasons:
        return "GL", "; ".join(reasons)

    return "Non-GL", ""

def Fn_LoGTS(df):

    pt_cols = _get_vf_cols(df, colname="td")

    out = df.copy()

    res = out[pt_cols].apply(LoGTS_clf_reason, axis=1)

    out["LoGTS_clf"] = res.apply(lambda x: x[0])
    out["LoGTS_reason"] = res.apply(lambda x: x[1])

    return out

########################################################
########################################################


# def Kangs_clf(row):
#     values = pd.to_numeric(row, errors='coerce').values
#     td_grid = convertVF_to_2D(values)

#     # criterion 1: cluster of 3 contiguous points with TD < -5 dB
#     if has_cluster(td_grid < -5, min_size=3):
#         return 'GL'
#     # criterion 2: cluster of 2 contiguous points with TD < -10 dB
#     if has_cluster(td_grid < -10, min_size=2):
#         return 'GL'
#     return 'Non-GL'


# def Fn_Kangs(df):    
#     pt_cols = _get_vf_cols(df, colname='td')
#     out = df.copy()
#     out['Kangs_clf'] = out[pt_cols].apply(Kangs_clf, axis=1)
#     return out


def Kangs_clf_reason(row):

    values = pd.to_numeric(row, errors="coerce").values
    td_grid = convertVF_to_2D(values)

    reasons = []

    # Criterion 1
    if has_cluster(td_grid < -5, min_size=3):
        reasons.append("Cluster of 3 points with TD < -5 dB")

    # Criterion 2
    if has_cluster(td_grid < -10, min_size=2):
        reasons.append("Cluster of 2 points with TD < -10 dB")

    if reasons:
        return "GL", "; ".join(reasons)

    return "Non-GL", ""


def Fn_Kangs(df):

    pt_cols = _get_vf_cols(df, colname="td")

    out = df.copy()

    res = out[pt_cols].apply(Kangs_clf_reason, axis=1)

    out["Kangs_clf"] = res.apply(lambda x: x[0])
    out["Kangs_reason"] = res.apply(lambda x: x[1])

    return out

########################################################
########################################################


# # Sector point indices (1-based) for OD and OS — direction-corrected
# _FOSTER_OD_SUP = [22,23,24,13,14,15,16,11,12,19,20,21,1,2,5,6,7,8,3,4,9,10]
# _FOSTER_OD_INF = [31,32,33,39,40,41,42,28,29,30,37,38,45,46,47,48,51,52,49,50,53,54]
# _FOSTER_OS_SUP = [22,23,24,13,14,15,16,17,18,25,26,27,3,4,8,9,10,1,2,5,6]
# _FOSTER_OS_INF = [31,32,33,39,40,41,42,34,35,36,43,44,48,49,50,53,54,45,46,51,52]


# def Foster_clf(row):
#     eye = _normalise_eye(_eye_col(row))
#     if eye is None:
#         return 'Non-GL'

#     pt_cols = _pt_cols_from_row(row)
#     if not pt_cols:
#         return 'Non-GL'
#     pfx = pt_cols[0][0]   # 's' or 'l'

#     if eye == 'OD':
#         sup_cols = [f'{pfx}{n}' for n in _FOSTER_OD_SUP]
#         inf_cols = [f'{pfx}{n}' for n in _FOSTER_OD_INF]
#     else:
#         sup_cols = [f'{pfx}{n}' for n in _FOSTER_OS_SUP]
#         inf_cols = [f'{pfx}{n}' for n in _FOSTER_OS_INF]

#     # keep only cols that actually exist (guards against 52-pt datasets)
#     sup_cols = [c for c in sup_cols if c in row.index]
#     inf_cols = [c for c in inf_cols if c in row.index]

#     s_vals = pd.to_numeric(row[sup_cols], errors='coerce')
#     i_vals = pd.to_numeric(row[inf_cols], errors='coerce')

#     gl_sum_flag  = (s_vals.sum() > 0.005) and (i_vals.sum() > 0.005)
#     gl_diff_flag = (s_vals.values - i_vals.values[:len(s_vals)]).tolist()
#     gl_diff_flag = abs(sum(gl_diff_flag)) > 0.01

#     all_pt   = pd.to_numeric(row[pt_cols], errors='coerce')
#     count_05 = (all_pt <= 0.05).sum()

#     if (gl_sum_flag or gl_diff_flag) and (count_05 >= 3):
#         return 'GL'
#     return 'Non-GL'


def Foster_clf(row):
    """
    Foster criteria:

    GHT outside normal limits
    AND
    cluster of 3 points at P < 5%
    (if PD unavailable due to severe depression,
     cluster criterion automatically satisfied)
    """

    # -----------------
    # GHT check
    # -----------------
    ght_value = None

    for ght_col in ["GHT", "ght"]:
        if ght_col in row.index:
            ght_value = row[ght_col]
            break

    if pd.isna(ght_value):
        return "Error: missing GHT"

    ght_ok = _is_ght_outside_normal_limits(ght_value)

    # -----------------
    # PD cluster check
    # -----------------
    pt_cols = _get_vf_cols(pd.DataFrame([row]), colname='pdp')
    pd_values = pd.to_numeric(
        row[pt_cols],
        errors="coerce"
    ).values

    prob_grid = convertVF_to_2D(pd_values)

    cluster_ok = has_cluster(
        prob_grid < 0.05,
        min_size=3
    )

    # -----------------
    # Final decision
    # -----------------
    return "GL" if (ght_ok and cluster_ok) else "Non-GL"


def Fn_Foster(df):
    out = df.copy()
    out['Foster_clf'] = out.apply(Foster_clf, axis=1)
    out["Foster_reason"] = np.where(
            out["Foster_clf"] == "GL",
            "GHT outside AND cluster of 3 PDP points < 5%",
            "",
        )
    return out


########################################################
########################################################

# def combine_dataframes(df_input, df1, df2, df3, df4, df5):
#     # Combine the DataFrames along the columns axis
#     result_combined = pd.concat([df1, df2], axis=1)
    
#     # Reset indices to ensure proper alignment
#     m1_reset = df_input.reset_index(drop=True)
#     m2_reset = result_combined.reset_index(drop=True)
    
#     # Add the specified columns from m1_reset to the first four columns of m2_reset
#     m2_reset.insert(0, 'ID', m1_reset['id'])
#     m2_reset.insert(1, 'Eye', m1_reset['eye'])
#     m2_reset.insert(2, 'Age', m1_reset['age'])
#     m2_reset.insert(3, 'Date', m1_reset['date'])  # Add the Date column from df_input
    
#     result_combined = m2_reset
    
#     # Concatenate df3
#     result_combined = pd.concat([result_combined, df3.reset_index(drop=True)], axis=1)
    
#     # Concatenate df4
#     result_combined = pd.concat([result_combined, df4.reset_index(drop=True)], axis=1)
    
#     # Concatenate df5
#     result_combined = pd.concat([result_combined, df5.reset_index(drop=True)], axis=1)
    
#     # Return the combined DataFrame
#     return result_combined

# def Fn_ensemble_decision(df_input, df1, df2, df3, df4, df5, weights):
#     # Call the combine_dataframes function with your DataFrames
#     result_combined = combine_dataframes(df_input, df1, df2, df3, df4, df5)

#     # Map categorical values to numeric equivalents for all columns except the first four
#     for column in result_combined.columns[4:]:
#         result_combined[column] = result_combined[column].map({'GL': 1, 'Non-GL': 0})

#     # Convert data type to string to ensure consistency
#     result_combined_en = result_combined.astype(str)

#     # Calculate weighted average of predictions
#     predictions = result_combined_en.iloc[:, 4:].apply(pd.to_numeric, errors='coerce').fillna(0)
#     result_combined['Ensemble'] = np.average(predictions, axis=1, weights=weights)
    
#     return result_combined



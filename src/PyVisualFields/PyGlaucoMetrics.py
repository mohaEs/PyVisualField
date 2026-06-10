
import numpy as np
import pandas as pd

import numpy as np
import pandas as pd



def _normalise_eye(val):
    """Return 'OD' or 'OS' regardless of input format."""
    v = str(val).strip().lower()
    if v in ('od', 'right', 'r', '1', 'righteye', 're'):
        return 'OD'
    if v in ('os', 'left', 'l', '0', 'lefteye', 'le'):
        return 'OS'
    return None   # unknown — caller returns Non-GL


def _pt_cols_from_row(row):
    """Return sorted point column names (s* or l*) from a row's index."""
    cols = sorted(
        [c for c in row.index if len(c) >= 2 and c[0] in ('s', 'l') and c[1:].isdigit()],
        key=lambda x: int(x[1:])
    )
    return cols


def _pt_cols_from_df(df):
    """Return sorted point column names (s* or l*) from a dataframe."""
    cols = sorted(
        [c for c in df.columns if len(c) >= 2 and c[0] in ('s', 'l') and c[1:].isdigit()],
        key=lambda x: int(x[1:])
    )
    return cols


def _eye_col(row):
    """Return the eye value from whichever column name exists (Eye/eye/EYE)."""
    for name in ('Eye', 'eye', 'EYE'):
        if name in row.index:
            return row[name]
    return None


def _col(prefix, n, pt_cols):
    """
    Return the column name for point n (1-indexed) using whatever prefix
    is present in pt_cols (s or l).
    """
    actual_prefix = pt_cols[0][0] if pt_cols else 's'
    return f'{actual_prefix}{n}'


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




def has_pd_cluster_3_with_1_at_1pct(pd_values):
    """
    Criterion:
    cluster of 3 points at P < 5%,
    with at least 1 of those points at P < 1%.
    """
    pd_grid = convertVF_to_2D(pd_values)

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


def _is_ght_outside_normal_limits(x):
    if pd.isna(x):
        return False

    x = str(x).strip().lower()

    return (
        "outside normal limits" in x
        or "outside" in x
        or x in {"onl", "abnormal"}
    )


def _is_psd_p_less_5(row):
    """
    Handles possible column names:
    PSD_P, PSD_p, PSDp, PSD_probability, PSD
    If only PSD is present as a p-value, it checks PSD < 0.05.
    """
    possible_cols = [
        "PSD_P", "PSD_p", "PSDp", "psd_p",
        "PSD_probability", "psd_probability",
        "PSD", "psd"
    ]

    for col in possible_cols:
        if col in row.index:
            val = pd.to_numeric(row[col], errors="coerce")
            if pd.notna(val) and val < 0.05:
                return True

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
    pt_cols = _pt_cols_from_df(pd.DataFrame([row]))
    pd_values = pd.to_numeric(row[pt_cols], errors="coerce").values

    # Criterion 1: GHT outside normal limits
    for ght_col in ["GHT", "ght"]:
        if ght_col in row.index and _is_ght_outside_normal_limits(row[ght_col]):
            return "GL"

    # Criterion 2: PD cluster
    if has_pd_cluster_3_with_1_at_1pct(pd_values):
        return "GL"

    # Criterion 3: PSD P < 5%
    if _is_psd_p_less_5(row):
        return "GL"

    return "Non-GL"


def Fn_HAP2(df_PDP):
    out = df_PDP.copy()
    out["HAP2_clf"] = out.apply(HAP2_clf, axis=1)
    return out


# def Fn_HAP2_partII(df_sensitivity, df_PDP):



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


########################################################
########################################################

def UKGTS_clf(row_prob, row_db):
    prob_values = pd.to_numeric(row_prob, errors="coerce").values
    db_values = pd.to_numeric(row_db, errors="coerce").values

    prob_grid = convertVF_to_2D(prob_values)
    db_grid = convertVF_to_2D(db_values)

    # Criterion 1: cluster of 2 points at P < 1%
    if has_cluster(prob_grid < 0.01, min_size=2):
        return "GL"

    # Criterion 2: cluster of 3 points at P < 5%
    if has_cluster(prob_grid < 0.05, min_size=3):
        return "GL"

    # Criterion 3: cluster of 2 points with 10 dB difference across nasal horizontal midline
    if has_nasal_step_10db(db_grid):
        return "GL"

    return "Non-GL"

def Fn_UKGTS(df_TDP, df_TD):
    prob_cols = _pt_cols_from_df(df_TDP)
    db_cols = _pt_cols_from_df(df_TD)

    if len(prob_cols) != 54 or len(db_cols) != 54:
        raise ValueError("Expected 54 VF point columns in both probability and dB dataframes.")

    out = df_TDP.copy()

    out["UKGTS_clf"] = [
        UKGTS_clf(df_TDP.loc[i, prob_cols], df_TD.loc[i, db_cols])
        for i in df_TDP.index
    ]

    return out


########################################################
########################################################


# def LoGTS_clf(row):
#     numeric_values = pd.to_numeric(row, errors='coerce')
#     return 'GL' if (numeric_values < -10).sum() >= 2 else 'Non-GL'


def Fn_LoGTS(df_TD):
    pt_cols = _pt_cols_from_df(df_TD)
    df = df_TD.copy()
    df['LoGTS_clf'] = df[pt_cols].apply(LoGTS_clf, axis=1)
    return df   


def LoGTS_clf(row):
    values = pd.to_numeric(row, errors='coerce').values
    VF_2D = convertVF_to_2D(values)   # ← use the result

    # criterion 1: cluster of 2 points with TD < -10 dB
    if has_cluster(VF_2D < -10, min_size=2):
        return "GL"

    # criterion 2: cluster of 3 points with TD < -8 dB
    if has_cluster(VF_2D < -8, min_size=3):
        return "GL"

    return "Non-GL"

########################################################
########################################################


def Kangs_clf(row):
    values = pd.to_numeric(row, errors='coerce').values
    td_grid = convertVF_to_2D(values)

    # criterion 1: cluster of 3 contiguous points with TD < -5 dB
    if has_cluster(td_grid < -5, min_size=3):
        return 'GL'
    # criterion 2: cluster of 2 contiguous points with TD < -10 dB
    if has_cluster(td_grid < -10, min_size=2):
        return 'GL'
    return 'Non-GL'


def Fn_Kangs(df_TD):
    pt_cols = _pt_cols_from_df(df_TD)
    df = df_TD.copy()
    df['Kangs_clf'] = df[pt_cols].apply(Kangs_clf, axis=1)
    return df


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
    pt_cols = _pt_cols_from_df(pd.DataFrame([row]))
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



def Fn_Foster(df_PDP):
    df_P = df_PDP.copy()
    df_P['Foster_clf'] = df_P.apply(Foster_clf, axis=1)
    return df_P


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



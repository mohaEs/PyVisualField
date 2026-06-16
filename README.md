# PyVisualFields 

## A python tool collection for analyzing visual fields 

This packages includes functions for visuald field analysis and display. 

https://pypi.org/project/PyVisualFields/

Version 2 is R-independent while maintaining the original module organization. The modules are inspired by vfprogression (Elze et al. [3]) and visualFields (Marin-Franch et al. [4]). 
Additionally, PyGlaucoMetric[5] has been integrated to enable glaucoma classification based on visual field patterns.

These functions are implemented in Python, and their functionalities are demonstrated across four primary categories:
-     Data Presentation
-     Plotting
-     Scoring and Progression Analysis
-     Normalization Analysis
-     Glaucoma Detection

For each category, we provide comprehensive Jupyter notebooks containing practical examples, detailed function descriptions, required inputs/dependencies, and expected outputs.

## Citation
If you found this package impactful for your research, please cite the following article: 
- PyVisualFields v2
- Mohammad Eslami, Saber Kazeminasab, Vishal Sharma, Yangjiani Li, Mojtaba Fazli, Mengyu Wang, Nazlee Zebardast, Tobias Elze; PyVisualFields: A Python Package for Visual Field Analysis. Trans. Vis. Sci. Tech. 2023;12(2):6. https://doi.org/10.1167/tvst.12.2.6.

and of course the corresponding sub-package:
- vfprogression (by Elze et al. [3])
- visualFields (by Marin-Granch et al. [4])
- PyGlaucoMetrics (by Moradi et al. [5])

## Installation: 

> pip install PyVisualFields

## Demo jupyter notebooks

The list and description of all functions are available at [All_Functions](#list-of-functions). They are all examined and introduced with examples in 4 different notebooks categorized: </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Normalization and deviation analysis [demo_2_Deviation_Analysis.ipynb](demo_2_Deviation_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Progression Analysis [demo_4_ProgressionAnalysis.ipynb](demo_4_ProgressionAnalysis.ipynb)
- Glaucoma Detection [demo5_PyGlaucoMetrics.ipynb](demo5_PyGlaucoMetrics.ipynb) </br>

__Notice:__ PyGlaucoMetric is also available as a seperatre PyPI package and GitHub repository (built upon PyVisualFields), which includes a graphical user interface (GUI) for progression analysis and glaucoma detection. Indeed PyVisualFields is designed as a developer-facing package library, while PyGlaucoMetric serves as an accessible GUI application implementing selected visual field analysis components.
https://github.com/Mousamoradi/PyGlaucoMetrics


## references:
[1] PyVisualFields v2
[2] Mohammad Eslami, Saber Kazeminasab, Vishal Sharma, Yangjiani Li, Mojtaba Fazli, Mengyu Wang, Nazlee Zebardast, Tobias Elze; PyVisualFields: A Python Package for Visual Field Analysis. Trans. Vis. Sci. Tech. 2023;12(2):6. https://doi.org/10.1167/tvst.12.2.6.
[3] https://cran.r-project.org/web/packages/vfprogression/index.html </br>
[4] https://cran.r-project.org/web/packages/visualFields/index.html </br>
[5] Moradi, Mousa, Saber Kazeminasab Hashemabad, Daniel M. Vu, Allison R. Soneru, Asahi Fujita, Mengyu Wang, Tobias Elze, Mohammad Eslami, and Nazlee Zebardast. 2025. "PyGlaucoMetrics: A Stacked Weight-Based Machine Learning Approach for Glaucoma Detection Using Visual Field Data" Medicina 61, no. 3: 541. https://doi.org/10.3390/medicina61030541 
</br>


## list of functions
The list and description of all functions are as follow. They are all examined and introduced with examples in 4 different notebooks. It is important to mention that, based on the background modules, the input VF dataframe needs to have columns with special column names. Make sure, to consider the data notebook. If further information is required, see the corresponding references: _vfprogression[1]_, _visualFields[2]_ </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Normalization and deviation analysis [demo_2_Deviation_Analysis.ipynb](demo_2_Deviation_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Progression Analysis [demo_4_ProgressionAnalysis.ipynb](demo_4_ProgressionAnalysis.ipynb)
- Glaucoma Detection [demo5_PyGlaucoMetrics.ipynb](demo5_PyGlaucoMetrics.ipynb)
</br>

### Notice:
Version 2 has been validated exclusively for the 24-2 format. Additionally, the system assumes all visual field measurements are provided in right eye (OD) format.

Functions based on _vfprogression_ package accept 24-2 or 30-2 visual field measurement while functions based on _visualFields_ also accept 10-2. 


# Function Reference

<details>
<summary><b>Data Utilities </b></summary>
## Data Utilities

| Function | Description | Reference |
|----------|-------------|--------|
| `utils.canonicalize_vf_df()` | Canonicalize VF data to PyVisualFields format | PyVisualFieldsV2 |
| `utils.canonicalize_vf_df(, sort_byDateAge=True)` | Canonicalize and sort VFs by date/age within each patient | PyVisualFieldsV2 |
| `utils.print_vf_summary()` | Print a summary of available VF information | PyVisualFieldsV2 |
| `utils.investigate_vf_df()` | Return a summary of available VF information | PyVisualFieldsV2 |
| `utils.vf_blocks()` | Identify available VF blocks (`s`, `td`, `pd`, `tdp`, `pdp`) | PyVisualFieldsV2 |
| `utils.missing_blocks()` | Identify missing VF blocks | PyVisualFieldsV2 |
| `utils.compute_missing_blocks()` | Compute missing blocks using current normative setting NV | PyVisualFieldsV2 |
</details>


<details>
<summary><b>Data Structures and Canonicalization </b></summary>
## Data Structures and Canonicalization

## Data Canonicalization

PyVisualFields provides two helper functions:

```python
canonicalize_vf_df()
canonicalize_vf_row()
```

to standardize visual field data into a unified format compatible with all package functions.

The canonicalization functions standardize recognized visual field and metadata columns while preserving all other columns unchanged, allowing user-specific variables and auxiliary information to be retained throughout the analysis pipeline.

### Supported Pointwise Data

The following pointwise aliases are automatically recognized:

```python
POINT_ALIASES = {
    "sens": ["l", "s", "sen", "sens", "sensitivity"],
    "td": ["td"],
    "pd": ["pd"],
    "tdp": ["tdp"],
    "pdp": ["pdp"],
}
```

The parser automatically handles:

* Different prefixes (e.g., `s`, `sen`, `sens`, `sensitivity`)
* Upper/lower-case variations (e.g., `TD1`, `td1`)
* Common separators (e.g., `td1`, `td_1`, `td-1`, `td 1`)

and converts them into the canonical format:

```text
l1-l54      Raw sensitivity values
td1-td54    Total Deviation values
tdp1-tdp54  Total Deviation probability values
pd1-pd54    Pattern Deviation values
pdp1-pdp54  Pattern Deviation probability values
```

Both 52-point and 54-point visual fields are supported automatically. For 52-point fields, the two blind-spot locations are inserted automatically.

### Supported Metadata

Common metadata fields are also standardized when possible, including:

```text
patientid
eyeid
date
age
yearsfollowed
md
mdprob
psd
psdprob
ght
vfi
vfiprob
msens
msensprob
ssens
ssensprob
tmd
tmdprob
tsd
tsdprob
pmd
pmdprob
gh
ghprob
fpr
fnr
fl
duration
```

For example:

```text
patient_id  -> patientid
subjectid   -> patientid
mrn         -> patientid

eye         -> eyeid
laterality  -> eyeid

examdate    -> date
testdate    -> date

mdp         -> mdprob
psdp        -> psdprob
vfip        -> vfiprob
```

After canonicalization, all PyVisualFields functions can assume a consistent schema regardless of the original data source.

PyVisualFields supports both device-reported and computed global indices.

| Variable           | Description                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **s** / **l1-l54** | Raw visual field sensitivities (dB) at each test location.                                                           |
| **msens**          | Mean sensitivity (MS) across all visual field locations.                                                                  |
| **ssens**          | Standard deviation of sensitivity values across locations.                                                           |
| **td1-td54**       | Total Deviation values (measured sensitivity − age-expected normal sensitivity).                                     |
| **tdp1-tdp54**       |    Total Deviation probability values; statistical significance of each TD location.                  |
| **pdp1-pdp54**       |       Pattern Deviation probability values; statistical significance of each PD location.          |
| **MD**            | The Humphrey MD index.                     |
| **tmd**            | Total Mean Deviation; weighted mean of Total Deviation values. Similar to the Humphrey MD index.                     |
| **tsd**            | Total Standard Deviation; weighted standard deviation of Total Deviation values.                                     |
| **pd1-pd54**       | Pattern Deviation values (Total Deviation corrected for generalized depression).                                     |
| **pmd**            | Pattern Mean Deviation; weighted mean of Pattern Deviation values.                                                   |
| **psd**            | Pattern Standard Deviation; weighted standard deviation of Pattern Deviation values.                                 |
| **ght**            | Glaucoma Hemifield Test result (Within Normal Limits, Borderline, Outside Normal Limits, etc.).                      |
| **gh**             | General Height (generalized sensitivity adjustment used in Pattern Deviation calculations).                          |
| **vfi**            | Visual Field Index (%), where 100 indicates a normal visual field and lower values indicate greater functional loss. |
| **fpr**            | False Positive Rate (%).                                                                                             |
| **fnr**            | False Negative Rate (%).                                                                                             |
| **fl**             | Fixation Loss Rate (%).                                                                                              |
| **duration**       | Test duration.                                                                                                       |



</details>


<details>
<summary><b>Example Datasets</b></summary>
## Example Datasets

| Function | Description | Reference |
|----------|-------------|--------|
| `visualFields.data_vfpwgRetest24d2()` | Humphrey 24-2 retest dataset | visualFields |
| `visualFields.data_vfctrSunyiu24d2()` | SUNY-IU control dataset | visualFields |
| `visualFields.data_vfpwgSunyiu24d2()` | SUNY-IU glaucoma dataset | visualFields |
| `visualFields.data_vfctrSunyiu10d2()` | SUNY-IU 10-2 control dataset | visualFields |
| `visualFields.data_vfctrIowaPC26()` | Iowa PC26 dataset | visualFields |
| `visualFields.data_vfctrIowaPeri()` | Iowa Peri dataset | visualFields |
| `vfprogression.data_vfseries()` | Longitudinal VF series dataset | vfprogression |
| `vfprogression.data_vfi()` | VFI dataset | vfprogression |
| `vfprogression.data_cigts()` | CIGTS dataset | vfprogression |
| `vfprogression.data_plrnouri2012()` |  | vfprogression |
| `vfprogression.data_schell2014()` |  | vfprogression |
</details>


<details>
<summary><b>Deviation Analysis </b></summary>
## Deviation Analysis

| Function | Description | Reference |
|----------|-------------|--------|
| `visualFields.getnv()` | Get current normative environment/setting | visualFields |
| `visualFields.setnv()` |  change/set normalization environment based on a predefined NV | visualFields |
| `visualFields.get_info_normvals()` | all avialbale predefined normalization environments/settings | visualFields |
| `visualFields.nvgenerate()` |generate a normalization environment based new data | visualFields |
| `utils.compute_missing_blocks()` | Compute missing blocks ( `td`, `pd`, `tdp`, `pdp`) using current normative setting NV | PyVisualFieldsV2 |
| `visualFields.gettd()` | compute td using current normative setting NV | visualFields |
| `visualFields.gettdp()` | compute tdp using current normative setting NV | visualFields |
| `visualFields.getpd()` | compute pd using current normative setting NV | visualFields |
| `visualFields.getpdp()` | compute pdp using current normative setting NV | visualFields |
| `visualFields.getgh()` | compute general heigh using current normative setting NV | visualFields |
| `visualFields.getgl()` | compute gl (global incices, e.g. msens (MS), tmd (i.e. MD, but weighted mean of TD values), pmd (i.e. weighted mean of PD values) psd, vfi, gh ) using current normative setting NV | visualFields |
| `visualFields.getglp()` | compute gl's probabilities (e.g. mdprob, psdprob) using current normative setting NV | visualFields |
</details>

<details>
<summary><b>Progression Analysis </b></summary>
## Progression Analysis 

| Function | Description |Reference |
|----------|-------------|--------|
| `vfprogression.get_score_AGIS()` | Compute AGIS score | vfprogression |
| `vfprogression.get_score_CIGTS()` | Compute CIGTS score | vfprogression |
| `vfprogression.progression_agis()` | AGIS progression analysis | vfprogression |
| `vfprogression.progression_cigts()` | CIGTS progression analysis | vfprogression |
| `vfprogression.progression_vfi()` | VFI progression analysis | vfprogression |
| `vfprogression.progression_plrnouri2012()` | Nouri et al. progression analysis | vfprogression |
| `vfprogression.progression_schell2014()` | Schell et al. progression analysis | vfprogression |
| `visualFields.glr()` | Linear regression with global indices | visualFields |
| `visualFields.plr()` | Pointwise linear regression (PLR) | visualFields |
| `visualFields.poplr()` | PoPLR regression analysis  | visualFields |
</details>


<details>
<summary><b>Glaucoma Diagnostic</b></summary>

## Glaucoma Diagnostic Criteria (PyGlaucoMetrics)

| Function | Description | Reference |
|----------|-------------|-----------|
| `PyGlaucoMetrics.Fn_HAP2()` | HAP2 glaucoma diagnosis | PyGlaucoMetrics[1,5] |
| `PyGlaucoMetrics.Fn_HAP2_part2()` | HAP2 severity classification | PyGlaucoMetrics[1,5] |
| `PyGlaucoMetrics.Fn_UKGTS()` | UKGTS criteria |PyGlaucoMetrics[1,5] |
| `PyGlaucoMetrics.Fn_LoGTS()` | LoGTS criteria |PyGlaucoMetrics[1,5] |
| `PyGlaucoMetrics.Fn_Foster()` | Foster criteria |PyGlaucoMetrics[1,5] |
| `PyGlaucoMetrics.Fn_Kangs()` | Kang's criteria |PyGlaucoMetrics[1,5] |

</details>


<details>
<summary><b>Visualization Functions</b></summary>
## Visualization

| Function | Description |
|----------|-------------|
| `vfprogression.plotValues()` | Plot sensitivity, TD, or PD values |
| `vfprogression.plotProbabilities()` | Plot TDP or PDP probability maps |
| `visualFields.vfplot()` | Generic VF plotting function |
| `visualFields.vfplot_s()` | Sensitivity plot |
| `visualFields.vfplot_td()` | Total deviation plot |
| `visualFields.vfplot_pd()` | Pattern deviation plot |
| `visualFields.vfplotsparklines()` | Sparkline visualization |
| `visualFields.vflegoplot()` | Lego plot visualization |
| `visualFields.plotProbColormap()` | Probability colormap legend |
| `visualFields.vfplotplr()` |  |
| `utils.Fn_report()` | Make a report of an eye | PyVisualFieldsV2 |
</details>




## Snapshots

[See Github Repository](https://github.com/mohaEs/PyVisualField)

<img src="./imgs/1_(12).png" width="50%">
<img src="./imgs/1_(13).png" width="50%">
<img src="./imgs/1_(1).png" width="50%">
<img src="./imgs/1_(2).png" width="50%">
<img src="./imgs/1_(3).png" width="50%">
<img src="./imgs/1_(4).png" width="50%">
<img src="./imgs/1_(5).png" width="50%">
<img src="./imgs/1_(6).png" width="50%">
<img src="./imgs/1_(8).png" width="50%">
<img src="./imgs/1_(7).png" width="50%">
<img src="./imgs/1_(9).png" width="50%">
<img src="./imgs/1_(10).png" width="50%">

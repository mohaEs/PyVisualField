# PyVisualFields 

## A python tool collection for analyzing visual fields 

This packages includes functions for visuald field analysis and display. 

https://pypi.org/project/PyVisualFields/

Version 2 is R-independent while maintaining the original module organization. The modules are inspired by vfprogression (Elze et al. [1]) and visualFields (Marin-Franch et al. [2]). 
Additionally, pyGlaucoMetric has been integrated to enable glaucoma classification based on visual field patterns.

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
- vfprogression (by Elze et al. [1])
- visualFields (by Marin-Granch et al. [2])
- pyGlaucoMetrics (by Moradi et al. [3])

## Installation: 

> pip install PyVisualFields

## Demo jupyter notebooks

The list and description of all functions are available at [All_Functions](#list-of-functions). They are all examined and introduced with examples in 4 different notebooks categorized: </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Normalization and deviation analysis [demo_2_Deviation_Analysis.ipynb](demo_2_Deviation_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Progression Analysis [demo_4_Analysis.ipynb](demo_4_Analysis.ipynb)
- Glaucoma Detection [demo5_PyGlaucoMetrics.ipynb](demo5_PyGlaucoMetrics.ipynb) </br>

__Notice:__ PyGlaucoMetric is also available as a seperatre PyPI package and GitHub repository (built upon PyVisualFields), which includes a graphical user interface (GUI) for progression analysis and glaucoma detection. Indeed PyVisualFields is designed as a developer-facing package library, while pyGlaucoMetric serves as an accessible GUI application implementing selected visual field analysis components.
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

</br>

-   &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   __function__  &nbsp; ----------------------------- &nbsp; __description__ &nbsp; ----------- &nbsp; __from package__ </br> </br>


from PyVisualFields.utils import canonicalize_vf_df
from PyVisualFields.utils import vf_blocks, missing_blocks
from PyVisualFields.utils import compute_missing_blocks
from PyVisualFields.utils import print_vf_summary, investigate_vf_df


- utils.canonicalize_vf_df() &nbsp; ----------- &nbsp; canonicalize the VF data &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 
- utils.canonicalize_vf_df(, sort_byDateAge=True) &nbsp; ----------- &nbsp; canonicalize the VF data and sort based on date or age of for each patient &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 
- utils.print_vf_summary() &nbsp; ----------- &nbsp; investigate the VF data and print a summary of all available information &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_
- utils.investigate_vf_df() &nbsp; ----------- &nbsp; investigate the VF data and return a summary of all available information &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 
- utils.vf_blocks() &nbsp; ----------- &nbsp; investigate available VF data (blocks: s, td, pd, tdp, pdp) &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 
- utils.missing_blocks() &nbsp; ----------- &nbsp; investigate VF data and returns missing blocks &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 
- utils.compute_missing_blocks() &nbsp; ----------- &nbsp; Will calculate the missing blocks. Based on current NV settings. See Deviation Analysis demo &nbsp; ----------- &nbsp; _PyVisualFieldsV2[1]_ 


- visualFields.data_vfpwgRetest24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.data_vfpwgRetest24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 

- visualFields.data_vfpwgRetest24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.data_vfctrSunyiu24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.data_vfpwgSunyiu24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.data_vfctrSunyiu10d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
-  visualFields.data_vfctrIowaPC26() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.data_vfctrIowaPeri() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[4]_ </br></br>
- vfprogression.data_vfseries() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[3]_ 
- vfprogression.data_vfi() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[3]_ 
-  vfprogression.data_cigts() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[3]_ 
- vfprogression.data_plrnouri2012() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[3]_ 
- vfprogression.data_schell2014()  &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[3]_  </br></br>
- vfprogression.get_score_AGIS() &nbsp; ----------- &nbsp;  get AGIS score &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.get_score_CIGTS() &nbsp; ----------- &nbsp;  get CIGTS score &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.progression_cigts() &nbsp; ----------- &nbsp;  progression analysis by CIGTS &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.progression_plrnouri2012() &nbsp; ----------- &nbsp;  progression analysis by Nouri et al. &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.progression_vfi()&nbsp; ----------- &nbsp;  progression analysis by VFi measurements &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.progression_schell2014()&nbsp; ----------- &nbsp;  progression analysis by schell et al. &nbsp; ----------- &nbsp; _vfprogression[3]_
- vfprogression.progression_agis()&nbsp; ----------- &nbsp;  progression analysis by AGIS &nbsp; ----------- &nbsp; _vfprogression[3]_ </br></br> 
- visualFields.glr() &nbsp; ----------- &nbsp;  Linear regression with global indices  &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.plr() &nbsp; ----------- &nbsp;  pointwise linear regression (PLR)  &nbsp; ----------- &nbsp; _visualFields[4]_  
- visualFields.poplr() &nbsp; ----------- &nbsp;  PoPLR regression analysis  &nbsp; ----------- &nbsp; _visualFields[4]_ </br></br>
- vfprogression.plotValues() &nbsp; ----------- &nbsp; plot/save VF values (s, td, pd) &nbsp; ----------- &nbsp; _vfprogression[3]_ 
- vfprogression.plotProbabilities() ----------- &nbsp; plot/save tdp/pdp values (tdp, pdp) &nbsp; ----------- &nbsp; _vfprogression[3]_
- visualFields.vfplot() ----------- &nbsp; plot/save s/td/pd/tds/pds values (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplot_s()  &nbsp; ----------- &nbsp; alias for vfplot(type='s') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplot_td()  &nbsp; ----------- &nbsp; alias for vfplot(type='td') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplot_pd() &nbsp; ----------- &nbsp; alias for vfplot(type='pd') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplot_tds()  &nbsp; ----------- &nbsp; alias for vfplot(type='tds') (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplot_pds()  &nbsp; ----------- &nbsp; alias for vfplot(type='pds') (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.plotProbColormap() &nbsp; ----------- &nbsp; show colormap of probablies &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplotsparklines() &nbsp; ----------- &nbsp; plot/save sparklines (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplotsparklines_s()  &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='s') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplotsparklines_td() &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='td') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplotsparklines_pd() &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='pd') &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vfplotplr() &nbsp; ----------- &nbsp; -- &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.vflegoplot() &nbsp; ----------- &nbsp; -- &nbsp; ----------- &nbsp; _visualFields[4]_ 
- currentNV = visualFields.getnv() &nbsp; ----------- &nbsp; get current normative environment/setting (NV) &nbsp; ----------- &nbsp; _visualFields[4]_ 
- visualFields.vfsfa() [obsolete] &nbsp; ----------- &nbsp; Generates one-page report of single field analyses as a pdf file &nbsp; ----------- &nbsp; _visualFields[4]_  </br></br>
- visualFields.getallvalues() [obsolete] &nbsp; ----------- &nbsp; compute all td, pd, pdp, tdp, gl, gh,glp based on the current NV &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.gettd() &nbsp; ----------- &nbsp; compute td &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.getgl() &nbsp; ----------- &nbsp;  compute gl &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.gettdp() &nbsp; ----------- &nbsp; compute tdp &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.getpd() &nbsp; ----------- &nbsp;  compute pd &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.getgh() &nbsp; ----------- &nbsp;  compute gh &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.getpdp() &nbsp; ----------- &nbsp;  compute pdp &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.getglp() &nbsp; ----------- &nbsp;  compute gi &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.get_info_normvals() &nbsp; ----------- &nbsp; Get all avialbale predefined normalization environments/settings &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.setnv() &nbsp; ----------- &nbsp; change/set normalization environment based on a predefined NV &nbsp; ----------- &nbsp; _visualFields[4]_
- visualFields.nvgenerate &nbsp; ----------- &nbsp; generate a normalization environment based new data &nbsp; ----------- &nbsp; _visualFields[4]_</br></br>

- PyGlaucoMetrics.Fn_HAP2 &nbsp; ----------- &nbsp; determine glaucoma cases based on criteria: HAP2 &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_
- PyGlaucoMetrics.Fn_HAP2_part2 &nbsp; ----------- &nbsp; determine VF defect severity based on criteria: HAP2 partII &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_
- PyGlaucoMetrics.Fn_UKGTS &nbsp; ----------- &nbsp; determine glaucoma cases based on criteria: UKGTS &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_
- PyGlaucoMetrics.Fn_LoGTS &nbsp; ----------- &nbsp; determine glaucoma cases based on criteria: LoGTS &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_
- PyGlaucoMetrics.Fn_Foster &nbsp; ----------- &nbsp; determine glaucoma cases based on criteria: Foster &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_
- PyGlaucoMetrics.Fn_Kangs &nbsp; ----------- &nbsp; determine glaucoma cases based on criteria: Kangs &nbsp; ----------- &nbsp; PyGlaucoMetrics[1,5]_


## Snapshots



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

# PyVisualFields 

## A python tool collection for analyzing visual fields 

This packages includes functions for visuald field analysis and display. 

We use the rpy2 as the python wrapper to use R in Python. Then, we define and prepare the methods to call the methods and data implemented and introduced in R packages vfprogression (by Elze et al. [1]) and visualFields (by Marin-Granch et al. [2]). We write these functions in python language and demonstrate their functionalities in four categories of presenting data, plotting, scoring and progression analysis, and normalization analysis. For each category, we provide the examples, description of each function, associated requirements, and the output of that function in Jupyter notebooks.


## Demo jupyter notebooks

The list and description of all functions are available at [All_Functions](#list-of-functions). They are all examined and introduced witn examples in 4 different notebooks categorized: </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Normalization and deviation analysis [demo_2_Deviation_Analysis.ipynb](demo_2_Deviation_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Analysis [demo_4_Analysis.ipynb](demo_4_Analysis.ipynb)


## Installation: 
This python package depends on 
- R 
- rpy2 python package
- vfprogression R package
- visualFields R package

Make sure to install them before installing this PyVisualFields package:

- If you want to create a seperate conda environment and install everything from scratch follow this guidline: [readme_Installation_conda.md](readme_Installation_conda.md)
or these videos: 

- If you have your preinstalled R or rpy2, follow the steps provided in our guideline: [readme_Installation.md](readme_Installation.md)

## references:
[1] https://cran.r-project.org/web/packages/vfprogression/index.html </br>
[2] https://cran.r-project.org/web/packages/visualFields/index.html 

</br>

![](./imgs/img.jpg)


## list of functions
-   &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   __function__  &nbsp; ----------------------------- &nbsp; __description__ &nbsp; ----------- &nbsp; __from package__ </br> </br>
- visualFields.data_vfpwgRetest24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.data_vfctrSunyiu24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.data_vfpwgSunyiu24d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.data_vfctrSunyiu10d2() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ 
-  visualFields.data_vfctrIowaPC26() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.data_vfctrIowaPeri() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _visualFields[2]_ </br></br>
- vfprogression.data_vfseries() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[1]_ 
- vfprogression.data_vfi() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[1]_ 
-  vfprogression.data_cigts() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[1]_ 
- vfprogression.data_plrnouri2012() &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[1]_ 
- vfprogression.data_schell2014()  &nbsp; ----------- &nbsp; VF data &nbsp; ----------- &nbsp; _vfprogression[1]_  </br></br>
- vfprogression.get_score_AGIS() &nbsp; ----------- &nbsp;  get AGIS score &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.get_score_CIGTS() &nbsp; ----------- &nbsp;  get CIGITS score &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.progression_cigts() &nbsp; ----------- &nbsp;  progression analysis by CIGITS &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.progression_plrnouri2012() &nbsp; ----------- &nbsp;  progression analysis by Nouri et al. &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.progression_vfi()&nbsp; ----------- &nbsp;  progression analysis by VFi measurements &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.progression_schell2014()&nbsp; ----------- &nbsp;  progression analysis by schell et al. &nbsp; ----------- &nbsp; _vfprogression[1]_
- vfprogression.progression_agis()&nbsp; ----------- &nbsp;  progression analysis by AGIS &nbsp; ----------- &nbsp; _vfprogression[1]_ </br></br> 
- visualFields.glr() &nbsp; ----------- &nbsp;  Linear regression with global indices  &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.plr() &nbsp; ----------- &nbsp;  pointwise linear regression (PLR)  &nbsp; ----------- &nbsp; _visualFields[2]_  
- visualFields.poplr() &nbsp; ----------- &nbsp;  PoPLR regression analysis  &nbsp; ----------- &nbsp; _visualFields[2]_ </br></br>
- vfprogression.plotValues() &nbsp; ----------- &nbsp; plot/save VF values (s, td, pd) &nbsp; ----------- &nbsp; _vfprogression[1]_ 
- vfprogression.plotProbabilities() ----------- &nbsp; plot/save tdp/pdp values (tdp, pdp) &nbsp; ----------- &nbsp; _vfprogression[1]_
- visualFields.vfplot() ----------- &nbsp; plot/save s/td/pd/tds/pds values (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplot_s()  &nbsp; ----------- &nbsp; alias for vfplot(type='s') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplot_td()  &nbsp; ----------- &nbsp; alias for vfplot(type='td') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplot_pd() &nbsp; ----------- &nbsp; alias for vfplot(type='pd') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplot_tds()  &nbsp; ----------- &nbsp; alias for vfplot(type='tds') (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplot_pds()  &nbsp; ----------- &nbsp; alias for vfplot(type='pds') (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.plotProbColormap() &nbsp; ----------- &nbsp; show colormap of probablies &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplotsparklines() &nbsp; ----------- &nbsp; plot/save sparklines (s, td, pd) &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplotsparklines_s()  &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='s') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplotsparklines_td() &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='td') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplotsparklines_pd() &nbsp; ----------- &nbsp; alias for vfplotsparklines(type='pd') &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vfplotplr() &nbsp; ----------- &nbsp; -- &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.vflegoplot() &nbsp; ----------- &nbsp; -- &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.vfsfa() &nbsp; ----------- &nbsp; Generates of one-page reports of single field analyses as a pdf file &nbsp; ----------- &nbsp; _visualFields[2]_  </br></br>
- currentNV = visualFields.getnv() &nbsp; ----------- &nbsp; get current normative environment/setting (NV) &nbsp; ----------- &nbsp; _visualFields[2]_ 
- visualFields.getallvalues() &nbsp; ----------- &nbsp; compute all td, pd, pdp, tdp, gl, gh,glp based on the current NV &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.gettd() &nbsp; ----------- &nbsp; alias for getallvalues only to compute td &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.getgl() &nbsp; ----------- &nbsp; alias for getallvalues only to compute gl &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.gettdp() &nbsp; ----------- &nbsp; alias for getallvalues only to compute tdp &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.getpd() &nbsp; ----------- &nbsp; alias for getallvalues only to compute pd &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.getgh() &nbsp; ----------- &nbsp; alias for getallvalues only to compute gh &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.getpdp() &nbsp; ----------- &nbsp; alias for getallvalues only to compute pdp &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.getglp() &nbsp; ----------- &nbsp; alias for getallvalues only to compute gi &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.get_info_normvals() &nbsp; ----------- &nbsp; Get all predefined normalization environments/settings &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.setnv() &nbsp; ----------- &nbsp; change/set normalization environment based on a predefined NV &nbsp; ----------- &nbsp; _visualFields[2]_
- visualFields.nvgenerate &nbsp; ----------- &nbsp; generate a normalization environment based new data &nbsp; ----------- &nbsp; _visualFields[2]_


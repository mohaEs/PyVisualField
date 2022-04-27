# PyVisualField tool collection for analyzing visual field 

This packages includes functions for visuald field analysis and display. 

We use the rpy2 as the python wrapper to use R in Python. Then, we define and prepare the methods to call the methods and data implemented and introduced in R packages vfprogression (by Elze et al. [1]) and visualFields (by Marin-Granch et al. [2]). We write these functions in python language and demonstrate their functionalities in four categories of presenting data, plotting, scoring and progression analysis, and normalization analysis. For each category, we provide the examples, description of each function, associated requirements, and the output of that function in Jupyter notebooks.


## Demo jupyter notebooks

You can find provived examples in 4 different notebooks categorized to: </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Analysis [demo_2_Analysis.ipynb](demo_2_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Normalization and deviation analysis [demo_4_Normalization_Deviation_Analysis.ipynb](demo_4_Normalization_Deviation_Analysis.ipynb)

## Installation: 
This package depends on 
- R 
- rpy2 python package
- vfprogression R package
- visualFields R package

Make sure to install them before installing this PyVisualFields package:

- If you want to create a seperate conda environment and install everything from scratch follow this guidline: [readme_Installation_conda.md](readme_Installation_conda.md)
or these videos: 

- If you have your preinstalled R or rpy2, follow the steps provided in our guideline: [readme_Installation.md](readme_Installation.md)

## references:
[1] https://cran.r-project.org/web/packages/vfprogression/index.html
[2] https://cran.r-project.org/web/packages/visualFields/index.html 


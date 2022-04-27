# PyVisualField tool collection for analyzing visual field 


## Demo jupyter notebooks

You can find provived examples in 4 different notebooks categorized to: </br>
- Data [demo_1_Data.ipynb](demo_1_Data.ipynb)
- Analysis [demo_2_Analysis.ipynb](demo_2_Analysis.ipynb)
- Plotting [demo_3_Plotting.ipynb](demo_3_Plotting.ipynb)
- Normalization and deviation analysis [demo_4_Normalization_Deviation_Analysis.ipynb](demo_4_Normalization_Deviation_Analysis.ipynb)

## Address the following steps to prepare the system

1- Installs and set R and rpy2 work well </br>
2- Install R requirements </br>
3- Install python requirements </br>
4- install our PyVisualFields package

## 1- verify the R and rpy2 installation
This package needs R >= 4.1.1 and rpy2 >= 3.4.5 to be installed and work fine. </br>
After your prefered installation approach, use the _test_rpy2.py_ to verify that your installation works.
If you recieved error: "R_HOME must be set in the environment or Registry", you need to fix it first (see the section 2 or 3 of the readme). 

## 2- install R packages
use _install_R_packages.py_ to install required R packages.

## 3- install python packages
install other requirements with requirement.txt file:
> pip install -r requirements.txt </br>

or simply manually install these:   </br>
&emsp;    tzlocal >= 3.0 </br>
&emsp;    scikit-image >= 0.18.1 </br>
&emsp;    pandas >= 1.2.4 </br>
&emsp;    PyPDF2 >=  1.26.0 </br>
&emsp;    PyMuPDF >= 1.19.1 </br>
&emsp;    reportlab >=  3.6.2 </br>
&emsp;    matplotlib >= 3.3.4 </br>

### Done: now you can import the library and use the notebooks 
### ++++++++++++ Section 2 +++++++++++++++++++++++

## rpy2 problem (R_HOME)
if you have installed R and rpy2 and have a problem to set the R_HOME error: </br>
Quick fix: </br> 
### A) Get your R path (path/to/R) </br>
in R terminal type R.home() and get the path of installed R. </br>
example: </br>
> \> R.home() </br>
[1] "C:/Users/mohae/anaconda3/envs/env_test_pyVF/lib/R" </br>
so we have our path/to/R as "C:/Users/mohae/anaconda3/envs/env_test_pyVF/lib/R" 

### B) add the R_HOME variable
Then set the R_HOME environment variable to this path. </br>
==> For windows:</br>
in cmd or anaconda prompt, set a permanent setting path:
> setx R_HOME path/to/R

==> For mac or Linux: </br>
permanently: </br>
> echo 'export R_HOME=path/to/R' >> ~/.bash_profile 

### Notice: You need to close and open a new terminal to have changes

### +++++++++++++ Section 3 ++++++++++++++++++++++
## set up everything from scratch
If you have not installed any R or rpy2, or want to make a seperate environment with Anaconda, follow our intruction:

> conda create --name env_pyVF python=3.8 </br>
> conda activate env_pyVF </br>

install R 4.1.2: </br>
> conda install -c conda-forge r-base==4.1.2 

set the R_HOME environment variable/path: </br>
see section 2 (notice R is insilde the conda environment)

close the terminal and open a new one </br>

open a new conda prompt </br>
activate the environement e.g. 
> conda activate env_pyVF

install rpy2 </br>
> pip install rpy2==3.4.5 

use _test_installation_rpy2.py_ to check the R and rpy2 installation

install required R packages with _install_R_packages.py_

evaluate the installation with _test_all.py_

done </br>
but make sure to close the terminal and open a new one
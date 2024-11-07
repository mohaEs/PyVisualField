## set up everything from scratch

If you have not installed any R or rpy2, or want to make a seperate environment with Anaconda, follow our intruction:

### 0- Download/clone the GitHub repository
[GitHub link](https://github.com/mohaEs/PyVisualField) 

### 1- create and activate a conda environment:

> \> conda create --name env_pyVF python=3.8 </br>
> \> conda activate env_pyVF </br>

### 2- install R in the environment
install R 4.1.2: </br>
> (env_pyVF) \> conda install -c conda-forge r-base==4.1.2 

### 3- set R_HOME variable
set the R_HOME environment variable/path to the R version installed in the environment: </br>
#### A) Get your R path (path/to/R) </br>
in R terminal type R.home() and get the path of installed R. </br>
example: </br>
> (env_pyVF)\> R </br>
> \> R.home() </br>
[1] "C:/Users/mohae/anaconda3/envs/env_pyVF/lib/R" </br>

so now, we have our path/to/R as "C:/Users/mohae/anaconda3/envs/env_pyVF/lib/R" </br>
copy the path and quit from R


#### B) add the R_HOME variable
Then set the R_HOME environment variable to this path. </br>
==> For windows:</br>
in cmd or anaconda prompt, set a permanent setting path:
> \> setx R_HOME path/to/R

==> For mac or Linux: </br>
permanently: </br>
> \> echo 'export R_HOME=path/to/R' >> ~/.bash_profile 

close the terminal and open a new one </br>

### 4- install rpy2
open a new conda prompt </br>
activate the environement e.g. 
> \> conda activate env_pyVF

install rpy2 </br>
> (env_pyVF)\> pip install rpy2==3.4.5 

use _test_rpy2.py_ to verify the R and rpy2 installation.

### 5- install required R packages
install required R packages with _install_R_packages.py_
> (env_pyVF)\> python install_R_packages.py

evaluate the installation with _test_Rpacks.py_

### 6- install required python packages (you can skip this)
> (env_pyVF)\> pip install -r requirements.txt

### 7- install PyVisualFields
if all above sections work properly, install the PyVisualFields Package:
> (env_pyVF)\> pip install PyVisualFields


### 8- install every other packages do you need in the environment, e.g. jupyter
> (env_pyVF)\> ..

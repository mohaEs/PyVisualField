## set up everything from scratch
If you have not installed any R or rpy2, or want to make a seperate environment with Anaconda, follow our intruction:

> conda create --name env_pyVF python=3.8 </br>
> conda activate env_pyVF </br>

install R 4.1.2: </br>
> conda install -c conda-forge r-base==4.1.2 

set the R_HOME environment variable/path to the R version installed in the environment: </br>
### A) Get your R path (path/to/R) </br>
in R terminal type R.home() and get the path of installed R. </br>
example: </br>
> \> R </br>
> \> R.home() </br>
[1] "C:/Users/mohae/anaconda3/envs/env_pyVF/lib/R" </br>
so we have our path/to/R as "C:/Users/mohae/anaconda3/envs/env_pyVF/lib/R" 

### B) add the R_HOME variable
Then set the R_HOME environment variable to this path. </br>
==> For windows:</br>
in cmd or anaconda prompt, set a permanent setting path:
> setx R_HOME path/to/R

==> For mac or Linux: </br>
permanently: </br>
> echo 'export R_HOME=path/to/R' >> ~/.bash_profile 
see section 2 (notice R is insilde the conda environment)

close the terminal and open a new one </br>

open a new conda prompt </br>
activate the environement e.g. 
> conda activate env_pyVF

install rpy2 </br>
> pip install rpy2==3.4.5 

use _test_installation_rpy2.py_ to check the R and rpy2 installation

install required R packages with _install_R_packages.py_

evaluate the installation with _test_Rpacks.py_

done </br>
but make sure to close the terminal and open a new one

We can also install jupyter in the environment

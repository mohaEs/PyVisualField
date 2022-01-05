
1- Installs and set R and rpy2 work well
2- Install R requirements
3- Install python requirements

1- 
This package needs R >= 4.1.1 and rpy2 >= 3.4.5 works fine. After youe prefered installation approach, use the pr_test_installation_rpy2.py to verify that your installation works.
If you recieved error: "R_HOME must be set in the environment or Registry", you need to fix it first.

Quick fix: 
--- Get your R path (path/to/R)
in R terminal type R.home() and get the path of installed R. 
example:
> R.home()
[1] "C:/Users/mohae/anaconda3/envs/env_test_pyVF/lib/R"

Then set the R_HOME environment variable to this path. 
For windows:
 in cmd or anaconda promt:
permanent setting (prefered):
   > setx R_HOME path/to/R

For mac and Linux:
> export R_HOME=path/to/R
or permanent:
> echo 'export R_HOME="path/to/R"' >> ~/.bash_profile 

Notice: You need to close and open a new terminal to have changes

2- 
use pr_install_R_packages.py to install required R pacages.

3- 
other requirements are: 
    pip install tzlocal
    pip install scikit-image
    pip install pandas

    pip install PyPDF2
    pip install PyMuPDF 
    pip install reportlab
    pip install matplotlib



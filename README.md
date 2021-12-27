


create conda environment to install R and rpy2:
    conda create -n env_pyVisualField r-essentials r-base python=3.7
    conda activate env_pyVisualField
    conda install -c r rpy2

test rpy2 is installed properly by opening python:
    
    python
    import rpy2.situation
    for row in rpy2.situation.iter_info():
        print(row)
    from rpy2.robjects.vectors import DataFrame, FloatVector, IntVector, StrVector, ListVector, Matrix
    quit()

if correct, install required R packages

    R # enter to R console
    install.packages("visualFields")
    install.packages("vfprogression")
    q()

all other dependencies ################################

pip install tzlocal
pip install skimage
pip install pandas

pip install PyPDF2
pip install PyMuPDF 
pip install reportlab


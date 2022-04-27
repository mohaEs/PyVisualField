
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


try: 
    import rpy2
    print("===> rpy2 version: ', rpy2.__version__")
    
    import rpy2.robjects as robjects

    from rpy2.robjects.packages import importr
    # import rpy2's package module
    import rpy2.robjects.packages as rpackages
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
    print("===> R and rpy2 work fine!")
except:
    print("===> Something is wrong: rpy2 does not work fine or is not available!")

try: 
    lib_vf = importr('visualFields')
    print("===> visualFields R package is loaded successfully!")
except:
    print("===> Something is wrong: required R packages are not available!") 

try:
    lib_vfprogression = importr('vfprogression')
    print("===> vfprogression R package is loaded successfully!")    
except:
    print("===> Something is wrong: required R packages are not available!") 
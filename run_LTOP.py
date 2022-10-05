######################################################################################################### 
##                                                                                                    #\\
##                                         LandTrendr Optimization workflow                           #\\
##                                                                                                    #\\
#########################################################################################################

# date: 2022-09-02
# author: Peter Clary        | clarype@oregonstate.edu
#         Robert Kennedy     | rkennedy@coas.oregonstate.edu
#         Ben Roberts-Pierel | robertsb@oregonstate.edu
# website: https:#github.com/eMapR/LT-GEE

##################################################/
################ Import modules ##########################/
##################################################/
import ee 
import params
import ltop 
from run_SNIC_01 import run_snic
print(ee.__version__)

# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
ee.Initialize()

'''
This script is the primary place to run the full LandTrendr Optimization (LTOP) workflow.
This script depends on the 01-05 LTOP component scripts as well as three additional Python scripts 
for some additional steps. See [DOCS] for more information. 
'''

if __name__ == '__main__': 
    print(params)
    #run_snic(params)
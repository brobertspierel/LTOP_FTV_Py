######################################################################################################### 
##                                                                                                    #\\
##                                        Step 4 LandTrendr Optimization workflow                     #\\
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
print(ee.__version__)

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()
abstractImagesPath = params.assetsRoot+params.assetsChild+'/revised_abstract_image_'; 

##################################################/
################ Call the functions ########################/
##################################################/

#this just takes the abstract images that were uploaded after step 3.1 and assembles them into an imageCollection 
abstract_output03_2 = ltop.abstractSampler03_2(abstractImagesPath,params.startYear,params.endYear); 

# 4. get Landsat values for the points in the abstract images. This will automatically generate csvs in a gDrive folder that starts with your place name  
abstract_output04 = ltop.abstractImager04(abstract_output03_2, params.place,params.abstract_image_pts); 
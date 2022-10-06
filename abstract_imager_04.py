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

import ee
import ltop

# Initialize the library.
ee.Initialize()


def run_LT_abstract_imgs(*args): 
    args = args[0]
    abstractImagesPath = args['assetsRoot']+args['assetsChild']+'/synthetic_image_'
    abstractImagesPts = args['assetsRoot']+args['assetsChild']+'/abstract_images_grid_points'
    #this just takes the abstract images that were uploaded after step 3.1 and assembles them into an imageCollection 
    abstract_output03_2 = ltop.abstractSampler03_2(abstractImagesPath,args['startYear'],args['endYear']) 

    # 4. get Landsat values for the points in the abstract images. This will automatically generate csvs in a gDrive folder that starts with your place name  
    abstract_output04 = ltop.abstractImager04(abstract_output03_2, args['place'],abstractImagesPts) 

    return None
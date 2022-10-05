######################################################################################################### 
##                                                                                                    #\\
##                                Step 5 LandTrendr Optimization workflow                             #\\
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
#from sys import path
#path.append("/home/flipflop/PycharmProjects/pyLTOP/")


import params
import ltop
print(ee.__version__)

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()
#naming convention based on previously generated image
cluster_img = ee.Image(params.assetsRoot+params.assetsChild+"/LTOP_KMEANS_cluster_image_"+params.randomPts.toString()+"_pts_"+params.maxClusters.toString()+"_max_"+params.minClusters.toString()+"_min_clusters_"+params.place+"_c2_"+params.startYear.toString());
#  cluster_img = ee.Image('users/clarype/LTOP/kmeans_testing/LTOP_KMEANS_cluster_image_20000_pts_2500_max_2500_min_clusters_Cambodia_c2_1990_tc')
##################################################/
################ Landsat Composites ########################/
##################################################/
annualSRcollection; 

#these composites are used for the last two steps and span the full period
if params.params["imageSource"] == 'medoid':
   annualSRcollection = ltgee.buildSRcollection(params.startYear, params.endYear, params.startDate, params.endDate, params.aoi, params.masked); 

elif params.params["imageSource"] != 'medoid':
     annualSRcollection = ltop.buildSERVIRcompsIC(params.startYear,params.endYear); 


##################################################/
################ Call the functions ########################/
##################################################/

# 5. create the optimized output
optimized_output05 = ltop.optimizedImager05(params.selectedLTparams,annualSRcollection,cluster_img,params.aoi); #note that table is the selected paramaters from the python script after step four

task = ee.batch.Export.image.toAsset(
    image = optimized_output05,
    description = 'Optimized_LT_'+params.startYear.toString()+'_start_'+params.place+'_all_cluster_ids_tc',
    assetId = params.assetsChild+'/Optimized_LT_'+params.startYear+'_start_'+params.place+'_all_cluster_ids_tc',
    region = params.aoi,
    scale = 30,
    maxPixels = 1e13
  )   


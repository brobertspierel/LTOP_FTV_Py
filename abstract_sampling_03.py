######################################################################################################### 
##                                                                                                    #\\
##                               Step 3 LandTrendr Optimization workflow                              #\\
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

##################################################/
################ Landsat Composites ########################/
##################################################/
annualSRcollection; 

#these composites are used for the last two steps and span the full period
if params.params["image_source"] == 'medoid': 
    annualSRcollection = ltgee.buildSRcollection(startYear, endYear, startDate, endDate, aoi, masked); 

elif params.params["image_source"] != 'comp':
    annualSRcollection = ltop.buildSERVIRcompsIC(params.startYear,params.endYear); 


##################################################/
################ Call the functions ########################/
##################################################/
#3. create some abstract images - NOTE this is split into two because there is a process that still has to take place in Python 
abstract_output03_1 = ltop.abstractSampler03_1(annualSRcollection,
                                                ee.FeatureCollection('users/clarype/LTOP/kmeans_testing/LTOP_KMEANS_stratified_points_2500_max_2500_min_clusters_Cambodia_c2_1990_tc'),
                                                # ee.FeatureCollection(params.assetsRoot+params.assetsChild+'/LTOP_KMEANS_stratified_points_'+params.maxClusters.toString()+'_max_'+params.minClusters.toString()+'_min_clusters_'+params.place+'_c2_'+params.startYear.toString()),
                                                params.startYear, 
                                                params.endYear); 

# Export the points
task = ee.batch.Export.table.toDrive(
  collection = abstract_output03_1, 
  description = "LTOP_"+params.place+"_Abstract_Sample_annualSRcollection_NBRTCWTCGNDVIB5_c2_"+params.startYear.toString()+"_start_tc", 
  fileNamePrefix = "LTOP_"+params.place+"_Abstract_Sample_annualSRcollection_NBRTCWTCGNDVIB5_c2_"+params.startYear.toString()+"_start_tc", 
  folder = params.place+'_abstract_images',
  fileFormat = 'csv'
)

 
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

# print(ee.__version__)

# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
ee.Initialize()

##################################################/
################ Call the functions ########################/
##################################################/
# 2. cluster the snic patches with kmeans - create the stratified random points - this was (usually) causing a computation timeout when doing it in one step
kmeans_output02_2 = ltop.kmeans02_2(ee.Image(params.assetsRoot+params.assetsChild+"/LTOP_KMEANS_cluster_image_"+params.randomPts.toString()+"_pts_"+params.maxClusters.toString()+"_max_"+params.minClusters.toString()+"_min_clusters_"+params.place+"_c2_"+params.startYear.toString()))
#export a fc with one point for every unique cluster id in the kmeans output

task = ee.batch.Export.table.toAsset(
            collection=kmeans_output02_2,
            description= 'LTOP_KMEANS_stratified_points_'+params.maxClusters.toString()+'_max_'+params.minClusters.toString()+'_min_clusters_'+params.place+'_c2_'+params.startYear.toString(), 
            assetId=params.assetsChild+'/LTOP_KMEANS_stratified_points_'+params.maxClusters.toString()+'_max_'+params.minClusters.toString()+'_min_clusters_'+params.place+'_c2_'+params.startYear.toString()
) 
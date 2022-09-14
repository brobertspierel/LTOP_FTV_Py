####################################################################################################### 
# \\
#                                         LandTrendr Optimization workflow                           #\\
# \\
#######################################################################################################

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

# ltgee = require('users/ak_glaciers/adpc_servir_LTOP:modules/LandTrendr.js');
# ltop = require('users/ak_glaciers/adpc_servir_LTOP:modules/LTOP_modules.js');
#sparams = require('users/ak_glaciers/adpc_servir_LTOP:modules/params.js');

print('You are currently running version: ', params.params["version"], ' of the LTOP workflow');

##################################################/
################ Call the functions ########################/
##################################################/
# 2. cluster the snic patches with kmeans - added a filter to remove points that didn't get valid values in previous step
kmeans_output02_1 = ltop.kmeans02_1(ee.FeatureCollection(
    params.params["assetsRoot"] + params.params["assetsChild"] + "/LTOP_SNIC_pts_" + params.params["place"] + "_c2_" + str(params.params["randomPts"]) + "_pts_" + str(params.params["startYear"])).filter(ee.Filter.neq('B1_mean', None)),
    ee.Image(params.params["assetsRoot"] + params.params["assetsChild"] + "/LTOP_SNIC_imagery_" + params.params["place"] + "_c2_" + str(params.params["randomPts"]) + "_pts_" + str(params.params["startYear"])),
    params.params["aoi"],
    params.params["minClusters"],
    params.params["maxClusters"]
    )


# export the kmeans output image to an asset
task = ee.batch.Export.image.toAsset(
    image= kmeans_output02_1,  # kmeans_output02.get(0),
    description= "LTOP_KMEANS_cluster_image_" + str(params.params["randomPts"]) + "_pts_" + str(params.params["maxClusters"]) + "_max_" + str(params.params["minClusters"]) + "_min_clusters_" + params.params["place"] + "_c2_" + str(params.params["startYear"]),
    assetId= params.params["assetsRoot"] + "/LTOP_KMEANS_cluster_image_" + str(params.params["randomPts"]) + "_pts_" + str(params.params["maxClusters"]) + "_max_" + str(params.params["minClusters"]) + "_min_clusters_" + params.params["place"] + "_c2_" + str(params.params["startYear"]),
    region= params.params["aoi"],
    scale= 30,
    maxPixels= 10000000000000
)
task.start()

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
# import params
import ltop
# print(ee.__version__)

# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
ee.Initialize()

##################################################/
################ Call the functions ########################/
##################################################/
# 2. cluster the snic patches with kmeans - added a filter to remove points that didn't get valid values in previous step
def generate_tasks(*args): 
    args = args[0]
    #note that paths need to be changed to access a Google cloud project 
    kmeans_output02_1 = ltop.kmeans02_1(ee.FeatureCollection(
        args["assetsRoot"] + "/LTOP_SNIC_pts_" + args["place"] + "_c2_" + str(args["randomPts"]) + "_pts_" + str(args["startYear"])).filter(ee.Filter.neq('B1_mean', None)),
        ee.Image(args["assetsRoot"] + "/LTOP_SNIC_imagery_" + args["place"] + "_c2_" + str(args["randomPts"]) + "_pts_" + str(args["startYear"])),
        args["aoi"],
        args["minClusters"],
        args["maxClusters"]
        )

    # export the kmeans output image to an asset
    task = ee.batch.Export.image.toAsset(
        image= kmeans_output02_1,  # kmeans_output02.get(0),
        description= "LTOP_KMEANS_cluster_image_" + str(args["randomPts"]) + "_pts_" + str(args["maxClusters"]) + "_max_" + str(args["minClusters"]) + "_min_clusters_" + args["place"] + "_c2_" + str(args["startYear"]),
        assetId= args["assetsRoot"] + "/LTOP_KMEANS_cluster_image_" + str(args["randomPts"]) + "_pts_" + str(args["maxClusters"]) + "_max_" + str(args["minClusters"]) + "_min_clusters_" + args["place"] + "_c2_" + str(args["startYear"]),
        region= args["aoi"],
        scale= 30,
        maxPixels= 10000000000000
    )
    task.start()
    return task.status()
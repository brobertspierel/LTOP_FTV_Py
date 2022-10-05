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
    kmeans_output02_1 = ltop.kmeans02_1(ee.FeatureCollection(
        args.params["assetsRoot"] + args.params["assetsChild"] + "/LTOP_SNIC_pts_" + args.params["place"] + "_c2_" + str(args.params["randomPts"]) + "_pts_" + str(args.params["startYear"])).filter(ee.Filter.neq('B1_mean', None)),
        ee.Image(args.params["assetsRoot"] + args.params["assetsChild"] + "/LTOP_SNIC_imagery_" + args.params["place"] + "_c2_" + str(args.params["randomPts"]) + "_pts_" + str(args.params["startYear"])),
        args.params["aoi"],
        args.params["minClusters"],
        args.params["maxClusters"]
        )

    # export the kmeans output image to an asset
    task = ee.batch.Export.image.toAsset(
        image= kmeans_output02_1,  # kmeans_output02.get(0),
        description= "LTOP_KMEANS_cluster_image_" + str(args.params["randomPts"]) + "_pts_" + str(args.params["maxClusters"]) + "_max_" + str(args.params["minClusters"]) + "_min_clusters_" + args.params["place"] + "_c2_" + str(args.params["startYear"]),
        assetId= args.params["assetsRoot"] + "/LTOP_KMEANS_cluster_image_" + str(args.params["randomPts"]) + "_pts_" + str(args.params["maxClusters"]) + "_max_" + str(args.params["minClusters"]) + "_min_clusters_" + args.params["place"] + "_c2_" + str(args.params["startYear"]),
        region= args.params["aoi"],
        scale= 30,
        maxPixels= 10000000000000
    )
    task.start()
    return task.status()
######################################################################################################### 
##                                                                                                    #\\
##                              Step 1 LandTrendr Optimization workflow                               #\\
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


print('You are currently running version: ',params.params["version"],' of the LTOP workflow')

##################################################/
#################### Composites ########################/
##################################################/
LandsatComposites=0
if params.params["image_source"] == 'medoid':

    imageEnd = ltgee.buildSRcollection(2021, 2021, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()
    imageMid = ltgee.buildSRcollection(2005, 2005, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()
    imageStart = ltgee.buildSRcollection(1990, 1990, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()

elif params.params["image_source"] != 'comp':

    comps = ltop.buildSERVIRcompsIC(params.params["startYear"],params.params["endYear"])

    #now make an image out of a start, mid and end point of the time series
    imageEnd = comps.filter(ee.Filter.eq('system:index','2021')).first()
    imageMid = comps.filter(ee.Filter.eq('system:index','2005')).first()
    imageStart = comps.filter(ee.Filter.eq('system:index','1990')).first()

    LandsatComposites = imageEnd.addBands(imageMid).addBands(imageStart)

##################################################/
################ Call the functions ########################/
##################################################/
# 1. run the snic algorithm 
snic_output01 = ltop.snic01(LandsatComposites,params.params["aoi"],params.params["randomPts"],params.params["seedSpacing"])

task = ee.batch.Export.table.toAsset(
              collection= snic_output01.get(0),
              description="LTOP_SNIC_pts_"+params.params["place"]+"_c2_"+str(params.params["randomPts"])+"_pts_"+str(params.params["startYear"]),
              assetId= params.params["assetsRoot"]+"/LTOP_SNIC_pts_"+params.params["place"]+"_c2_"+str(params.params["randomPts"])+"_pts_"+str(params.params["startYear"]),
              
)

task2 = ee.batch.Export.image.toAsset(
              image= ee.Image(snic_output01.get(1)),
              description="LTOP_SNIC_imagery_"+params.params["place"]+"_c2_"+str(params.params["randomPts"])+"_pts_"+str(params.params["startYear"]),
              assetId=params.params["assetsRoot"]+"/LTOP_SNIC_imagery_"+params.params["place"]+"_c2_"+str(params.params["randomPts"])+"_pts_"+str(params.params["startYear"]),
              region= params.params["aoi"],
              scale=30,
              maxPixels=10000000000000
)

task.start()
task2.start()
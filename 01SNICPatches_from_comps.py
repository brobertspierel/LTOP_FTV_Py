
######################################################################################################## 
##                                                                                                    #\\
##                                         LANDTRENDR LIBRARY                                         #\\
##                                                                                                    #\\
#########################################################################################################


# date: 2020-12-10
# author: Peter Clary        | clarype@oregonstate.edu
#         Robert Kennedy     | rkennedy@coas.oregonstate.edu
#         Ben Roberts-Pierel | robertsb@oregonstate.edu
# website: https://github.com/eMapR/LT-GEE

#////////////////////////////////////////////////////////
#///////////////Import Modules ////////////////////////////
#//////////////////////// /////////////////////////////
#note that this needs to be changed to the public version when that is available 
import ee
import params
import ltop
print(ee.__version__)

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

#ltgee = require('users/emaprlab/public:Modules/LandTrendr.js'); 

#////////////////////////////////////////////////////////
#/////////////////// vector////////////////////////////
#//////////////////////// /////////////////////////////
place = ''


#use the full servir area
aoi = ee.FeatureCollection("projects/servir-mekong/hydrafloods/CountryBasinsBuffer").geometry()

#/////////////////////////////////////////////////////////////////
#////////////////// time and mask params//////////////////////////
#//////////////////////// ////////////////////////////////////////

startYear = 1990; 
endYear = 2021; 

#/////////////////////////////////////////////////////////////////
#//////////////////////Landsat Composites/////////////////////////
#/////////////////////////////////////////////////////////////////
#get the SERVIR composites
yr_images = [];
timeseries = list(range(startYear,endYear+1)) 
for y in timeseries :
	print(y)
	im = ee.Image("projects/servir-mekong/composites/" + str(y)); 
	yr_images.append(im); 
  


servir_ic = ee.ImageCollection.fromImages(yr_images); 
#print(servir_ic,'servir ic'); 
#in this version we don't build composites but pull them from existing composites
# comps = ee.ImageCollection('projects/servir-mekong/regionalComposites').filterBounds(aoi);

#the rest of the scripts will be easier if we just rename the bands of these composites to match what comes out of the LT modules
#note that if using the SERVIR composites the default will be to get the first six bands without the percentile bands
def map_servir_ic(img):
	return img.select(['blue','green','red','nir','swir1','swir2'],['B1','B2','B3','B4','B5','B7'])


comps = servir_ic.map(map_servir_ic)
  

#now make an image that looks like the outputs of the LT modules
image2021 = comps.filter(ee.Filter.eq('system:index','2021')).first();
image2005 = comps.filter(ee.Filter.eq('system:index','2005')).first();
image1990 = comps.filter(ee.Filter.eq('system:index','1990')).first();

LandsatComposites = image2021.addBands(image2005).addBands(image1990); 
#print(LandsatComposites)
#//////////////////////////////////////////////////////
#////////////////SNIC//////////////////////////////////
#/////////////////////////////////////////////////////

snicImagery = ee.Algorithms.Image.Segmentation.SNIC(LandsatComposites,10, 1).clip(aoi);
  
# Map.addLayer(snicImagery,{"opacity":1,"bands":["B3_mean","B2_mean","B1_mean"],"min":242.47874114990233,"max":962.1856112670898,"gamma":1},'snicImagey1')

#////////////////////////////////////////////////////////
#////////////SNIC split by bands////////////////////////
#/////////////////////////////////////////////////////

patchRepsMean = snicImagery.select(["seeds","clusters",  "B1_mean", "B2_mean",  "B3_mean",  "B4_mean",  "B5_mean",  "B7_mean",  "B1_1_mean",  "B2_1_mean",  "B3_1_mean",  "B4_1_mean",  "B5_1_mean","B7_1_mean",  "B1_2_mean",  "B2_2_mean",  "B3_2_mean",  "B4_2_mean",  "B5_2_mean",  "B7_2_mean"]);

patchRepSeeds = snicImagery.select(['seeds']);

#/#////////////////////////////////////////////////////
#/////Select singel pixel from each patch/////////////
#/////#////////////////////////////////////////////////

SNIC_means_image = patchRepSeeds.multiply(patchRepsMean) #.reproject({  crs: 'EPSG:4326',  scale: 30});#.clip(aoi)

# Map.addLayer(SNIC_means_image,{"opacity":1,"bands":["B3_mean","B2_mean","B1_mean"],"min":242.47,"max":962.18,"gamma":1},'SNIC_means_image')

# //////////////////////////////////
#// //////////////Export SNIC/////////
#// //////////////////////////////////

task = ee.batch.Export.image.toAsset(
        image=snicImagery.toInt32().clip(aoi), 
        description='SNIC_c2_comps', 
        assetId='users/clarype/SNIC_c2_comps', 
        region=aoi, 
        scale=30, 
        maxPixels= 1e13 
      )     

task2 = ee.batch.Export.image.toAsset(
        image=SNIC_means_image.toInt32().clip(aoi), 
        description= 'sNICseed_c2_comps', 
        assetId='users/clarype/sNICseed_c2_comps', 
        #fileNamePrefix= place+"_SNICseed_c2_comps2", 
        region=aoi, 
        scale=30, 
        maxPixels= 1e13 
      )   

task.start()
task2.start()
print(task.status())


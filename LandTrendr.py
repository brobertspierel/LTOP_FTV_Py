import ee
import math
ee.Initialize()

# #######################################################################################
# ###### INDEX CALCULATION FUNCTIONS ####################################################
# #######################################################################################

# TASSELLED CAP
def tcTransform(img): 
    b = ee.Image(img).select(["B1", "B2", "B3", "B4", "B5", "B7"]) # select the image bands
    brt_coeffs = ee.Image.constant([0.2043, 0.4158, 0.5524, 0.5741, 0.3124, 0.2303]); # set brt coeffs - make an image object from a list of values - each of list element represents a band
    grn_coeffs = ee.Image.constant([-0.1603, -0.2819, -0.4934, 0.7940, -0.0002, -0.1446]); # set grn coeffs - make an image object from a list of values - each of list element represents a band
    wet_coeffs = ee.Image.constant([0.0315, 0.2021, 0.3102, 0.1594, -0.6806, -0.6109]); # set wet coeffs - make an image object from a list of values - each of list element represents a band

    sum = ee.Reducer.sum(); # create a sum reducer to be applyed in the next steps of summing the TC-coef-weighted bands
    brightness = b.multiply(brt_coeffs).reduce(sum); # multiply the image bands by the brt coef and then sum the bands
    greenness = b.multiply(grn_coeffs).reduce(sum); # multiply the image bands by the grn coef and then sum the bands
    wetness = b.multiply(wet_coeffs).reduce(sum); # multiply the image bands by the wet coef and then sum the bands
    angle = (greenness.divide(brightness)).atan().multiply(180/math.pi).multiply(100)
    tc = (brightness.addBands(greenness)
                    .addBands(wetness)
                    .addBands(angle)
                    .select([0,1,2,3], ['TCB','TCG','TCW','TCA']) #stack TCG and TCW behind TCB with .addBands, use select() to name the bands
                    .set('system:time_start', img.get('system:time_start')))
    return tc


# # NBR
#  nbrTransform = function(img) {
#      nbr = img.normalizedDifference(['B4', 'B7']) # calculate normalized difference of B4 and B7. orig was flipped: ['B7', 'B4']
#                  .multiply(1000) # scale results by 1000
#                  .select([0], ['NBR']) # name the band
#                  .set('system:time_start', img.get('system:time_start'));
#     return nbr;
# };

# #Ben added
# # NDFI - from CODED utility (original: users/bullocke/coded:coded/miscUtilities)
#  ndfiTransform = function(img) {

#   # pre-defined endmembers
#    params = ee.Dictionary({
#     'cfThreshold': 0.01, # CLOUD THRESHOLD 
#     'soil': [2000, 3000, 3400, 5800, 6000, 5800],
#     'gv': [500, 900, 400, 6100, 3000, 1000],
#     'npv': [1400, 1700, 2200, 3000, 5500, 3000],
#     'shade': [0, 0, 0, 0, 0, 0],
#     'cloud': [9000, 9600, 8000, 7800, 7200, 6500]
#     });
    
#     /* Utility function for calculating spectral indices */
#      gv = params.get('gv');
#      shade = params.get('shade');
#      npv = params.get('npv');
#      soil = params.get('soil');
#      cloud = params.get('cloud');
#     # cfThreshold = ee.Image.constant(params.get('cfThreshold'))
#     /*  Do spectral unmixing on a single image  */
#      unmixImage = ee.Image(img).unmix([gv, shade, npv, soil, cloud], true,true)
#                     .rename(['band_0', 'band_1', 'band_2','band_3','band_4']);
#      newImage = ee.Image(img).addBands(unmixImage);
#     # mask = newImage.select('band_4').lt(cfThreshold)
  
#      ndfi = unmixImage.expression(
#       '((GV / (1 - SHADE)) - (NPV + SOIL)) / ((GV / (1 - SHADE)) + NPV + SOIL)', {
#         'GV': unmixImage.select('band_0'),
#         'SHADE': unmixImage.select('band_1'),
#         'NPV': unmixImage.select('band_2'),
#         'SOIL': unmixImage.select('band_3')
#       }); 
#      ndvi = ee.Image(img).normalizedDifference(['B4','B3']).rename('NDVI')
#      evi = ee.Image(img).expression(
#           'float(2.5*(((B4/10000) - (B3/10000)) / ((B4/10000) + (6 * (B3/10000)) - (7.5 * (B1/10000)) + 1)))',
#           {
#               'B4': ee.Image(img).select(['B4']),
#               'B3': ee.Image(img).select(['B3']),
#               'B1': ee.Image(img).select(['B1'])
#           }).rename('EVI');    
          
#      toExp = newImage
#           .addBands([ndfi.rename(['NDFI']), ndvi, evi])
#           .select(['band_0','band_1','band_2','band_3','NDFI','NDVI','EVI','B1','B2','B3','B4','B5'])
#           .rename(['GV','Shade','NPV','Soil','NDFI','NDVI','EVI','Blue','Green','Red','NIR','SWIR1']); 
#           #.updateMask(mask)

#   toExp = toExp.select(['NDFI'])
#               .multiply(1000)
#               .set('system:time_start', img.get('system:time_start'));
#   return toExp;

# };

# # NDVI
#  ndviTransform = function(img){ 
#    ndvi = img.normalizedDifference(['B4', 'B3']) # calculate normalized dif between band 4 and band 3 (B4-B3/B4_B3)
#                 .multiply(1000) # scale results by 1000
#                 .select([0], ['NDVI']) # name the band
#                 .set('system:time_start', img.get('system:time_start'));
#   return ndvi;
# };
                
# # NDSI
#  ndsiTransform = function(img){ 
#    ndsi = img.normalizedDifference(['B2', 'B5']) # calculate normalized dif between band 4 and band 3 (B4-B3/B4_B3)
#                 .multiply(1000) # scale results by 1000
#                 .select([0], ['NDSI']) # name the band
#                 .set('system:time_start', img.get('system:time_start'));
#   return ndsi;
# };

# # NDMI
#  ndmiTransform = function(img) {
#      ndmi = img.normalizedDifference(['B4', 'B5']) # calculate normalized difference of B4 and B7. orig was flipped: ['B7', 'B4']
#                  .multiply(1000) # scale results by 1000
#                  .select([0], ['NDMI']) # name the band
#                  .set('system:time_start', img.get('system:time_start'));
#     return ndmi;
# };

# # EVI
#  eviTransform = function(img) {
#    evi = img.expression(
#       '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
#         'NIR': img.select('B4'),
#         'RED': img.select('B3'),
#         'BLUE': img.select('B1')
#   })
#   .multiply(1000) # scale results by 1000
#   .select([0], ['EVI']) # name the band
#   .set('system:time_start', img.get('system:time_start')); 
#   return evi;
# };

# CALCULATE A GIVEN INDEX
def calcIndex(img, inx, flip): 
    # make sure index string in upper case
    inx = inx.upper()
    
    # figure out if we need to calc tc
    tcList = ['TCB', 'TCG', 'TCW', 'TCA'];
    doTC = tcList.index(inx);
    if doTC >= 0: 
        tc = tcTransform(img)
  
    # need to flip some indices if this is intended for segmentation
    indexFlip = 1
    if flip == 1: 
        indexFlip = -1
  
    # need to cast raw bands to float to make sure that we don't get errors regarding incompatible bands
    # ...derivations are already float because of division or multiplying by decimal
    #note that this was a switch/case/default syntax but that only works in python 3.10
    #its possible there are some issues with other packages when running that version so for compatibility its changed to if/elif but 
    #that might not be the best way to do it. 
    indexImg = 0 
    if inx == 'B1': 
      indexImg = img.select(['B1']).float();#.multiply(indexFlip);
    elif inx == 'B2':
      indexImg = img.select(['B2']).float();#.multiply(indexFlip);
    elif inx == 'B3':
      indexImg = img.select(['B3']).float();#.multiply(indexFlip);
    elif inx == 'B4':
      indexImg = img.select(['B4']).multiply(indexFlip).float()
    elif inx == 'B5':
      indexImg = img.select(['B5']).float();#.multiply(indexFlip);
    elif inx == 'B7':
      indexImg = img.select(['B7']).float();#.multiply(indexFlip);
    #TODO note that these modules just haven't been translated yet 
    # elif inx == 'NBR':
    #   indexImg = nbrTransform(img).multiply(indexFlip);
    # case 'NDMI':
    #   indexImg = ndmiTransform(img).multiply(indexFlip);
    #   break;
    # case 'NDVI':
    #   indexImg = ndviTransform(img).multiply(indexFlip);
    #   break;
    # case 'NDSI':
    #   indexImg = ndsiTransform(img).multiply(indexFlip);
    #   break;
    # case 'EVI':
    #   indexImg = eviTransform(img).multiply(indexFlip);
    #   break;
    elif inx == 'TCB':
      indexImg = tc.select(['TCB'])#.multiply(indexFlip);
    elif inx == 'TCG':
      indexImg = tc.select(['TCG']).multiply(indexFlip)
    elif inx == 'TCW':
      indexImg = tc.select(['TCW']).multiply(indexFlip)
    elif inx == 'TCA':
      indexImg = tc.select(['TCA']).multiply(indexFlip)
    #  case 'NDFI':
    #   indexImg = ndfiTransform(img).multiply(indexFlip);
    #   break;
    # default:
    else: 
      print('The index you provided is not supported')

    return indexImg.set('system:time_start', img.get('system:time_start'))



def calc_bands(img,bandList): 
    allStack = calcIndex(img, bandList[0], 0)
    for band in range(len(bandList)): 

        bandImg = calcIndex(img, bandList[band], 0)
        allStack = allStack.addBands(bandImg)
    return allStack.set('system:time_start', img.get('system:time_start'))

def transformSRcollection(srCollection, bandList): 
    return srCollection.map(lambda x: calc_bands(x,bandList))
        
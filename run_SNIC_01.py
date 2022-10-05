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
# import params
import LandTrendr as ltgee
import ltop
print(ee.__version__)

# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
ee.Initialize()

##################################################/

#################### Composites ########################/
##################################################/
class RunSNIC(object): 
    '''
    Run the GEE SNIC algorithm in Python. There are still some hardcoded self.args in here, 
    mostly the years that we're going to use to run snic and the TC bands that could
    be changed to be user defined in the future. 
    See params.py and the docs for more information on the self.args that are passed.
    '''

    def __init__(self,*args): 
        self.args = args[0]
        
    def build_image_collection(self): 
        LandsatComposites=0
        if self.args.params["image_source"] == 'medoid':
            pass
            #note that this won't actually work unless we convert the buildSRcollection module in LandTrendr.js to Python
            # imageEnd = ltgee.buildSRcollection(2021, 2021, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()
            # imageMid = ltgee.buildSRcollection(2005, 2005, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()
            # imageStart = ltgee.buildSRcollection(1990, 1990, params.params["startDate"], params.params["endDate"], params.params["aoi"], params.params["masked"]).mosaic()

            # LandsatComposites = imageEnd.addBands(imageMid).addBands(imageStart)
        elif self.args.params["image_source"] != 'medoid':
            comps = ltop.buildSERVIRcompsIC(self.args.params['startYear'],self.args.params['endYear'])
            #TODO this transformSRcollection function needs to be moved to python 
            tc = ltgee.transformSRcollection(comps, ['tcb','tcg','tcw'])
        
            #TODO this could probably be wrapped into a list comprehension for brevity 
            #now make an image out of a start, mid and end point of the time series 
            image21 = tc.filter(ee.Filter.eq('system:index','2021')).first()
            image18 = tc.filter(ee.Filter.eq('system:index','2018')).first()
            image14 = tc.filter(ee.Filter.eq('system:index','2014')).first()
            image10 = tc.filter(ee.Filter.eq('system:index','2010')).first()
            image06 = tc.filter(ee.Filter.eq('system:index','2006')).first()
            image02 = tc.filter(ee.Filter.eq('system:index','2002')).first()
            image98 = tc.filter(ee.Filter.eq('system:index','1998')).first()
            image94 = tc.filter(ee.Filter.eq('system:index','1994')).first()
            image90 = tc.filter(ee.Filter.eq('system:index','1990')).first()

            LandsatComposites = image90.addBands(image94).addBands(image98).addBands(image02).addBands(image06).addBands(image10).addBands(image14).addBands(image18).addBands(image21); 
        return LandsatComposites

    # 1. run the snic algorithm 
    def generate_tasks(self): 
        LandsatComposites = self.build_image_collection()


        snic_output01 = ltop.snic01(LandsatComposites,self.args.params["aoi"],self.args.params["randomPts"],self.args.params["seedSpacing"])

        task = ee.batch.Export.table.toAsset(
                    collection= snic_output01.get(0),
                    description="LTOP_SNIC_pts_"+self.args.params["place"]+"_c2_"+str(self.args.params["randomPts"])+"_pts_"+str(self.args.params["startYear"]),
                    assetId= self.args.params["assetsRoot"]+self.args.params["assetsChild"]+"/LTOP_SNIC_pts_"+self.args.params["place"]+"_c2_"+str(self.args.params["randomPts"])+"_pts_"+str(self.args.params["startYear"]),
                    
        )

        task2 = ee.batch.Export.image.toAsset(
                    image= ee.Image(snic_output01.get(1)),
                    description="LTOP_SNIC_imagery_"+self.args.params["place"]+"_c2_"+str(self.args.params["randomPts"])+"_pts_"+str(self.args.params["startYear"]),
                    assetId=self.args.params["assetsRoot"]+self.args.params["assetsChild"]+"/LTOP_SNIC_imagery_"+self.args.params["place"]+"_c2_"+str(self.args.params["randomPts"])+"_pts_"+str(self.args.params["startYear"]),
                    region= self.args.params["aoi"],
                    scale=30,
                    maxPixels=10000000000000
        )

        task.start()
        task2.start()

        return task.status(), task2.status()
            




from run_ltop_complete import RunLTOPFull
# import params
import ee
import yaml



#TODO add the authorize and something to check that its been done 
# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
ee.Initialize()

'''
Example of one way to run the LTOP workflow for a number of different ROIs. This can also be run for just one ROI. 
'''

if __name__ == '__main__':

    grid = ee.FeatureCollection('projects/ee-ltop-py/assets/ltop_large_scale_runs/clipped_test_grid')
    grid_list = grid.toList(grid.size())

    for i in range(grid.size().getInfo()): 
        input_aoi = ee.Feature(grid_list.get(i)).geometry()
        #modify the params file inputs
        #TODO this is not a good way of doing this: 
 
        place = 'grid_'+ee.Number(ee.Feature(grid_list.get(i)).get('id')).format().getInfo()
        assetsRoot = 'projects/ee-ltop-py/assets/'
        assetsChild = 'LTOP_py_SERVIR_grid'

        params = {
            "place": place,
            "startYear": 1990,
            "endYear": 2021,
            "seedSpacing": 10,
            "randomPts": 20000,
            "imageSource": 'servir',
            "assetsRoot": assetsRoot,
            #the script is going to check if this folder exists and if it doesn't it will make it for you
            "assetsChild": assetsChild, 
            #note that whatever you use here needs to be cast as a geometry before running
            "aoi":input_aoi,#ee.FeatureCollection("USDOS/LSIB/2017").filter(ee.Filter.eq('COUNTRY_NA','Cambodia')).geometry(),
            # "aoi": geometry,#ee.FeatureCollection("projects/servir-mekong/hydrafloods/CountryBasinsBuffer").geometry(),
            "maxClusters": 2500,
            "minClusters": 2500,
            # this has to be uploaded from a local directory and changed https://code.earthengine.google.com/?asset=projects/ee-ltop-py/assets/LTOP_testing/abstract_images_grid_points
            # "abstract_image_pts": ee.FeatureCollection(),
            "selectedLTparams": ee.FeatureCollection(assetsRoot+assetsChild+'/'+'LTOP_'+place+'_selected_LT_params_tc'),
            "image_source": 'comp',
            #these should be local directories
            #this one will be created automatically if it does not exist 
            "param_scoring_inputs": f"/vol/v1/general_files/user_files/ben/LTOP_FTV_py_revised/output_04_{place}/",
            "outfile": f"/vol/v1/general_files/user_files/ben/LTOP_FTV_py_revised/selected_lt_params/LTOP_{place}_selected_LT_params_tc.csv",
            "njobs": 8, 
            #note that this must be set up in advance, the script will not do it for you!!
            "cloud_bucket":"ltop_assets_storage",

            # only needed for medoid composites
            "startDate":'11-20',
            "endDate": '03-10',
            "masked": ['cloud', 'shadow']
        }
                

        test = RunLTOPFull(params,max_time = 1200)
        test.runner()
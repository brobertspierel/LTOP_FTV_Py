#  ########################################################################################################
#  # #\\
#  # LandTrendr Optimization Paramater File                           #\\
#  # #\\
#  ########################################################################################################
import ee
# ee.Authenticate() #uncomment after testing
ee.Initialize()

#just use for testing 
geometry = ee.Geometry.Polygon(
        [[[104.89306074775232, 16.260851065722026],
          [104.89306074775232, 16.03924306136429],
          [105.25011641181482, 16.03924306136429],
          [105.25011641181482, 16.260851065722026]]])

#note that its important you set up the place and the imageSource in advance because this will determine
#your naming conventions going forward. 
params = {
    "version": '0.0.1',
    "place": 'servir_comps_revised',
    "startYear": 2015,
    "endYear": 2021,
    "seedSpacing": 10,
    "randomPts": 20000,
    "imageSource": 'servir',
    "assetsRoot": 'projects/ee-ltop-py/assets/',
    #TODO this is going to break if you try to pass a folder that doesn't exist
    "assetsChild": 'LTOP_testing', 
    "aoi": geometry,#ee.FeatureCollection("projects/servir-mekong/hydrafloods/CountryBasinsBuffer").geometry(),
    "maxClusters": 5000,
    "minClusters": 5000,
    # this has to be uploaded from a local directory and changed https://code.earthengine.google.com/?asset=projects/ee-ltop-py/assets/LTOP_testing/abstract_images_grid_points
    # "abstract_image_pts": ee.FeatureCollection(),
    "selectedLTparams": ee.FeatureCollection('users/ak_glaciers/servir_comps_revised_workflow/LTOP_servir_comps_revised_kmeans_pts_config_selected_for_GEE_upload_new_weights_gee_implementation'),
    "image_source": 'comp',
    # only needed for medoid composites
    "startDate":'11-20',
    "endDate": '03-10',
    "masked": ['cloud', 'shadow']
}
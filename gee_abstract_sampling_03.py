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

# GLOBAL IABLES
PRJ = "EPSG:3857"

'''
This script demonstrates how to generate a synthetic image in 
GEE alone without using the Python API or local downloads.

The demonstration consists of the following steps:
1. Generating an medoid time-series over a small area
2. Sampling the values from the medoid time series
3. Generating a synthetic image from the sampled values
4. Exporting the synthetic image as an asset along with the relevant point collections (original and grid)
'''

#add a new def to replace the random sample def TODO we don't actually need this in here because it can just reference another existing function in the modules 
def samplePts(pts,collection){
   img = collection.toBands() 
   output = pts.map(def(pt){
     value = img.reduceRegion({
    reducer:ee.Reducer.first(), 
    geometry:pt.geometry(),
    scale:30
    
    }) 
  return ee.Feature(pt.geometry(),value) 
  }) 
  return ee.FeatureCollection(output) 
}


# Add a sequential ID to a set of points
def add_sequential_id (cur, prev): 
  
    # Cast the inputs
    cur = ee.Feature(cur)
    prev = ee.List(prev)

    # Get the ID value from the previous feature
    prev_id = ee.Feature(prev.get(-1)).getNumber("GRID_ID")

    # Assign the new grid ID
    cur = cur.set("GRID_ID", prev_id.add(1).toInt64())

    return prev.add(cur)
  
  
# Generate a grid of points. Resolution and row length can be specified. 
def generate_point_grid (num_points, num_points, resolution): 
  
    # Starting coordinates
    x = resolution / 2
    y = resolution / 2

    # Create a grid with some number of points and with rows of some length
    grid = []
    for i in range(num_points):
        # Construct the point geometry
        pt_geo = ee.Geometry.Point([x, y], PRJ)

        # Construct the output feature the join property ID
        pt = ee.Feature(pt_geo, {"GRID_ID": i})

        # Increment the row position by the desired resolution
        x = x + resolution

        # Append to the grid
        grid = grid.append(pt) #this was previously concat, that should be a js convention which we can change to append? 


    # Cast the grid as a feature collection
    output = ee.FeatureCollection(grid).sort('GRID_ID')

    return output 

def loop_over_year(index,start_year,resolution,buffers): 
    
    # Cast the input
    index = ee.Number(index)

    # Get the relevant band values from the collection of points\
    index_str = ee.Number(start_year).add(index).toInt16().format()
    original_names = [
    index_str.cat('_NBR'), index_str.cat('_TCW'), index_str.cat('_TCG'),
    index_str.cat('_NDVI'), index_str.cat('_B5')
    ]
    new_names = ['NBR','TCW','TCG','NDVI','B5']
    current_props = buffers.select(original_names, new_names)

    # Construct the synthetic image
    b1 = ee.Image([0]).toInt16().paint(current_props, "NBR").reproject(PRJ, None, resolution).rename('NBR')
    b2 = ee.Image([0]).toInt16().paint(current_props, "TCW").reproject(PRJ, None, resolution).rename('TCW')
    b3 = ee.Image([0]).toInt16().paint(current_props, "TCG").reproject(PRJ, None, resolution).rename('TCG')
    b4 = ee.Image([0]).toInt16().paint(current_props, "NDVI").reproject(PRJ, None, resolution).rename('NDVI')
    b5 = ee.Image([0]).toInt16().paint(current_props, "B5").reproject(PRJ, None, resolution).rename('B5')
    #  b7 = ee.Image([0]).toInt16().paint(current_props, "B7").reproject(PRJ, null, resolution).rename('B7')
    synthetic = ee.Image.cat([b1, b2, b3, b4, b5]).rename(new_names)


    # Assign the metadata info
    metadate = ee.Date.fromYMD(ee.Number(start_year).add(index), 8, 1).millis()
    synthetic = synthetic.set('system:time_start', metadate)

    return synthetic

def buffer_func(feat) { #TODO convert this to lambda 
    return ee.Feature(feat).buffer(resolution / 2, error, PRJ).bounds(error, PRJ)
    })

# Unpack the join results 
def unpack_inner_join_output (feature):
    # Cast and unpack
    feature = ee.Feature(feature)
    grid_pt = ee.Feature(feature.get('primary'))
    sample_pt = ee.Feature(feature.get('secondary'))

    return grid_pt.copyProperties(sample_pt)

# Genenerate a time-series of synthetic images
def generate_synethetic_collection (point_grid, samples, start_year, end_year, resolution): 
  
    # Cast the two inputs
    point_grid = ee.FeatureCollection(point_grid)
    samples = ee.FeatureCollection(samples)

    # Join the two collections togeheter using the GRID_ID property
    join_filter = ee.Filter.equals({leftField: 'GRID_ID', rightField: 'GRID_ID'})
    join_opperator = ee.Join.inner('primary', 'secondary')
    joined = join_opperator.apply(point_grid, samples, join_filter)

    # Unpack the join results
    grid_with_spectral = joined.map(lambda x: unpack_inner_join_output(x))

    # Buffer the desired properties into squares
    error = ee.ErrorMargin(1, 'projected')
    buffers = grid_with_spectral.map(def(feat) { #TODO convert this to lambda 
    return ee.Feature(feat).buffer(resolution / 2, error, PRJ).bounds(error, PRJ)
    })
  
  # Loop over each year and construct the synthetic image
  

    synthetic_images = ee.ImageCollection.fromImages(
    ee.List.sequence(0, (end_year - start_year)).map(lambda x: loop_over_year(x,start_year,resolution,buffers)) #TODO convert this - the loop_over_year func needs (index,start_year,resolution,buffers): 
    )
  
    return synthetic_images, grid_with_spectral, samples
  



  

#this needs to be renamed 
def generate_abstract_images(kmeans_pts,aoi,assets_folder,grid_res,start_year,end_year):
    
    #make sure the stratified points from kmeans are cast to a featureCollection 
    kmeans_pts = ee.FeatureCollection(kmeans_pts)

    # Specify the number of points to be extracted
    num_points = kmeans_pts.size().getInfo()

    ##/ Code ##

    # TODO Generate a time-series from servir composites - this could also be passed as an arg? 
    sr_collection = ltop.buildSERVIRcompsIC(start_year,end_year) 

    # Unmask the values int the original collection with some unique value - TODO not entirely clear if we need this 
    # sr_collection = sr_collection.map(def (img) { 
    # return ee.Image(img).unmask(-9999, false)
    # })

    # Get the random point locations from which spectral values will be extracted - change to the kmeans stratified random points 
    sample_list = samplePts(pts,sr_collection).toList(num_points)

    print(sample_list.slice(0))

    # Add a sequential ID to the samples
    seed_object = ee.List([ee.Feature(null, {"GRID_ID": -1})])
    samples = ee.FeatureCollection(
    ee.List(sample_list.iterate(add_sequential_id, seed_object)).slice(1)
    )
    print('samples',samples)
    # Generate the grid of points 
    point_grid = generate_point_grid(num_points, num_points, grid_res)
    Map.addLayer(point_grid,{},'point grid')
    print(point_grid)
    # Generate the synthetic image
    outputs = generate_synethetic_collection(point_grid, samples, start_year, end_year, grid_res)
    synthetic_collection = outputs[0]
    print(synthetic_collection.first())
    grid_points = outputs[1]
    sample_locations = outputs[2]

    # Export the synthetic collection to an output collection
    export_geometry = point_grid.geometry().bounds(ee.ErrorMargin(1e-3, 'projected'), PRJ)
    for ( cur_year = start_year cur_year <= end_year cur_year++) {

    # Filter the collection to get the image
        start_date = ee.Date.fromYMD(cur_year, 1, 1)
        end_date = ee.Date.fromYMD(cur_year, 12, 31)
        synthetic_image = ee.Image(synthetic_collection.filterDate(start_date, end_date).first())
    print('synthetic', synthetic_image)
    # Export the image
        Export.image.toAsset({
        image: synthetic_image, 
        description: "Asset-Synth-" + cur_year.toString(), 
        assetId: output_collection + "synthetic_" + cur_year.toString(), 
        region: export_geometry,
        scale: grid_res, 
        crs: PRJ, 
        maxPixels: 1e13
        })
    
  }
  
  # Export the original point locations
  Export.table.toAsset({
    collection: grid_points ,
    description: "Asset-GridPoints", 
    assetId: assets_folder + "grid_points"
  })
   
  # Export the grid locations
  Export.table.toAsset({
    collection: sample_locations ,
    description: "Asset-SampleLocations", 
    assetId: assets_folder + "sample_locations"
  })
  
  # Visualize stuff
  # Map.addLayer(sr_collection, {min:0, max:1500}, "Medoids", false)
  # Map.addLayer(samples, {color:'red'}, "samples", false)
  # Map.addLayer(synthetic_collection, {min:0, max:[2250, 5500, 1500], bands:['B7','B4','B3']}, "Synthetic")
  # Map.addLayer(point_grid, {color:'red'}, "point_grid", false)
  # Map.centerObject(point_grid, 18)
  
  return null
  
}

# Extract a random sample from a time-series
# def extract_random_sample (collection, num_points, roi) {
  
#   # Convert the image collection into a single image
#    image_to_sample = collection.toBands()
  
#   # Get the random samples
#    samples = image_to_sample.sample({
#     region: roi, 
#     scale: 30, 
#     projection: PRJ, 
#     numPixels: num_points, 
#     dropNulls: true,
#     geometries: true
#   })
  
#   return samples
  
# }



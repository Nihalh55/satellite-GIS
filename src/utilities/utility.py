import ee, os, geemap, geetools, time

# 1. USGS/SRTMGL1_003                       -> elevation                https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003#bands
# 2. NASA/ASTER_GED/AG100_003               -> elevation, LST, NDVI     https://developers.google.com/earth-engine/datasets/catalog/NASA_ASTER_GED_AG100_003 
# 3. HYCOM/sea_surface_elevation            -> surface_elevation        https://developers.google.com/earth-engine/datasets/catalog/HYCOM_sea_surface_elevation
# 4. CSP/ERGo/1_0/Global/SRTM_topoDiversity -> constant                 https://developers.google.com/earth-engine/datasets/catalog/CSP_ERGo_1_0_Global_SRTM_topoDiversity


class Utility():

    # Function Definition -> Save image to drive
    def saveToDrive(self, fileName, folderName, image, isImageCollection):
        task_config_image = {
            "description": fileName,
            'fileFormat': 'GeoTIFF',
            "dimensions":720,
            "maxPixels":1e12,
            'folder': folderName
        }
        task_config_imagecollection = {
            "collection": image,
            'fileFormat': 'GeoTIFF',
            "maxPixels": 1e12,
            'folder': folderName
        }
        if isImageCollection == True:
            print("Starting export of image collection!")
            tasks   = geetools.batch.Export.imagecollection.toDrive(**task_config_imagecollection)
            print("Number of tasks: " + str(len(tasks)))
        else:
            print("Starting export of image!")
            task    = ee.batch.Export.image.toDrive(image, **task_config_image)
            task.start()

    # Function Definition -> Clip the image by a shape file
    def clipByShape(self, image, shapeName, isImageCollection):
        shape           = geemap.shp_to_ee("uploads\\"+shapeName+".shp")
        def algo(image):
            return image.clipToBoundsAndScale(shape)
        if isImageCollection:
            clippedImage = image.map(algorithm=algo)
        else:
            clippedImage    = algo(image)
        return clippedImage	

    # Function Definition -> Load dataset from satellite
    def loadSatelliteDataset(self, satelliteName, filterDate1, filterDate2):
        if satelliteName == "HYCOM/sea_surface_elevation":
            dataset = ee.ImageCollection(satelliteName).filter(ee.Filter.date(filterDate1, filterDate2))
        else:
            dataset = ee.Image(satelliteName)
        return dataset

    # Function Definition -> Get information from bands in dataset
    def getInformation(self, dataset, typeOfData, satelliteName):
        if typeOfData == 'Elevation':
            elevation   = dataset.select('elevation')
            res         = ee.Terrain.slope(elevation)

        elif typeOfData == 'LST' and satelliteName == "NASA/ASTER_GED/AG100_003":
            res     = dataset.select('temperature')
            res     = ee.Image.constant(ee.Number(0.01)).multiply(res)

        elif typeOfData == 'NDVI' and satelliteName == "NASA/ASTER_GED/AG100_003":
            res     = dataset.select('ndvi')
            res     = ee.Image.constant(ee.Number(0.01)).multiply(res)

        elif typeOfData == 'seaSurfaceElevation':
            res     = dataset.select('surface_elevation')
            def algo(image):
                return ee.Image.constant(ee.Number(0.001)).multiply(image)
            res     = res.map(algorithm=algo)

        elif typeOfData == 'topographicDiversity':
            res     = dataset.select('constant')

        else:
            res     = None
        return res
    
    


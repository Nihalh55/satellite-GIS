import ee, os, geemap

class Utility():
    
    
    # Function Definition -> Save image to drive
    def saveImageToDrive(self, fileName, folderName, image):
        task_config = {
            "description": fileName,
            'fileFormat': 'GeoTIFF',
            "dimensions":720,
            "maxPixels":1e12,
            'folder': folderName
        }
        task        = ee.batch.Export.image.toDrive(image, **task_config)
        task.start()

    # Function Definition -> Load dataset from SRTM satellites
    # 1. USGS/SRTMGL1_003                       -> elevation                https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003#bands
    # 2. NASA/ASTER_GED/AG100_003               -> elevation, LST, NDVI     https://developers.google.com/earth-engine/datasets/catalog/NASA_ASTER_GED_AG100_003 
    # 3. TODO: FIX THIS - >HYCOM/sea_surface_elevation            -> surface_elevation        https://developers.google.com/earth-engine/datasets/catalog/HYCOM_sea_surface_elevation
    # 4. CSP/ERGo/1_0/Global/SRTM_topoDiversity -> constant                 https://developers.google.com/earth-engine/datasets/catalog/CSP_ERGo_1_0_Global_SRTM_topoDiversity
    def loadSatelliteDataset(self, satelliteName):
        dataset = ee.Image(satelliteName)
        return dataset

    # Function Definition -> Get information from bands in dataset
    # TODO: Calculate LST and NDVI
    def getInformation(self, dataset, typeOfData):
        if typeOfData == 'Elevation':
            elevation = dataset.select('elevation')
            res     = ee.Terrain.slope(elevation)
        elif typeOfData == 'LST':
            res     = dataset.select('temperature')
        elif typeOfData == 'NDVI':
            res     = dataset.select('ndvi')
        elif typeOfData == 'seaSurfaceElevation':
            res     = dataset.select('surface_elevation')
        elif typeOfData == 'topographicDiversity':
            res     = dataset.select('constant')
        else:
            res     = None
        return res
    
    # Function Definition -> Clip the image by a shape file
    def clipImageByShape(self, image, shapeName):
        shape           = geemap.shp_to_ee("uploads\\"+shapeName+".shp")
        clippedImage    = image.clipToBoundsAndScale(shape)
        return clippedImage	


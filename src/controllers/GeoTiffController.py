import ee, logging, zipfile
from utilities.utility import Utility
from flask import jsonify

utilityHelper = Utility()

class GeoTIFF():

    # Function Definition -> Is dataset an ImageCollection
    def isDatasetImageCollection(self, satelliteName):
        imageCollectionSatelliteList = ["HYCOM/sea_surface_elevation", "TRMM/3B42", "TRMM/3B43V7", "MODIS/006/MOD11A1", "LANDSAT/LC08/C01/T1_8DAY_NDVI", "MODIS/006/MOD13A2"]
        return (satelliteName in imageCollectionSatelliteList)

    # Function Definition -> Unzip file 
    def unzipShapeFile(self, shapeFileName):
        with zipfile.ZipFile("uploads\\"+shapeFileName, 'r') as zip_ref:
            zip_ref.extractall("uploads")

    # Function Definition -> Get TIFF file based on configuration
    def getGeoTiffFile(self, configuration):
        try:
            self.unzipShapeFile(configuration["shapeFileName"])
            isImageCollection   = self.isDatasetImageCollection(configuration["satelliteName"])
            dataset             = utilityHelper.loadSatelliteDataset(configuration["satelliteName"], configuration["temporalInfo1"], configuration["temporalInfo2"], isImageCollection)
            image               = utilityHelper.getInformation(dataset, configuration["typeOfData"], configuration["satelliteName"])
            if image == None:
                return {"message":"Error. Resend Configuration!"} , 400
            image               = utilityHelper.clipByShape(image, configuration["shapeName"], isImageCollection)
            utilityHelper.saveToDrive(configuration["fileName"], configuration["folderName"], image, isImageCollection)
            return {"message":"Check your Google Drive for the TIF file!"} , 200
        except Exception as e:
            logging.error(e)
            return {"message":"Error. Resend Configuration! If you are sending Image collection try a different range"} , 400

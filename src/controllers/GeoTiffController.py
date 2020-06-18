import ee, logging, zipfile
from utilities.utility import Utility
from flask import jsonify

utilityHelper = Utility()

class GeoTIFF():

    # Function Definition -> Unzip file 
    def unzipShapeFile(self, shapeFileName):
        with zipfile.ZipFile("uploads\\"+shapeFileName, 'r') as zip_ref:
            zip_ref.extractall("uploads")

    # Function Definition -> Get TIFF file based on configuration
    def getGeoTiffFile(self, configuration):
        try:
            isImageCollection = (configuration["satelliteName"] == "HYCOM/sea_surface_elevation")
            self.unzipShapeFile(configuration["shapeFileName"])
            dataset = utilityHelper.loadSatelliteDataset(configuration["satelliteName"], configuration["temporalInfo1"], configuration["temporalInfo2"])
            image   = utilityHelper.getInformation(dataset, configuration["typeOfData"], configuration["satelliteName"])
            if image == None:
                return {"message":"Error. Resend Configuration!"} , 400
            image   = utilityHelper.clipByShape(image, configuration["shapeName"], isImageCollection)
            utilityHelper.saveToDrive(configuration["fileName"], configuration["folderName"], image, isImageCollection)
            return {"message":"Check your Google Drive for the TIF file!"} , 200
        except Exception as e:
            logging.error(e)
            return {"message":"Error. Resend Configuration!"} , 400

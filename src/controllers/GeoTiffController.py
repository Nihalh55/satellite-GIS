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
            self.unzipShapeFile(configuration["shapeFileName"])
            dataset = utilityHelper.loadSatelliteDataset(configuration["satelliteName"])
            image   = utilityHelper.getInformation(dataset, configuration["typeOfData"])
            image   = utilityHelper.clipImageByShape(image, configuration["shapeName"])
            utilityHelper.saveImageToDrive(configuration["fileName"], configuration["folderName"], image)
            return {"message":"Check your Google Drive for the TIF file!"} , 200
        except Exception as e:
            logging.error(e)
            return {"message":"Error. Resend Configuration!"} , 400

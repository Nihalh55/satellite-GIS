import ee
from utilities.utility import Utility
from flask import jsonify
utilityHelper = Utility()

class GeoTIFF():
    
    # Function Definition -> Get TIFF file based on configuration
    def getGeoTiffFile(self, configuration):
        try:
            dataset = utilityHelper.loadSatelliteDataset(configuration["satelliteName"])
            image   = utilityHelper.getInformation(dataset, configuration["typeOfData"])
            if configuration["isShapeFileUsed"] == False:
                image   = utilityHelper.clipByBounds(image, configuration["coordinates"])
            else:
                image   = utilityHelper.clipImageByShape(image, configuration["shapeName"])
            #TODO : Use formulae
            utilityHelper.saveImageToDrive(configuration["fileName"], configuration["folderName"], image)
            return jsonify({"message":"Sucess"}) , 200
        except Exception as e:
            return jsonify({"message":e}) , 400

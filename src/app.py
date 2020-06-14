from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.GeoTiffController import GeoTIFF
import ee

ee.Initialize()
app = Flask(__name__)
CORS(app)
geoTiffHelper = GeoTIFF()

# ROUTES
# Route Definition -> Generate Geo Tiff file based on configuration provided
@app.route('/get-geotiff', methods=['POST'])
def getGeoTiff():
    body    = request.get_json() 
    return geoTiffHelper.getGeoTiffFile(body["configuration"])
    
# RUN
if __name__ == '__main__':
    app.run()

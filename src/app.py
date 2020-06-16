from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_cors import CORS
from controllers.GeoTiffController import GeoTIFF
from werkzeug.utils import secure_filename
import ee, logging, os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'zip'}

ee.Initialize()
app = Flask(__name__)
app.secret_key = "ACb12F3niJhklTg56ZDbdKbWnOdi"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
geoTiffHelper = GeoTIFF()


#---------------------------------------------------------------------------------------------
#                                   FUNCTIONS
#---------------------------------------------------------------------------------------------

# Function Defintion -> Check if it is an allowed file type to be saved
def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

# Function Defintion -> Save shape file
def saveFile(fileNameAttr):
    if fileNameAttr not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files[fileNameAttr]
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        f = open("uploads\\" + file.filename.split(".")[0], "wb")
        f.write(file.read())
        return file.filename.split(".")[0]

#---------------------------------------------------------------------------------------------
#                                    ROUTES
#---------------------------------------------------------------------------------------------

# Route Definition -> Get index page
@app.route('/', methods=['GET'])
def getIndex():
    return render_template('index.html')

# Route Definition -> Generate Geo Tiff file based on configuration provided
@app.route('/get-geotiff', methods=['POST'])
def getGeoTiff():
    configuration                   = {}
    configuration["shapeName"]      = request.form['shapeName']
    configuration["shapeFileName"]  = saveFile('file')
    configuration["satelliteName"]  = request.form['satelliteName']
    configuration["typeOfData"]     = request.form['typeOfData']
    configuration["fileName"]       = request.form['fileName']
    configuration["folderName"]     = request.form['folderName']
    response                        = geoTiffHelper.getGeoTiffFile(configuration)
    logging.debug(response)
    flash(response[0]["message"])
    return render_template('index.html')
    
# RUN
if __name__ == '__main__':
    app.run()

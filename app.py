from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#ROUTES
@app.route('/first', methods=['POST'])
def example():
    pass

# RUN
if __name__ == '__main__':
    app.run()

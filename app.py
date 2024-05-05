import cv2
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
from detect import Detect
import base64
from flask_cors import CORS
from io import BytesIO
import os
import requests

app = Flask(__name__)
CORS(app)

dt = Detect()

@app.route('/detect', methods=['POST'])
def predict():
    file = request.files['image']
    plant_detected = dt.detect(file)
    return jsonify({"plant_detected": plant_detected})

if __name__ == '__main__':
    # dt = Detect()
    # app.run(port=5000, debug=True)
    app.run(host='0.0.0.0', debug=True)






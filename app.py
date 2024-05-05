import cv2
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
from detect import Detect
import base64
from flask_cors import CORS
from io import BytesIO
import os
import requests

# app = Flask(__name__)
# CORS(app)
#
#
# @app.route('/detect', methods=['POST'])
# def predict():
#     file = request.files['image']
#     plant_detected = dt.detect(file)
#     return jsonify({"plant_detected": plant_detected})
#
# if __name__ == '__main__':
#     dt = Detect()
#     # app.run(port=5000, debug=True)
#     app.run(host='0.0.0.0', debug=True)

from socketio import Client
from detect import Detect

class DetectClient(Client):
    def __init__(self):
        super().__init__()

    def on_image(self, image_data):
        # Detect the plant in the image
        plant_detected = dt.detect(image_data)

        # Emit the detected plant data back to the server
        self.emit('image', plant_detected)
        return plant_detected

if __name__ == "__main__":
    dt = Detect()

    # Kết nối tới server
    client = DetectClient()
    client.connect('http://localhost:3000')

    client.on('image', client.on_image)

    # Bắt đầu lắng nghe sự kiện từ server
    client.wait()





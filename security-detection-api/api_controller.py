import os
import config
import cv2
import numpy as np
import json
import base64
import face_recognition_service
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def info():
    if request.method == 'GET':
        return "Security-detection-api is running"


@app.route('/persons', methods=['GET'])
def submit_name():
    if request.method == 'GET':
        name = request.args['name'].lower()
        if name not in os.listdir(config.data_dir):
            return "FOUND"
        return "NOT_FOUND"


@app.route('/persons/photos', methods=['POST'])
def submit_photos():
    if request.method == 'POST':
        name = request.form['name'].lower()
        images = json.loads(request.form['images'])

        os.mkdir(os.path.join(config.data_dir, str(name)))

        person_directory = os.path.join(config.data_dir, name)
        for i, image in enumerate(images):
            image_numpy = np.fromstring(base64.b64decode(image.split(",")[1]), np.uint8)
            image = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)
            cv2.imwrite(os.path.join(person_directory, str(i) + '.png'), image)

        face_recognition_service.generate_dataset_festures()

        return "results"


@app.route("/persons/predictions", methods=['POST'])
def predict_frame():
    if request.method == 'POST':
        image = request.form['image']
        image_numpy = np.fromstring(base64.b64decode(image.split(",")[1]), np.uint8)
        image = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)

        image = face_recognition_service.predict_people(image)

        retval, buffer = cv2.imencode('.png', image)
        img_as_text = base64.b64encode(buffer)

        return img_as_text


if __name__ == "__main__":
    app.run(debug=False, port=config.web_app_port)

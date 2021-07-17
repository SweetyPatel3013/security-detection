import os
import config
import cv2
import numpy as np
import json
import base64
from facerecognition.tensorflow.FaceRecognitionTensorFlow import FaceRecognitionTensorFlow
from facerecognition.dlib.FaceRecognitionDlib import FaceRecognitionDlib
from flask import Flask, request
from flask_cors import CORS
from movementdetection.MovementDetector import MovementDetector

app = Flask(__name__)
CORS(app)

if config.face_recognition_type == 'DLIB':
    face_recognition_service = FaceRecognitionDlib()
else:
    face_recognition_service = FaceRecognitionTensorFlow()


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
        person_photos = []
        for i, image in enumerate(images):
            image_numpy = np.fromstring(base64.b64decode(image.split(",")[1]), np.uint8)
            image = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)
            cv2.imwrite(os.path.join(person_directory, str(i) + '.png'), image)
            person_photos.append(image)

        face_recognition_service.add_person_face(name, person_photos)
        return "results"


@app.route("/persons/predictions", methods=['POST'])
def predict_frame():
    if request.method == 'POST':
        image = request.form['image']
        image_numpy = np.fromstring(base64.b64decode(image.split(",")[1]), np.uint8)
        image = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)

        image_response = face_recognition_service.detect_faces_from_img(image)

        if image_response is None:
            retval, buffer = cv2.imencode('.png', image)
            return base64.b64encode(buffer)

        retval, buffer = cv2.imencode('.png', image_response)
        img_as_text = base64.b64encode(buffer)

        return img_as_text


@app.route("/movements", methods=['POST'])
def detect_movement():
    if request.method == 'POST':
        image_a = request.form['image_a']
        image_b = request.form['image_b']

        image_a = __decode_img(image_a)
        image_b = __decode_img(image_b)

        image_response = MovementDetector.detect(image_a, image_b)
        if image_response is None:
            retval, buffer = cv2.imencode('.png', image_a)
            return base64.b64encode(buffer)

        retval, buffer = cv2.imencode('.png', image_response)
        img_as_text = base64.b64encode(buffer)

        return img_as_text


def __decode_img(img):
    image_numpy = np.fromstring(base64.b64decode(img.split(",")[1]), np.uint8)
    return cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)

if __name__ == "__main__":
    app.run(debug=False, port=config.web_app_port)

import os
import cv2
import dlib
import pickle
import config
import numpy as np
import tensorflow as tf
from imutils import face_utils
from facerecognition.tensorflow.siameseNetwork import get_siamese_model, preprocess_input
from facerecognition.FaceRecognitionService import FaceRecognitionService


class _Persons:
    def __init__(self):
        self.names = []
        self.features = []

    def add(self, name: str, features):
        self.names.append(name)
        self.features.append(features)


class FaceRecognitionTensorFlow(FaceRecognitionService):

    def __init__(self):
        self.model = get_siamese_model()
        self.face_detector = dlib.get_frontal_face_detector()
        self.persons = _Persons()
        self.dumpable_features = self.__load_dataset_feature()

    def add_person_face(self, person_name: str, images: []):
        if person_name not in self.persons.names:
            try:
                nparr = self.__generate_image_features(images)
                self.persons.add(person_name, nparr)
                self.dumpable_features[person_name] = nparr
            except Exception as exception:
                print(exception)

    def detect_faces_from_img(self, image):
        name = 'not known'
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.face_detector(gray, 0)
        for face in faces:
            face_bounding_box = face_utils.rect_to_bb(face)
            if all(i >= 0 for i in face_bounding_box):
                [x, y, w, h] = face_bounding_box
                frame = image[y:y + h, x:x + w]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.resize(frame, (224, 224))
                frame = np.asarray(frame, dtype=np.float64)
                frame = np.expand_dims(frame, axis=0)
                frame = preprocess_input(frame)
                feature = self.model.get_features(frame)

                dist = tf.norm(self.persons.features - feature, axis=1)
                name = 'not known'
                loc = tf.argmin(dist)
                if dist[loc] < 0.8:
                    name = self.persons.names[loc]

                font_face = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, name, (x, y - 5), font_face, 0.8, (0, 0, 255), 3)
        return image

    def __load_dataset_feature(self):
        dumpable_features = {}
        pickle_file = os.path.join(config.feature_dir, 'weights.pkl')
        if os.path.isfile(pickle_file):
            dumpable_features = self.__load_pickle_file(pickle_file)
        self.__dump_pickle_file(pickle_file, dumpable_features)
        print("Model Dumpped !!")
        return dumpable_features

    def __generate_image_features(self, images: []):
        tmp_images = []
        for image in images:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector(gray, 0)
            if len(faces) == 0:
                continue
            for face in [faces[0]]:
                face_bounding_box = face_utils.rect_to_bb(face)
                if all(i >= 0 for i in face_bounding_box):
                    [x, y, w, h] = face_bounding_box
                    frame = image[y:y + h, x:x + w]
                    frame = cv2.resize(frame, (224, 224))
                    frame = np.asarray(frame, dtype=np.float64)
                    tmp_images.append(frame)
        tmp_images = np.asarray(tmp_images)
        tmp_images = preprocess_input(tmp_images)
        tmp_images = tf.convert_to_tensor(tmp_images)
        feature = self.model.get_features(tmp_images)
        feature = tf.reduce_mean(feature, axis=0)
        return feature

    def __load_pickle_file(self, pickle_file):
        dumpable_features = {}
        with open(pickle_file, 'rb') as f:
            dumpable_features = pickle.load(f)
        for key, value in dumpable_features.items():
            self.persons.add(key, value)
        return dumpable_features

    def __dump_pickle_file(self, pickle_file, dumpable_features):
        if len(list(dumpable_features.keys())) > 0:
            with open(pickle_file, 'wb') as f:
                pickle.dump(dumpable_features, f)

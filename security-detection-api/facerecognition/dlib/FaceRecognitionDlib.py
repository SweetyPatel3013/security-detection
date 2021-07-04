import cv2
import face_recognition
from facerecognition.FaceRecognitionService import FaceRecognitionService


class FaceRecognitionDlib(FaceRecognitionService):
    IS_FACE_RECOGNITION_ENABLED = True

    def __init__(self):
        self.persons = []

    def add_person_face(self, person_name: str, images: []):
        face_encodings = []
        for img in images:
            face_encoding = self.__encode_face_from_img(img)
            face_encodings.append(face_encoding)
        person = {
            'name': person_name,
            'face_encodings': face_encodings
        }
        self.persons.append(person)

    def detect_faces_from_img(self, image):
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='hog')
        all_face_encodings = face_recognition.face_encodings(image, face_locations)
        return self.__recognize_faces(image, face_locations, all_face_encodings)

    def __encode_face_from_img(self, image):
        if image is None:
            return None
        face_encoding = face_recognition.face_encodings(image)[0]
        return face_encoding

    def __recognize_faces(self, current_frame, face_locations, face_encoding, scale=1):
        for current_face_location, current_face_encoding in zip(face_locations, face_encoding):
            top_pos, right_pos, bottom_pos, left_pos = current_face_location
            top_pos = top_pos * scale
            right_pos = right_pos * scale
            bottom_pos = bottom_pos * scale
            left_pos = left_pos * scale
            name = 'Unknown face'
            for person in self.persons:
                known_face_encoding = person.get('face_encodings', None)
                if known_face_encoding is None:
                    continue
                all_matches = face_recognition.compare_faces(known_face_encoding, current_face_encoding)
                if True in all_matches:
                    name = person.get('name')
                    break
            cv2.rectangle(current_frame, (left_pos, top_pos), (right_pos, bottom_pos), (255, 0, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(current_frame, name, (left_pos, bottom_pos), font, 0.5, (255, 255, 255), 1)
        return current_frame

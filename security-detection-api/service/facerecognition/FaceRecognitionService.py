from abc import ABC, abstractmethod


class FaceRecognitionService(ABC):

    @abstractmethod
    def add_person_face(self, person_name: str, images: []):
        pass

    @abstractmethod
    def detect_faces_from_img(self, image):
        pass

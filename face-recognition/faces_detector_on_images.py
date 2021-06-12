import cv2
import dlib
import face_recognition

print(cv2.__version__)
print(dlib.__version__)
print(face_recognition.__version__)


def detect_number_faces(image):
    all_faces = face_recognition.face_locations(image, model='hog')
    return all_faces


def print_out_face_location(faces_locations):
    for index, current_face_location in enumerate(faces_locations):
        top_pos, right_pos, bottom_pos, left_pos = current_face_location
        print(f'Found face {index + 1} at top: {top_pos}, right: {right_pos}, bottom: {bottom_pos}, left: {left_pos}')


def detect_faces_from_image(image_path: str):
    image_to_detect = cv2.imread(image_path)
    all_faces_locations = detect_number_faces(image_to_detect)
    print(f'There are {len(all_faces_locations)} # of faces in the image')
    print_out_face_location(all_faces_locations)


if __name__ == '__main__':
    detect_faces_from_image('images/trump_biden.jpeg')

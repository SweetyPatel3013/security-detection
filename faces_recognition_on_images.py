import cv2
import face_recognition

#TARGET_IMAGE = 'images/samples/trump-and-biden.jpeg'
#TARGET_IMAGE = 'images/samples/many-trump-biden.jpeg'
TARGET_IMAGE = 'images/samples/trump-and-others.jpeg'

trump = {
    'name': 'Donald Trump',
    'image': 'images/samples/trump-sample.jpeg'
}

biden = {
    'name': 'Biden',
    'image': 'images/samples/biden.jpeg'
}


def encode_faces(faces_info):
    faces_encoding = []
    face_names = []
    for face in faces_info:
        image_loaded = face_recognition.load_image_file(face['image'])
        face_encodings = face_recognition.face_encodings(image_loaded)[0]
        faces_encoding.append(face_encodings)
        face_names.append(face['name'])
    return faces_encoding, face_names


def recognize_faces(immutable_image, image_to_recognize):
    all_face_locations = face_recognition.face_locations(image_to_recognize, model='hog')
    all_face_encodings = face_recognition.face_encodings(image_to_recognize, all_face_locations)
    print('There are {} of faces in the image'.format(len(all_face_locations)))
    for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encodings):
        top_pos, right_pos, bottom_pos, left_pos = current_face_location
        print(f'Found face at top: {top_pos}, right: {right_pos}, bottom: {bottom_pos}, left: {left_pos}')
        all_matches = face_recognition.compare_faces(known_face_encoding, current_face_encoding)
        name = 'Unknown face'
        if True in all_matches:
            first_match_index = all_matches.index(True)
            name = known_face_names[first_match_index]
        cv2.rectangle(immutable_image, (left_pos, top_pos), (right_pos, bottom_pos), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(immutable_image, name, (left_pos, bottom_pos), font, 0.5, (255, 255, 255), 1)
    cv2.imshow('Faces identified', immutable_image)
    cv2.waitKey()


faces = [trump, biden]
known_face_encoding, known_face_names = encode_faces(faces)
original_image = cv2.imread(TARGET_IMAGE)
image = face_recognition.load_image_file(TARGET_IMAGE)
recognize_faces(original_image, image)

import cv2
import dlib
import face_recognition

print(cv2.__version__)
print(dlib.__version__)
print(face_recognition.__version__)

IS_FACE_RECOGNITION_ENABLED = True

trump = {
    'name': 'Donald Trump',
    'image': 'images/samples/trump-sample.jpeg'
}

biden = {
    'name': 'Biden',
    'image': 'images/samples/biden.jpeg'
}

milo = {
    'name': 'Camilo Espitia',
    'image': 'images/samples/Milo.png'
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


class FramePositions:
    def __init__(self, frame, top, bottom, right, left):
        self.frame = frame
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left


def detect_face(current_frame, faces_locations, scale=1):
    for index, current_face_location in enumerate(faces_locations):
        top_pos, right_pos, bottom_pos, left_pos = current_face_location
        top_pos = top_pos * scale
        right_pos = right_pos * scale
        bottom_pos = bottom_pos * scale
        left_pos = left_pos * scale
        print(f'Found face {index + 1} at top: {top_pos}, right: {right_pos}, bottom: {bottom_pos}, left: {left_pos}')
        current_frame_positions = FramePositions(current_frame, top_pos, bottom_pos, right_pos, left_pos)
        draw_rectangle_on_face(current_frame_positions)


def draw_rectangle_on_face(frame_positions: FramePositions):
    color_rectangle = (255, 192, 255)
    cv2.rectangle(frame_positions.frame,
                  (frame_positions.left, frame_positions.top),
                  (frame_positions.right, frame_positions.bottom),
                  color_rectangle, 2)


def release_webcam(webcam_video_stream):
    webcam_video_stream.release()
    cv2.destroyAllWindows()


def is_key_stop():
    return cv2.waitKey(1) & 0xFF == ord('q')


def recognize_faces(current_frame, face_locations, face_encoding, scale=1):
    print('There are {} of faces in the image'.format(len(face_locations)))
    for current_face_location, current_face_encoding in zip(face_locations, face_encoding):
        top_pos, right_pos, bottom_pos, left_pos = current_face_location
        top_pos = top_pos * scale
        right_pos = right_pos * scale
        bottom_pos = bottom_pos * scale
        left_pos = left_pos * scale
        print(f'Found face at top: {top_pos}, right: {right_pos}, bottom: {bottom_pos}, left: {left_pos}')
        all_matches = face_recognition.compare_faces(known_face_encoding, current_face_encoding)
        name = 'Unknown face'
        if True in all_matches:
            first_match_index = all_matches.index(True)
            name = known_face_names[first_match_index]
        cv2.rectangle(current_frame, (left_pos, top_pos), (right_pos, bottom_pos), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(current_frame, name, (left_pos, bottom_pos), font, 0.5, (255, 255, 255), 1)


def detect_faces_from(familiar_faces, source=0):
    webcam_video_stream = cv2.VideoCapture(source)
    while True:
        ret, current_frame = webcam_video_stream.read()
        current_frame_small = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(current_frame_small, number_of_times_to_upsample=3, model='cnn')
        #face_locations = face_recognition.face_locations(current_frame_small, number_of_times_to_upsample=1, model='hog')
        all_face_encodings = face_recognition.face_encodings(current_frame_small, face_locations)
        if IS_FACE_RECOGNITION_ENABLED:
            recognize_faces(current_frame, face_locations, all_face_encodings, scale=4)
        else:
            detect_face(current_frame, face_locations, scale=4)
        cv2.imshow("Webcam video", current_frame)
        if is_key_stop():
            release_webcam(webcam_video_stream)
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webcam = 0
    video = 'videos/any_video.mp4'
    faces = [trump, biden, milo]
    known_face_encoding, known_face_names = encode_faces(faces)
    detect_faces_from(webcam)

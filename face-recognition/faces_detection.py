import cv2
import dlib
import face_recognition

print(cv2.__version__)
print(dlib.__version__)
print(face_recognition.__version__)


class FramePositions:
    def __init__(self, frame, top, bottom, right, left):
        self.frame = frame
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left


def print_out_face_location_on_frame(current_frame, faces_locations, scale=1):
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


def detect_faces_from(source=0):
    webcam_video_stream = cv2.VideoCapture(source)
    while True:
        ret, current_frame = webcam_video_stream.read()
        current_frame_small = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(current_frame_small, model='hog')
        print_out_face_location_on_frame(current_frame, face_locations, scale=4)
        cv2.imshow("Webcam video", current_frame)
        if is_key_stop():
            release_webcam(webcam_video_stream)
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webcam = 0
    video = 'videos/xxx.mp4'
    detect_faces_from()

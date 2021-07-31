import cv2
import dlib


class FaceTracker:

    def __draw_text_info(self, is_tracking_face, frame):
        menu_pos_1 = (10, 20)
        menu_pos_2 = (10, 40)

        cv2.putText(frame, "Use '1' to re-initialize tracking", menu_pos_1, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255))
        if is_tracking_face:
            cv2.putText(frame, 'tracking the face', menu_pos_2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        else:
            cv2.putText(frame, 'Detecting a face to initialize tracking...', menu_pos_2, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))

    def run(self):
        capture = cv2.VideoCapture(0)
        detector = dlib.get_frontal_face_detector()
        tracker = dlib.correlation_tracker()
        is_tracking = False

        while True:
            ret, frame = capture.read()
            self.__draw_text_info(is_tracking, frame)
            if is_tracking:
                print(tracker.update(frame))
                pos = tracker.get_position()
                cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())),
                              (0, 255, 0), 3)
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 0)
                if len(rects) > 0:
                    tracker.start_track(frame, rects[0])
                    is_tracking = True

            key = 0xFF & cv2.waitKey(1)
            if key == ord('1'):
                is_tracking = False

            if key == ord('q'):
                break

            cv2.imshow('Face tracking using dlib frontal face detector and correlations filters for tracking', frame)

        capture.release()
        cv2.destroyAllWindows()


face_tracker = FaceTracker()
face_tracker.run()

import cv2


class MovementDetector:

    @staticmethod
    def detect(frame_a, frame_b):
        diff = cv2.absdiff(frame_a, frame_b)
        grey = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # dilating 3 times'iterations=3' kernel=none
        dilated = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 3000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame_a, (x, y), (x + w, y + h), (0, 255, 0), 3)
        return frame_a

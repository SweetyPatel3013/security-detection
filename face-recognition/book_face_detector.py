import dlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import face_recognition


def show_detection(image, faces):
    """ Draws a rectangle over each detected face"""
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
    return image


def show_img_with_matplotlib(color_img, tittle, pos):
    """ Shows an image using matplotlib capabilities """
    img_RGB = color_img[:, :, :: -1]
    ax = plt.subplot(1, 2, pos)
    plt.imshow(img_RGB)
    plt.title(tittle)
    plt.axis('off')


class HaarCascadeFaceDetector:

    def run(self):
        # Load image and convert to grayscale
        img = cv2.imread('images/samples/trump-and-others.jpeg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load cascade classifier
        alt2 = 'resources/haarcascade_frontalface_alt2.xml'
        default = 'resources/haarcascade_frontalface_default.xml'

        cas_alt2 = cv2.CascadeClassifier(alt2)
        cas_default = cv2.CascadeClassifier(default)

        # Detect faces:
        faces_alt2 = cas_alt2.detectMultiScale(gray)
        faces_default = cas_default.detectMultiScale(gray)

        # Draw face detections:
        img_faces_alt2 = show_detection(img.copy(), faces_alt2)
        img_faces_default = show_detection(img.copy(), faces_default)

        # Plot the images:
        show_img_with_matplotlib(img_faces_alt2, "Face detection with ALT2", 1)
        show_img_with_matplotlib(img_faces_default, "Face detection with Default", 2)
        plt.show()


################################################
#   Face detection with TensorFlow
################################################
class TensorFlowFaceDetector:

    def run(self, img_path):
        img = cv2.imread(img_path)
        net = cv2.dnn.readNetFromTensorflow('resources/opencv_face_detector_uint8.pb',
                                            'resources/opencv_face_detector.pbtxt')
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104., 117., 123.], False, False)

        # Get dimensions of the input image (to be used later):
        (h, w) = img.shape[:2]

        # Set the blob as input and obtain the detections:
        net.setInput(blob)
        detections = net.forward()

        detected_faces = 0

        # Iterate over all detections:
        for i in range(0, detections.shape[2]):
            # Get the confidence (probability) of the current detection:
            confidence = detections[0, 0, i, 2]

            # Only consider detections if confidence is greater than a fixed minimum confidence:
            if confidence > 0.7:
                # Increment the number of detected faces:
                detected_faces += 1
                # Get the coordinates of the current detection:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw the detection and the confidence:
                text = "{:.3f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(img, (startX, startY), (endX, endY), (255, 0, 0), 3)
                cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Create the dimensions of the figure and set title:
        fig = plt.figure(figsize=(10, 5))
        plt.suptitle("Face detection using OpenCV DNN face detector", fontsize=14, fontweight='bold')
        fig.patch.set_facecolor('silver')

        # Plot the images:
        show_img_with_matplotlib(img, "DNN face detector: " + str(detected_faces), 1)

        # Show the Figure:
        plt.show()


class DlibFaceDetector:

    def __show_detection(self, image, faces):
        for face in faces:
            cv2.rectangle(image, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 10)
        return image

    def run_hog(self, img_path):
        # Load image and convert to grayscale
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        detector = dlib.get_frontal_face_detector()
        rects_1 = detector(gray, 0)
        rects_2 = detector(gray, 1)

        img_faces_1 = self.__show_detection(img.copy(), rects_1)
        img_faces_2 = self.__show_detection(img.copy(), rects_2)

        # Plot the images:
        show_img_with_matplotlib(img_faces_1, "detector(gray, 0): " + str(len(rects_1)), 1)
        show_img_with_matplotlib(img_faces_2, "detector(gray, 1): " + str(len(rects_2)), 2)

        # Show the Figure:
        plt.show()

    def run_cnn(self, image_path):
        cnn_face_detector = dlib.cnn_face_detection_model_v1('resources/mmod_human_face_detector.dat')
        img = cv2.imread(image_path)
        # Detect faces
        rects = cnn_face_detector(img, 0)
        img_faces = show_detection(img.copy(), rects)
        # Plot the images:
        show_img_with_matplotlib(img_faces, "cnn_face_detector(img, 0): " + str(len(rects)), 1)
        plt.show()


class FaceRecognitionLibDetector:

    def __show_detection(self, image, faces):
        for face in faces:
            top, right, bottom, left = face
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 10)
        return image

    def run(self, img_path, model='hog'):
        img = cv2.imread(img_path)
        #img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb = img[:, :, ::-1]
        #The first parameter is the input (RGB) image.
        # The second parameter sets how many times the input image is upsampled before the detection process has been carried out.
        # The third parameter determines which face detection model will be used.
        rects_1 = face_recognition.face_locations(rgb, 0, model)
        rects_2 = face_recognition.face_locations(rgb, 1, model)

        img_faces_1 = self.__show_detection(img.copy(), rects_1)
        img_faces_2 = self.__show_detection(img.copy(), rects_2)

        # Plot the images:
        show_img_with_matplotlib(img_faces_1, f'face_locations(rgb, 0, {model}): {str(len(rects_1))}', 1)
        show_img_with_matplotlib(img_faces_2, f'face_locations(rgb, 0, {model}): {str(len(rects_2))}', 2)

        # Show the Figure:
        plt.show()


haar_cascade_detector = HaarCascadeFaceDetector()
#haar_cascade_detector.run()

tensorflow_detector = TensorFlowFaceDetector()
#tensorflow_detector.run('images/samples/trump-and-biden.jpeg')

dlib_detector = DlibFaceDetector()
#dlib_detector.run_hog('images/samples/trump-and-others.jpeg')
#dlib_detector.run_cnn('images/samples/trump-and-others.jpeg')

face_recognition_detector = FaceRecognitionLibDetector()
face_recognition_detector.run('images/samples/trump-and-others.jpeg', 'hog')
face_recognition_detector.run('images/samples/trump-and-others.jpeg', 'cnn')

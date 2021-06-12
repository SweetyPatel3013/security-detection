# Importing required libraries
#!pip install opencv-contrib-python
import numpy as np
import os
import cv2
from PIL import Image


# Code for Collecting the Images/Frames of Employee Faces
def imgdata_collect():
    # Defining the Window Size for the Facial Data Capturing

    img_cap = cv2.VideoCapture(0)
    img_cap.set(6, 720)
    img_cap.set(9, 640)

    face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')

    # For each New Employee, enter a different ID
    new_emp_id = input('\n Please enter Employee ID and press <return> : ')
    print("\n !!CAPTURING FACIAL DATA!! Kindly Look at the Camera and Wait...")

    # Counter for initializing the Employee Face Count
    count = 0

    while (True):
        r, img_frame = img_cap.read()
        img_frame = cv2.flip(img_frame, 1)
        g_scale = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
        emp_faces = face_cascade.detectMultiScale(g_scale, 1.2, 5)
        for (x, y, w, h) in emp_faces:
            cv2.rectangle(img_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

            # Saving the image frames in 'dataset' folder
            cv2.imwrite("dataset/User." + str(new_emp_id) + '.' + str(count) + ".jpg", g_scale[y:y + h, x:x + w])
            cv2.imshow('Image', img_frame)

        # Press 'ESC' for exiting from the window or after taking 20 frames it stops the capture and ends the window
        k = cv2.waitKey(50) & 0xff
        if k == 27:
            break
        elif count >= 20:
            break

    # Intimating the User to Run the code again for New Employee
    print("\n Data Saved. For New Employee kindly run again")
    img_cap.release()
    cv2.destroyAllWindows()

    return


# Code for Training the Algorithm using frames captured
def train_recog():
    from PIL import Image
    import os

    # Path for storing the image frames
    path = 'dataset'

    # Using Local Binary Patterns Histogram (LBPHFaceRecognizer) for recognizing Employee Faces
    face_recog = cv2.face.LBPHFaceRecognizer_create()
    face_class = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml");

    # Function to route the images
    def image_train(path):
        img_loc = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for emp_img in img_loc:
            PIL_img = Image.open(emp_img).convert('L')  # grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(emp_img)[-1].split(".")[1])
            faces = face_class.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

    print("\n Training Model for Emp faces. It will take a few seconds. Wait ...")
    faces, ids = image_train(path)
    face_recog.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    face_recog.write('trainer/trainer.yml')

    # Print the numer of faces trained and end program
    print("\n {0} faces trained.".format(len(np.unique(ids))))
    print("\n Face Recognition Model is trained.")


# Code for Implementing the Facial Recognition
def face_recognition():
    face_recog = cv2.face_LBPHFaceRecognizer.create()
    face_recog.read('trainer/trainer.yml')
    path = "resources/haarcascade_frontalface_default.xml"
    img_cascade = cv2.CascadeClassifier(path);
    font = cv2.FONT_HERSHEY_COMPLEX

    # Initiate Counter for ID
    id = 0
    # Names matching to IDs i.e. 1 = Dhaval Barot & so on..
    emp_names = ['None', 'Dhaval Barot', 'Camilo Espitia']

    # Using Webcam capturing Real-Time data

    img_cap = cv2.VideoCapture(0)
    img_cap.set(6, 720)
    img_cap.set(9, 640)

    # Minimum size defined for Face Recognition
    min_wid = 0.1 * img_cap.get(6)
    min_hgt = 0.1 * img_cap.get(9)
    while True:
        r, img_frame = img_cap.read()
        img_frame = cv2.flip(img_frame, 1)
        g_scale = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

        emp_faces = img_cascade.detectMultiScale(g_scale, scaleFactor=1.2, minNeighbors=5,
                                                 minSize=(int(min_wid), int(min_hgt)), )
        for (x, y, w, h) in emp_faces:
            cv2.rectangle(img_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, match = face_recog.predict(g_scale[y:y + h, x:x + w])

            # If match is less than 100, image tends to show perfect ID. "0 = Perfect Match"
            if (match < 100):
                id = emp_names[id]
                match = "  {0}%".format(round(100 - match))
            else:
                id = "unknown"
                match = "  {0}%".format(round(100 - match))

            # Positioning of the Names and %age of matching
            cv2.putText(img_frame, str(id), (x + 5, y + h - 5), font, 1, (0, 255, 0), 2)
            cv2.putText(img_frame, str(match), (x + 15, y - 5), font, 1, (255, 0, 0), 2)

        cv2.imshow('Webcam Live', img_frame)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    img_cap.release()
    cv2.destroyAllWindows()


#imgdata_collect()
#train_recog()
face_recognition()

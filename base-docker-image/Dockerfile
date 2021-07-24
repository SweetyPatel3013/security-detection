FROM tensorflow/tensorflow:2.6.0rc0

# Install dependencies
#RUN pip3 install -r requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir opencv-python
RUN pip3 install --no-cache-dir flask
RUN pip3 install --no-cache-dir gunicorn
RUN pip3 install --no-cache-dir flask_cors
RUN pip3 install --no-cache-dir imutils
RUN pip3 install --no-cache-dir cmake
RUN pip3 install --no-cache-dir face_recognition
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

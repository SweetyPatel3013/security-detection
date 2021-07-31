from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index_new.html')


@app.route('/faces')
def persons():
    # return render_template('AddPerson.html')
    return render_template('add-person_new.html')


@app.route('/faces1')
def persons1():
    return render_template('AddPerson.html')


@app.route('/faces/recognition')
def face_recognition():
    return render_template('face-recognition_new.html')
    # return render_template('FaceRecognition.html')


@app.route('/movements')
def movements():
    return render_template('movement-detector_new.html')
    # return render_template('MovementDetector.html')

@app.route('/facemask')
def movements():
    return render_template('face-mask_new.html')

if __name__ == "__main__":
    app.run(debug=False)

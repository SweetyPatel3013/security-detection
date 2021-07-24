from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/faces')
def persons():
    return render_template('AddPerson.html')


@app.route('/faces/recognition')
def face_recognition():
    return render_template('FaceRecognition.html')


@app.route('/movements')
def movements():
    return render_template('MovementDetector.html')


if __name__ == "__main__":
    app.run(debug=False)

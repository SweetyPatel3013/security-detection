from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=False)

import os
import numpy as np

# FLASK imports
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getDetectionData', methods = ['GET'])
def getDetectionData():

    data = request.get_json()
    frame_in_json = data['data']
    frame = np.asarray(frame_in_json)

    boxes = [[0.0]*4]*200
    boxes[0] = [0.18,0.05,0.9,0.35]
    boxes[1] = [0.2,0.4,0.99,0.67]
    boxes[2] = [0.09,0.74,0.93,0.92]
    boxes = [boxes]
    scores = [0.0]*200
    scores[0] = 0.9
    scores[1] = 0.9
    scores[2] = 0.9
    scores = [scores]
    classes = [1.0]*200
    classes[1] = 2.0
    classes[2] = 3.0
    classes = [classes]
    return jsonify({'boxes' : boxes, 'scores' : scores, 'classes' : classes, 'num' : 200})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

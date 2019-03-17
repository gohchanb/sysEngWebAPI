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
<<<<<<< HEAD
    boxes[0] = [0.18,0.05,0.9,0.35]
    boxes[1] = [0.2,0.4,0.99,0.67]
    boxes[2] = [0.09,0.74,0.93,0.92]
    boxes = [boxes]
    scores = [0.0]*200
    scores[0] = 0.7
    # scores[1] = 0.7
    scores[2] = 0.7
=======
    boxes[0] = [0.15,0.7,0.9,0.89]
    boxes[1] = [0.1,0.35,0.90,0.62]
    boxes[2] = [0.15,0.11,0.95,0.3]
    boxes = [boxes]
    scores = [0.0]*200
    scores[0] = 0.9
    # scores[1] = 0.9
    # scores[2] = 0.9
>>>>>>> bebaaddfa28938418801ff6168695af763726697
    scores = [scores]
    classes = [1.0]*200
    classes[1] = 2.0
    classes[2] = 3.0
    classes = [classes]
    return jsonify({'boxes' : boxes, 'scores' : scores, 'classes' : classes, 'num' : 200})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

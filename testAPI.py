import os
import cv2
import numpy as np
import tensorflow as tf

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
    boxes[0] = [0.25,0.25,0.75,0.75]
    boxes = [boxes]
    scores = [0.0]*200
    scores[0] = 0.7
    scores = [scores]
    classes = [1.0]*200
    classes = [classes]
    return jsonify({'boxes' : boxes, 'scores' : scores, 'classes' : classes, 'num' : 200})

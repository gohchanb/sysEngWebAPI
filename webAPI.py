import os
import cv2
import numpy as np
import tensorflow as tf

# FLASK imports
from flask import Flask
from flask import jsonify
from flask import request

# Detection Imports
from object_detection.detectionAlgorithm import *

MODEL_NAME = 'object_detection/instruments_graph'

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

sessData = [detection_boxes, detection_scores, detection_classes, num_detections]

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getDetectionData', methods = ['GET'])
def getDetectionData():

    data = request.get_json()
    frame_in_json = data['data']
    frame = np.asarray(frame_in_json)

    (boxes, scores, classes, num) = runDetectionModel(frame, image_tensor, sess, sessData)
    #print(num.tolist())
    return jsonify({'boxes' : boxes.tolist(), 'scores' : scores.tolist(), 'classes' : classes.tolist(), 'num' : num.tolist()})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

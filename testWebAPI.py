import os
import time
import numpy as np
import cv2
# import tensorflow as tf

import socket

# MODEL_NAME = 'object_detection/instruments_graph'
#
# CWD_PATH = os.getcwd()
# PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
#
# detection_graph = tf.Graph()
# with detection_graph.as_default():
#     od_graph_def = tf.GraphDef()
#     with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
#         serialized_graph = fid.read()
#         od_graph_def.ParseFromString(serialized_graph)
#         tf.import_graph_def(od_graph_def, name='')
#
#     sess = tf.Session(graph=detection_graph)
#
# image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
# detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# num_detections = detection_graph.get_tensor_by_name('num_detections:0')
#
# sessData = [detection_boxes, detection_scores, detection_classes, num_detections]

def recieveDataOfSize(conn,size):
    byteCount = 0
    fullData = ''.encode('utf-8')
    fail = 0
    while byteCount<size:
        data = conn.recv(size)
        byteCount += len(data)
        fullData += data
        print(byteCount)
        if not data:
            msg = 'ERROR did not get full Image'
            conn.sendall(msg.encode('utf-8'))
            fail = 1
            break
    # print(np.frombuffer(fullData,dtype='uint8'))
    # print(fullData)
    if byteCount!=size:
        fail = 1
        msg = 'ERROR sent too much data'
        conn.sendall(msg.encode('utf-8'))
    return fullData, fail

def shapeToString(shape):
    s = ''
    for i in shape:
        s += str(i)+','
    return s[:-1]

def stringToShape(s):
    shape = ()
    nums = s.split(',')
    for i in nums:
        shape += (int(i),)
    return shape

def sendData(conn, data):
    shape = data.shape
    dataBytes = data.tostring()
    size = len(dataBytes)

    msg = "SIZE %s %s" % (size, shapeToString(shape))
    s.sendall(msg.encode('utf-8'))

    data = s.recv(1024)
    if(data.decode('utf-8')=='GOT SIZE'):
        # print(frame)
        s.sendall(dataBytes)
        data = s.recv(1024)
        if(data.decode('utf-8')=='GOT DATA'):
            return 1
        else:
            return 0

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            text = data.decode('utf-8')
                # print(text)
            if text.startswith('SIZE'):
                t = text.split(' ')
                size = int(t[1])
                shape = stringToShape(t[2])
                print("got size "+t[1]+" and shape "+str(shape))

                msg = 'GOT SIZE'
                conn.sendall(msg.encode('utf-8'))

                fullImage, fail = recieveDataOfSize(conn, size)

                if not fail:
                    frame = np.frombuffer(fullImage,dtype='uint8').reshape(shape)

                    # boxes, scores, classes, num = sess.run(sessData, feed_dict={image_tensor:frame})
                    boxes = [[0.0]*4]*200
                    boxes[0] = [0.18,0.05,0.9,0.35]
                    boxes[1] = [0.2,0.4,0.99,0.67]
                    boxes[2] = [0.09,0.74,0.93,0.92]
                    boxes = [boxes]
                    scores = [0.0]*200
                    scores[0] = 0.7
                    # scores[1] = 0.7
                    scores[2] = 0.7
                    boxes[0] = [0.15,0.7,0.9,0.89]
                    boxes[1] = [0.1,0.35,0.90,0.62]
                    boxes[2] = [0.15,0.11,0.95,0.3]
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

                    if not sendData(conn, boxes):
                        print('ERROR in sending boxes')
                    if not sendData(conn, classes):
                        print('ERROR in sending data')
                    if not sendData(conn, scores):
                        print('ERROR in sending scores')
                    # msg = 'GOT IMAGE'
                    # conn.sendall(msg.encode('utf-8'))
                    # conn.sendall(data)
                # tAfter = time.time()
                # print("Time main: " + str(tAfter-tBefore))
            else:
                msg = 'ERROR with initialising SIZE'
                conn.sendall(msg.encode('utf-8'))



# @app.route('/getDetectionData', methods = ['GET'])
# def getDetectionData():
#
#     data = request.get_json()
#     frame_in_json = data['data']
#     frame = np.asarray(frame_in_json)
#
#     boxes = [[0.0]*4]*200
#     boxes[0] = [0.18,0.05,0.9,0.35]
#     boxes[1] = [0.2,0.4,0.99,0.67]
#     boxes[2] = [0.09,0.74,0.93,0.92]
#     boxes = [boxes]
#     scores = [0.0]*200
#     scores[0] = 0.7
#     # scores[1] = 0.7
#     scores[2] = 0.7
#     scores = [scores]
#     classes = [1.0]*200
#     classes[1] = 2.0
#     classes[2] = 3.0
#     classes = [classes]
#     return jsonify({'boxes' : boxes, 'scores' : scores, 'classes' : classes, 'num' : 200})
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0',debug=True)

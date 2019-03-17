import os
import time
import numpy as np

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

size = 1024
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
                print("got size "+t[1])
                msg = 'GOT SIZE'
                conn.sendall(msg.encode('utf-8'))

                fullImage, fail = recieveDataOfSize(conn, size)

                if not fail:
                    frame = np.frombuffer(fullImage,dtype=int)
                    msg = 'GOT IMAGE'
                    conn.sendall(msg.encode('utf-8'))
                    # conn.sendall(data)
                # tAfter = time.time()
                # print("Time main: " + str(tAfter-tBefore))
            else:
                msg = 'ERROR with initialising SIZE'
                conn.sendall(msg.encode('utf-8'))

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
    # print(np.frombuffer(fullImage,dtype=int))
    if byteCount!=size:
        fail = 1
        msg = 'ERROR sent too much data'
        conn.sendall(msg.encode('utf-8'))

    return fullData, fail



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

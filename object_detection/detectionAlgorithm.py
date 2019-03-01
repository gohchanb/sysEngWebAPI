
def runDetectionModel(frame, image_tensor, sess, sessData):
    detectionData = sess.run(sessData,feed_dict={image_tensor: frame})
    return detectionData

def test(x):
    return x

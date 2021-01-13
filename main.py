# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from gtts import gTTS
import numpy as np
import argparse
import imutils
import time
import cv2
from playsound import playsound
import os
import threading

import text_to_speech as speech
import statistics

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default="MobileNetSSD_deploy.prototxt.txt",
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", default="MobileNetSSD_deploy.caffemodel",
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "mobil", "cat", "kursi", "cow", "diningtable",
           "dog", "horse", "sepedamotor", "orang", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
IGNORE = set(["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "cat", "cow", "diningtable",
	"dog", "horse", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"])
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")

orang = 0
kursi = 0
motor = 0
mobil = 0
stop = 0

def task1():

 #vs = VideoStream('sample.mkv').start()
 vs = VideoStream(src=0).start()
 #vs = cv2.VideoCapture('sample.mp4')
 time.sleep(2.0)
 fps = FPS().start()
 # loop over the frames from the video stream
 while True:
    global orang, kursi, motor, mobil, stop
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])

            if CLASSES[idx] in IGNORE:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            if CLASSES[idx] == 'orang':
                orang = 1
            elif CLASSES[idx] == 'kursi':
                kursi = 1
            elif CLASSES[idx] == 'sepedamotor':
                motor = 1
            elif CLASSES[idx] == 'mobil':
                mobil = 1
            else:
                orang = 0
                kursi = 0
                motor = 0
                mobil = 0

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        stop =1
        break

    # update the FPS counter
    fps.update()


 # stop the timer and display FPS information
 fps.stop()
 print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
 print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

 # do a bit of cleanup
 cv2.destroyAllWindows()
 vs.stop()

def task2():
    global orang, kursi, motor, mobil, stop

    while True:
        if orang == 1:
            playsound('Orang.mp3')
            orang = 0
        elif kursi == 1:
            #speech.speak("Kursi", lang="id")
            playsound('Kursi.mp3')
            kursi = 0
        elif motor == 1:
            #speech.speak("Motor", lang="id")
            playsound('Motor.mp3')
            motor = 0
        elif mobil == 1:
            #speech.speak("Mobil", lang="id")
            playsound('Mobil.mp3')
            mobil = 0
        elif stop == 1:
            break


if __name__ == "__main__":
    t1 = threading.Thread(target=task1)
    t1.start()
    t2 = threading.Thread(target=task2)
    t2.start()




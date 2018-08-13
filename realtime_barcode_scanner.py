# USAGE
# python detect_barcode.py
# python detect_barcode.py --video video/video_games.mov

# import the necessary packages
from imutils.video import VideoStream
import argparse
import time
import cv2
from urllib2 import urlopen
import imutils
import numpy as np
import Image
import zbar
from pyzbar import pyzbar
import requests


host = 'http://10.0.0.220:8080/'
url = host + 'shot.jpg'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True,
	help="Source of video stream (webcam/host)")
args = vars(ap.parse_args())

if args["source"] == "webcam":
	capture = cv2.VideoCapture(0)

time.sleep(2.0)


# keep looping over the frames
while True:
	# grab the current frame and then handle if the frame is returned
	# from either the 'VideoCapture' or 'VideoStream' object,
	# respectively
	if args["source"] == "webcam":
		ret, frame = capture.read()
	else:
		imgResp=urlopen(url)
		imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
		frame=cv2.imdecode(imgNp,-1)


        frame = imutils.resize(frame, width=800)

        barcodes = pyzbar.decode(frame)
        barcodeData=''

    # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            print("Barcode Found :", barcodeData)

        if barcodeData != '':
            break

        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")


api_key='7E53B18FA49BB5A9A434CF81E9271C13'
api_endpoint='https://api.upcdatabase.org/product'
api_url=str(api_endpoint+'/'+barcodeData+'/'+api_key)
print api_url

response=requests.get(api_url)

cv2.destroyAllWindows()

print response.text
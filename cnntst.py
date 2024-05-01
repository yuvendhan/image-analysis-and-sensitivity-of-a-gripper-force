import tensorflow.python.keras
from PIL import Image, ImageOps
import numpy as np
import time
import cv2
from time import sleep
import requests
import serial
import matplotlib.pyplot as plt

serialPort = serial.Serial(
    port="COM9", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)         

serialPort.write('D'.encode())

model = tensorflow.keras.models.load_model('keras_model.h5')

cap = cv2.VideoCapture(0)

# Load the labels
class_names = open("labels.txt", "r").readlines()

font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (50, 50)
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 255, 0)
  
# Line thickness of 2 px
thickness = 2

cname=""

while True:
        ret, image = cap.read()
        
        #(rpiName, image) = imageHub.recv_image()
        #imageHub.send_reply(b'OK')
        cv2.imwrite('image.jpg', image)

        #cv2.imshow('Data', image)

        # Using cv2.putText() method
        image = cv2.putText(image, cname, org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)

        cv2.imshow("Object Detection", image)
        
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

# Load the model
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
        image = Image.open('image.jpg')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.LANCZOS)

#turn the image into a numpy array
        image_array = np.asarray(image)

# Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
        data[0] = normalized_image_array

        newsize = (480, 480)
        image = image.resize(newsize)
        #image.show()

# run the inference
        prediction = model.predict(data)
        ynew=np.argmax(prediction,axis=1)
        print(prediction)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)

        
        if ynew == [0]:
                print("  ")
                cname=""
                #r =requests.get('http://www.iotclouddata.com/22log/062/iot22.php?A=' + '*A@')
        if ynew == [1]:
                print(" Apple ")
                cname="Apple"
                serialPort.write('A'.encode())
        if ynew == [2]:
                print(" Egg ")
                cname="Egg"
                serialPort.write('B'.encode())
        if ynew == [3]:
                print(" Wood ")
                cname="Wood"
                serialPort.write('C'.encode())
        print(ynew)
# Plotting the predictions and force readings
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(predictions)
plt.title('Predictions over Time')
plt.xlabel('Time')
plt.ylabel('Class')

plt.subplot(2, 1, 2)
plt.plot(force_readings)
plt.title('Force Readings over Time')
plt.xlabel('Time')
plt.ylabel('Force')

plt.tight_layout()
plt.show()

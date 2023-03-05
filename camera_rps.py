# Third Party
import cv2
from keras.models import load_model
import numpy as np
import time
from datetime import datetime
from datetime import timedelta


class CameraCapturePrediction:

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.topLeftCornerOfText = (10, 20)
        self.bottomLeftCornerOfText = (10, 200)
        self.fontScale = 1
        self.fontColor = (0, 0, 255)
        self.thickness = 2
        self.lineType = 4

    def countdown(self, time):
        """
        counts for 3 seconds printing count to screen without using sleep.
        :param time: object
        """
        start = time.time()
        time_difference = 0
        print_second_list = [1, 2, 3]
        for seconds_count in print_second_list:
            print(print_second_list[::-1][seconds_count - 1])
            while time_difference < seconds_count:
                current = time.time()
                time_difference = current - start

    def print_webcam_text_to_screen(self, image_for_screen, print_time):
        cv2.putText(image_for_screen, print_time,
                    self.bottomLeftCornerOfText, self.font,
                    self.fontScale, self.fontColor,
                    self.thickness, self.lineType)


    def get_prediction(self):
        """
        get what the camera predicted the hand pose to be.
        :return user_choice: string containing either 'rock', 'paper', or 'scissors'
        """
        # Load the model
        model = load_model('keras_model.h5')

        # CAMERA can be 0 or 1 based on default camera of your computer.
        camera = cv2.VideoCapture(0)

        # Grab the labels from the labels.txt file. This will be used later.
        # it is better to use .read().splitlines() to remove the carriage returns.
        labels = open('labels.txt', 'r').read().splitlines()
        start_time = time.time()
        start_time_datetime = datetime.fromtimestamp(start_time)
        t0 = start_time_datetime + timedelta(seconds=0)
        t1 = start_time_datetime + timedelta(seconds=1)
        t2 = start_time_datetime + timedelta(seconds=2)
        t3 = start_time_datetime + timedelta(seconds=3)
        t4 = start_time_datetime + timedelta(seconds=4)

        print("start_time", start_time)
        user_choice = ''
        time_lapsed = start_time_datetime + timedelta(seconds=0)

        while time_lapsed < t4:
            current_time = time.time()
            time_lapsed = datetime.fromtimestamp(current_time)

            # Grab the webcameras image.
            ret, image = camera.read()
            # Resize the raw image into (224-height,224-width) pixels.
            image_for_screen = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            print(start_time)
            if (time_lapsed < t1) and (time_lapsed > t0):
                self.print_webcam_text_to_screen(image_for_screen, "3")
                print("1:", time_lapsed)
            if (time_lapsed < t2) and (time_lapsed > t1):
                self.print_webcam_text_to_screen(image_for_screen, "2")
                print("2:", time_lapsed)
            if (time_lapsed < t3) and (time_lapsed > t2):
                self.print_webcam_text_to_screen(image_for_screen, "1")

            print("out:", time_lapsed)
            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image_for_screen, dtype=np.float32).reshape(1, 224, 224, 3)
            # Normalize the image array
            image = (image / 127.5) - 1
            # Have the model predict what the current image is. Model.predict
            # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
            # it is the first label and 80% sure its the second label.
            probabilities = model.predict(image)
            user_choice = labels[np.argmax(probabilities)]
            # Print what the highest value probability label
            cv2.putText(image_for_screen, user_choice,
                        self.topLeftCornerOfText, self.font,
                        self.fontScale, self.fontColor,
                        self.thickness, self.lineType)
            # Show the image in a window
            cv2.imshow('Webcam Image', image_for_screen)
            cv2.waitKey(1)
            #camera.release()
            #cv2.destroyAllWindows()
        return user_choice




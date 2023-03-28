import cv2
from datetime import datetime
from datetime import timedelta
from keras.models import load_model
import numpy as np
import random
import time


class CameraCapturePrediction:

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.topLeftCornerOfText = (10, 20)
        self.bottomLeftCornerOfText = (10, 200)
        self.fontScale = 1
        self.fontColor = (0, 0, 255)
        self.thickness = 2
        self.lineType = 4

    def print_countdown_to_screen_during_video_capture(self, time_lapsed, seconds_after, image_for_screen):
        """
        counts down for 3 seconds, print the numbers 3, 2, 1 to screen after each second has passed.
        This is done without a while loop, so that video capture can resume after printing to screen has completed.
        :param time_lapsed: time object containing the amount of time that has passed.
        :param seconds_after: list of delta time objects containing the number of seconds after time 0
        :param image_for_screen: image array of the current frame to print the text onto
        """
        print_seconds = [1, 2, 3]
        for seconds_count in print_seconds:
            if (time_lapsed < seconds_after[seconds_count]) and (time_lapsed > seconds_after[seconds_count-1]):
                self.print_text_to_webcam_screen(image_for_screen, str(print_seconds[::-1][seconds_count-1]),
                                                 self.bottomLeftCornerOfText)

    def print_text_to_webcam_screen(self, image_for_screen, text, location):
        """ prints a text to screen.
        In this case the text is a number identifying the number of seconds counting down until last capture
        :param image_for_screen: image array of the current frame to print the text onto.
        :param text: string containing the text to print onto that frame.
        :param location: tuple containing the location coordinate
        """
        cv2.putText(image_for_screen, text,
                    location, self.font,
                    self.fontScale, self.fontColor,
                    self.thickness, self.lineType)

    def get_start_time_time_deltas_and_time_lapsed(self):
        """ gets the start time, the time stamps at different time deltas, and initialises time lapsed since the start
        :return start_time: time stamp object of the start time.
        :return t0 to t4: time stamp object each second after time 0, up to  seconds after.
        :return timelapsed: time stamp initialization object after time has lapsed.
        """
        start_time = time.time()
        start_time_datetime = datetime.fromtimestamp(start_time)
        t1 = start_time_datetime + timedelta(seconds=1)
        t2 = start_time_datetime + timedelta(seconds=2)
        t3 = start_time_datetime + timedelta(seconds=3)
        t4 = start_time_datetime + timedelta(seconds=4)
        seconds_after = [t1, t2, t3, t4]
        time_lapsed = start_time_datetime + timedelta(seconds=0)
        return start_time, seconds_after, time_lapsed

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
        start_time, seconds_after, time_lapsed = self.get_start_time_time_deltas_and_time_lapsed()

        while time_lapsed < seconds_after[3]:
            current_time = time.time()
            time_lapsed = datetime.fromtimestamp(current_time)

            # Grab the webcameras image.
            ret, image = camera.read()
            # Resize the raw image into (224-height,224-width) pixels.
            image_for_screen = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            self.print_countdown_to_screen_during_video_capture(time_lapsed, seconds_after, image_for_screen)
            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image_for_screen, dtype=np.float32).reshape(1, 224, 224, 3)
            # Normalize the image array
            image = (image / 127.5) - 1
            # Have the model predict what the current image is. Model.predict
            # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
            # it is the first label and 80% sure its the second label.
            probabilities = model.predict(image)
            prediction = labels[np.argmax(probabilities)]
            # Print what the highest value probability label
            self.print_text_to_webcam_screen(image_for_screen, prediction, self.topLeftCornerOfText)
            # Show the image in a window
            cv2.imshow('Webcam Image', image_for_screen)
            cv2.waitKey(1)
        return prediction


class RockPaperScissors:
    def __init__(self):
        self.user_choice = ''
        self.computer_choice = ''
        self.camera_capture_prediction_instance = CameraCapturePrediction()
        self.user_wins = bool

    def get_computer_choice(self):
        """ get the randomly chosen computers choice
        :return computer_choice: string containing either 'rock', 'paper' or 'scissors'
        """
        choices = ['rock', 'paper', 'scissors']
        self.computer_choice = random.choice(choices)

    def get_user_choice(self):
        """
        get the users input choice
        :return user_choice: string containing either 'rock', 'paper' or 'scissors'
        """
        self.user_choice = self.camera_capture_prediction_instance.get_prediction()

    def get_winner(self):
        """
        combines the computers choice and the users choice into a tuple
        the win combinations and lose combinations are defined
        and then the if, elif, else statements determine whether the outcome is "You won!", "You lost!", or "it is a tie"
        :param computer_choice: string containing either 'rock', 'paper' or 'scissors'
        :param user_choice: string containing either 'rock', 'paper' or 'scissors'
        :return user_wins: integer containing either a True or False.  True if user won. False if user lost.
        """
        choice_combination = (self.computer_choice, self.user_choice)
        lose_combinations = [('paper', 'rock'), ('scissors', 'paper'), ('rock', 'scissors')]
        win_combinations = [('rock', 'paper'), ('paper', 'scissors'), ('scissors', 'rock')]

        if choice_combination in lose_combinations:
            print("You lost!")
            self.user_wins = False
        elif choice_combination in win_combinations:
            print("You won!")
            self.user_wins = True
        else:
            print("it is a tie!")

    def count_down_on_camera_prior_to_prediction(self):
        """
        a computationally efficient 6, 5, 4, countdown that happens before prediction starts.
        """

        camera = cv2.VideoCapture(0)
        tstart = time.time()
        while time.time() - tstart < 3:
            ret, image = camera.read()
            image_for_screen = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            count_down_text = str(7 - int(time.time() - tstart))
            self.camera_capture_prediction_instance.print_text_to_webcam_screen(
                image_for_screen,
                count_down_text,
                self.camera_capture_prediction_instance.bottomLeftCornerOfText)
            cv2.imshow('Webcam Image', image_for_screen)
            cv2.waitKey(1)

    def play(self):
        """
        gets the computers, and users choice and determines who the winner is.
        :return user_win: integer containing either a True or False.  True if user won, False if user lost.
        """
        self.count_down_on_camera_prior_to_prediction()
        self.get_computer_choice()
        self.get_user_choice()
        print("computer choice: ", self.computer_choice)
        print("user choice: ", self.user_choice)
        self.get_winner()
    def first_to_three_wins(self):
        """
        run play a few times to get the best of three. print to screen the number of times you lost or won once either
        you or the computer reach three wins.
        """
        total_computer_wins, total_user_wins = 0, 0
        while total_computer_wins <= 3 and total_user_wins <= 3:
                self.play()
                if self.user_wins:
                    total_user_wins += 1
                else:
                    total_computer_wins += 1
        if total_computer_wins > total_user_wins:
            print(f"You Lost {total_computer_wins} times")
        else:
            print(f"You Won {total_user_wins} times")


if __name__ == "__main__":
    rps_instance = RockPaperScissors()
    rps_instance.first_to_three_wins()

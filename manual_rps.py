import cv2
from keras.models import load_model
import numpy as np
import random


def get_computer_choice():
    """ get the randomly chosen computers choice
    :returns computer_choice: string containing either 'rock', 'paper' or 'scissors'
    """
    # choices = ['rock', 'paper', 'scissors']
    # computer_choice = random.choice(choices)
    # return computer_choice
    # Load the model
    model = load_model('keras_model.h5')

    # CAMERA can be 0 or 1 based on default camera of your computer.
    camera = cv2.VideoCapture(0)

    # Grab the labels from the labels.txt file. This will be used later.
    labels = open('labels.txt', 'r').readlines()

    while True:
        # Grab the webcameras image.
        ret, image = camera.read()
        # Resize the raw image into (224-height,224-width) pixels.
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Show the image in a window
        cv2.imshow('Webcam Image', image)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Have the model predict what the current image is. Model.predict
        # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
        # it is the first label and 80% sure its the second label.
        probabilities = model.predict(image)
        computer_choice = labels[np.argmax(probabilities)]
        # Print what the highest value probabilitie label
        camera.release()
        cv2.destroyAllWindows()
        return computer_choice
    #     # Listen to the keyboard for presses.
    #     keyboard_input = cv2.waitKey(1)
    #     # 27 is the ASCII for the esc key on your keyboard.
    #     if keyboard_input == 27:
    #         break
    #
    # camera.release()
    # cv2.destroyAllWindows()


def get_user_choice():
    """
    get the users input choice
    :returns user_choice: string containing either 'rock', 'paper' or 'scissors'
    """
    user_choice = input("enter rock, paper, or scissors:\n")
    user_choice = user_choice.lower()
    return user_choice


def get_winner(computer_choice, user_choice):
    """
    combined the computers choice and the users choice into a tuple
    the win combinations and lose combinations are defined
    and then the if, elif, else statements determine whether the outcome is "You won!", "You lost!", or "it is a tie"
    :param computer_choice: string containing either 'rock', 'paper' or 'scissors'
    :param user_choice: string containing either 'rock', 'paper' or 'scissors'
    """
    choice_combination = (computer_choice, user_choice)
    win_combinations = [('rock', 'paper'), ('paper', 'scissors'), ('scissors', 'rock')]
    lose_combinations = [('paper', 'rock'), ('scissors', 'paper'), ('rock', 'scissors')]
    if choice_combination in win_combinations:
        print("You won!")
    elif choice_combination in lose_combinations:
        print("You lost!")
    else:
        print("it is a tie!")


def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    get_winner(computer_choice, user_choice)


play()

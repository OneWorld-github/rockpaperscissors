# Standard Library
import random

# Rock Paper Scissors
from camera_rps import CameraCapturePrediction


class RockPaperScissors:
    def get_computer_choice(self):
        """ get the randomly chosen computers choice
        :return computer_choice: string containing either 'rock', 'paper' or 'scissors'
        """
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        return computer_choice

    def get_user_choice(self):
        """
        get the users input choice
        :return user_choice: string containing either 'rock', 'paper' or 'scissors'
        """
        camera_capture_prediction_instance = CameraCapturePrediction()
        user_choice = camera_capture_prediction_instance.get_prediction()
        return user_choice

    def get_winner(self, computer_choice, user_choice):
        """
        combines the computers choice and the users choice into a tuple
        the win combinations and lose combinations are defined
        and then the if, elif, else statements determine whether the outcome is "You won!", "You lost!", or "it is a tie"
        :param computer_choice: string containing either 'rock', 'paper' or 'scissors'
        :param user_choice: string containing either 'rock', 'paper' or 'scissors'
        :return computer_wins: integer containing either a 1 or 0.  1 if computer won. 0 if computer lost
        :return user_wins: integer containing either a 1 or 0.  1 if user won. 0 if user lost.
        """
        computer_wins = 0
        user_wins = 0
        choice_combination = (computer_choice, user_choice)
        lose_combinations = [('paper', 'rock'), ('scissors', 'paper'), ('rock', 'scissors')]
        win_combinations = [('rock', 'paper'), ('paper', 'scissors'), ('scissors', 'rock')]

        if choice_combination in lose_combinations:
            print("You lost!")
            computer_wins = 1
        elif choice_combination in win_combinations:
            print("You won!")
            user_wins = 1
        else:
            print("it is a tie!")
        return computer_wins, user_wins

    def play(self):
        """
        gets the computers, and users choice and determines who the winner is.
        :return computer_win: integer containing either a 1 or 0.  1 if computer won, 0 if computer lost
        :return user_win: integer containing either a 1 or 0.  1 if user won, 0 if user lost.
        """
        computer_choice = self.get_computer_choice()
        user_choice = self.get_user_choice()
        print("computer choice: ", computer_choice)
        print("user choice: ", user_choice)
        computer_win, user_win = self.get_winner(computer_choice, user_choice)
        return computer_win, user_win

    def first_to_three_wins(self):
        """
        run play a few times to get the best of three. print to screen the number of times you lost or won once either
        you or the computer reach three wins.

        """
        total_computer_wins = 0
        total_user_wins = 0
        while total_computer_wins <= 3 and total_user_wins <= 3:
                computer_wins, user_wins = self.play()
                total_computer_wins += computer_wins
                total_user_wins += user_wins
        if total_computer_wins > total_user_wins:
            print(f"You Lost {total_computer_wins} times")
        else:
            print(f"You Won {total_user_wins} times")


rps_instance = RockPaperScissors()
rps_instance.first_to_three_wins()



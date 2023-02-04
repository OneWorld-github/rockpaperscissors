# Standard Library
import random

# Rock Paper Scissors
import camera_rps

def get_computer_choice():
    """ get the randomly chosen computers choice
    :returns computer_choice: string containing either 'rock', 'paper' or 'scissors'
    """
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    return computer_choice

def get_user_choice():
    """
    get the users input choice
    :returns user_choice: string containing either 'rock', 'paper' or 'scissors'
    """
    user_choice = camera_rps.get_prediction()
    return user_choice

def get_winner(computer_choice, user_choice):
    """
    combined the computers choice and the users choice into a tuple
    the win combinations and lose combinations are defined
    and then the if, elif, else statements determine whether the outcome is "You won!", "You lost!", or "it is a tie"
    :param computer_choice: string containing either 'rock', 'paper' or 'scissors'
    :param user_choice: string containing either 'rock', 'paper' or 'scissors'
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


def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    print("computer choice: ", computer_choice)
    print("user choice: ", user_choice)
    computer_win, user_win = get_winner(computer_choice, user_choice)
    return computer_win, user_win


def first_to_three_wins():
    total_computer_wins = 0
    total_user_wins = 0
    for count in range(20):
        if total_computer_wins == 3 or total_user_wins == 3:
            break
        else:
            computer_wins, user_wins = play()
            total_computer_wins += computer_wins
            total_user_wins += user_wins
    print(f"You Lost {total_computer_wins} times")
    print(f"You Won {total_user_wins} times")

first_to_three_wins()
import random


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

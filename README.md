# ROCK PAPER SCISSORS

This model was trained on roughly 60-70 images in each of the of the Rock, Paper, Scissors, and Nothing class.

The input was a desktop webcam, and it uses Googles Teachable Machine to organise the data and train the Image model.


# Milestone 3

This code has four function definitions.
get_computer_choice, get_user_choice, get winner, and play.

get_computer_choice randomly selects either rock, paper or scissors from a list

get_user_choice takes user input, turns it all into lower case and passesit out.
It does not do any fancy input checking on the code.
Although, there is a neat way to limit selection here:-
https://stackoverflow.com/questions/37565793/how-to-let-the-user-select-an-input-from-a-finite-list


play simply runs the above functions for the gameplay by calling each of them
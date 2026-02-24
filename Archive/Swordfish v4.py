#Wordle.py

#This version includes a way of tracking words and exporting them into a json file. It can also check if the word chosen is in the json file and remove items from the json file after three months. Also some bug fixes with multiple attempts with words that are not in the list

#imports
import random
import sys
import json
import os
from word_list_file import word_options_as_list
from datetime import datetime, timedelta

#Here is where it will check that the user wants to play
def play():
    first_response = input("Would you like to play Wordle: ").lower()
    
    if first_response in ["not now", "no", "n"]:
        print("\nAlright, maybe later\n")
        play()
    elif first_response in ["yes", "yeah", "y"]:
        print("\nThe rules are:\n-You have to choose a five letter word\n-You want to guess the same word that the computer chose\n-You have to use real English words\n\nAlright, let's play!")
    else:
        print("\nThat is not one of the options, please choose yes or no\n")
        play()

#Here is where it will scan the json and remove anything older than 90 days from the list
def cleanup_data(most_recent_words):
    three_months_ago = datetime.now() - timedelta(days=90)

    if os.path.exists('recent_words.json'):
            with open('recent_words.json', 'r') as file:
                data = json.load(file)
            
            filtered_data = {
                word: date_str for word, date_str in data.items()
                if datetime.strptime(date_str, '%Y-%m-%d') > three_months_ago
            }

            with open('recent_words.json', 'w') as file:
                json.dump(filtered_data, file, indent=4)
                
            return filtered_data
    return {}

#Here is where the computer chooses its word
def computer_as_word(word_options_as_list):
    computer_choice = random.choice(word_options_as_list)
    return computer_choice

#Here is where I would like to add the choice and the time of said choice into a separate file
def keep_track_of_when_used(computer_choice):
    most_recent_words[computer_choice] = datetime.now().strftime("%Y-%m-%d")
    with open('recent_words.json', 'w') as file:
        json.dump(most_recent_words, file, indent=4)
    return most_recent_words

#Here is where it will load existing data to file, or start with empty dict
if os.path.exists('recent_words.json'):
    with open('recent_words.json', 'r') as file:
        most_recent_words = json.load(file)
else:
    most_recent_words = {}

#Here is where the word gets split into a list
def computer(computer_choice):
    computer_list = list(computer_choice)
    return computer_list

#Here is where I create the string of the word for the user
def user(word_options_as_list):
    user_choice = input("\nTry a word: ").lower()
    if user_choice not in word_options_as_list:
        print("That is not a valid word")
        user_list = user(word_options_as_list)
    else:
        user_list = list(user_choice)
    return user_list

#Here is where we check if the user actually wins or loses
def check_win(computer_list, user_list):
    if user_list == computer_list:
        sys.exit("\nYou have found the wordle!")
    else:
        for l in range(len(user_list)):
            if user_list[l] == computer_list[l]:
                print(user_list[l] + " is the correct letter!")
            elif user_list[l] in computer_list:
                print(user_list[l] + " is in the wrong position")
            else:
                print(user_list[l] + " is not in the word")

#Here is where they can try again
def repeat_two_to_six(word_options_as_list, computer_list, computer_choice):
    for attempt in range(5):
        user_list = user(word_options_as_list)
        check_win(computer_list, user_list)
    sys.exit("\nUnfortunately, you have not gotten it. Thanks for playing!\nThe correct word was: " + computer_choice)

#Here is where I call the functions to actually happen
play()
cleanup_data(most_recent_words)
computer_choice = computer_as_word(word_options_as_list)
if computer_choice in most_recent_words:
    computer_choice = computer_as_word(word_options_as_list)
most_recent_words = keep_track_of_when_used(computer_choice)
computer_list = computer(computer_choice)
user_list = user(word_options_as_list)
check_win(computer_list, user_list)
repeat_two_to_six(word_options_as_list, computer_list, computer_choice)
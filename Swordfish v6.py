#Wordle.py

#This version includes changes to the font color instead of spelling out the letters place

#imports
import random
import sys
import json
import os
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from word_list_file import word_options_as_list

init()

#Here is where it will check that the user wants to play
def play():
    first_response = input("\nWould you like to play Wordle: ").lower()
    
    if first_response in ["not now", "no", "n"]:
        print("\nAlright, maybe later\n")
        play()
    elif first_response in ["yes", "yeah", "y"]:
        print("\nThe rules are:\n-You have to choose a five letter word\n-You want to guess the same word that the computer chose\n-You have to use real English words\n-Green indicates that it is the right letter\n-Yellow indicates that is in the word, but the wrong location\n-White indicates that it is not in the word\n\nAlright, let's play!")
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

#Here is where the computer word gets split into a list
def computer(computer_choice):
    computer_list = list(computer_choice)
    return computer_list

#Here is where I create the string of the word for the user
def user1(word_options_as_list):
    user_choice = input("\nTry a word: ").lower()
    if user_choice not in word_options_as_list:
        print("That is not a valid word")
        return user1(word_options_as_list)
    else:
        return user_choice

#Here is where the user word is converted to a list
def user2(user_choice):
    user_list = list(user_choice)
    return user_list

#Here is the list of the alphabet that will be motified by available function
unused_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l","m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

#Here is where it will show the user what letters are still available to use
def available(user_list):

    global unused_letters

    for a in user_list:
        if a in unused_letters:
            unused_letters.remove(a)
    print("\n\nThese are the letters that you have not used:\n\n ", unused_letters)

#Here is where we check if the user actually wins or loses
def check_win(computer_list, user_list, user_choice):
    if user_list == computer_list:
        sys.exit(Fore.GREEN + user_choice + Style.RESET_ALL + "\nYou have found the wordle!")
    else:
        for l in range(len(user_list)):
            if user_list[l] == computer_list[l]:
                print(Fore.GREEN + user_list[l] + Style.RESET_ALL, end="")
            elif user_list[l] in computer_list:
                print(Fore.YELLOW + user_list[l] + Style.RESET_ALL, end="")
            else:
                print(user_list[l], end="")
    available(user_list)

#Here is where they can try again
def repeat_two_to_six(word_options_as_list, computer_list, computer_choice):
    for attempt in range(5):
        user_choice = user1(word_options_as_list)
        user_list = user2(user_choice)
        check_win(computer_list, user_list, user_choice)
    sys.exit("\nUnfortunately, you have not gotten it. Thanks for playing!\nThe correct word was: " + computer_choice)

#Here is where I call the functions to actually happen
play()
cleanup_data(most_recent_words)
computer_choice = computer_as_word(word_options_as_list)
if computer_choice in most_recent_words:
    computer_choice = computer_as_word(word_options_as_list)
most_recent_words = keep_track_of_when_used(computer_choice)
computer_list = computer(computer_choice)
user_choice = user1(word_options_as_list)
user_list = user2(user_choice)
check_win(computer_list, user_list, user_choice)
repeat_two_to_six(word_options_as_list, computer_list, computer_choice)
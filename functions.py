from flask import Flask, session
from boggle import Boggle
import time

boggle_game = Boggle()
# make_board = boggle_game.make_board()
# board = copy.deepcopy(make_board)

def create_board():
    """[creates a boggle game board]

    Returns:
        [array of arrays]
    """
    board = boggle_game.make_board()
    return board

def compare_to_dictionary(data):
    """[compares the guesses to the words in the dictionary. Requires json data object as a parameter]
    
        Returns:
            [a list containing only words in the users guessses that were in the dictionary]
    """ 
    guessed_words = []
    guesses = data.get("guesses")
    for i in range(len(guesses)):
        guessed_words.append(guesses.get(f"{i}"))
    guessed_words = set(guessed_words)
    dictionary = set(boggle_game.words)
    correct = guessed_words & dictionary
    correct = list(correct)
    return correct

def not_in_dictionary(data):
    """[compares guesses to words in dictionary]

    Args:
        data ([type] json): [json object gotten from javascript axios post request]

    Returns:
        [a list containing all the words that were not in the dictionary (opposite of compare_to_dictionary)]
    """
    guessed_words = []
    guesses = data.get("guesses")
    for i in range(len(guesses)):
        guessed_words.append(guesses.get(f"{i}"))
    guessed_words = set(guessed_words)
    dictionary = set(boggle_game.words)
    missing_words = guessed_words - dictionary
    missing_words = list(missing_words)
    return missing_words

def not_on_board(data):
    """[compares guesses to words on the board]

    Args:
         data ([type] json): [json object gotten from javascript axios post request]
    Returns:
        [a list of all the words that were not on the board]
    """
    guessed_words = []
    missing = []
    guesses = data.get("guesses")
    for i in range(len(guesses)):
        guessed_words.append(guesses.get(f"{i}"))
    for word in guessed_words:
        if not boggle_game.find(session.get("board"),word.upper()):
            missing.append(word)

    return missing

def compare_to_board(correct):
    """compares guesses to the words on the board

    Args:
        correct ([type] list): [correct is a list returned from the compare_to_dictionary function.
        In other-words, correct is a list containing all the words that are in the dictionary. Now we 
        compare those words to the board]

    Returns:
        [list]: [of all the words on both the board and the dictionary]
    """
    final_correct = []
    for word in correct:
        if boggle_game.find(session.get("board"),word.upper()):
            final_correct.append(word)
    return final_correct
   
def calculate_score(final):
    """[calculates the score for the user based on each length of each correct word]

    Args:
        final ([list]): [final is the list that is returned from compare_to_board function]

    Returns:
        [int]: [a number added from the length of each word]
    """
    sum_arr = []
    for word in final:
        sum_arr.append(len(word))
    score = sum(sum_arr)
    
    return score

# def start_timer():
#     t = 60
#     while t:
#         mins, secs = divmod(t,60)
#         timer = '{:02d}:{:02d}'.format(mins, secs) 
#         time.sleep(1)
#         t-=1
    
    
    
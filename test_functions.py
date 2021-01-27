from unittest import TestCase
from app import app
from functions import boggle_game
from random import choice
import functions
import string
from flask import session
from boggle import Boggle
import json
import copy


class FunctionTests(TestCase):

#     # TODO -- write tests for every view function / feature!
    def setUp(self):
        app.config['TESTING'] = True
    
    def tearDown(self):
        pass
    
    def test_create_board(self):
        """[Tests the create_board function in the functions.py file. Converts the nested array into a single
            array and then creates an array that only allows strings. The length of the array should always be 25 strings]
        """
        board = boggle_game.make_board()
        board_list = [item for sublist in board for item in sublist]
        string_board = [val for val in board_list if isinstance(val,str)]
        self.assertEqual(len(string_board),25)
        
    def test_compare_to_dictionary(self):
        """[Tests the compare_to_dictionary function in the functions.py file]
        """
        
        json_obj = {"data":{"guesses":{"0":"word","1":"help","2":"can"}}}
        
        correct_words = set(functions.compare_to_dictionary(json_obj))
        set_lst = set(["word","help","can"])
       
        self.assertEqual(correct_words & set_lst,{"word","help","can"})
    
    def test_not_in_dictionary(self):
        """[Tests the not_in_dictionary function in functions.py file]
        """
        json_obj1 = {"data":{"guesses":{"0":"sadfasd","1":"help","2":"can"}}}
        
        json_obj2 = {"data":{"guesses":{"0":"sadfasd","1":"hjdfh","2":"jklj"}}}
        missing_words = set(functions.not_in_dictionary(json_obj2))
        set_lst = set(["sadfasd","hjdfh","jklj"])
        
        
        self.assertEqual(functions.not_in_dictionary(json_obj1),["sadfasd"])
        self.assertEqual(missing_words & set_lst,{"sadfasd","hjdfh","jklj"})
        
    def test_calculate_score(self):
        """[Tests the calculate_score function in functions.py]
        """
        
        test_list = ["word","self","has"]
        
        self.assertEqual(functions.calculate_score(test_list),11)
        
    
        

        
        


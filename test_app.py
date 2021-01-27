from unittest import TestCase
from app import app
from functions import boggle_game
import functions
from flask import session
from boggle import Boggle
import json
import copy


class AppTests(TestCase):
    # TODO -- write tests for every view function / feature!
    
    def setUp(self):
        app.config['TESTING'] = True
    def tearDown(self):
        pass
    
    
    def test_start_page(self):
        """[This tests the landing page to make sure we can get the page and 
            the proper HTML is there]
        """
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Let\'s Play Some Boggle!</h1>",html)
    
    def test_new_game(self):
        """[This tests the post request that happens when a user clicks the new game button.
            User should be redirected, code 302]
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["board"] = boggle_game.make_board()
            resp = client.post("/")

            self.assertEqual(resp.status_code, 302)
            
    def test_profile_page(self):
        """[This tests getting the profile page and some of the HTML on the page]
        """
       with app.test_client() as client:
            resp = client.get('/profile')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Your Boggle Profile",html)

    def test_play_game_page_no_board(self):
        """[This test is for if a user trys to access the /play path before ever creating a new game
            at the home page. User should be redirected to the home page, code 302]
        """
        with app.test_client() as client:
            resp = client.get('/play')

            self.assertEqual(resp.status_code, 302)
            
    def test_play_game_page_with_board(self):
        """[This test is for if a user trys to access the /play path after already creating a new game.
            Maybe their game board is still in session or they opened a new tab and went to the path]
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["board"] = boggle_game.make_board()
            resp = client.get('/play')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Type Your Guesses Here:</u></label>",html)
            
    def test_posting_words(self):
        """[This tests four things:
            1. Tests if we get json response when user submits post request of their words
            2. Tests the function not_on_board() in functions.py file
            3. Tests the function compare_to_board() in functions.py file
            4. Tests the function determine_top_score() in the functions.py file]
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["board"] = [['J', 'R', 'O', 'F', 'E'],
                                ['H', 'I', 'L', 'W', 'B'],
                                ['V', 'Y', 'B', 'Q', 'N'],
                                ['U', 'W', 'X', 'M', 'D'],
                                ['B', 'K', 'V', 'Y', 'M']]
                sess["plays"] = 0
            resp = client.post("/play", json={"data":{"guesses":{"0":"word","1":"help","2":"can"}}})
            json_obj = {"data":{"guesses":{"0":"word","1":"help","2":"can"}}}
            correct = ["for","hi","web"]
            self.assertEqual(session.get("top-score"),0)
            score1 = 1
            score2 = 5
            functions.determine_top_score(score1)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(functions.not_on_board(json_obj),["word","help","can"])
            self.assertEqual(functions.compare_to_board(correct),["for","hi","web"])
            self.assertEqual(session["top-score"],1)
            functions.determine_top_score(score2)
            self.assertEqual(session["top-score"],5)
            
    
    
            
    


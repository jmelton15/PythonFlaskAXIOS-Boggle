from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    # TODO -- write tests for every view function / feature!
    def test_start_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Let\'s Play Some Boggle!</h1>",html)
    
    def test_new_game(self):
        with app.test_client() as client:
            resp = client.post("/play")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            self.assertIn("BOGGLE</h1>",html)
            
    def test_play_game_page(self):
        with app.test_client() as client:
            resp = client.get('/play')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("Type Your Guesses Here:</u></label>",html)

    def test_submit_words(self):
         with app.test_client() as client:
            resp = client.post("/play", 
                               data = {'guesses': {0:"asdfasdf"}})
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>asdfasdf</li>",html)
    


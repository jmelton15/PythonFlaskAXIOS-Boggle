from boggle import Boggle
#from functions import not_in_dictionary, not_on_board,compare_to_board,compare_to_dictionary, calculate_score,create_board
import functions 
from flask import Flask, request, render_template, redirect, flash, jsonify, session, Blueprint, Response
#from flask_debugtoolbar import DebugToolbarExtension
#from flask_session import Session
import json
import copy
import mimetypes
mimetypes.add_type('application/javascript', '.mjs')

app = Flask(__name__)
#SESSION_TYPE = 'filesystem'
#app.config.from_object(__name__)
app.config['SECRET_KEY'] = "SUPER-SECRET-CODE"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #set to true if you want to debug
#debug = DebugToolbarExtension(app) #app bcs app name is app
#Session(app)


@app.route('/', methods=["GET","POST"])
def show_start_page():
    """[Shows the landing page where a user can start a new game of boggle]

    Returns:
       if the user is just get requesting the page, it will render the homepage template.'
       Otherwise on a post request (new game button press), it will redirect the user to the 
       play page.
    """
    if request.method == "POST":
        functions.clear_session_variables()
        make_board = functions.create_board()
        board = copy.deepcopy(make_board)
        session["board"] = board
        return redirect("/play")
    else:
        if session.get("plays") is None:
            session["plays"] = 0
        return render_template("homepage.html")

@app.route('/profile', methods=["GET","POST"])
def show_user_profile():
    """[Shows user profile stats such as times played and top score and how many times they played
        will add more data to this as this app is built further]
    """
    return render_template("profile.html")
    

@app.route('/play', methods=["GET","POST"])
def show_game_board():
    """[When a non-post request is recieved on this page, it will just render the play-game template
          which will show the game board. If post request is sent (i.e. submit words button) the server
          will grab the json data that is sent from the javascript axios post request and respond with a 
          python dictionary of data]
    """
    board = session.get('board')
    if request.method == "POST":
        session["score"] = ''
        data = request.get_json()
        session["plays"] += 1
        session["missing-dict"] = functions.not_in_dictionary(data)
        session["missing-board"] = functions.not_on_board(data)
        session["on-board"] = functions.compare_to_board(functions.compare_to_dictionary(data))
        session["score"] = functions.calculate_score(functions.compare_to_board(functions.compare_to_dictionary(data)))
        functions.determine_top_score(session["score"])
        jsonObj = {
            "missing_dict": session.get("missing-dict"),
            "missing_board": session.get("missing-board"),
            "on_board": session.get("on-board"),
            "score": session.get("score")
        }
        return jsonObj
    else:
        return render_template("play-game.html", board=board)
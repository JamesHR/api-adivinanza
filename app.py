from flask import Flask
from controllers.game_controller import register_user, login_user, start_game, guess_number, get_status, restart_game, get_statistics, get_leaderboard
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Rutas
app.route('/register', methods=['POST'])(register_user)
app.route('/login', methods=['POST'])(login_user)
app.route('/start', methods=['POST'])(start_game)
app.route('/guess', methods=['POST'])(guess_number)
app.route('/status', methods=['GET'])(get_status)
app.route('/restart', methods=['POST'])(restart_game)
app.route('/statistics', methods=['GET'])(get_statistics)
app.route('/leaderboard', methods=['GET'])(get_leaderboard)

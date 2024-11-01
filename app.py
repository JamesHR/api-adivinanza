from flask import Flask
from controllers.game_controller import start_game, guess_number, get_status, restart_game

app = Flask(__name__)

# Rutas
app.route('/start', methods=['POST'])(start_game)
app.route('/guess/<int:numero>', methods=['POST'])(guess_number)
app.route('/status', methods=['GET'])(get_status)
app.route('/restart', methods=['POST'])(restart_game)

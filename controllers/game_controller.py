from flask import jsonify, request
from models.game_model import GameModel

def start_game():
    estado = GameModel.reiniciar_juego()
    return jsonify({"message": "¡El juego ha comenzado! Adivina un número entre 1 y 100."})

def guess_number(numero):
    estado = GameModel.cargar_estado()
    estado["intentos"] += 1

    numero_secreto = estado["numero_secreto"]

    if numero < numero_secreto:
        respuesta = "Muy bajo"
    elif numero > numero_secreto:
        respuesta = "Muy alto"
    else:
        respuesta = f"¡Correcto! Adivinaste en {estado['intentos']} intentos."

    GameModel.guardar_estado(estado)
    return jsonify({"message": respuesta})

def get_status():
    estado = GameModel.cargar_estado()
    return jsonify({
        "intentos": estado["intentos"],
        "message": "Sigue intentando, ¡puedes hacerlo!"
    })

def restart_game():
    GameModel.reiniciar_juego()
    return jsonify({"message": "¡El juego se ha reiniciado! Adivina el nuevo número."})

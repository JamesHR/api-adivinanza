from flask import jsonify, request
from models.game_model import GameModel

def start_game():
    estado = GameModel.reiniciar_juego()
    return jsonify({"message": "¡El juego ha comenzado! Adivina un número entre 1 y 100."}), 201

def guess_number(numero):
    estado = GameModel.cargar_estado()

    if not estado.get("juego_activo"):
        return jsonify({"message": "El juego ya ha terminado. Reinicia el juego para volver a jugar."}), 400

    estado["intentos"] += 1
    numero_secreto = estado["numero_secreto"]

    if numero < numero_secreto:
        respuesta = "Muy bajo"
    elif numero > numero_secreto:
        respuesta = "Muy alto"
    else:
        respuesta = f"¡Correcto! Adivinaste en {estado['intentos']} intentos."
        estado["juego_activo"] = False
        GameModel.guardar_estado(estado)
        return jsonify({"message": respuesta}), 200

    GameModel.guardar_estado(estado)
    return jsonify({"message": respuesta}), 200

def get_status():
    estado = GameModel.cargar_estado()
    if estado.get("juego_activo"):
        message = "Sigue intentando, ¡puedes hacerlo!"
        return jsonify({
            "intentos": estado["intentos"],
            "message": message
        }), 200
    else:
        message = "El juego ha terminado. Reinicia el juego para volver a jugar."
        return jsonify({
            "intentos": estado["intentos"],
            "message": message
        }), 400

def restart_game():
    GameModel.reiniciar_juego()
    return jsonify({"message": "¡El juego se ha reiniciado! Adivina el nuevo número."}), 201

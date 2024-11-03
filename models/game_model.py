import json
import random

class GameModel:
    DATA_FILE = 'data.json'

    @staticmethod
    def guardar_estado(estado):
        with open(GameModel.DATA_FILE, 'w') as f:
            json.dump(estado, f)

    @staticmethod
    def cargar_estado():
        try:
            with open(GameModel.DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            estado_inicial = {"numero_secreto": 0, "intentos": 0, "juego_activo": False}
            GameModel.guardar_estado(estado_inicial)
            return estado_inicial

    @staticmethod
    def reiniciar_juego():
        estado = {
            "numero_secreto": random.randint(1, 100),
            "intentos": 0,
            "juego_activo": True
        }
        GameModel.guardar_estado(estado)
        return estado

import json
import random
import bcrypt
import os

from dotenv import load_dotenv

load_dotenv()
MAX_NUMBER = int(os.environ.get('MAX_NUMBER'))

class GameModel:
    DATA_FILE = 'data.json'

    @staticmethod
    def guardar_datos(datos):
        with open(GameModel.DATA_FILE, 'w') as f:
            json.dump(datos, f)

    @staticmethod
    def cargar_datos():
        try:
            with open(GameModel.DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            datos_iniciales = {}
            GameModel.guardar_datos(datos_iniciales)
            return datos_iniciales

    @staticmethod
    def crear_perfil(usuario, correo, password):
        datos = GameModel.cargar_datos()

        if usuario in datos:
            return "usuario_existente"

        for perfil in datos.values():
            if perfil["correo"] == correo:
                return "correo_existente"

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        datos[usuario] = {
            "correo": correo,
            "password": hashed_password,
            "numero_secreto": random.randint(1, MAX_NUMBER),
            "intentos": 0,
            "juego_activo": True
        }
        GameModel.guardar_datos(datos)
        return "perfil_creado"

    @staticmethod
    def verificar_credenciales(usuario, password):
        datos = GameModel.cargar_datos()
        perfil = datos.get(usuario)

        if perfil and bcrypt.checkpw(password.encode(), perfil["password"].encode()):
            return True
        return False

    @staticmethod
    def cargar_estado(usuario):
        datos = GameModel.cargar_datos()
        return datos.get(usuario)

    @staticmethod
    def guardar_estado(usuario, estado):
        datos = GameModel.cargar_datos()
        datos[usuario] = estado
        GameModel.guardar_datos(datos)

    @staticmethod
    def reiniciar_juego(usuario):
        estado = {
            "correo": GameModel.cargar_estado(usuario)["correo"],
            "password": GameModel.cargar_estado(usuario)["password"],
            "numero_secreto": random.randint(1, MAX_NUMBER),
            "intentos": 0,
            "juego_activo": True
        }
        GameModel.guardar_estado(usuario, estado)
        return estado

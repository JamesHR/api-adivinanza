import json
import random
import bcrypt
import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MAX_NUMBER = int(os.environ.get('MAX_NUMBER'))
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
adivinanza_collection = db['adivinanza']

class GameModel:
    @staticmethod
    def crear_perfil(usuario, correo, password):
        # Verificar si el usuario o el correo ya existen
        if adivinanza_collection.find_one({"usuario": usuario}):
            return "usuario_existente"
        if adivinanza_collection.find_one({"correo": correo}):
            return "correo_existente"
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Crear perfil
        perfil = {
            "usuario": usuario,
            "correo": correo,
            "password": hashed_password,
            "numero_secreto": random.randint(1, MAX_NUMBER),
            "intentos": 0,
            "juego_activo": True,
            "partidas_jugadas": 0,
            "puntos": 0
        }
        adivinanza_collection.insert_one(perfil)
        return "perfil_creado"

    @staticmethod
    def verificar_credenciales(usuario, password):
        perfil = adivinanza_collection.find_one({"usuario": usuario})
        if perfil and bcrypt.checkpw(password.encode(), perfil["password"].encode()):
            return True
        return False

    @staticmethod
    def cargar_estado(usuario):
        return adivinanza_collection.find_one({"usuario": usuario}, {"_id": 0})

    @staticmethod
    def guardar_estado(usuario, estado):
        adivinanza_collection.update_one(
            {"usuario": usuario},
            {"$set": estado}
        )

    @staticmethod
    def reiniciar_juego(usuario):
        nuevo_estado = {
            "numero_secreto": random.randint(1, MAX_NUMBER),
            "intentos": 0,
            "juego_activo": True
        }
        adivinanza_collection.update_one(
            {"usuario": usuario},
            {"$set": nuevo_estado}
        )
        return GameModel.cargar_estado(usuario)

    @staticmethod
    def actualizar_estadisticas(usuario, intentos):
        perfil = adivinanza_collection.find_one({"usuario": usuario})
        if perfil:
            puntos = perfil["puntos"]
            partidas_jugadas = perfil["partidas_jugadas"] + 1
            if intentos <= 5:
                puntos += 5
            elif 6 <= intentos <= 10:
                puntos += 3
            else:
                puntos += 1

            adivinanza_collection.update_one(
                {"usuario": usuario},
                {"$set": {
                    "partidas_jugadas": partidas_jugadas,
                    "puntos": puntos,
                    "juego_activo": False
                }}
            )
            return GameModel.cargar_estado(usuario)
        return None

    @staticmethod
    def obtener_leaderboard():
        # Obtener y ordenar los usuarios por puntos desde MongoDB
        leaderboard = list(adivinanza_collection.find({}, {"_id": 0, "usuario": 1, "puntos": 1, "partidas_jugadas": 1}))
        leaderboard.sort(key=lambda x: x["puntos"], reverse=True)
        return leaderboard
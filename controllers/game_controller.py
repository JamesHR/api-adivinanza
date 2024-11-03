import jwt
import os
from datetime import datetime, timedelta
from flask import jsonify, request
from models.game_model import GameModel
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
MAX_NUMBER = int(os.environ.get('MAX_NUMBER'))

def generate_token(usuario):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"usuario": usuario, "exp": expiration}, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["usuario"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user():
    data = request.get_json()
    usuario = data.get("usuario")
    correo = data.get("correo")
    password = data.get("password")

    if not usuario or not correo or not password:
        return jsonify({"message": "Se requiere nombre de usuario, correo y contraseña para registrarse."}), 400

    resultado = GameModel.crear_perfil(usuario, correo, password)
    
    if resultado == "perfil_creado":
        return jsonify({"message": f"Perfil creado para el usuario '{usuario}' con correo '{correo}'."}), 201
    elif resultado == "usuario_existente":
        return jsonify({"message": f"El nombre de usuario '{usuario}' ya está en uso. Intenta con otro nombre de usuario."}), 409
    elif resultado == "correo_existente":
        return jsonify({"message": f"El correo '{correo}' ya está en uso. Intenta con otro correo o inicia sesión"}), 409

def login_user():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"message": "Se requiere nombre de usuario y contraseña para iniciar sesión."}), 400

    if GameModel.verificar_credenciales(usuario, password):
        token = generate_token(usuario)
        return jsonify({"message": f"Inicio de sesión exitoso para el usuario '{usuario}'.", "token": token}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas. Verifica tu nombre de usuario y contraseña."}), 401

def start_game():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    usuario = verify_token(token)

    if not usuario:
        return jsonify({"message": "Token no válido o expirado. Inicia sesión nuevamente."}), 401

    estado = GameModel.reiniciar_juego(usuario)
    return jsonify({"message": f"¡El juego ha comenzado para {usuario}! Adivina un número entre 1 y {MAX_NUMBER}."}), 201

def guess_number():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    usuario = verify_token(token)

    if not usuario:
        return jsonify({"message": "Token no válido o expirado. Inicia sesión nuevamente."}), 401

    data = request.get_json()
    numero = data.get("numero")
    
    if numero is None:
        return jsonify({"message": "Se requiere un número para adivinar."}), 400

    estado = GameModel.cargar_estado(usuario)
    
    if not estado:
        return jsonify({"message": f"No se encontró el perfil para el usuario '{usuario}'. Regístrate primero."}), 404

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
        estado = GameModel.actualizar_estadisticas(usuario, estado["intentos"])
        estado["juego_activo"] = False

    GameModel.guardar_estado(usuario, estado)
    return jsonify({"message": respuesta}), 200

def get_status():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    usuario = verify_token(token)

    if not usuario:
        return jsonify({"message": "Token no válido o expirado. Inicia sesión nuevamente."}), 401

    estado = GameModel.cargar_estado(usuario)
    
    if not estado:
        return jsonify({"message": f"No se encontró el perfil para el usuario '{usuario}'. Regístrate primero."}), 404

    if estado.get("juego_activo"):
        message = "Sigue intentando, ¡puedes hacerlo!"
    else:
        message = "El juego ha terminado. Reinicia el juego para volver a jugar."
        
    return jsonify({
        "intentos": estado["intentos"],
        "message": message
    }), 200

def restart_game():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    usuario = verify_token(token)

    if not usuario:
        return jsonify({"message": "Token no válido o expirado. Inicia sesión nuevamente."}), 401

    estado = GameModel.reiniciar_juego(usuario)
    return jsonify({"message": f"¡El juego se ha reiniciado para {usuario}! Adivina el nuevo número."}), 201

def get_statistics():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    usuario = verify_token(token)

    if not usuario:
        return jsonify({"message": "Token no válido o expirado. Inicia sesión nuevamente."}), 401

    estado = GameModel.cargar_estado(usuario)
    
    if not estado:
        return jsonify({"message": f"No se encontró el perfil para el usuario '{usuario}'. Regístrate primero."}), 404

    return jsonify({
        "usuario": usuario,
        "partidas_jugadas": estado["partidas_jugadas"],
        "puntos": estado["puntos"]
    }), 200

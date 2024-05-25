import time
import json
import uuid
import sys
import datetime
import os

from environment import config
from processors.login import crear_usuario, login

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token

# Variables app Flask
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # Acepta dede todas las direcciones con el *
app.config['JWT_SECRET_KEY'] = config.get_jwt_secret_key()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=40)
jwt = JWTManager(app)

tstart = None
json_data = ''


@app.route('/',methods=['GET'])
def get():
    return 'Bienvenido al Servidor de UNIVERSICLETA'

@app.route('/',methods=['POST'])
def executor():
    global json_data, tstart
    global json_data, tstart
    print('\n* NUEVA SOLICITUD')
    print('* HORA: ',time.localtime().tm_hour,':',time.localtime().tm_min,':',time.localtime().tm_sec)
    tstart= time.time()
    json_data = request.json

    if json_data['action'] == 'login':
        try:
            print("** NUEVO INICIO DE SESIÓN")
            usuario_login = json_data["username"]
            password_login = json_data["password"]
            inicio_sesion = login(usuario_login, password_login)
            return inicio_sesion
        except   Exception as e:
            print(e)    
            return jsonify({'error':'Error en la solicitud de inicio de sesión'}) 
        
    return jsonify({'error': 'Acción no válida'}), 400   

if __name__ == '__main__':
    app.run(host = config.get_server_url(), port = config.get_server_port(), debug=True)
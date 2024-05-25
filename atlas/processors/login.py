import hashlib
import time
import uuid
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
import processors.personas as personas

def login(user, password):
    pass_hash =hashear_contraseña(password)
    usuario_registrado = personas.buscar_usuario(user)
    if usuario_registrado != False:
            if usuario_registrado['contrasena'] == pass_hash:
                print('** INICIO DE SESIÓN EXITOSO')
                role = usuario_registrado["rol"]
                acces_token = create_access_token(identity=user)
                return jsonify({"login": "ok", "acces_token": acces_token , "role": role})
            else:
                print('** ERROR CONTRASEÑA')
                return jsonify({"error": "Contraseña no  válida"})
    else:
        print('** ERROR USUARIO NO ENCONTRADO')
        return jsonify({"error": "Usuario no válido"})
    
def hashear_contraseña(password):
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()


def token_info():
    # Obtener la identidad del usuario del token
    current_user = get_jwt_identity()
    # Obtener el tiempo de expiración del token
    exp_time = get_jwt()['exp']
    # Calcular el tiempo restante antes de la expiración del token (en segundos)
    remaining_time = exp_time - time.time()
    # Devolver la información al cliente
    return jsonify(logged_in_as=current_user, expires_in=remaining_time), 200


def crear_usuario(datos):
     usuario_nuevo = datos
     usuario_nuevo["id"] = str(uuid.uuid4())
     contrasena_hasehada = hashear_contraseña(usuario_nuevo["contrasena"])
     usuario_nuevo["contrasena"] = contrasena_hasehada
     usuarios_existentes = personas.cargar_usuarios()
     usuarios_existentes["usuarios"].append(usuario_nuevo)
     personas.actualizar_base_usuarios(usuarios_existentes)
     return {"respuesta" : "Usuario Creado Exitosamente" }
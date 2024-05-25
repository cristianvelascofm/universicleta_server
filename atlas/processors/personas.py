import json

def cargar_usuarios():
    print('CARGAR')
    try:
        with open('opt/data/general/personas/usuarios.json', 'r', encoding='utf-8') as archivo:
            casa = json.load(archivo)
            print('aja ',casa)
            return casa
    except FileNotFoundError as e:
        print('error', e)
        return {"error": e}  



def buscar_usuario(nombre_usuario):
    print('** BUSCANDO USUARIOS')
    usuarios_existentes = cargar_usuarios()
    print('Usuarios: ',  usuarios_existentes)
    if  "error" in usuarios_existentes:
        return False
    else:
        for usuario in usuarios_existentes["usuarios"]:
            print('Usuario: ',  nombre_usuario)
            if usuario["usuario"] == nombre_usuario:
                return usuario
    return False


def actualizar_base_usuarios(datos):
    with open('opt/data/general/personas/usuarios.json', 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo)
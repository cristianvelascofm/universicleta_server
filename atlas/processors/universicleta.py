import json
import aiohttp
import asyncio
from quart import Quart, jsonify, request

from atlas.processors.gestion_esp import comunicar_esp
app = Quart(__name__)

async def comunicacion_8266(msg):
    try:
        with open('opt/data/general/universicleta/estaciones.json', 'r', encoding='utf-8') as archivo:
            estaciones = json.load(archivo)["estaciones"]

            estacion_prueba = estaciones[0]
            ip_estacion = estacion_prueba["ip_base"]
            puerto_estacion = estacion_prueba["puerto"]

            # Construir la URL
            url = f"http://{ip_estacion}:{puerto_estacion}/"

            # Enviar el mensaje usando una solicitud HTTP POST asíncrona
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data="vacio") as response:
                    if response.status == 200:
                        print("Mensaje enviado con éxito")
                        return {"status": "ok"}
                    else:
                        print("Error al enviar el mensaje", response.status)
                        return {"status": "error"}
            
    except FileNotFoundError as e:
        print('Error al encontrar el archivo:', e)
        return {"error": str(e)}
    except aiohttp.ClientError as e:
        print('Error al enviar la solicitud HTTP:', e)
        return {"error": str(e)}

# Función principal para ejecutar la función asíncrona



def obtener_estaciones():
    with open('opt/data/general/universicleta/estaciones.json', 'r', encoding='utf-8') as archivo:
        estaciones = json.load(archivo)["estaciones"]
        return estaciones
    


def reservar_bicicleta(estacion_inicial):
    try:
        with open('opt/data/general/universicleta/estaciones.json', 'r', encoding='utf-8') as archivo:
            estaciones = json.load(archivo)["estaciones"]
            for estacion in estaciones:
                if estacion["id"] == estacion_inicial:
                    anclajes = estacion["anclajes"]
                    for anclaje in anclajes:
                        if anclaje["estado"] == "disponible":
                            bicicleta = comunicar_esp(anclaje["ip_anclaje"])
                            if comunicar_esp:
                                return {
                                    "bicicleta": bicicleta,
                                    "anclaje": anclaje
                                }
                        else:
                            print("** ANCLAJE NO DISPONIBLE")
                            return {
                                "error": "Anclaje no disponible"
                            }
                else:
                    return {
                        "error": "Estación no encontrada"
                    }
    except FileNotFoundError as e:
        print('Error al encontrar el archivo:', e)
        return {"error": str(e)}
    except aiohttp.ClientError as e:
        print('Error al enviar la solicitud HTTP:', e)
        return {"error": str(e)}                   



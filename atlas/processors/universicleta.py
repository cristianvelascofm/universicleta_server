import json
import aiohttp
import asyncio
from quart import Quart, jsonify, request
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
                async with session.post(url, data={'message': msg}) as response:
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


import json
import aiohttp
import requests

async def comunicar_esp(ip_anclaje):
    try:
        url = f"http://{ip_anclaje}/"

        async with aiohttp.ClientSession() as session:
                async with session.post(url, data="vacio") as response:
                    if response.status == 200:
                        bicicleta_tag_id = response.content["tag"]
                        with open('opt/data/general/universicleta/bicicletas.json', 'r', encoding='utf-8') as archivo:
                             bicicletas = json.load(archivo)["bicicletas"]
                             for bicicleta in bicicletas:
                                 if bicicleta["tag_id"] == bicicleta_tag_id:
                                    return bicicleta
                    else:
                        print("Error al enviar el mensaje", response.status)
                        return False
    except aiohttp.ClientError as e:
        print('Error al enviar la solicitud HTTP:', e)
        return {"error": str(e)}
    pass

import requests

TOKEN = "8848025045:AAHjnGaYeoYFYNUVUuhvRWEfsOGwOqXIJLQ"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

respuesta = requests.get(url)

datos = respuesta.json()

print(datos)

import random
import time
import os
import threading
import Pyro4
import requests

# =================================
# CONFIGURACIÓN LOCAL
# =================================
IP_SERVIDOR = "127.0.0.1"
PUERTO = 50000

URL_BASE_DATOS = "http://127.0.0.1:5001"

# Únicamente requerimos el Token y el Chat ID de Telegram
TOKEN = "8848025045:AAHjnGaYeoYFYNUVUuhvRWEfsOGwOqXIJLQ"
CHAT_ID = "8898908251"

codigos = {}
intentos = {}
intentos_mfa = {}
bloqueados = {}
lock = threading.RLock()

def consultar_base_datos(endpoint, datos):
    try:
        respuesta = requests.post(
            f"{URL_BASE_DATOS}/{endpoint}",
            json=datos,
            timeout=5
        )
        return respuesta.json()
    except requests.RequestException:
        return {"estado": "error", "mensaje": "No se pudo conectar con la base de datos (Flask)."}

@Pyro4.expose
class Servidor:

    def registrar_usuario(self, usuario, password):
        return consultar_base_datos("registrar", {"usuario": usuario, "password": password})

    def iniciar_sesion(self, usuario, password):
        with lock:
            if usuario in bloqueados:
                if time.time() < bloqueados[usuario]:
                    tiempo = int(bloqueados[usuario] - time.time())
                    return {
                        "estado": "bloqueado",
                        "mensaje": f"Usuario bloqueado. Espera {tiempo} segundos."
                    }
                else:
                    del bloqueados[usuario]

            respuesta = consultar_base_datos("validar", {"usuario": usuario, "password": password})

            if respuesta.get("estado") == "error" and "No se pudo conectar" in respuesta.get("mensaje", ""):
                return respuesta

            if respuesta.get("estado") != "ok":
                intentos[usuario] = intentos.get(usuario, 0) + 1
                restantes = 3 - intentos[usuario]

                if intentos[usuario] >= 3:
                    bloqueados[usuario] = time.time() + 60
                    intentos[usuario] = 0
                    return {
                        "estado": "bloqueado",
                        "mensaje": "Demasiados intentos. Usuario bloqueado durante 60 segundos."
                    }

                return {
                    "estado": "error",
                    "mensaje": f"Usuario o contraseña incorrectos. Te quedan {restantes} intentos."
                }

            intentos[usuario] = 0
            codigo = str(random.SystemRandom().randint(100000, 999999))
            
            codigos[usuario] = {
                "codigo": codigo,
                "expira": time.time() + 180
            }
            intentos_mfa[usuario] = 0

            # Enviar a Telegram al chat configurado de tu amigo
            try:
                resp_tel = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text": f"Usuario intentando acceder: {usuario}\nTu código MFA es: {codigo}\nVálido por 3 minutos."
                    },
                    timeout=10
                )
                if not resp_tel.ok or not resp_tel.json().get("ok"):
                    codigos.pop(usuario, None)
                    return {"estado": "error", "mensaje": "No se pudo enviar el código a Telegram."}
            except requests.RequestException:
                codigos.pop(usuario, None)
                return {"estado": "error", "mensaje": "Error de conexión con Telegram."}

            return {
                "estado": "ok",
                "mensaje": "Credenciales correctas. Código enviado correctamente a Telegram."
            }

    def verificar_codigo_mfa(self, usuario, codigo):
        with lock:
            if usuario not in codigos:
                return {"estado": "error", "mensaje": "No existe un código activo para este usuario."}

            if time.time() > codigos[usuario]["expira"]:
                del codigos[usuario]
                intentos_mfa.pop(usuario, None)
                return {"estado": "expirado", "mensaje": "El código MFA ha expirado."}

            if codigos[usuario]["codigo"] != codigo:
                intentos_mfa[usuario] = intentos_mfa.get(usuario, 0) + 1
                restantes = 3 - intentos_mfa[usuario]

                if intentos_mfa[usuario] >= 3:
                    del codigos[usuario]
                    intentos_mfa.pop(usuario, None)
                    return {"estado": "bloqueado", "mensaje": "Demasiados códigos incorrectos. Debe iniciar sesión nuevamente."}

                return {"estado": "error", "mensaje": f"Código MFA incorrecto. Te quedan {restantes} intentos."}

            del codigos[usuario]
            intentos_mfa.pop(usuario, None)
            return {"estado": "ok", "mensaje": "¡Autenticación exitosa! Bienvenido al sistema."}

if __name__ == "__main__":
    daemon = Pyro4.Daemon(host=IP_SERVIDOR, port=PUERTO)
    daemon.register(Servidor(), objectId="servidor")
    
    print("====================================")
    print("    SERVIDOR MFA LOCAL INICIADO     ")
    print("====================================")
    print(f"Pyro4 URI fija: PYRO:servidor@{IP_SERVIDOR}:{PUERTO}")
    print("====================================\n")
    daemon.requestLoop()
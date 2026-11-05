import Pyro4


def main():
  try:
    # Localizar el Name Server
    ns = Pyro4.locateNS()
    uri = ns.lookup("practica.mensajeria")
    print(f"[Cliente] Conectado al servicio a través del Name Server.")

    # Crear un proxy para interactuar con el servicio remoto
    servicio = Pyro4.Proxy(uri)

    print("\n" + "=" * 45)
    print("   SISTEMA DE MENSAJERÍA - CLIENTE INTERACTIVO")
    print("   Escribe tu mensaje y presiona Enter.")
    print("   Escribe 'salir' para cerrar la conexión.")
    print("=" * 45 + "\n")

    while True:
      mensaje = input("Tú: ")
      if mensaje.lower() == "salir":
        print("[Cliente] Cerrando sesión...")
        break
      if not mensaje.strip():
        continue

      # Enviar mensaje al servidor remoto
      respuesta = servicio.enviar_mensaje(mensaje)
      print(f"Servidor -> {respuesta}\n")

  except Exception as e:
    print(f"[Cliente] Ocurrió un error: {e}")


if __name__ == "__main__":
  main()
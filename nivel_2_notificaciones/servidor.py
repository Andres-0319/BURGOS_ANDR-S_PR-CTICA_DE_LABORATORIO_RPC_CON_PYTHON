import Pyro4

# Configuramos el servidor para que acepte múltiples clientes concurrentemente usando hilos
Pyro4.config.SERVERTYPE = "thread"


@Pyro4.expose
class ServicioMensajes:

  def enviar_mensaje(self, mensaje):
    print(f"[Servidor] Mensaje recibido: {mensaje}")
    return f"Procesado con éxito: '{mensaje}'"


def main():
  # Iniciar el daemon de Pyro4
  daemon = Pyro4.Daemon()

  # Registrar la clase como un objeto remoto
  uri = daemon.register(ServicioMensajes)

  # Localizar el Name Server y registrar el servicio
  ns = Pyro4.locateNS()
  ns.register("practica.mensajeria", uri)

  print("[Servidor] ¡Servidor listo y preparado para múltiples clientes!")
  print("[Servidor] Registrado en el Name Server como: practica.mensajeria")

  # Iniciar el bucle de peticiones
  daemon.requestLoop()


if __name__ == "__main__":
  main()
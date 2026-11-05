import Pyro4
import time

@Pyro4.expose
class Procesador:

    def procesar_datos(self, cantidad):
        print("Servidor: Iniciando procesamiento...")

        resultado = 0

        for i in range(cantidad):
            resultado += i ** 2

        time.sleep(5)

        print("Servidor: Procesamiento terminado.")

        return resultado


daemon = Pyro4.Daemon()

uri = daemon.register(Procesador)

print("Servidor iniciado correctamente.")
print("URI del servidor:", uri)

daemon.requestLoop()

import Pyro4

@Pyro4.expose
class Calculadora(object):

    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b == 0:
            return "Error: No se puede dividir entre cero"
        return a / b


daemon = Pyro4.Daemon()

ns = Pyro4.locateNS()

uri = daemon.register(Calculadora)

ns.register("calculadora", uri)

print("Servidor de calculadora listo.")
print("Esperando solicitudes del cliente...")

daemon.requestLoop()

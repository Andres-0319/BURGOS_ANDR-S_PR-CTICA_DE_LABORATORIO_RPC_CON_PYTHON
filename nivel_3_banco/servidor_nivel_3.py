import Pyro4

@Pyro4.expose
class saldo_insuficiente(Exception):
    pass

@Pyro4.behavior(instance_mode="session")
@Pyro4.expose
class nivel_3(object):
    def __init__(self):
        self.saldo = 0.0

    def solicitar_numero(self, mensaje):
        while True:
            try:
                return float(input(mensaje))
            except ValueError:
                print("Error. No se puede ingresar cantidades negativas")

    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            return f"Deposito realizado con éxito. Saldo Actual: {self.saldo}"
        else:
            return f"No se puede ingresar cantidades negativas o cero. Intentelo de nuevo."

    def retirar(self, cantidad):
        if cantidad > self.saldo:
            raise saldo_insuficiente(f"Fondos insuficientes. Saldo Actual: {self.saldo}, Intento de retiro: {cantidad}")
        if cantidad > 0:
            self.saldo -= cantidad
            return f"Retiro realizado con éxito. Saldo Actual: {self.saldo}"
        else:
            return f"No se puede retirar cantidades negativas o cero. Intentelo de nuevo."

    def consultar_saldo(self):
        return self.saldo

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(nivel_3)   # register the greeting maker as a Pyro object
ns.register("nivel_3", uri)   # register the object with a name in the name server

print("Ready. Servidor nivel 3 activo")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
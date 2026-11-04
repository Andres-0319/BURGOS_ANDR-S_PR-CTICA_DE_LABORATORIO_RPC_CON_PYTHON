import Pyro4 
import time

uri = input("Ingrese la URI del servidor: ")

servidor = Pyro4.Proxy(uri)

servidor._pyroAsync()

print("\nCliente: Enviando solicitud de procesamiento...")

future = servidor.procesar_datos(1000000)

print("Cliente: Solicitud enviada correctamente.")

for i in range(5): print("Cliente: Realizando otras tareas...", i + 1) 
time.sleep(1)

print("\nCliente: Esperando el resultado...")

resultado = future.value

print("\nResultado recibido del servidor:", resultado)

print("Cliente: Proceso finalizado.")
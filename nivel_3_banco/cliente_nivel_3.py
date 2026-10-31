# saved as greeting-client.py
import Pyro4

name = input("¿Cuál es tu nombre? ").strip()

nivel_3 = Pyro4.Proxy("PYRONAME:nivel_3")    # use name server object lookup uri shortcut

while True:
    print("Nivel 3: Banco Distribuido y Control de Estado (Stateful Services)")
    print("1.- Depositar")
    print("2.- Retirar")
    print("3.- Cosulta de saldo")
    print("4.- Salir")

    try:
        op = int(input("Seleccione una opción: "))
    except ValueError:
        print("Error. Ingrese un número válido")
        continue

    if op == 1:
        cantidad = float(input("INGRESE LA CANTIDAD A DEPOSITAR: "))
        resultado = nivel_3.depositar(cantidad)
        print(resultado)
    elif op == 2:
        cantidad = float(input("INGRESE LA CANTIDAD A RETIRAR: "))
        try:
            resultado = nivel_3.retirar(cantidad)
            print(resultado)
        except Exception as e:
            print(f"Excepción remota capturada: {e}")
    elif op == 3:
        saldo_actual = nivel_3.consultar_saldo()
        print(f"Tu saldo actual es de: {saldo_actual}")
    elif op == 4:
        print("Saliendo del sistema...")
        break
    else:
        print("Opción no válida. Intentelo de nuevo")
import Pyro4

# Conectarse a la calculadora remota
calculadora = Pyro4.Proxy("PYRONAME:calculadora")

while True:
    print("\n===== CALCULADORA CON PYRO4 =====")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Salir")

    opcion = input("Seleccione una opcion: ")

    if opcion == "5":
        print("Saliendo de la calculadora...")
        break

    if opcion not in ("1", "2", "3", "4"):
        print("Opcion no valida. Intente nuevamente.")
        continue

    try:
        a = float(input("Ingrese el primer numero: "))
        b = float(input("Ingrese el segundo numero: "))

        if opcion == "1":
            resultado = calculadora.sumar(a, b)

        elif opcion == "2":
            resultado = calculadora.restar(a, b)

        elif opcion == "3":
            resultado = calculadora.multiplicar(a, b)

        elif opcion == "4":
            resultado = calculadora.dividir(a, b)

        print("Resultado:", resultado)

    except ValueError:
        print("Error: debe ingresar numeros validos.")

    except Pyro4.errors.CommunicationError:
        print("Error: no se pudo comunicar con el servidor.")
        break

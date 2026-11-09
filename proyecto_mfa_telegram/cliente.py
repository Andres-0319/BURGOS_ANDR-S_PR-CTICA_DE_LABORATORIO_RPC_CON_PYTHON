import Pyro4
from getpass import getpass

# Conexión local fija al servidor MFA
servidor = Pyro4.Proxy("PYRO:servidor@127.0.0.1:50000")

def menu():
    while True:
        print("\n================================")
        print("      SISTEMA MFA (LOCAL)       ")
        print("================================")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        print("================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n===== REGISTRO DE USUARIO =====")
            usuario = input("Ingrese usuario: ")
            password = getpass("Ingrese contraseña (mínimo 8 caracteres): ")
            try:
                respuesta = servidor.registrar_usuario(usuario, password)
                print("\n" + respuesta["mensaje"])
            except Exception as e:
                print("\nError durante el registro:", e)

        elif opcion == "2":
            print("\n===== INICIO DE SESIÓN =====")
            usuario = input("Ingrese usuario: ")
            password = getpass("Ingrese contraseña: ")

            try:
                respuesta = servidor.iniciar_sesion(usuario, password)
                print("\n" + respuesta["mensaje"])

                if respuesta["estado"] != "ok":
                    continue

                # Verificación MFA
                print("\n===== VERIFICACIÓN MFA =====")
                while True:
                    codigo = input("Ingrese el código de 6 dígitos recibido en Telegram: ").strip()
                    resultado = servidor.verificar_codigo_mfa(usuario, codigo)
                    print("\n" + resultado["mensaje"])

                    if resultado["estado"] in ("ok", "bloqueado", "expirado"):
                        break
            except Exception as e:
                print("\nError durante el inicio de sesión:", e)

        elif opcion == "3":
            print("\nGracias por utilizar el sistema MFA.")
            break
        else:
            print("\nOpción incorrecta. Intente nuevamente.")

if __name__ == "__main__":
    try:
        print("\nConectando con el servidor MFA local...")
        menu()
    except Pyro4.errors.CommunicationError:
        print("\nERROR: No se pudo conectar con el servidor MFA. Asegúrate de iniciar servidor.py.")
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
    finally:
        servidor._pyroRelease()
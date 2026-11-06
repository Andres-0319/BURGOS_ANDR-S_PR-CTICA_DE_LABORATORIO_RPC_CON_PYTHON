import Pyro4
import threading


# ==========================================
# CONFIGURACIÓN
# ==========================================

IP_SERVIDOR = "172.17.44.71"
PUERTO_NS = 9090
NOMBRE_SUBASTA = "subastas.central"

detener = threading.Event()
servidor = None
producto_seleccionado = None
hilo_monitoreo = None
evento_monitoreo = None


# ==========================================
# CONECTAR CON EL SERVIDOR
# ==========================================

def conectar_servidor():
    ns = Pyro4.locateNS(
        host="172.17.44.71",
        port=9090
    )

    return Pyro4.Proxy(ns.lookup(NOMBRE_SUBASTA))


# ==========================================
# MOSTRAR INFORMACIÓN DE UN PRODUCTO
# ==========================================

def mostrar_estado(estado):
    print("\n========== ESTADO DE SUBASTA ==========")
    print("Producto:", estado["producto"])
    print("Precio inicial: $", estado["precio_inicial"])
    print("Precio actual: $", estado["precio_actual"])
    print("Mejor postor:", estado["mejor_postor"])
    print("Tiempo restante:", estado["tiempo_restante"], "segundos")

    print(
        "Estado:",
        "SUBASTA ABIERTA" if estado["abierta"] else "SUBASTA FINALIZADA"
    )

    print("=======================================")


# ==========================================
# MOSTRAR PRODUCTOS DISPONIBLES
# ==========================================

def mostrar_productos():
    try:
        productos = servidor.listar_productos()

        print("\n========== PRODUCTOS DISPONIBLES ==========")

        for p in productos:
            print(f"\nID: {p['id']}")
            print("Producto:", p["producto"])
            print("Precio inicial: $", p["precio_inicial"])
            print("Precio actual: $", p["precio_actual"])
            print("Mejor postor:", p["mejor_postor"])
            print("Tiempo restante:", p["tiempo_restante"], "segundos")

            print(
                "Estado:",
                "SUBASTA ABIERTA" if p["abierta"] else "SUBASTA FINALIZADA"
            )

        print("\n===========================================")

        return productos

    except Pyro4.errors.PyroError as error:
        print("\nError de comunicación:", error)
        return []


# ==========================================
# MONITOREAR SUBASTA
# ==========================================

def monitorear_subasta(producto_id, evento):
    conexion = None

    try:
        conexion = conectar_servidor()
        ultima_version = -1

        while not evento.is_set():
            estado = conexion.estado(producto_id)

            if estado["version"] != ultima_version:
                print("\n========== ACTUALIZACIÓN DE SUBASTA ==========")
                print("Producto:", estado["producto"])
                print("Precio actual: $", estado["precio_actual"])
                print("Mejor postor:", estado["mejor_postor"])
                print("Tiempo restante:", estado["tiempo_restante"], "segundos")
                print("==============================================")

                ultima_version = estado["version"]

            if not estado["abierta"]:
                print("\n¡La subasta de", estado["producto"], "ha finalizado!")
                print("Ganador:", estado["mejor_postor"])
                print("Precio final: $", estado["precio_actual"])

                break

            evento.wait(2)

    except Exception as error:
        if not evento.is_set():
            print("\nError en el monitoreo:", error)

    finally:
        if conexion is not None:
            conexion._pyroRelease()


# ==========================================
# DETENER MONITOREO ANTERIOR
# ==========================================

def detener_monitoreo():
    global evento_monitoreo, hilo_monitoreo

    if evento_monitoreo is not None:
        evento_monitoreo.set()

    if hilo_monitoreo is not None:
        hilo_monitoreo.join()


# ==========================================
# SELECCIONAR PRODUCTO
# ==========================================

def seleccionar_producto():
    global producto_seleccionado, hilo_monitoreo, evento_monitoreo

    productos = mostrar_productos()

    if not productos:
        return

    try:
        producto_id = int(
            input("\nIngrese el ID del producto que desea subastar: ")
        )

        producto = next(
            (p for p in productos if p["id"] == producto_id),
            None
        )

        if producto is None:
            print("\nEl ID del producto no existe.")
            return

        if not producto["abierta"]:
            print("\nEste producto ya no está disponible para ofertas.")
            return

        detener_monitoreo()

        producto_seleccionado = producto_id

        print("\n===================================")
        print("       PRODUCTO SELECCIONADO")
        print("===================================")
        print("Producto:", producto["producto"])
        print("Precio actual: $", producto["precio_actual"])
        print("Mejor postor:", producto["mejor_postor"])
        print("===================================")

        evento_monitoreo = threading.Event()

        hilo_monitoreo = threading.Thread(
            target=monitorear_subasta,
            args=(producto_id, evento_monitoreo),
            daemon=True
        )

        hilo_monitoreo.start()

    except ValueError:
        print("\nDebe ingresar un número válido.")

    except Pyro4.errors.PyroError as error:
        print("\nError de comunicación:", error)


# ==========================================
# REALIZAR OFERTA
# ==========================================

def realizar_oferta(nombre):
    if producto_seleccionado is None:
        print("\nPrimero debe seleccionar un producto.")
        return

    try:
        monto = float(
            input("\nIngrese el monto de su oferta: ")
        )

        respuesta = servidor.ofertar(
            producto_seleccionado,
            nombre,
            monto
        )

        print("\n========== OFERTA ==========")
        print(respuesta["mensaje"])
        print("Producto:", respuesta["producto"])
        print("Nuevo precio: $", respuesta["precio_actual"])
        print("Mejor postor:", respuesta["mejor_postor"])
        print("============================")

    except (ValueError, TypeError, RuntimeError) as error:
        print("\nOferta rechazada:", error)

    except Pyro4.errors.PyroError as error:
        print("\nError de comunicación:", error)


# ==========================================
# CONSULTAR ESTADO
# ==========================================

def consultar_estado():
    if producto_seleccionado is None:
        print("\nPrimero debe seleccionar un producto.")
        return

    try:
        estado = servidor.estado(producto_seleccionado)

        mostrar_estado(estado)

    except Pyro4.errors.PyroError as error:
        print("\nError de comunicación:", error)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

try:
    servidor = conectar_servidor()

    print("\n===================================")
    print("   CONECTADO AL SERVIDOR DE SUBASTAS")
    print("===================================")

except Exception as error:
    print("\nNo se pudo conectar al servidor:", error)
    raise SystemExit(1)


# ==========================================
# SOLICITAR NOMBRE
# ==========================================

nombre = input("\nIngrese su nombre: ").strip()

while not nombre:
    print("El nombre no puede estar vacío.")

    nombre = input("Ingrese su nombre: ").strip()


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

try:
    while not detener.is_set():

        print("\n========== MENÚ DE SUBASTA ==========")
        print("1. Ver productos disponibles")
        print("2. Seleccionar producto")
        print("3. Realizar una oferta")
        print("4. Consultar estado de la subasta")
        print("5. Salir")
        print("=====================================")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            mostrar_productos()

        elif opcion == "2":
            seleccionar_producto()

        elif opcion == "3":
            realizar_oferta(nombre)

        elif opcion == "4":
            consultar_estado()

        elif opcion == "5":
            print("\nSaliendo de la subasta...")
            break

        else:
            print("\nOpción no válida.")

except KeyboardInterrupt:
    print("\nCliente desconectado.")

finally:
    detener.set()

    detener_monitoreo()

    if servidor is not None:
        servidor._pyroRelease()

    print("\nConexión cerrada.")
import Pyro4 
import time 
import threading 
import math

@Pyro4.expose 
class Subasta:

 def __init__(self):

    # LISTA DE PRODUCTOS PARA SUBASTAR
    self.productos = [

        {
            "id": 1,
            "producto": "Laptop ASUS",
            "precio_inicial": 500.00,
            "precio_actual": 500.00,
            "mejor_postor": "Sin ofertas",
            "duracion": 120,
            "inicio": time.monotonic(),
            "version": 0
        },

        {
            "id": 2,
            "producto": "Celular Samsung",
            "precio_inicial": 300.00,
            "precio_actual": 300.00,
            "mejor_postor": "Sin ofertas",
            "duracion": 120,
            "inicio": time.monotonic(),
            "version": 0
        },

        {
            "id": 3,
            "producto": "Tablet Lenovo",
            "precio_inicial": 200.00,
            "precio_actual": 200.00,
            "mejor_postor": "Sin ofertas",
            "duracion": 120,
            "inicio": time.monotonic(),
            "version": 0
        },

        {
            "id": 4,
            "producto": "Smartwatch Xiaomi",
            "precio_inicial": 100.00,
            "precio_actual": 100.00,
            "mejor_postor": "Sin ofertas",
            "duracion": 120,
            "inicio": time.monotonic(),
            "version": 0
        }
    ]

    # CONTROL DE CONCURRENCIA
    self.lock = threading.Lock()

    print("Servidor de subastas creado correctamente.")
    print("Cantidad de productos:", len(self.productos))

# ==========================================
# BUSCAR PRODUCTO POR ID
# ==========================================

def buscar_producto(self, producto_id):

    for producto in self.productos:

        if producto["id"] == producto_id:
            return producto

    return None

# ==========================================
# LISTAR PRODUCTOS
# ==========================================

def listar_productos(self):

    with self.lock:

        lista = []

        for producto in self.productos:

            fin = producto["inicio"] + producto["duracion"]

            tiempo_restante = max(
                0,
                int(fin - time.monotonic())
            )

            lista.append({

                "id": producto["id"],
                "producto": producto["producto"],
                "precio_inicial": producto["precio_inicial"],
                "precio_actual": producto["precio_actual"],
                "mejor_postor": producto["mejor_postor"],
                "tiempo_restante": tiempo_restante,
                "abierta": tiempo_restante > 0,
                "version": producto["version"]

            })

        return lista

# ==========================================
# CONSULTAR ESTADO DE UN PRODUCTO
# ==========================================

def estado(self, producto_id):

    with self.lock:

        producto = self.buscar_producto(producto_id)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        fin = producto["inicio"] + producto["duracion"]

        tiempo_restante = max(
            0,
            int(fin - time.monotonic())
        )

        return {

            "id": producto["id"],
            "producto": producto["producto"],
            "precio_inicial": producto["precio_inicial"],
            "precio_actual": producto["precio_actual"],
            "mejor_postor": producto["mejor_postor"],
            "tiempo_restante": tiempo_restante,
            "abierta": tiempo_restante > 0,
            "version": producto["version"]

        }

# ==========================================
# REALIZAR UNA OFERTA
# ==========================================

def ofertar(self, producto_id, nombre, monto):

    with self.lock:

        producto = self.buscar_producto(producto_id)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        # VALIDAR NOMBRE

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Nombre de cliente no válido.")

        # VALIDAR MONTO

        if isinstance(monto, bool) or not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un número.")

        if not math.isfinite(monto):
            raise ValueError("El monto debe ser un número finito.")

        if monto <= 0:
            raise ValueError("La oferta debe ser mayor que cero.")

        # COMPROBAR SI LA SUBASTA SIGUE ABIERTA

        fin = producto["inicio"] + producto["duracion"]

        if time.monotonic() >= fin:
            raise RuntimeError("La subasta ha finalizado.")

        # COMPROBAR SI SUPERA EL PRECIO ACTUAL

        if monto <= producto["precio_actual"]:

            raise ValueError(
                f"La oferta debe superar ${producto['precio_actual']:.2f}"
            )

        # ACEPTAR OFERTA

        producto["precio_actual"] = float(monto)

        producto["mejor_postor"] = nombre.strip()

        producto["version"] += 1

        print("\n========== NUEVA OFERTA ==========")
        print("Producto:", producto["producto"])
        print("Postor:", producto["mejor_postor"])
        print("Nuevo precio: $", producto["precio_actual"])
        print("==================================")

        return {

            "mensaje": "Oferta aceptada correctamente.",
            "producto": producto["producto"],
            "precio_actual": producto["precio_actual"],
            "mejor_postor": producto["mejor_postor"]

        }
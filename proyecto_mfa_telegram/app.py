from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_NAME = "usuarios.db"

def conectar_db():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    conexion = conectar_db()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexion.commit()
    conexion.close()

@app.route("/registrar", methods=["POST"])
def registrar():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    password = datos.get("password", "")

    if len(usuario) < 3 or len(usuario) > 30 or len(password) < 8 or len(password) > 128:
        return jsonify({"estado": "error", "mensaje": "Credenciales con longitud inválida."}), 400

    password_hash = generate_password_hash(password)

    try:
        conexion = conectar_db()
        conexion.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
            (usuario, password_hash)
        )
        conexion.commit()
        conexion.close()
        return jsonify({"estado": "ok", "mensaje": "Usuario registrado correctamente."})
    except sqlite3.IntegrityError:
        return jsonify({"estado": "error", "mensaje": "El usuario ya existe."}), 409

@app.route("/validar", methods=["POST"])
def validar():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "")
    password = datos.get("password", "")

    conexion = conectar_db()
    registro = conexion.execute(
        "SELECT password FROM usuarios WHERE usuario = ?",
        (usuario,)
    ).fetchone()
    conexion.close()

    if registro and check_password_hash(registro["password"], password):
        return jsonify({"estado": "ok", "mensaje": "Credenciales correctas."})

    return jsonify({"estado": "error", "mensaje": "Usuario o contraseña incorrectos."}), 401

if __name__ == "__main__":
    inicializar_db()
    print("==================================")
    print("      SERVIDOR SQLITE & FLASK     ")
    print("==================================")
    print("Host: localhost | Puerto: 5001")
    print("==================================")
    app.run(host="127.0.0.1", port=5001, debug=False)
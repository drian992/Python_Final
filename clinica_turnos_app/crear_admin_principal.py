import os
import getpass
from dotenv import load_dotenv
import mysql.connector
import bcrypt

def obtener_conexion():
    load_dotenv()
    return mysql.connector.connect(
        host=os.getenv("BD_HOST", "localhost"),
        port=int(os.getenv("BD_PUERTO", "3306")),
        user=os.getenv("BD_USUARIO"),
        password=os.getenv("BD_CONTRASENA"),
        database=os.getenv("BD_NOMBRE"),
    )

def main():
    nombre_usuario = input("Nombre de usuario (ADMIN_PRINCIPAL): ").strip()
    nombre_completo = input("Nombre completo: ").strip()
    contrasena = getpass.getpass("Contrasena: ").encode("utf-8")

    hash_contrasena = bcrypt.hashpw(contrasena, bcrypt.gensalt()).decode("utf-8")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario=%s", (nombre_usuario,))
    if cursor.fetchone():
        print("Ese nombre de usuario ya existe.")
        cursor.close()
        conexion.close()
        return

    cursor.execute("""
        INSERT INTO usuarios (nombre_usuario, hash_contrasena, nombre_completo, rol, activo)
        VALUES (%s, %s, %s, 'ADMIN_PRINCIPAL', 1)
    """, (nombre_usuario, hash_contrasena, nombre_completo))

    conexion.commit()
    cursor.close()
    conexion.close()
    print("ADMIN_PRINCIPAL creado correctamente.")

if __name__ == "__main__":
    main()
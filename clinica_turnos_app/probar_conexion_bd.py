import os
from dotenv import load_dotenv
import mysql.connector

def obtener_conexion():
    load_dotenv()
    return mysql.connector.connect(
        host=os.getenv("BD_HOST", "localhost"),
        port=int(os.getenv("BD_PUERTO", "3306")),
        user=os.getenv("BD_USUARIO", "root"),
        password=os.getenv("BD_CONTRASENA", ""),
        database=os.getenv("BD_NOMBRE"),
    )

def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    print("Conexion OK. Version del servidor:", version)

if __name__ == "__main__":
    main()
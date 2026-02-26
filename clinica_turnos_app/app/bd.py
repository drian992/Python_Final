import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("BD_HOST", "localhost"),
        port=int(os.getenv("BD_PUERTO", "3306")),
        user=os.getenv("BD_USUARIO", "root"),
        password=os.getenv("BD_CONTRASENA", ""),
        database=os.getenv("BD_NOMBRE", "clinica_turnos"),
        connection_timeout=8,
    )


def ejecutar_select(sql, parametros=None):
    if parametros is None:
        parametros = {}

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        return filas
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conexion.close()


def ejecutar_uno(sql, parametros=None):
    if parametros is None:
        parametros = {}

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        fila = cursor.fetchone()
        return fila
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conexion.close()


def ejecutar_escritura(sql, parametros=None):
    if parametros is None:
        parametros = {}

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.lastrowid
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conexion.close()
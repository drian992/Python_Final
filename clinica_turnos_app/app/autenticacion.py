from app.bd import ejecutar_uno, ejecutar_escritura
from app.seguridad import verificar_contrasena

def iniciar_sesion(nombre_usuario: str, contrasena: str):
    usuario = ejecutar_uno(
        """
        SELECT id, nombre_usuario, hash_contrasena, nombre_completo, rol, activo
        FROM usuarios
        WHERE nombre_usuario = %(nombre_usuario)s
        """,
        {"nombre_usuario": nombre_usuario},
    )

    if not usuario:
        return None

    if usuario["activo"] != 1:
        return None

    if not verificar_contrasena(contrasena, usuario["hash_contrasena"]):
        return None

    ejecutar_escritura(
        "UPDATE usuarios SET ultimo_ingreso = NOW() WHERE id = %(id)s",
        {"id": usuario["id"]},
    )

    # No devolvemos el hash
    return {
        "id": usuario["id"],
        "nombre_usuario": usuario["nombre_usuario"],
        "nombre_completo": usuario["nombre_completo"],
        "rol": usuario["rol"],
        "activo": usuario["activo"],
    }
from app.bd import ejecutar_select, ejecutar_uno, ejecutar_escritura
from app.seguridad import generar_hash_contrasena

def _es_admin_principal(usuario_actual: dict) -> bool:
    return usuario_actual and usuario_actual.get("rol") == "ADMIN_PRINCIPAL"

def listar_usuarios(usuario_actual: dict):
    if not _es_admin_principal(usuario_actual):
        raise PermissionError("Solo ADMIN_PRINCIPAL puede listar usuarios.")

    return ejecutar_select(
        """
        SELECT id, nombre_usuario, nombre_completo, rol, activo, ultimo_ingreso, creado_en
        FROM usuarios
        ORDER BY id DESC
        """
    )

def crear_admin(usuario_actual: dict, nombre_usuario: str, nombre_completo: str, contrasena: str, rol: str = "ADMIN"):
    if not _es_admin_principal(usuario_actual):
        raise PermissionError("Solo ADMIN_PRINCIPAL puede crear usuarios.")

    if rol not in ("ADMIN_PRINCIPAL", "ADMIN"):
        raise ValueError("Rol invalido.")

    existente = ejecutar_uno(
        "SELECT id FROM usuarios WHERE nombre_usuario=%(nombre_usuario)s",
        {"nombre_usuario": nombre_usuario},
    )
    if existente:
        raise ValueError("Ese nombre de usuario ya existe.")

    hash_contrasena = generar_hash_contrasena(contrasena)

    nuevo_id = ejecutar_escritura(
        """
        INSERT INTO usuarios (nombre_usuario, hash_contrasena, nombre_completo, rol, activo)
        VALUES (%(nombre_usuario)s, %(hash_contrasena)s, %(nombre_completo)s, %(rol)s, 1)
        """,
        {
            "nombre_usuario": nombre_usuario,
            "hash_contrasena": hash_contrasena,
            "nombre_completo": nombre_completo,
            "rol": rol,
        },
    )
    return nuevo_id

def actualizar_usuario(usuario_actual: dict, usuario_id: int, nombre_completo: str = None, rol: str = None, activo: int = None):
    if not _es_admin_principal(usuario_actual):
        raise PermissionError("Solo ADMIN_PRINCIPAL puede actualizar usuarios.")

    usuario_objetivo = ejecutar_uno(
        "SELECT id, rol FROM usuarios WHERE id=%(id)s",
        {"id": usuario_id},
    )
    if not usuario_objetivo:
        raise ValueError("Usuario no existe.")

    campos = []
    parametros = {"id": usuario_id}

    if nombre_completo is not None:
        campos.append("nombre_completo=%(nombre_completo)s")
        parametros["nombre_completo"] = nombre_completo

    if rol is not None:
        if rol not in ("ADMIN_PRINCIPAL", "ADMIN"):
            raise ValueError("Rol invalido.")
        campos.append("rol=%(rol)s")
        parametros["rol"] = rol

    if activo is not None:
        if activo not in (0, 1):
            raise ValueError("Activo debe ser 0 o 1.")
        campos.append("activo=%(activo)s")
        parametros["activo"] = activo

    if not campos:
        return 0

    sql = "UPDATE usuarios SET " + ", ".join(campos) + " WHERE id=%(id)s"
    ejecutar_escritura(sql, parametros)
    return 1

def cambiar_contrasena_usuario(usuario_actual: dict, usuario_id: int, nueva_contrasena: str):
    if not _es_admin_principal(usuario_actual):
        raise PermissionError("Solo ADMIN_PRINCIPAL puede cambiar contrasenas de otros usuarios.")

    hash_nuevo = generar_hash_contrasena(nueva_contrasena)
    ejecutar_escritura(
        "UPDATE usuarios SET hash_contrasena=%(hash)s WHERE id=%(id)s",
        {"hash": hash_nuevo, "id": usuario_id},
    )
    return 1

def cambiar_contrasena_propia(usuario_actual: dict, nueva_contrasena: str):
    if not usuario_actual:
        raise PermissionError("Debes iniciar sesion.")
    hash_nuevo = generar_hash_contrasena(nueva_contrasena)
    ejecutar_escritura(
        "UPDATE usuarios SET hash_contrasena=%(hash)s WHERE id=%(id)s",
        {"hash": hash_nuevo, "id": usuario_actual["id"]},
    )
    return 1
from app.bd import ejecutar_select, ejecutar_uno, ejecutar_escritura

def crear_profesional(datos_profesional: dict) -> int:
    return ejecutar_escritura(
        """
        INSERT INTO profesionales (matricula, nombre, apellido, especialidad, telefono, email, activo)
        VALUES (%(matricula)s, %(nombre)s, %(apellido)s, %(especialidad)s, %(telefono)s, %(email)s, 1)
        """,
        {
            "matricula": datos_profesional.get("matricula"),
            "nombre": datos_profesional.get("nombre"),
            "apellido": datos_profesional.get("apellido"),
            "especialidad": datos_profesional.get("especialidad"),
            "telefono": datos_profesional.get("telefono"),
            "email": datos_profesional.get("email"),
        },
    )

def obtener_profesional(profesional_id: int):
    return ejecutar_uno(
        "SELECT * FROM profesionales WHERE id=%(id)s",
        {"id": profesional_id},
    )

def listar_profesionales(texto_busqueda: str = ""):
    texto_busqueda = (texto_busqueda or "").strip()
    if texto_busqueda:
        patron = f"%{texto_busqueda}%"
        return ejecutar_select(
            """
            SELECT * FROM profesionales
            WHERE activo=1 AND (matricula LIKE %(p)s OR nombre LIKE %(p)s OR apellido LIKE %(p)s OR especialidad LIKE %(p)s)
            ORDER BY apellido, nombre
            """,
            {"p": patron},
        )
    return ejecutar_select(
        "SELECT * FROM profesionales WHERE activo=1 ORDER BY apellido, nombre"
    )

def actualizar_profesional(profesional_id: int, datos_profesional: dict):
    return ejecutar_escritura(
        """
        UPDATE profesionales
        SET matricula=%(matricula)s, nombre=%(nombre)s, apellido=%(apellido)s, especialidad=%(especialidad)s,
            telefono=%(telefono)s, email=%(email)s
        WHERE id=%(id)s
        """,
        {
            "id": profesional_id,
            "matricula": datos_profesional.get("matricula"),
            "nombre": datos_profesional.get("nombre"),
            "apellido": datos_profesional.get("apellido"),
            "especialidad": datos_profesional.get("especialidad"),
            "telefono": datos_profesional.get("telefono"),
            "email": datos_profesional.get("email"),
        },
    )

def desactivar_profesional(profesional_id: int):
    return ejecutar_escritura(
        "UPDATE profesionales SET activo=0 WHERE id=%(id)s",
        {"id": profesional_id},
    )
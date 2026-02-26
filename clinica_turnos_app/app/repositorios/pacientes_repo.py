from app.bd import ejecutar_select, ejecutar_uno, ejecutar_escritura

def crear_paciente(datos_paciente: dict) -> int:
    return ejecutar_escritura(
        """
        INSERT INTO pacientes (dni, nombre, apellido, telefono, email, domicilio, fecha_nacimiento, observaciones, activo)
        VALUES (%(dni)s, %(nombre)s, %(apellido)s, %(telefono)s, %(email)s, %(domicilio)s, %(fecha_nacimiento)s, %(observaciones)s, 1)
        """,
        {
            "dni": datos_paciente.get("dni"),
            "nombre": datos_paciente.get("nombre"),
            "apellido": datos_paciente.get("apellido"),
            "telefono": datos_paciente.get("telefono"),
            "email": datos_paciente.get("email"),
            "domicilio": datos_paciente.get("domicilio"),
            "fecha_nacimiento": datos_paciente.get("fecha_nacimiento"),
            "observaciones": datos_paciente.get("observaciones"),
        },
    )

def obtener_paciente(paciente_id: int):
    return ejecutar_uno(
        "SELECT * FROM pacientes WHERE id=%(id)s",
        {"id": paciente_id},
    )

def listar_pacientes(texto_busqueda: str = ""):
    texto_busqueda = (texto_busqueda or "").strip()
    if texto_busqueda:
        patron = f"%{texto_busqueda}%"
        return ejecutar_select(
            """
            SELECT * FROM pacientes
            WHERE activo=1 AND (dni LIKE %(p)s OR nombre LIKE %(p)s OR apellido LIKE %(p)s OR telefono LIKE %(p)s)
            ORDER BY apellido, nombre
            """,
            {"p": patron},
        )
    return ejecutar_select(
        "SELECT * FROM pacientes WHERE activo=1 ORDER BY apellido, nombre"
    )

def actualizar_paciente(paciente_id: int, datos_paciente: dict):
    return ejecutar_escritura(
        """
        UPDATE pacientes
        SET dni=%(dni)s, nombre=%(nombre)s, apellido=%(apellido)s, telefono=%(telefono)s, email=%(email)s,
            domicilio=%(domicilio)s, fecha_nacimiento=%(fecha_nacimiento)s, observaciones=%(observaciones)s
        WHERE id=%(id)s
        """,
        {
            "id": paciente_id,
            "dni": datos_paciente.get("dni"),
            "nombre": datos_paciente.get("nombre"),
            "apellido": datos_paciente.get("apellido"),
            "telefono": datos_paciente.get("telefono"),
            "email": datos_paciente.get("email"),
            "domicilio": datos_paciente.get("domicilio"),
            "fecha_nacimiento": datos_paciente.get("fecha_nacimiento"),
            "observaciones": datos_paciente.get("observaciones"),
        },
    )

def desactivar_paciente(paciente_id: int):
    return ejecutar_escritura(
        "UPDATE pacientes SET activo=0 WHERE id=%(id)s",
        {"id": paciente_id},
    )
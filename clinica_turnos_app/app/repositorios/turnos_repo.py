from app.bd import ejecutar_select, ejecutar_uno, ejecutar_escritura

ESTADOS_BLOQUEAN = ("RESERVADO", "ATENDIDO")  # podes ajustar

def _validar_intervalo(inicio: str, fin: str):
    # inicio y fin vienen como string "YYYY-MM-DD HH:MM:SS" o datetime en UI (luego lo normalizamos)
    if not inicio or not fin:
        raise ValueError("Inicio y fin son obligatorios.")
    # La comparacion real la haremos en BD con la consulta, pero igual evitamos casos obvios:
    if str(fin) <= str(inicio):
        raise ValueError("El fin debe ser mayor al inicio.")

def _hay_solapamiento(profesional_id: int, inicio: str, fin: str, turno_id_excluir: int = None) -> bool:
    parametros = {
        "profesional_id": profesional_id,
        "inicio": inicio,
        "fin": fin,
        "e1": ESTADOS_BLOQUEAN[0],
        "e2": ESTADOS_BLOQUEAN[1],
    }

    filtro_exclusion = ""
    if turno_id_excluir is not None:
        filtro_exclusion = "AND id <> %(excluir)s"
        parametros["excluir"] = turno_id_excluir

    fila = ejecutar_uno(
        f"""
        SELECT id
        FROM turnos
        WHERE profesional_id=%(profesional_id)s
          AND estado IN (%(e1)s, %(e2)s)
          AND inicio < %(fin)s
          AND fin > %(inicio)s
          {filtro_exclusion}
        LIMIT 1
        """,
        parametros
    )
    return fila is not None

def crear_turno(datos_turno: dict, usuario_actual: dict) -> int:
    if not usuario_actual:
        raise PermissionError("Debes iniciar sesion.")

    paciente_id = datos_turno.get("paciente_id")
    profesional_id = datos_turno.get("profesional_id")
    inicio = datos_turno.get("inicio")
    fin = datos_turno.get("fin")

    _validar_intervalo(inicio, fin)

    if _hay_solapamiento(profesional_id, inicio, fin):
        raise ValueError("El profesional ya tiene un turno que se solapa en ese horario.")

    return ejecutar_escritura(
        """
        INSERT INTO turnos (paciente_id, profesional_id, inicio, fin, motivo, estado, observaciones, creado_por)
        VALUES (%(paciente_id)s, %(profesional_id)s, %(inicio)s, %(fin)s, %(motivo)s, %(estado)s, %(observaciones)s, %(creado_por)s)
        """,
        {
            "paciente_id": paciente_id,
            "profesional_id": profesional_id,
            "inicio": inicio,
            "fin": fin,
            "motivo": datos_turno.get("motivo"),
            "estado": datos_turno.get("estado", "RESERVADO"),
            "observaciones": datos_turno.get("observaciones"),
            "creado_por": usuario_actual["id"],
        },
    )

def listar_turnos_por_dia(fecha_yyyy_mm_dd: str, profesional_id: int = None):
    parametros = {"fecha": fecha_yyyy_mm_dd}
    filtro_prof = ""

    if profesional_id is not None:
        filtro_prof = "AND profesional_id=%(profesional_id)s"
        parametros["profesional_id"] = profesional_id

    return ejecutar_select(
        f"""
        SELECT t.*,
               p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               pr.nombre AS profesional_nombre, pr.apellido AS profesional_apellido
        FROM turnos t
        JOIN pacientes p ON p.id = t.paciente_id
        JOIN profesionales pr ON pr.id = t.profesional_id
        WHERE DATE(t.inicio) = %(fecha)s
        {filtro_prof}
        ORDER BY t.inicio
        """,
        parametros,
    )

def actualizar_turno(turno_id: int, datos_turno: dict, usuario_actual: dict):
    if not usuario_actual:
        raise PermissionError("Debes iniciar sesion.")

    turno_actual = ejecutar_uno("SELECT * FROM turnos WHERE id=%(id)s", {"id": turno_id})
    if not turno_actual:
        raise ValueError("Turno no existe.")

    profesional_id = datos_turno.get("profesional_id", turno_actual["profesional_id"])
    inicio = datos_turno.get("inicio", turno_actual["inicio"])
    fin = datos_turno.get("fin", turno_actual["fin"])

    _validar_intervalo(str(inicio), str(fin))

    if _hay_solapamiento(int(profesional_id), str(inicio), str(fin), turno_id_excluir=turno_id):
        raise ValueError("El profesional ya tiene un turno que se solapa en ese horario.")

    ejecutar_escritura(
        """
        UPDATE turnos
        SET paciente_id=%(paciente_id)s,
            profesional_id=%(profesional_id)s,
            inicio=%(inicio)s,
            fin=%(fin)s,
            motivo=%(motivo)s,
            estado=%(estado)s,
            observaciones=%(observaciones)s,
            actualizado_por=%(actualizado_por)s
        WHERE id=%(id)s
        """,
        {
            "id": turno_id,
            "paciente_id": datos_turno.get("paciente_id", turno_actual["paciente_id"]),
            "profesional_id": profesional_id,
            "inicio": inicio,
            "fin": fin,
            "motivo": datos_turno.get("motivo", turno_actual.get("motivo")),
            "estado": datos_turno.get("estado", turno_actual.get("estado")),
            "observaciones": datos_turno.get("observaciones", turno_actual.get("observaciones")),
            "actualizado_por": usuario_actual["id"],
        },
    )
    return 1

def cancelar_turno(turno_id: int, usuario_actual: dict, observaciones: str = ""):
    if not usuario_actual:
        raise PermissionError("Debes iniciar sesion.")

    ejecutar_escritura(
        """
        UPDATE turnos
        SET estado='CANCELADO', observaciones=%(observaciones)s, actualizado_por=%(u)s
        WHERE id=%(id)s
        """,
        {"id": turno_id, "u": usuario_actual["id"], "observaciones": observaciones},
    )
    return 1
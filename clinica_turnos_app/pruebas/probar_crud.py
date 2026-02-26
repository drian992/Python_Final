from app.autenticacion import iniciar_sesion
from app.repositorios.pacientes_repo import crear_paciente, listar_pacientes, actualizar_paciente, desactivar_paciente
from app.repositorios.profesionales_repo import crear_profesional, listar_profesionales
from app.repositorios.turnos_repo import crear_turno, listar_turnos_por_dia

def main():
    nombre_usuario = input("Usuario: ").strip()
    contrasena = input("Contrasena: ").strip()

    usuario_actual = iniciar_sesion(nombre_usuario, contrasena)
    if not usuario_actual:
        print("Login fallido.")
        return

    print("Login OK:", usuario_actual)

    # Crear paciente
    datos_paciente = {
        "dni": "12345678",
        "nombre": "Juan",
        "apellido": "Perez",
        "telefono": "3810000000",
        "email": None,
        "domicilio": None,
        "fecha_nacimiento": None,
        "observaciones": "Paciente de prueba",
    }
    paciente_id = crear_paciente(datos_paciente)
    print("Paciente creado:", paciente_id)

    # Listar pacientes (lista de diccionarios)
    lista_pacientes = listar_pacientes("Perez")
    print("Pacientes encontrados:", len(lista_pacientes))
    for p in lista_pacientes:
        print(p["id"], p["apellido"], p["nombre"])

    # Actualizar paciente
    datos_paciente_actualizado = dict(datos_paciente)
    datos_paciente_actualizado["telefono"] = "3811111111"
    actualizar_paciente(paciente_id, datos_paciente_actualizado)
    print("Paciente actualizado.")

    # Crear profesional
    datos_profesional = {
        "matricula": "MAT-001",
        "nombre": "Ana",
        "apellido": "Lopez",
        "especialidad": "Ortodoncia",
        "telefono": "3812222222",
        "email": None,
    }
    profesional_id = crear_profesional(datos_profesional)
    print("Profesional creado:", profesional_id)

    lista_profesionales = listar_profesionales("Lopez")
    print("Profesionales encontrados:", len(lista_profesionales))

    # Crear turno (ajusta la fecha/hora a algo valido para hoy/mañana)
    datos_turno = {
        "paciente_id": paciente_id,
        "profesional_id": profesional_id,
        "inicio": "2026-01-22 10:00:00",
        "fin": "2026-01-22 10:30:00",
        "motivo": "Control",
        "estado": "RESERVADO",
        "observaciones": None,
    }
    turno_id = crear_turno(datos_turno, usuario_actual)
    print("Turno creado:", turno_id)

    turnos_del_dia = listar_turnos_por_dia("2026-01-22")
    print("Turnos del dia:", len(turnos_del_dia))
    for t in turnos_del_dia:
        print(t["inicio"], "-", t["paciente_apellido"], t["profesional_apellido"], t["estado"])

    # Desactivar paciente (borrado logico)
    desactivar_paciente(paciente_id)
    print("Paciente desactivado (borrado logico).")

if __name__ == "__main__":
    main()
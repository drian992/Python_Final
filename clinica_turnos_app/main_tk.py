import tkinter as tk
import re

from tkinter import ttk, messagebox

from app.autenticacion import iniciar_sesion
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tkinter import simpledialog

from app.repositorios.turnos_repo import (
    crear_turno,
    listar_turnos_por_dia,
    actualizar_turno,
    cancelar_turno,
)



from app.repositorios.pacientes_repo import (
    crear_paciente,
    listar_pacientes,
    obtener_paciente,
    actualizar_paciente,
    desactivar_paciente,
)

from app.repositorios.profesionales_repo import (
    crear_profesional,
    listar_profesionales,
    obtener_profesional,
    actualizar_profesional,
    desactivar_profesional,
)

from app.repositorios.usuarios_repo import (
    listar_usuarios,
    crear_admin,
    actualizar_usuario,
    cambiar_contrasena_usuario,
    cambiar_contrasena_propia,
)


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TELEFONO_REGEX = re.compile(r"^[0-9+()\-\s]{6,20}$")


def configurar_estilos(root: tk.Tk):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.configure(bg="#f2f4f8")
    style.configure("TFrame", background="#f2f4f8")
    style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=1)
    style.configure("TLabel", background="#f2f4f8", font=("Segoe UI", 10))
    style.configure("CardTitle.TLabel", background="#ffffff", font=("Segoe UI", 17, "bold"))
    style.configure("Hint.TLabel", background="#ffffff", foreground="#475569")
    style.configure("TButton", padding=(12, 8), font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))


def validar_email(email: str) -> bool:
    return email == "" or bool(EMAIL_REGEX.match(email))


def validar_telefono(telefono: str) -> bool:
    return telefono == "" or bool(TELEFONO_REGEX.match(telefono))


class AplicacionTurnos(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clinica Odontologica - Sistema de Turnos")
        self.geometry("1024x620")
        self.minsize(980, 580)
        configurar_estilos(self)

        self.usuario_actual = None

        self.contenedor = ttk.Frame(self, padding=16)
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_login()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_contenedor()
        FrameLogin(self.contenedor, self).pack(fill="both", expand=True)

    def mostrar_principal(self):
        self.limpiar_contenedor()
        FramePrincipal(self.contenedor, self, self.usuario_actual).pack(fill="both", expand=True)





    def mostrar_turnos(self):
        self.limpiar_contenedor()
        FrameTurnos(self.contenedor, self, self.usuario_actual).pack(fill="both", expand=True)
        
    def mostrar_pacientes(self):
        self.limpiar_contenedor()
        FramePacientes(self.contenedor, self, self.usuario_actual).pack(fill="both", expand=True)

    def mostrar_profesionales(self):
        self.limpiar_contenedor()
        FrameProfesionales(self.contenedor, self, self.usuario_actual).pack(fill="both", expand=True)

    def mostrar_usuarios(self):
        self.limpiar_contenedor()
        FrameUsuarios(self.contenedor, self, self.usuario_actual).pack(fill="both", expand=True)


class FrameLogin(ttk.Frame):
    def __init__(self, master, app: AplicacionTurnos):
        super().__init__(master)
        self.app = app

        self.var_nombre_usuario = tk.StringVar()
        self.var_contrasena = tk.StringVar()
        self.var_mostrar_contrasena = tk.BooleanVar(value=False)

        tarjeta = ttk.Frame(self, style="Card.TFrame", padding=24)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        titulo = ttk.Label(tarjeta, text="Ingreso al sistema", style="CardTitle.TLabel")
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(
            tarjeta,
            text="Usá tus credenciales para acceder al panel principal.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 14))

        ttk.Label(tarjeta, text="Usuario:", style="Hint.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.entry_usuario = ttk.Entry(tarjeta, textvariable=self.var_nombre_usuario, width=34)
        self.entry_usuario.grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(tarjeta, text="Contrasena:", style="Hint.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_contrasena = ttk.Entry(tarjeta, textvariable=self.var_contrasena, width=34, show="*")
        self.entry_contrasena.grid(row=3, column=1, sticky="w", pady=6)

        chk = ttk.Checkbutton(
            tarjeta,
            text="Mostrar contrasena",
            variable=self.var_mostrar_contrasena,
            command=self._alternar_mostrar_contrasena,
        )
        chk.grid(row=4, column=1, sticky="w", pady=(2, 10))

        botones = ttk.Frame(tarjeta)
        botones.grid(row=5, column=0, columnspan=2, sticky="e", pady=8)

        ttk.Button(botones, text="Ingresar", command=self._ingresar).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(botones, text="Salir", command=self.app.destroy).grid(row=0, column=1)

        self.entry_usuario.focus()
        self.entry_usuario.bind("<Return>", lambda e: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", lambda e: self._ingresar())

        tarjeta.columnconfigure(0, minsize=120)
        tarjeta.columnconfigure(1, weight=1)

    def _alternar_mostrar_contrasena(self):
        self.entry_contrasena.config(show="" if self.var_mostrar_contrasena.get() else "*")

    def _ingresar(self):
        nombre_usuario = self.var_nombre_usuario.get().strip()
        contrasena = self.var_contrasena.get()

        if not nombre_usuario or not contrasena:
            messagebox.showwarning("Datos incompletos", "Por favor, ingresá usuario y contrasena.")
            return

        try:
            usuario = iniciar_sesion(nombre_usuario, contrasena)
        except Exception as error:
            messagebox.showerror(
                "Error de conexion",
                "No se pudo validar el inicio de sesion.\n"
                "Verificá que MySQL/XAMPP esté encendido y que el .env sea correcto.\n\n"
                f"Detalle: {error}"
            )
            return

        if not usuario:
            messagebox.showwarning("Login", "Usuario o contrasena incorrectos, o usuario inactivo.")
            return

        self.app.usuario_actual = usuario
        self.app.mostrar_principal()


class FramePrincipal(ttk.Frame):
    def __init__(self, master, app: AplicacionTurnos, usuario_actual: dict):
        super().__init__(master)
        self.app = app
        self.usuario_actual = usuario_actual

        titulo = ttk.Label(self, text="Panel principal", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 10))

        texto_bienvenida = f"Bienvenido/a: {usuario_actual.get('nombre_completo')} ({usuario_actual.get('rol')})"
        ttk.Label(self, text=texto_bienvenida).grid(row=1, column=0, columnspan=5, sticky="w", pady=(0, 6))
        ttk.Label(
            self,
            text="Tip: empezá por Pacientes y Profesionales, luego registrá Turnos.",
            style="Hint.TLabel",
        ).grid(row=2, column=0, columnspan=5, sticky="w", pady=(0, 14))

        ttk.Button(self, text="Pacientes (CRUD)", width=22, command=self.app.mostrar_pacientes).grid(
            row=3, column=0, padx=6, pady=6, sticky="w"
        )
        ttk.Button(self, text="Profesionales (CRUD)", width=22, command=self.app.mostrar_profesionales).grid(
            row=3, column=1, padx=6, pady=6, sticky="w"
        )

        ttk.Button(self, text="Turnos (Agenda)", width=22, command=self.app.mostrar_turnos).grid(
            row=3, column=2, padx=6, pady=6, sticky="w"
        )

        if usuario_actual.get("rol") == "ADMIN_PRINCIPAL":
            ttk.Button(self, text="Usuarios (CRUD)", width=22, command=self.app.mostrar_usuarios).grid(
                row=4, column=0, padx=6, pady=6, sticky="w"
            )

        ttk.Button(self, text="Cambiar mi contrasena", command=self._cambiar_mi_contrasena).grid(
            row=5, column=0, padx=6, pady=(18, 6), sticky="w"
        )

        ttk.Button(self, text="Cerrar sesion", command=self._cerrar_sesion).grid(
            row=5, column=4, padx=6, pady=(18, 6), sticky="e"
        )

        for c in range(5):
            self.columnconfigure(c, weight=1)

    def _abrir_turnos(self):
        messagebox.showinfo("Turnos", "Fase 6: agenda + CRUD de turnos (con calendario y no solapar).")

    def _cambiar_mi_contrasena(self):
        ventana = VentanaCambiarContrasena(
            self,
            titulo="Cambiar mi contrasena",
            descripcion="Ingresá una nueva contrasena para tu usuario.",
        )
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            cambiar_contrasena_propia(self.usuario_actual, ventana.nueva_contrasena)
            messagebox.showinfo("OK", "Contrasena actualizada correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cambiar la contrasena.\n\nDetalle: {error}")

    def _cerrar_sesion(self):
        self.app.usuario_actual = None
        self.app.mostrar_login()


# -------------------------
# PACIENTES (FASE 4)
# -------------------------
class FramePacientes(ttk.Frame):
    def __init__(self, master, app: AplicacionTurnos, usuario_actual: dict):
        super().__init__(master)
        self.app = app
        self.usuario_actual = usuario_actual

        self.var_busqueda = tk.StringVar()

        titulo = ttk.Label(self, text="Pacientes - CRUD", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))

        barra = ttk.Frame(self)
        barra.grid(row=1, column=0, columnspan=8, sticky="ew", pady=(0, 10))

        ttk.Label(barra, text="Buscar:").grid(row=0, column=0, padx=(0, 8))
        entry_buscar = ttk.Entry(barra, textvariable=self.var_busqueda, width=40)
        entry_buscar.grid(row=0, column=1, padx=(0, 8))
        entry_buscar.bind("<Return>", lambda e: self._cargar_lista())

        ttk.Button(barra, text="Buscar", command=self._cargar_lista).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(barra, text="Limpiar", command=self._limpiar_busqueda).grid(row=0, column=3)

        barra.columnconfigure(1, weight=1)

        columnas = ("id", "dni", "apellido", "nombre", "telefono", "email")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=14)
        self.tabla.grid(row=3, column=0, columnspan=8, sticky="nsew")

        for col, texto in [
            ("id", "ID"),
            ("dni", "DNI"),
            ("apellido", "Apellido"),
            ("nombre", "Nombre"),
            ("telefono", "Telefono"),
            ("email", "Email"),
        ]:
            self.tabla.heading(col, text=texto)

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("dni", width=110, anchor="w")
        self.tabla.column("apellido", width=140, anchor="w")
        self.tabla.column("nombre", width=140, anchor="w")
        self.tabla.column("telefono", width=140, anchor="w")
        self.tabla.column("email", width=260, anchor="w")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=2, column=8, sticky="ns")

        acciones = ttk.Frame(self)
        acciones.grid(row=3, column=0, columnspan=8, sticky="w", pady=(12, 0))

        ttk.Button(acciones, text="Nuevo", command=self._nuevo).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(acciones, text="Editar", command=self._editar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(acciones, text="Desactivar", command=self._desactivar).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(acciones, text="Volver", command=self.app.mostrar_principal).grid(row=0, column=3, padx=(16, 0))

        self.info = ttk.Label(self, text="Seleccioná un paciente para editar o desactivar.")
        self.info.grid(row=4, column=0, columnspan=8, sticky="w", pady=(10, 0))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._cargar_lista()

    def _limpiar_busqueda(self):
        self.var_busqueda.set("")
        self._cargar_lista()

    def _cargar_lista(self):
        texto = self.var_busqueda.get().strip()
        try:
            lista = listar_pacientes(texto)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar pacientes.\n\nDetalle: {error}")
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for p in lista:
            self.tabla.insert(
                "",
                "end",
                values=(
                    p.get("id"),
                    p.get("dni") or "",
                    p.get("apellido") or "",
                    p.get("nombre") or "",
                    p.get("telefono") or "",
                    p.get("email") or "",
                ),
            )

        self.info.config(text=f"Registros: {len(lista)}")

    def _obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return None
        return int(valores[0])

    def _nuevo(self):
        ventana = VentanaPaciente(self, titulo="Nuevo paciente")
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            crear_paciente(ventana.datos_paciente)
            self._cargar_lista()
            messagebox.showinfo("OK", "Paciente creado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo crear el paciente.\n\nDetalle: {error}")

    def _editar(self):
        paciente_id = self._obtener_id_seleccionado()
        if not paciente_id:
            messagebox.showwarning("Atencion", "Seleccioná un paciente primero.")
            return

        try:
            paciente = obtener_paciente(paciente_id)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo leer el paciente.\n\nDetalle: {error}")
            return

        if not paciente:
            messagebox.showwarning("Atencion", "El paciente ya no existe.")
            self._cargar_lista()
            return

        ventana = VentanaPaciente(self, titulo="Editar paciente", datos_iniciales=paciente)
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            actualizar_paciente(paciente_id, ventana.datos_paciente)
            self._cargar_lista()
            messagebox.showinfo("OK", "Paciente actualizado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el paciente.\n\nDetalle: {error}")

    def _desactivar(self):
        paciente_id = self._obtener_id_seleccionado()
        if not paciente_id:
            messagebox.showwarning("Atencion", "Seleccioná un paciente primero.")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que querés desactivar este paciente?"):
            return

        try:
            desactivar_paciente(paciente_id)
            self._cargar_lista()
            messagebox.showinfo("OK", "Paciente desactivado (borrado logico).")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo desactivar.\n\nDetalle: {error}")


class VentanaPaciente(tk.Toplevel):
    def __init__(self, master, titulo="Paciente", datos_iniciales=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("520x420")
        self.resizable(False, False)

        self.guardo = False
        self.datos_paciente = {}

        self.var_dni = tk.StringVar(value=(datos_iniciales.get("dni") if datos_iniciales else "") or "")
        self.var_nombre = tk.StringVar(value=(datos_iniciales.get("nombre") if datos_iniciales else "") or "")
        self.var_apellido = tk.StringVar(value=(datos_iniciales.get("apellido") if datos_iniciales else "") or "")
        self.var_telefono = tk.StringVar(value=(datos_iniciales.get("telefono") if datos_iniciales else "") or "")
        self.var_email = tk.StringVar(value=(datos_iniciales.get("email") if datos_iniciales else "") or "")
        self.var_domicilio = tk.StringVar(value=(datos_iniciales.get("domicilio") if datos_iniciales else "") or "")
        self.var_fecha_nacimiento = tk.StringVar(
            value=(str(datos_iniciales.get("fecha_nacimiento")) if (datos_iniciales and datos_iniciales.get("fecha_nacimiento")) else "")
        )

        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="DNI:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_dni, width=34).grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Nombre *:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_nombre, width=34).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Apellido *:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_apellido, width=34).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Telefono:").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_telefono, width=34).grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Email:").grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_email, width=34).grid(row=4, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Domicilio:").grid(row=5, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_domicilio, width=34).grid(row=5, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Fecha nac. (YYYY-MM-DD):").grid(row=6, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_fecha_nacimiento, width=34).grid(row=6, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Observaciones:").grid(row=7, column=0, sticky="nw", pady=6)
        self.texto_observaciones = tk.Text(cont, width=38, height=6)
        self.texto_observaciones.grid(row=7, column=1, sticky="w", pady=6)

        observaciones_iniciales = (datos_iniciales.get("observaciones") if datos_iniciales else "") or ""
        self.texto_observaciones.insert("1.0", observaciones_iniciales)

        botones = ttk.Frame(cont)
        botones.grid(row=8, column=0, columnspan=2, sticky="e", pady=(14, 0))

        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)

        cont.columnconfigure(0, minsize=170)
        cont.columnconfigure(1, weight=1)

        self.grab_set()
        self.focus_force()

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()

        if not nombre or not apellido:
            messagebox.showwarning("Validacion", "Nombre y Apellido son obligatorios.")
            return

        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        if not validar_telefono(telefono):
            messagebox.showwarning("Validacion", "Telefono invalido. Usá solo números, +, -, espacios o paréntesis.")
            return

        if not validar_email(email):
            messagebox.showwarning("Validacion", "Email invalido. Ejemplo: usuario@dominio.com")
            return

        fecha_nacimiento = self.var_fecha_nacimiento.get().strip()
        if fecha_nacimiento:
            try:
                datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Validacion", "Fecha de nacimiento invalida. Formato esperado: YYYY-MM-DD")
                return
        else:
            fecha_nacimiento = None

        self.datos_paciente = {
            "dni": self.var_dni.get().strip() or None,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono or None,
            "email": email or None,
            "domicilio": self.var_domicilio.get().strip() or None,
            "fecha_nacimiento": fecha_nacimiento,
            "observaciones": self.texto_observaciones.get("1.0", "end").strip() or None,
        }

        self.guardo = True
        self.destroy()


# -------------------------
# PROFESIONALES (FASE 5)
# -------------------------
class FrameProfesionales(ttk.Frame):
    def __init__(self, master, app: AplicacionTurnos, usuario_actual: dict):
        super().__init__(master)
        self.app = app
        self.usuario_actual = usuario_actual

        self.var_busqueda = tk.StringVar()

        titulo = ttk.Label(self, text="Profesionales - CRUD", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))

        barra = ttk.Frame(self)
        barra.grid(row=1, column=0, columnspan=8, sticky="ew", pady=(0, 10))

        ttk.Label(barra, text="Buscar:").grid(row=0, column=0, padx=(0, 8))
        entry_buscar = ttk.Entry(barra, textvariable=self.var_busqueda, width=40)
        entry_buscar.grid(row=0, column=1, padx=(0, 8))
        entry_buscar.bind("<Return>", lambda e: self._cargar_lista())

        ttk.Button(barra, text="Buscar", command=self._cargar_lista).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(barra, text="Limpiar", command=self._limpiar_busqueda).grid(row=0, column=3)

        barra.columnconfigure(1, weight=1)

        columnas = ("id", "matricula", "apellido", "nombre", "especialidad", "telefono", "email")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=14)
        self.tabla.grid(row=3, column=0, columnspan=8, sticky="nsew")

        for col, texto in [
            ("id", "ID"),
            ("matricula", "Matricula"),
            ("apellido", "Apellido"),
            ("nombre", "Nombre"),
            ("especialidad", "Especialidad"),
            ("telefono", "Telefono"),
            ("email", "Email"),
        ]:
            self.tabla.heading(col, text=texto)

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("matricula", width=110, anchor="w")
        self.tabla.column("apellido", width=140, anchor="w")
        self.tabla.column("nombre", width=140, anchor="w")
        self.tabla.column("especialidad", width=160, anchor="w")
        self.tabla.column("telefono", width=130, anchor="w")
        self.tabla.column("email", width=260, anchor="w")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=2, column=8, sticky="ns")

        acciones = ttk.Frame(self)
        acciones.grid(row=3, column=0, columnspan=8, sticky="w", pady=(12, 0))

        ttk.Button(acciones, text="Nuevo", command=self._nuevo).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(acciones, text="Editar", command=self._editar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(acciones, text="Desactivar", command=self._desactivar).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(acciones, text="Volver", command=self.app.mostrar_principal).grid(row=0, column=3, padx=(16, 0))

        self.info = ttk.Label(self, text="Seleccioná un profesional para editar o desactivar.")
        self.info.grid(row=4, column=0, columnspan=8, sticky="w", pady=(10, 0))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._cargar_lista()

    def _limpiar_busqueda(self):
        self.var_busqueda.set("")
        self._cargar_lista()

    def _cargar_lista(self):
        texto = self.var_busqueda.get().strip()
        try:
            lista = listar_profesionales(texto)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar profesionales.\n\nDetalle: {error}")
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for pr in lista:
            self.tabla.insert(
                "",
                "end",
                values=(
                    pr.get("id"),
                    pr.get("matricula") or "",
                    pr.get("apellido") or "",
                    pr.get("nombre") or "",
                    pr.get("especialidad") or "",
                    pr.get("telefono") or "",
                    pr.get("email") or "",
                ),
            )

        self.info.config(text=f"Registros: {len(lista)}")

    def _obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return None
        return int(valores[0])

    def _nuevo(self):
        ventana = VentanaProfesional(self, titulo="Nuevo profesional")
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            crear_profesional(ventana.datos_profesional)
            self._cargar_lista()
            messagebox.showinfo("OK", "Profesional creado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo crear el profesional.\n\nDetalle: {error}")

    def _editar(self):
        profesional_id = self._obtener_id_seleccionado()
        if not profesional_id:
            messagebox.showwarning("Atencion", "Seleccioná un profesional primero.")
            return

        try:
            profesional = obtener_profesional(profesional_id)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo leer el profesional.\n\nDetalle: {error}")
            return

        if not profesional:
            messagebox.showwarning("Atencion", "El profesional ya no existe.")
            self._cargar_lista()
            return

        ventana = VentanaProfesional(self, titulo="Editar profesional", datos_iniciales=profesional)
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            actualizar_profesional(profesional_id, ventana.datos_profesional)
            self._cargar_lista()
            messagebox.showinfo("OK", "Profesional actualizado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el profesional.\n\nDetalle: {error}")

    def _desactivar(self):
        profesional_id = self._obtener_id_seleccionado()
        if not profesional_id:
            messagebox.showwarning("Atencion", "Seleccioná un profesional primero.")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que querés desactivar este profesional?"):
            return

        try:
            desactivar_profesional(profesional_id)
            self._cargar_lista()
            messagebox.showinfo("OK", "Profesional desactivado (borrado logico).")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo desactivar.\n\nDetalle: {error}")


class VentanaProfesional(tk.Toplevel):
    def __init__(self, master, titulo="Profesional", datos_iniciales=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("520x340")
        self.resizable(False, False)

        self.guardo = False
        self.datos_profesional = {}

        self.var_matricula = tk.StringVar(value=(datos_iniciales.get("matricula") if datos_iniciales else "") or "")
        self.var_nombre = tk.StringVar(value=(datos_iniciales.get("nombre") if datos_iniciales else "") or "")
        self.var_apellido = tk.StringVar(value=(datos_iniciales.get("apellido") if datos_iniciales else "") or "")
        self.var_especialidad = tk.StringVar(value=(datos_iniciales.get("especialidad") if datos_iniciales else "") or "")
        self.var_telefono = tk.StringVar(value=(datos_iniciales.get("telefono") if datos_iniciales else "") or "")
        self.var_email = tk.StringVar(value=(datos_iniciales.get("email") if datos_iniciales else "") or "")

        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Matricula:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_matricula, width=34).grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Nombre *:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_nombre, width=34).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Apellido *:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_apellido, width=34).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Especialidad:").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_especialidad, width=34).grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Telefono:").grid(row=4, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_telefono, width=34).grid(row=4, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Email:").grid(row=5, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_email, width=34).grid(row=5, column=1, sticky="w", pady=6)

        botones = ttk.Frame(cont)
        botones.grid(row=6, column=0, columnspan=2, sticky="e", pady=(14, 0))

        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)

        cont.columnconfigure(0, minsize=170)
        cont.columnconfigure(1, weight=1)

        self.grab_set()
        self.focus_force()

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        if not nombre or not apellido:
            messagebox.showwarning("Validacion", "Nombre y Apellido son obligatorios.")
            return

        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        if not validar_telefono(telefono):
            messagebox.showwarning("Validacion", "Telefono invalido. Usá solo números, +, -, espacios o paréntesis.")
            return

        if not validar_email(email):
            messagebox.showwarning("Validacion", "Email invalido. Ejemplo: usuario@dominio.com")
            return

        self.datos_profesional = {
            "matricula": self.var_matricula.get().strip() or None,
            "nombre": nombre,
            "apellido": apellido,
            "especialidad": self.var_especialidad.get().strip() or None,
            "telefono": telefono or None,
            "email": email or None,
        }

        self.guardo = True
        self.destroy()


# -------------------------
# USUARIOS (FASE 5.5)
# -------------------------
class FrameUsuarios(ttk.Frame):
    def __init__(self, master, app: AplicacionTurnos, usuario_actual: dict):
        super().__init__(master)
        self.app = app
        self.usuario_actual = usuario_actual

        self.usuarios_por_id = {}  # dict para acceder rapido al registro seleccionado

        titulo = ttk.Label(self, text="Usuarios - CRUD (solo ADMIN_PRINCIPAL)", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))

        columnas = ("id", "nombre_usuario", "nombre_completo", "rol", "activo", "ultimo_ingreso")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=14)
        self.tabla.grid(row=1, column=0, columnspan=8, sticky="nsew")

        for col, texto in [
            ("id", "ID"),
            ("nombre_usuario", "Usuario"),
            ("nombre_completo", "Nombre completo"),
            ("rol", "Rol"),
            ("activo", "Activo"),
            ("ultimo_ingreso", "Ultimo ingreso"),
        ]:
            self.tabla.heading(col, text=texto)

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre_usuario", width=140, anchor="w")
        self.tabla.column("nombre_completo", width=240, anchor="w")
        self.tabla.column("rol", width=140, anchor="w")
        self.tabla.column("activo", width=90, anchor="center")
        self.tabla.column("ultimo_ingreso", width=200, anchor="w")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=8, sticky="ns")

        acciones = ttk.Frame(self)
        acciones.grid(row=3, column=0, columnspan=8, sticky="w", pady=(12, 0))

        ttk.Button(acciones, text="Nuevo", command=self._nuevo).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(acciones, text="Editar", command=self._editar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(acciones, text="Cambiar contrasena", command=self._cambiar_contrasena).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(acciones, text="Activar/Desactivar", command=self._activar_desactivar).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(acciones, text="Volver", command=self.app.mostrar_principal).grid(row=0, column=4, padx=(16, 0))

        self.info = ttk.Label(self, text="Seleccioná un usuario para editar, cambiar contrasena o activar/desactivar.")
        self.info.grid(row=3, column=0, columnspan=8, sticky="w", pady=(10, 0))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._cargar_lista()

    def _cargar_lista(self):
        try:
            lista = listar_usuarios(self.usuario_actual)
        except PermissionError as error:
            messagebox.showerror("Permisos", str(error))
            self.app.mostrar_principal()
            return
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar usuarios.\n\nDetalle: {error}")
            return

        self.usuarios_por_id = {int(u["id"]): u for u in lista}

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for u in lista:
            activo_txt = "SI" if int(u.get("activo", 0)) == 1 else "NO"
            self.tabla.insert(
                "",
                "end",
                values=(
                    u.get("id"),
                    u.get("nombre_usuario") or "",
                    u.get("nombre_completo") or "",
                    u.get("rol") or "",
                    activo_txt,
                    str(u.get("ultimo_ingreso") or ""),
                ),
            )

        self.info.config(text=f"Registros: {len(lista)}")

    def _obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return None
        return int(valores[0])

    def _nuevo(self):
        ventana = VentanaUsuario(self, titulo="Nuevo usuario (ADMIN/ADMIN_PRINCIPAL)", modo="nuevo")
        self.wait_window(ventana)
        if not ventana.guardo:
            return

        try:
            crear_admin(
                self.usuario_actual,
                ventana.datos_usuario["nombre_usuario"],
                ventana.datos_usuario["nombre_completo"],
                ventana.datos_usuario["contrasena"],
                rol=ventana.datos_usuario["rol"],
            )
            self._cargar_lista()
            messagebox.showinfo("OK", "Usuario creado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo crear el usuario.\n\nDetalle: {error}")

    def _editar(self):
        usuario_id = self._obtener_id_seleccionado()
        if not usuario_id:
            messagebox.showwarning("Atencion", "Seleccioná un usuario primero.")
            return

        datos = self.usuarios_por_id.get(usuario_id)
        if not datos:
            self._cargar_lista()
            return

        ventana = VentanaUsuario(self, titulo="Editar usuario", modo="editar", datos_iniciales=datos)
        self.wait_window(ventana)
        if not ventana.guardo:
            return

        try:
            actualizar_usuario(
                self.usuario_actual,
                usuario_id,
                nombre_completo=ventana.datos_usuario["nombre_completo"],
                rol=ventana.datos_usuario["rol"],
                activo=ventana.datos_usuario["activo"],
            )
            self._cargar_lista()
            messagebox.showinfo("OK", "Usuario actualizado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario.\n\nDetalle: {error}")

    def _cambiar_contrasena(self):
        usuario_id = self._obtener_id_seleccionado()
        if not usuario_id:
            messagebox.showwarning("Atencion", "Seleccioná un usuario primero.")
            return

        datos = self.usuarios_por_id.get(usuario_id)
        if not datos:
            self._cargar_lista()
            return

        ventana = VentanaCambiarContrasena(
            self,
            titulo="Cambiar contrasena de usuario",
            descripcion=f"Usuario: {datos.get('nombre_usuario')} ({datos.get('rol')})",
        )
        self.wait_window(ventana)

        if not ventana.guardo:
            return

        try:
            cambiar_contrasena_usuario(self.usuario_actual, usuario_id, ventana.nueva_contrasena)
            messagebox.showinfo("OK", "Contrasena cambiada correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cambiar la contrasena.\n\nDetalle: {error}")

    def _activar_desactivar(self):
        usuario_id = self._obtener_id_seleccionado()
        if not usuario_id:
            messagebox.showwarning("Atencion", "Seleccioná un usuario primero.")
            return

        datos = self.usuarios_por_id.get(usuario_id)
        if not datos:
            self._cargar_lista()
            return

        activo_actual = int(datos.get("activo", 0))
        nuevo_activo = 0 if activo_actual == 1 else 1
        texto_accion = "desactivar" if nuevo_activo == 0 else "activar"

        if not messagebox.askyesno("Confirmar", f"¿Seguro que querés {texto_accion} este usuario?"):
            return

        try:
            actualizar_usuario(self.usuario_actual, usuario_id, activo=nuevo_activo)
            self._cargar_lista()
            messagebox.showinfo("OK", f"Usuario actualizado: activo={nuevo_activo}.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el estado.\n\nDetalle: {error}")


class VentanaUsuario(tk.Toplevel):
    def __init__(self, master, titulo="Usuario", modo="nuevo", datos_iniciales=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("540x360")
        self.resizable(False, False)

        self.modo = modo
        self.guardo = False
        self.datos_usuario = {}

        self.var_nombre_usuario = tk.StringVar(value=(datos_iniciales.get("nombre_usuario") if datos_iniciales else "") or "")
        self.var_nombre_completo = tk.StringVar(value=(datos_iniciales.get("nombre_completo") if datos_iniciales else "") or "")
        self.var_rol = tk.StringVar(value=(datos_iniciales.get("rol") if datos_iniciales else "ADMIN") or "ADMIN")
        self.var_activo = tk.IntVar(value=int((datos_iniciales.get("activo") if datos_iniciales else 1) or 1))

        self.var_contrasena = tk.StringVar()
        self.var_contrasena_2 = tk.StringVar()

        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Nombre de usuario *:").grid(row=0, column=0, sticky="w", pady=6)
        entry_usuario = ttk.Entry(cont, textvariable=self.var_nombre_usuario, width=34)
        entry_usuario.grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Nombre completo *:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_nombre_completo, width=34).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Rol:").grid(row=3, column=0, sticky="w", pady=6)
        combo_rol = ttk.Combobox(cont, textvariable=self.var_rol, values=["ADMIN", "ADMIN_PRINCIPAL"], state="readonly", width=32)
        combo_rol.grid(row=3, column=1, sticky="w", pady=6)

        ttk.Checkbutton(cont, text="Activo", variable=self.var_activo).grid(row=3, column=1, sticky="w", pady=(2, 10))

        # Password solo en modo nuevo (para editar usamos boton "Cambiar contrasena")
        if self.modo == "nuevo":
            ttk.Label(cont, text="Contrasena *:").grid(row=4, column=0, sticky="w", pady=6)
            ttk.Entry(cont, textvariable=self.var_contrasena, width=34, show="*").grid(row=4, column=1, sticky="w", pady=6)

            ttk.Label(cont, text="Repetir contrasena *:").grid(row=5, column=0, sticky="w", pady=6)
            ttk.Entry(cont, textvariable=self.var_contrasena_2, width=34, show="*").grid(row=5, column=1, sticky="w", pady=6)
        else:
            # En editar: no permitir cambiar nombre de usuario
            entry_usuario.config(state="disabled")

        botones = ttk.Frame(cont)
        botones.grid(row=6, column=0, columnspan=2, sticky="e", pady=(14, 0))

        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)

        cont.columnconfigure(0, minsize=200)
        cont.columnconfigure(1, weight=1)

        self.grab_set()
        self.focus_force()

    def _guardar(self):
        nombre_usuario = self.var_nombre_usuario.get().strip()
        nombre_completo = self.var_nombre_completo.get().strip()
        rol = self.var_rol.get().strip() or "ADMIN"
        activo = 1 if int(self.var_activo.get()) == 1 else 0

        if not nombre_usuario or not nombre_completo:
            messagebox.showwarning("Validacion", "Nombre de usuario y Nombre completo son obligatorios.")
            return

        if rol not in ("ADMIN", "ADMIN_PRINCIPAL"):
            messagebox.showwarning("Validacion", "Rol invalido.")
            return

        if self.modo == "nuevo":
            contrasena = self.var_contrasena.get()
            contrasena_2 = self.var_contrasena_2.get()

            if not contrasena or not contrasena_2:
                messagebox.showwarning("Validacion", "La contrasena es obligatoria.")
                return

            if contrasena != contrasena_2:
                messagebox.showwarning("Validacion", "Las contrasenas no coinciden.")
                return

            self.datos_usuario = {
                "nombre_usuario": nombre_usuario,
                "nombre_completo": nombre_completo,
                "rol": rol,
                "activo": activo,
                "contrasena": contrasena,
            }
        else:
            self.datos_usuario = {
                "nombre_usuario": nombre_usuario,
                "nombre_completo": nombre_completo,
                "rol": rol,
                "activo": activo,
            }

        self.guardo = True
        self.destroy()


class FrameTurnos(ttk.Frame):
    def __init__(self, master, app, usuario_actual: dict):
        super().__init__(master)
        self.app = app
        self.usuario_actual = usuario_actual
        self.turnos_por_id = {}
        self.profesionales_lista = []
        self.profesional_id_por_texto = {}
        titulo = ttk.Label(self, text="Turnos - Agenda diaria", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=10, sticky="w", pady=(0, 10))
        barra = ttk.Frame(self)
        barra.grid(row=1, column=0, columnspan=10, sticky="ew", pady=(0, 10))
        ttk.Label(barra, text="Fecha:").grid(row=0, column=0, padx=(0, 6))
        self.cal_fecha = DateEntry(barra, width=12, date_pattern="yyyy-mm-dd")
        self.cal_fecha.grid(row=0, column=1, padx=(0, 14))
        ttk.Label(barra, text="Profesional:").grid(row=0, column=2, padx=(0, 6))
        self.var_profesional = tk.StringVar(value="TODOS")
        self.combo_profesional = ttk.Combobox(barra, textvariable=self.var_profesional, state="readonly", width=28)
        self.combo_profesional.grid(row=0, column=3, padx=(0, 14))
        ttk.Label(barra, text="Estado:").grid(row=0, column=4, padx=(0, 6))
        self.var_estado = tk.StringVar(value="TODOS")
        self.combo_estado = ttk.Combobox(
            barra,
            textvariable=self.var_estado,
            state="readonly",
            width=16,
            values=["TODOS", "RESERVADO", "ATENDIDO", "CANCELADO", "AUSENTE"],
        )
        self.combo_estado.grid(row=0, column=5, padx=(0, 14))
        ttk.Button(barra, text="Cargar", command=self._cargar_turnos).grid(row=0, column=6, padx=(0, 10))
        ttk.Button(barra, text="Volver", command=self.app.mostrar_principal).grid(row=0, column=7)
        barra.columnconfigure(8, weight=1)
        columnas = ("id", "inicio", "fin", "estado", "paciente", "profesional", "motivo")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=16)
        self.tabla.grid(row=3, column=0, columnspan=10, sticky="nsew")
        for col, texto in [
            ("id", "ID"),
            ("inicio", "Inicio"),
            ("fin", "Fin"),
            ("estado", "Estado"),
            ("paciente", "Paciente"),
            ("profesional", "Profesional"),
            ("motivo", "Motivo"),
        ]:
            self.tabla.heading(col, text=texto)
        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("inicio", width=140, anchor="w")
        self.tabla.column("fin", width=140, anchor="w")
        self.tabla.column("estado", width=120, anchor="w")
        self.tabla.column("paciente", width=220, anchor="w")
        self.tabla.column("profesional", width=220, anchor="w")
        self.tabla.column("motivo", width=260, anchor="w")
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=3, column=10, sticky="ns")
        acciones = ttk.Frame(self)
        acciones.grid(row=3, column=0, columnspan=10, sticky="w", pady=(12, 0))
        ttk.Button(acciones, text="Nuevo", command=self._nuevo).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(acciones, text="Editar", command=self._editar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(acciones, text="Cancelar", command=self._cancelar).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(acciones, text="Marcar ATENDIDO", command=lambda: self._marcar_estado("ATENDIDO")).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(acciones, text="Marcar AUSENTE", command=lambda: self._marcar_estado("AUSENTE")).grid(row=0, column=4, padx=(0, 8))
        self.info = ttk.Label(self, text="Consejo: doble click para editar.")
        self.info.grid(row=4, column=0, columnspan=10, sticky="w", pady=(10, 0))
        self.tabla.bind("<Double-1>", lambda e: self._editar())
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self._cargar_profesionales_filtro()
        self._cargar_turnos()
    def _cargar_profesionales_filtro(self):
        try:
            self.profesionales_lista = listar_profesionales("")  # activos
        except Exception:
            self.profesionales_lista = []
        valores = ["TODOS"]
        self.profesional_id_por_texto = {"TODOS": None}
        for pr in self.profesionales_lista:
            texto = f"{pr['id']} - {pr.get('apellido','')} {pr.get('nombre','')}".strip()
            valores.append(texto)
            self.profesional_id_por_texto[texto] = int(pr["id"])
        self.combo_profesional["values"] = valores
        if self.var_profesional.get() not in valores:
            self.var_profesional.set("TODOS")
    def _formatear_dt(self, valor_dt):
        if valor_dt is None:
            return ""
        if isinstance(valor_dt, str):
            return valor_dt
        # datetime
        return valor_dt.strftime("%Y-%m-%d %H:%M")
    def _cargar_turnos(self):
        fecha = self.cal_fecha.get_date().strftime("%Y-%m-%d")
        profesional_txt = self.var_profesional.get()
        profesional_id = self.profesional_id_por_texto.get(profesional_txt)
        try:
            lista = listar_turnos_por_dia(fecha, profesional_id=profesional_id)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar turnos.\n\nDetalle: {error}")
            return
        estado_filtro = self.var_estado.get()
        if estado_filtro and estado_filtro != "TODOS":
            lista = [t for t in lista if (t.get("estado") == estado_filtro)]
        self.turnos_por_id = {int(t["id"]): t for t in lista}
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for t in lista:
            paciente = f"{t.get('paciente_apellido','')} {t.get('paciente_nombre','')}".strip()
            profesional = f"{t.get('profesional_apellido','')} {t.get('profesional_nombre','')}".strip()
            self.tabla.insert(
                "",
                "end",
                values=(
                    t.get("id"),
                    self._formatear_dt(t.get("inicio")),
                    self._formatear_dt(t.get("fin")),
                    t.get("estado") or "",
                    paciente,
                    profesional,
                    t.get("motivo") or "",
                ),
            )
        self.info.config(text=f"Turnos del dia: {len(lista)}")
    def _obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return None
        return int(valores[0])
    def _obtener_turno_seleccionado(self):
        turno_id = self._obtener_id_seleccionado()
        if not turno_id:
            return None, None
        return turno_id, self.turnos_por_id.get(turno_id)
    def _nuevo(self):
        fecha = self.cal_fecha.get_date()
        ventana = VentanaTurno(self, titulo="Nuevo turno", fecha_inicial=fecha)
        self.wait_window(ventana)
        if not ventana.guardo:
            return
        try:
            crear_turno(ventana.datos_turno, self.usuario_actual)
            self._cargar_turnos()
            messagebox.showinfo("OK", "Turno creado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo crear el turno.\n\nDetalle: {error}")
    def _editar(self):
        turno_id, turno = self._obtener_turno_seleccionado()
        if not turno_id or not turno:
            messagebox.showwarning("Atencion", "Seleccioná un turno primero.")
            return
        ventana = VentanaTurno(self, titulo="Editar turno", datos_iniciales=turno)
        self.wait_window(ventana)
        if not ventana.guardo:
            return
        try:
            actualizar_turno(turno_id, ventana.datos_turno, self.usuario_actual)
            self._cargar_turnos()
            messagebox.showinfo("OK", "Turno actualizado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el turno.\n\nDetalle: {error}")
    def _cancelar(self):
        turno_id, turno = self._obtener_turno_seleccionado()
        if not turno_id or not turno:
            messagebox.showwarning("Atencion", "Seleccioná un turno primero.")
            return
        if str(turno.get("estado")) == "CANCELADO":
            messagebox.showinfo("Info", "Ese turno ya esta CANCELADO.")
            return
        motivo = simpledialog.askstring("Cancelar turno", "Motivo/observacion (opcional):")
        if motivo is None:
            return  # canceló el diálogo
        if not messagebox.askyesno("Confirmar", "¿Seguro que querés cancelar este turno?"):
            return
        try:
            cancelar_turno(turno_id, self.usuario_actual, observaciones=motivo or "")
            self._cargar_turnos()
            messagebox.showinfo("OK", "Turno cancelado.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cancelar.\n\nDetalle: {error}")
    def _marcar_estado(self, estado_nuevo: str):
        turno_id, turno = self._obtener_turno_seleccionado()
        if not turno_id or not turno:
            messagebox.showwarning("Atencion", "Seleccioná un turno primero.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Marcar turno como {estado_nuevo}?"):
            return
        try:
            actualizar_turno(turno_id, {"estado": estado_nuevo}, self.usuario_actual)
            self._cargar_turnos()
            messagebox.showinfo("OK", f"Turno marcado como {estado_nuevo}.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cambiar el estado.\n\nDetalle: {error}")
class VentanaTurno(tk.Toplevel):
    def __init__(self, master, titulo="Turno", fecha_inicial=None, datos_iniciales=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("640x520")
        self.resizable(False, False)
        self.guardo = False
        self.datos_turno = {}
        self.paciente_id = None
        self.profesional_id = None
        # Datos iniciales (si es editar)
        if datos_iniciales:
            self.paciente_id = int(datos_iniciales.get("paciente_id"))
            self.profesional_id = int(datos_iniciales.get("profesional_id"))
        self.var_paciente = tk.StringVar(value=self._texto_persona_inicial(datos_iniciales, "paciente"))
        self.var_profesional = tk.StringVar(value=self._texto_persona_inicial(datos_iniciales, "profesional"))
        self.var_estado = tk.StringVar(value=(datos_iniciales.get("estado") if datos_iniciales else "RESERVADO") or "RESERVADO")
        self.var_motivo = tk.StringVar(value=(datos_iniciales.get("motivo") if datos_iniciales else "") or "")
        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)
        # Paciente
        ttk.Label(cont, text="Paciente *:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_paciente, width=40, state="readonly").grid(row=0, column=1, sticky="w", pady=6)
        ttk.Button(cont, text="Buscar", command=self._buscar_paciente).grid(row=0, column=2, padx=(8, 0))
        # Profesional
        ttk.Label(cont, text="Profesional *:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_profesional, width=40, state="readonly").grid(row=1, column=1, sticky="w", pady=6)
        ttk.Button(cont, text="Buscar", command=self._buscar_profesional).grid(row=1, column=2, padx=(8, 0))
        # Fecha + Hora + Duracion
        ttk.Label(cont, text="Fecha *:").grid(row=3, column=0, sticky="w", pady=6)
        self.cal_fecha = DateEntry(cont, width=12, date_pattern="yyyy-mm-dd")
        self.cal_fecha.grid(row=3, column=1, sticky="w", pady=6)
        ttk.Label(cont, text="Hora inicio (HH:MM) *:").grid(row=3, column=0, sticky="w", pady=6)
        self.var_hora = tk.StringVar()
        ttk.Entry(cont, textvariable=self.var_hora, width=16).grid(row=3, column=1, sticky="w", pady=6)
        ttk.Label(cont, text="Duracion (min) *:").grid(row=4, column=0, sticky="w", pady=6)
        self.var_duracion = tk.StringVar(value="30")
        ttk.Entry(cont, textvariable=self.var_duracion, width=16).grid(row=4, column=1, sticky="w", pady=6)
        # Estado
        ttk.Label(cont, text="Estado:").grid(row=5, column=0, sticky="w", pady=6)
        combo_estado = ttk.Combobox(
            cont,
            textvariable=self.var_estado,
            state="readonly",
            width=18,
            values=["RESERVADO", "ATENDIDO", "CANCELADO", "AUSENTE"],
        )
        combo_estado.grid(row=5, column=1, sticky="w", pady=6)
        # Motivo
        ttk.Label(cont, text="Motivo:").grid(row=6, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_motivo, width=42).grid(row=6, column=1, sticky="w", pady=6)
        # Observaciones
        ttk.Label(cont, text="Observaciones:").grid(row=7, column=0, sticky="nw", pady=6)
        self.texto_observaciones = tk.Text(cont, width=48, height=8)
        self.texto_observaciones.grid(row=7, column=1, columnspan=2, sticky="w", pady=6)
        observaciones_iniciales = (datos_iniciales.get("observaciones") if datos_iniciales else "") or ""
        self.texto_observaciones.insert("1.0", observaciones_iniciales)
        botones = ttk.Frame(cont)
        botones.grid(row=8, column=0, columnspan=3, sticky="e", pady=(14, 0))
        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)
        cont.columnconfigure(0, minsize=190)
        cont.columnconfigure(1, weight=1)
        # Inicializar fecha/hora si viene de editar o nuevo
        if datos_iniciales:
            inicio = datos_iniciales.get("inicio")
            fin = datos_iniciales.get("fin")
            if inicio:
                if isinstance(inicio, str):
                    dt_inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
                else:
                    dt_inicio = inicio
                self.cal_fecha.set_date(dt_inicio.date())
                self.var_hora.set(dt_inicio.strftime("%H:%M"))
            if inicio and fin:
                dt_inicio = inicio if not isinstance(inicio, str) else datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
                dt_fin = fin if not isinstance(fin, str) else datetime.strptime(fin, "%Y-%m-%d %H:%M:%S")
                minutos = int((dt_fin - dt_inicio).total_seconds() // 60)
                self.var_duracion.set(str(max(minutos, 1)))
        else:
            if fecha_inicial:
                self.cal_fecha.set_date(fecha_inicial)
            self.var_hora.set("10:00")
        self.grab_set()
        self.focus_force()
    def _texto_persona_inicial(self, datos, tipo):
        if not datos:
            return ""
        if tipo == "paciente":
            return f"{datos.get('paciente_apellido','')} {datos.get('paciente_nombre','')}".strip()
        return f"{datos.get('profesional_apellido','')} {datos.get('profesional_nombre','')}".strip()
    def _buscar_paciente(self):
        ventana = VentanaSeleccion(
            self,
            titulo="Seleccionar paciente",
            columnas=[("id", "ID", 70), ("dni", "DNI", 120), ("apellido", "Apellido", 160), ("nombre", "Nombre", 160), ("telefono", "Telefono", 140)],
            funcion_listar=listar_pacientes,
        )
        self.wait_window(ventana)
        if ventana.seleccion:
            self.paciente_id = int(ventana.seleccion["id"])
            texto = f"{ventana.seleccion.get('apellido','')} {ventana.seleccion.get('nombre','')}".strip()
            self.var_paciente.set(texto)
    def _buscar_profesional(self):
        ventana = VentanaSeleccion(
            self,
            titulo="Seleccionar profesional",
            columnas=[("id", "ID", 70), ("matricula", "Matricula", 120), ("apellido", "Apellido", 160), ("nombre", "Nombre", 160), ("especialidad", "Especialidad", 180)],
            funcion_listar=listar_profesionales,
        )
        self.wait_window(ventana)
        if ventana.seleccion:
            self.profesional_id = int(ventana.seleccion["id"])
            texto = f"{ventana.seleccion.get('apellido','')} {ventana.seleccion.get('nombre','')}".strip()
            self.var_profesional.set(texto)
    def _guardar(self):
        if not self.paciente_id or not self.profesional_id:
            messagebox.showwarning("Validacion", "Paciente y Profesional son obligatorios.")
            return
        hora_txt = self.var_hora.get().strip()
        duracion_txt = self.var_duracion.get().strip()
        try:
            hora_dt = datetime.strptime(hora_txt, "%H:%M").time()
        except Exception:
            messagebox.showwarning("Validacion", "Hora invalida. Usá formato HH:MM (ej: 10:30).")
            return
        try:
            duracion = int(duracion_txt)
            if duracion <= 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validacion", "Duracion invalida. Ej: 30")
            return
        fecha = self.cal_fecha.get_date()
        inicio_dt = datetime.combine(fecha, hora_dt)
        fin_dt = inicio_dt + timedelta(minutes=duracion)
        estado = self.var_estado.get().strip() or "RESERVADO"
        motivo = self.var_motivo.get().strip() or None
        observaciones = self.texto_observaciones.get("1.0", "end").strip() or None
        self.datos_turno = {
            "paciente_id": self.paciente_id,
            "profesional_id": self.profesional_id,
            "inicio": inicio_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "fin": fin_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "motivo": motivo,
            "estado": estado,
            "observaciones": observaciones,
        }
        self.guardo = True
        self.destroy()
class VentanaSeleccion(tk.Toplevel):
    def __init__(self, master, titulo, columnas, funcion_listar):
        super().__init__(master)
        self.title(titulo)
        self.geometry("820x460")
        self.resizable(False, False)
        self.funcion_listar = funcion_listar
        self.columnas = columnas
        self.seleccion = None
        self.var_busqueda = tk.StringVar()
        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)
        barra = ttk.Frame(cont)
        barra.pack(fill="x", pady=(0, 10))
        ttk.Label(barra, text="Buscar:").pack(side="left")
        entry = ttk.Entry(barra, textvariable=self.var_busqueda, width=40)
        entry.pack(side="left", padx=(8, 8))
        entry.bind("<Return>", lambda e: self._cargar())
        ttk.Button(barra, text="Buscar", command=self._cargar).pack(side="left", padx=(0, 8))
        ttk.Button(barra, text="Limpiar", command=self._limpiar).pack(side="left")
        frame_tabla = ttk.Frame(cont)
        frame_tabla.pack(fill="both", expand=True)
        cols = [c[0] for c in columnas]
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=16)
        self.tabla.pack(side="left", fill="both", expand=True)
        for clave, texto, ancho in columnas:
            self.tabla.heading(clave, text=texto)
            self.tabla.column(clave, width=ancho, anchor="w")
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        botones = ttk.Frame(cont)
        botones.pack(fill="x", pady=(10, 0))
        ttk.Button(botones, text="Seleccionar", command=self._seleccionar).pack(side="right", padx=(8, 0))
        ttk.Button(botones, text="Cancelar", command=self.destroy).pack(side="right")
        self.tabla.bind("<Double-1>", lambda e: self._seleccionar())
        entry.focus()
        self._cargar()
        self.grab_set()
        self.focus_force()
    def _limpiar(self):
        self.var_busqueda.set("")
        self._cargar()
    def _cargar(self):
        texto = self.var_busqueda.get().strip()
        try:
            lista = self.funcion_listar(texto)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar.\n\nDetalle: {error}")
            return
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in lista:
            valores = []
            for clave, _, _ in self.columnas:
                valores.append(fila.get(clave) if fila.get(clave) is not None else "")
            self.tabla.insert("", "end", values=tuple(valores), tags=(str(fila.get("id")),))
    def _seleccionar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Seleccioná un registro.")
            return
        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return
        # reconstruir dict básico
        datos = {}
        for i, (clave, _, _) in enumerate(self.columnas):
            datos[clave] = valores[i]
        # ID siempre presente
        datos["id"] = int(datos["id"])
        self.seleccion = datos
        self.destroy()




class VentanaCambiarContrasena(tk.Toplevel):
    def __init__(self, master, titulo="Cambiar contrasena", descripcion=""):
        super().__init__(master)
        self.title(titulo)
        self.geometry("520x240")
        self.resizable(False, False)

        self.guardo = False
        self.nueva_contrasena = ""

        self.var_contrasena = tk.StringVar()
        self.var_contrasena_2 = tk.StringVar()

        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text=descripcion).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(cont, text="Nueva contrasena *:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_contrasena, width=34, show="*").grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(cont, text="Repetir contrasena *:").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(cont, textvariable=self.var_contrasena_2, width=34, show="*").grid(row=3, column=1, sticky="w", pady=6)

        botones = ttk.Frame(cont)
        botones.grid(row=3, column=0, columnspan=2, sticky="e", pady=(14, 0))

        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)

        cont.columnconfigure(0, minsize=200)
        cont.columnconfigure(1, weight=1)

        self.grab_set()
        self.focus_force()

    def _guardar(self):
        contrasena = self.var_contrasena.get()
        contrasena_2 = self.var_contrasena_2.get()

        if not contrasena or not contrasena_2:
            messagebox.showwarning("Validacion", "La contrasena es obligatoria.")
            return
        if contrasena != contrasena_2:
            messagebox.showwarning("Validacion", "Las contrasenas no coinciden.")
            return

        self.nueva_contrasena = contrasena
        self.guardo = True
        self.destroy()


def main():
    app = AplicacionTurnos()
    app.mainloop()


if __name__ == "__main__":
    main()
# Sistema de Turnos Odontológicos (Python Desktop)

Aplicación de escritorio desarrollada con **Tkinter + MySQL** para gestionar:
- Pacientes
- Profesionales
- Turnos
- Usuarios (solo administrador principal)

---

## 1) Mejoras incorporadas en esta versión

- **Mejoras visuales**: tema más moderno, mejor espaciado, tarjetas de acceso, tablas más legibles.
- **Mayor intuitividad**: login centrado con mensaje guía y panel principal con indicaciones de flujo recomendado.
- **Validaciones y manejo de errores**:
  - Validación de email en pacientes/profesionales.
  - Validación de formato de teléfono.
  - Validación estricta de fecha de nacimiento (`YYYY-MM-DD`).
  - Mensajes de error más claros al iniciar sesión.
- **Compatibilidad con XAMPP sin usuario/contraseña**:
  - La conexión ahora usa por defecto `BD_USUARIO=""` y `BD_CONTRASENA=""`.

---

## 2) Requisitos para ejecutar en Windows

1. **Windows 10/11**
2. **Python 3.11+** (recomendado 3.11 o 3.12)
3. **XAMPP** con módulo **MySQL** activo
4. Paquetes Python:
   - `mysql-connector-python`
   - `python-dotenv`
   - `tkcalendar`

---

## 3) Guía completa paso a paso (Windows + XAMPP)

## Paso 1: Instalar Python

1. Descargá Python desde: https://www.python.org/downloads/windows/
2. Durante la instalación, marcá la opción **"Add Python to PATH"**.
3. Verificá en `CMD` o `PowerShell`:

```bash
python --version
pip --version
```

## Paso 2: Instalar XAMPP

1. Descargá XAMPP desde: https://www.apachefriends.org/es/index.html
2. Instalá XAMPP y abrí el **XAMPP Control Panel**.
3. Iniciá el servicio **MySQL**.
4. Entrá a `http://localhost/phpmyadmin`.

## Paso 3: Crear base de datos

En phpMyAdmin:
1. Crear base de datos, por ejemplo: `clinica_turnos`.
2. Importar tu script SQL (si ya lo tenés) o crear tablas manualmente según tu modelo.

> Si querés, en una siguiente iteración te puedo preparar un `schema.sql` completo listo para importar.

## Paso 4: Descargar / abrir el proyecto

Desde una terminal (CMD/PowerShell):

```bash
git clone <URL_DEL_REPOSITORIO>
cd Python_Final
```

Si ya lo tenés descargado, solo ubicáte en la carpeta raíz del proyecto.

## Paso 5: Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

Si usás PowerShell y te bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Paso 6: Instalar dependencias

```bash
pip install mysql-connector-python python-dotenv tkcalendar
```

## Paso 7: Configurar variables de entorno (`.env`)

Crear un archivo `.env` dentro de `clinica_turnos_app/` con este contenido:

```env
BD_HOST=localhost
BD_PUERTO=3306
BD_NOMBRE=clinica_turnos

# Como usás XAMPP sin usuario/clave:
BD_USUARIO=
BD_CONTRASENA=
```

> Importante: si tu MySQL en realidad usa `root` sin contraseña, entonces usá:
>
> ```env
> BD_USUARIO=root
> BD_CONTRASENA=
> ```

## Paso 8: Crear administrador principal (solo primera vez)

Desde la raíz del repo:

```bash
python clinica_turnos_app/crear_admin_principal.py
```

## Paso 9: Ejecutar la app

```bash
python clinica_turnos_app/main_tk.py
```

---

## 4) Solución de errores comunes

### Error: "No se pudo validar el inicio de sesión"
- Verificá que **MySQL esté iniciado en XAMPP**.
- Revisá que el `.env` esté en `clinica_turnos_app/.env`.
- Confirmá `BD_HOST`, `BD_PUERTO` y `BD_NOMBRE`.

### Error de conexión MySQL (Access denied)
- Si pusiste usuario vacío y falla, probá `BD_USUARIO=root`.
- Dejá `BD_CONTRASENA=` vacía si no usás contraseña.

### No abre la interfaz Tkinter
- Confirmá que Python está bien instalado (`python --version`).
- Reinstalá dependencias en el entorno virtual activo.

---

## 5) Flujo recomendado de uso del sistema

1. Iniciar sesión.
2. Cargar pacientes.
3. Cargar profesionales.
4. Crear turnos.
5. Gestionar usuarios (solo admin principal).

---

## 6) Estructura principal del proyecto

- `clinica_turnos_app/main_tk.py`: interfaz gráfica y navegación.
- `clinica_turnos_app/app/bd.py`: conexión y utilidades de BD.
- `clinica_turnos_app/app/repositorios/`: operaciones CRUD por módulo.
- `clinica_turnos_app/crear_admin_principal.py`: alta de admin principal.

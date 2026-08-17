import pyodbc

class conexionBD:
    def __init__(self):
        self.servidor = r"KOBIN\SQLEXPRESS"
        self.base_datos = "Clinica_Dental"
        self.driver = "ODBC Driver 18 for SQL Server"
        self.trust = "yes"

    def obtener_conexion(self):
        cadena = (
            f"DRIVER={self.driver};"
            f"SERVER={self.servidor};"
            f"DATABASE={self.base_datos};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate={self.trust};"
        )
        return pyodbc.connect(cadena)

def login(usuario: str, contrasena: str): #usado para el log in del inicio, comprueba las credenciales
    """
    Si todo es correcto, retorna (conn, id_funcionario, nombre_completo).
    Si algo falla, lanza ValueError con el mensaje correspondiente.
    """
    bd = conexionBD() #declaramos la clase conexion BD
    conn = bd.obtener_conexion() #llamamos a bd y de esta manera llamar a obtener conexion
    cursor = conn.cursor() #se llama a si mismo dentro de conn

    cursor.execute(
        """
        SELECT f.id_funcionario, f. usuario, f.nombre_completo,f.estado,f.contrasena
        FROM Funcionario f
        WHERE f.usuario = ?;
        """,
        usuario, #usuario tambien lo pasamos,equivalente de sql
    )
    row = cursor.fetchone() #fetchone trae una sola fila del resultado como tupla

    if row is None: #si el usuario no es valido o no lo encuentra
        conn.close()
        raise ValueError("Usuario no encontrado")

    id_funcionario, usuario,nombre_completo, estado,contrasena_guardada = row

    if not estado: #usuario inactivo segun la tabla
        conn.close()
        raise ValueError("Usuario inactivo")

    if str(contrasena_guardada) != str(contrasena): #clave
        conn.close()
        raise ValueError("Contraseña incorrecta")

    cursor.execute( #
        "EXEC sp_set_session_context @key=N'id_funcionario', @value=?",
        id_funcionario,
    )
    conn.commit()

    return conn, id_funcionario, f"{nombre_completo}" #usuario actual

# ------------------------------------------------------------------
# FUNCIONARIO a SQL, cruds
# ------------------------------------------------------------------
COLUMNAS_FUNCIONARIO = [
    "id_funcionario", "usuario", "nombre_completo", "estado", "contrasena",
]

def listar_funcionarios(conn: pyodbc.Connection, filtro: str = ""): #conn: pyodbc.Connection, se espera que sea un objeto de conexión de pyodbc. 
    cursor = conn.cursor()
    if filtro:
        like = f"%{filtro}%" #LIKE usa %, significa cualquier cantidad de caracteres incluyendo cero, plantilla que va a hacer que sql busque cualquier fila contenga el filtro
        cursor.execute(
            f"""
            SELECT {', '.join(COLUMNAS_FUNCIONARIO)}
            FROM Funcionario
            WHERE id_funcionario LIKE ? OR usuario LIKE ? OR nombre_completo LIKE ?
            ORDER BY id_funcionario
            """, #querys de sql
            (like, like, like),
        )
    else:
        cursor.execute(
            f"SELECT {', '.join(COLUMNAS_FUNCIONARIO)} FROM Funcionario ORDER BY id_funcionario"
        )
    return cursor.fetchall()


def obtener_funcionario_por_usuario(conn: pyodbc.Connection, usuario: str):
    """Usado para validar duplicados y para el login."""
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {', '.join(COLUMNAS_FUNCIONARIO)} FROM Funcionario WHERE usuario = ?",
        usuario,
    )
    return cursor.fetchone()


def crear_funcionario(conn: pyodbc.Connection, data: dict) -> None: #data: dict → data se espera que sea un diccionario., -> None → indica que la función no retorna nada
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Funcionario (id_funcionario, usuario, nombre_completo, estado, contrasena)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["id_funcionario"], data["usuario"], data["nombre_completo"],
            data["estado"], data["contrasena"],
        ),
    )
    conn.commit()


def actualizar_funcionario(conn: pyodbc.Connection, id_funcionario: str, data: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Funcionario
        SET usuario = ?, nombre_completo = ?, estado = ?, contrasena = ?
        WHERE id_funcionario = ?
        """,
        (
            data["usuario"], data["nombre_completo"], data["estado"],
            data["contrasena"], id_funcionario,
        ),
    )
    conn.commit()


def eliminar_funcionario(conn: pyodbc.Connection, id_funcionario: str) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Funcionario WHERE id_funcionario = ?", id_funcionario)
    conn.commit()


# ------------------------------------------------------------------
# Encargado a SQL, cruds
# ------------------------------------------------------------------

COLUMNAS_ENCARGADO = [
    "id_encargado", "nombre_completo", "identificacion", "direccion",
    "provincia", "canton", "distrito", "telefono", "correo_electronico",
]

def listar_encargados(conn: pyodbc.Connection, filtro: str = ""): #conn: pyodbc.Connection, se espera que sea un objeto de conexión de pyodbc. 
    cursor = conn.cursor()
    if filtro:
        like = f"%{filtro}%" #LIKE usa %, significa cualquier cantidad de caracteres incluyendo cero, plantilla que va a hacer que sql busque cualquier fila contenga el filtro
        cursor.execute(
            f"""
            SELECT {', '.join(COLUMNAS_ENCARGADO)}
            FROM Encargados
            WHERE nombre_completo LIKE ? OR identificacion LIKE ?
            ORDER BY id_encargado
            """, #querys de sql
            (like, like),
        )
    else:
        cursor.execute(
            f"SELECT {', '.join(COLUMNAS_ENCARGADO)} FROM Encargados ORDER BY id_encargado"
        )
    return cursor.fetchall()

def obtener_encargado_por_identificacion(conn: pyodbc.Connection, identificacion: str): #usamos identificacion para encontrar
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {', '.join(COLUMNAS_ENCARGADO)} FROM Encargados WHERE identificacion = ?", #equivalencia en sql
        identificacion,
    )
    return cursor.fetchone() #solo uno, el que concuerda

def crear_encargado(conn: pyodbc.Connection, data: dict) -> int: #
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Encargados (nombre_completo, identificacion, direccion,
                                provincia, canton, distrito, telefono, correo_electronico)
        OUTPUT INSERTED.id_encargado
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["nombre_completo"], data["identificacion"], data["direccion"],
            data["provincia"], data["canton"], data["distrito"],
            data["telefono"], data["correo_electronico"],
        ),
    )
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    return nuevo_id #al ser una PK,debemos asegurarnos que no se caiga por la parte de sql por el id.

def actualizar_encargado(conn: pyodbc.Connection, id_encargado: int, data: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Encargados
        SET nombre_completo = ?, identificacion = ?, direccion = ?,
            provincia = ?, canton = ?, distrito = ?, telefono = ?, correo_electronico = ?
        WHERE id_encargado = ?
        """,
        (
            data["nombre_completo"], data["identificacion"], data["direccion"],
            data["provincia"], data["canton"], data["distrito"],
            data["telefono"], data["correo_electronico"], id_encargado,
        ),
    )
    conn.commit()

def contar_menores_de_encargado(conn: pyodbc.Connection, id_encargado: int) -> int: #metodo especial para saber cuantos y cuales menores estan asociados.
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM MenoresEdad WHERE id_encargado = ?", id_encargado)
    return cursor.fetchone()[0]

def eliminar_encargado(conn: pyodbc.Connection, id_encargado: int) -> None:
    """Elimina el encargado y sus menores a cargo, en su totalidad. Es una decision de disenho
    si algo falla, se revierte completo. con rollback"""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM MenoresEdad WHERE id_encargado = ?", id_encargado)
        cursor.execute("DELETE FROM Encargados WHERE id_encargado = ?", id_encargado)
        conn.commit()
    except pyodbc.Error:
        conn.rollback()
        raise

# ------------------------------------------------------------------
# CRUD - MENOR DE EDAD
# ------------------------------------------------------------------
COLUMNAS_MENOR = [
    "id_menor_edad", "nombre", "primer_apellido", "segundo_apellido",
    "sexo", "fecha_nacimiento", "id_encargado",
]

def listar_menores(conn: pyodbc.Connection, filtro: str = ""):
    """Trae los menores junto con el nombre de su encargado (JOIN),
    ya que MenoresEdad solo guarda el id_encargado, no el nombre."""
    cursor = conn.cursor()
    if filtro:
        like = f"%{filtro}%"
        cursor.execute(
            """
            SELECT m.id_menor_edad, m.nombre, m.primer_apellido, m.segundo_apellido,
            m.sexo, m.fecha_nacimiento, m.id_encargado, e.nombre_completo, e.identificacion
            FROM MenoresEdad m
            JOIN Encargados e ON e.id_encargado = m.id_encargado
            WHERE m.nombre LIKE ? OR m.primer_apellido LIKE ?
            OR CAST(m.id_menor_edad AS VARCHAR) LIKE ? OR e.identificacion LIKE ?
            ORDER BY m.id_menor_edad
            """,
            (like, like, like, like),
        )
    else:
        cursor.execute(
            """
            SELECT m.id_menor_edad, m.nombre, m.primer_apellido, m.segundo_apellido,
            m.sexo, m.fecha_nacimiento, m.id_encargado, e.nombre_completo, e.identificacion
            FROM MenoresEdad m
            JOIN Encargados e ON e.id_encargado = m.id_encargado
            ORDER BY m.id_menor_edad
            """
        )
    return cursor.fetchall()


def crear_menor(conn: pyodbc.Connection, data: dict) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO MenoresEdad (nombre, primer_apellido, segundo_apellido, sexo, fecha_nacimiento, id_encargado)
        OUTPUT INSERTED.id_menor_edad
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["nombre"], data["primer_apellido"], data["segundo_apellido"],
            data["sexo"], data["fecha_nacimiento"], data["id_encargado"],
        ),
    )
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    return nuevo_id


def actualizar_menor(conn: pyodbc.Connection, id_menor: int, data: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE MenoresEdad
        SET nombre = ?, primer_apellido = ?, segundo_apellido = ?, sexo = ?,
            fecha_nacimiento = ?, id_encargado = ?
        WHERE id_menor_edad = ?
        """,
        (
            data["nombre"], data["primer_apellido"], data["segundo_apellido"],
            data["sexo"], data["fecha_nacimiento"], data["id_encargado"], id_menor,
        ),
    )
    conn.commit()


def contar_citas_de_menor(conn: pyodbc.Connection, id_menor: int) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ServiciosBrindados WHERE id_menor_edad = ?", id_menor)
    return cursor.fetchone()[0]


def eliminar_menor(conn: pyodbc.Connection, id_menor: int) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MenoresEdad WHERE id_menor_edad = ?", id_menor)
    conn.commit()

# ------------------------------------------------------------------
# CRUD - SERVICIOS DISPONIBLES
# ------------------------------------------------------------------
COLUMNAS_SERVICIO = ["id_servicio", "nombre_servicio", "costo", "descripcion"]


def listar_servicios(conn: pyodbc.Connection, filtro: str = ""):
    cursor = conn.cursor()
    if filtro:
        like = f"%{filtro}%"
        cursor.execute(
            f"""
            SELECT {', '.join(COLUMNAS_SERVICIO)}
            FROM ServiciosDisponibles
            WHERE id_servicio LIKE ? OR nombre_servicio LIKE ?
            ORDER BY id_servicio
            """,
            (like, like),
        )
    else:
        cursor.execute(
            f"SELECT {', '.join(COLUMNAS_SERVICIO)} FROM ServiciosDisponibles ORDER BY id_servicio"
        )
    return cursor.fetchall()


def obtener_servicio(conn: pyodbc.Connection, id_servicio: str):
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {', '.join(COLUMNAS_SERVICIO)} FROM ServiciosDisponibles WHERE id_servicio = ?",
        id_servicio,
    )
    return cursor.fetchone()


def crear_servicio(conn: pyodbc.Connection, data: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ServiciosDisponibles (id_servicio, nombre_servicio, costo, descripcion)
        VALUES (?, ?, ?, ?)
        """,
        (data["id_servicio"], data["nombre_servicio"], data["costo"], data["descripcion"]),
    )
    conn.commit()


def actualizar_servicio(conn: pyodbc.Connection, id_servicio: str, data: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE ServiciosDisponibles
        SET nombre_servicio = ?, costo = ?, descripcion = ?
        WHERE id_servicio = ?
        """,
        (data["nombre_servicio"], data["costo"], data["descripcion"], id_servicio),
    )
    conn.commit()


def contar_citas_de_servicio(conn: pyodbc.Connection, id_servicio: str) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ServiciosBrindados WHERE id_servicio = ?", id_servicio)
    return cursor.fetchone()[0]


def eliminar_servicio(conn: pyodbc.Connection, id_servicio: str) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ServiciosDisponibles WHERE id_servicio = ?", id_servicio)
    conn.commit()
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
        WHERE f.usuario = ?; #equivalente de sql
        """,
        usuario, #usuario tambien lo pasamos
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
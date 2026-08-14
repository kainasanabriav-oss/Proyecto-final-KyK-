import xml.etree.ElementTree as ET


class Funcionario:
    """Modelo de funcionario. La interfaz se encarga de pedir los datos."""
    funcionarios = []
    usuario_Actual = None

    def __init__(self, ID_funcionario, Usuario, Nombre_Completo, Estado=True, Contrasena="1234"):
        self.ID_funcionario = ID_funcionario
        self.Usuario = Usuario
        self.Nombre_Completo = Nombre_Completo
        self.Estado = Estado
        self.Contrasena = Contrasena

    @property
    def ID_funcionario(self):
        return self.__ID_funcionario

    @ID_funcionario.setter
    def ID_funcionario(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El ID del funcionario no puede estar vacío.")
        self.__ID_funcionario = valor

    @property
    def Usuario(self):
        return self.__Usuario

    @Usuario.setter
    def Usuario(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El usuario no puede estar vacío.")
        self.__Usuario = valor

    @property
    def Nombre_Completo(self):
        return self.__Nombre_Completo

    @Nombre_Completo.setter
    def Nombre_Completo(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self.__Nombre_Completo = valor

    @property
    def Estado(self):
        return self.__Estado

    @Estado.setter
    def Estado(self, valor):
        self.__Estado = bool(valor)

    @classmethod
    def buscar_por_usuario(cls, usuario):
        usuario = usuario.strip().lower()
        return next((f for f in cls.funcionarios if f.Usuario.lower() == usuario), None)

    @classmethod
    def cargar_Funcionarios_xml(cls, ruta):
        cls.funcionarios.clear()
        try:
            raiz = ET.parse(ruta).getroot()
            for nodo in raiz.findall("funcionario"):
                usuario = (nodo.findtext("usuario") or "").strip()
                nombre = (nodo.findtext("nombre_completo") or "").strip()
                estado = (nodo.findtext("estado") or "True") == "True"
                contrasena = nodo.findtext("contrasena") or "1234"
                cls.funcionarios.append(cls(nodo.get("id", ""), usuario, nombre, estado, contrasena))
        except (FileNotFoundError, ET.ParseError):
            pass

    @classmethod
    def guardar_Funcionarios_xml(cls, ruta):
        raiz = ET.Element("funcionarios")
        for fun in cls.funcionarios:
            nodo = ET.SubElement(raiz, "funcionario", id=str(fun.ID_funcionario))
            ET.SubElement(nodo, "usuario").text = fun.Usuario
            ET.SubElement(nodo, "nombre_completo").text = fun.Nombre_Completo
            ET.SubElement(nodo, "estado").text = str(fun.Estado)
            ET.SubElement(nodo, "contrasena").text = fun.Contrasena
        ET.ElementTree(raiz).write(ruta, encoding="utf-8", xml_declaration=True)

import xml.etree.ElementTree as ET
from datetime import date
from MenorEdad import MenorEdad


class Encargado:
    """Modelo del padre o encargado y sus hijos."""
    encargados = []

    def __init__(self, ID_encargado, Nombre_Completo, Identificacion, Provincia, Canton, Distrito,
                 Direccion, Telefono, Correo_Electronico):
        self.ID_encargado = str(ID_encargado).strip()
        self.Nombre_Completo = Nombre_Completo
        self.Identificacion = Identificacion
        self.Provincia = Provincia
        self.Canton = Canton
        self.Distrito = Distrito
        self.Direccion = Direccion
        self.Telefono = Telefono
        self.Correo_Electronico = Correo_Electronico
        self.menoresEdad = []#se guardan los niños

    @property
    def Nombre_Completo(self):
        return self.__Nombre_Completo

    @Nombre_Completo.setter
    def Nombre_Completo(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre completo no puede estar vacío.")
        self.__Nombre_Completo = valor

    @property
    def Identificacion(self):
        return self.__Identificacion

    @Identificacion.setter
    def Identificacion(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("La identificación no puede estar vacía.")
        self.__Identificacion = valor

    @property
    def Telefono(self):
        return self.__Telefono

    @Telefono.setter
    def Telefono(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El teléfono no puede estar vacío.")
        if not valor.replace("-", "").isdigit():
            raise ValueError("El teléfono solo puede contener números y guiones.")
        self.__Telefono = valor

    @property
    def Correo_Electronico(self):
        return self.__Correo_Electronico

    @Correo_Electronico.setter
    def Correo_Electronico(self, valor):
        valor = str(valor).strip()
        if valor and "@" not in valor:
            raise ValueError("El correo electrónico debe contener @.")
        self.__Correo_Electronico = valor

    @classmethod
    def buscar_por_identificacion(cls, identificacion):
        return next((e for e in cls.encargados if e.Identificacion == identificacion.strip()), None)

    @classmethod
    def todos_los_menores(cls):
        salida = []
        for encargado in cls.encargados:
            for menor in encargado.menoresEdad:
                salida.append((encargado, menor))
        return salida

    @classmethod
    def cargar_Encargados_xml(cls, ruta):
        cls.encargados.clear()
        try:
            try:
                raiz = ET.parse(ruta).getroot()
            except ET.ParseError:
                # El XML del Proyecto 1 tenía texto accidental después de </encargados>.
                # Se recupera únicamente la parte XML válida para no perder los registros.
                with open(ruta, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                cierre = "</encargados>"
                if cierre not in contenido:
                    raise
                raiz = ET.fromstring(contenido[:contenido.index(cierre) + len(cierre)])
            for nodo in raiz.findall("encargado"):
                # Compatibilidad con el XML del Proyecto 1: nombre + apellidos separados.
                nombre_completo = nodo.findtext("nombre_completo")
                if not nombre_completo:
                    nombre_completo = " ".join(filter(None, [nodo.findtext("nombre"), nodo.findtext("primer_apellido"), nodo.findtext("segundo_apellido")]))
                encargado = cls(
                    nodo.get("id", ""), nombre_completo, nodo.findtext("identificacion") or "",
                    nodo.findtext("provincia") or "", nodo.findtext("canton") or "",
                    nodo.findtext("distrito") or nodo.findtext("codigo_postal") or "",
                    nodo.findtext("direccion") or "", nodo.findtext("telefono") or "",
                    nodo.findtext("correo") or ""
                )
                menores = nodo.find("menores")
                if menores is not None:
                    for m in menores.findall("menor"):
                        encargado.menoresEdad.append(MenorEdad(
                            m.get("id", ""), m.findtext("nombre") or "", m.findtext("primer_apellido") or "",
                            m.findtext("segundo_apellido") or "", m.findtext("sexo") or "",
                            date.fromisoformat(m.findtext("fecha_nacimiento"))
                        ))
                cls.encargados.append(encargado)
        except (FileNotFoundError, ET.ParseError, ValueError):
            pass

    @classmethod
    def guardar_Encargados_xml(cls, ruta):
        raiz = ET.Element("encargados")
        for enc in cls.encargados:
            nodo = ET.SubElement(raiz, "encargado", id=str(enc.ID_encargado))
            ET.SubElement(nodo, "nombre_completo").text = enc.Nombre_Completo
            ET.SubElement(nodo, "identificacion").text = enc.Identificacion
            ET.SubElement(nodo, "provincia").text = enc.Provincia
            ET.SubElement(nodo, "canton").text = enc.Canton
            ET.SubElement(nodo, "distrito").text = enc.Distrito
            ET.SubElement(nodo, "direccion").text = enc.Direccion
            ET.SubElement(nodo, "telefono").text = enc.Telefono
            ET.SubElement(nodo, "correo").text = enc.Correo_Electronico
            menores = ET.SubElement(nodo, "menores")
            for m in enc.menoresEdad:
                mn = ET.SubElement(menores, "menor", id=str(m.ID_menorEdad))
                ET.SubElement(mn, "nombre").text = m.Nombre
                ET.SubElement(mn, "primer_apellido").text = m.Primer_Apellido
                ET.SubElement(mn, "segundo_apellido").text = m.Segundo_Apellido
                ET.SubElement(mn, "sexo").text = m.Sexo
                ET.SubElement(mn, "fecha_nacimiento").text = str(m.Fecha_Nacimiento)
        ET.ElementTree(raiz).write(ruta, encoding="utf-8", xml_declaration=True)

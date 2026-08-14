import xml.etree.ElementTree as ET


class ServiciosDisponibles:
    servicios = []

    def __init__(self, ID_Servicio, Nombre_Servicio, Costo, Descripcion=""):
        self.ID_Servicio = str(ID_Servicio).strip()
        self.Nombre_Servicio = str(Nombre_Servicio).strip()
        self.Costo = float(Costo)
        self.Descripcion = str(Descripcion).strip()
        if not self.ID_Servicio or not self.Nombre_Servicio:
            raise ValueError("Código y nombre del servicio son obligatorios.")
        if self.Costo < 0:
            raise ValueError("El costo no puede ser negativo.")

    @classmethod
    def cargar_Servicios_xml(cls, ruta):
        cls.servicios.clear()
        try:
            raiz = ET.parse(ruta).getroot()
            for nodo in raiz.findall("servicio"):
                cls.servicios.append(cls(
                    nodo.get("id", ""), nodo.findtext("nombre_servicio") or "",
                    float(nodo.findtext("costo") or 0), nodo.findtext("descripcion") or ""
                ))
        except (FileNotFoundError, ET.ParseError, ValueError):
            pass

    @classmethod
    def guardar_Servicios_xml(cls, ruta):
        raiz = ET.Element("servicios")
        for ser in cls.servicios:
            nodo = ET.SubElement(raiz, "servicio", id=ser.ID_Servicio)
            ET.SubElement(nodo, "nombre_servicio").text = ser.Nombre_Servicio
            ET.SubElement(nodo, "costo").text = str(ser.Costo)
            ET.SubElement(nodo, "descripcion").text = ser.Descripcion
        ET.ElementTree(raiz).write(ruta, encoding="utf-8", xml_declaration=True)

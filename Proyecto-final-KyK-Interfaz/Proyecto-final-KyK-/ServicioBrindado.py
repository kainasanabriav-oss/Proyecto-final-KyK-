import xml.etree.ElementTree as ET
from datetime import date
from ServiciosDisponibles import ServiciosDisponibles
from MenorEdad import MenorEdad
from Funcionario import Funcionario


class ServicioBrindado:
    IVA = 0.02
    facturas = []
    consecutivo = 0

    def __init__(self, Menor, Funcionario, Fecha_Cita=None, id_externo=None):
        if id_externo is None:
            ServicioBrindado.consecutivo += 1
            self.ID_cita = ServicioBrindado.consecutivo
        else:
            self.ID_cita = int(id_externo)
            ServicioBrindado.consecutivo = max(ServicioBrindado.consecutivo, self.ID_cita)
        self.Menor = Menor
        self.Funcionario = Funcionario
        self.Fecha_Cita = Fecha_Cita or date.today()
        self.Cancelado = False
        self.Servicios = []

    def agregar_Servicio(self, servicio):
        self.Servicios.append(servicio)

    def eliminar_Servicio(self, servicio):
        if servicio in self.Servicios:
            self.Servicios.remove(servicio)

    def calcular_Subtotal(self):
        return sum(s.Costo for s in self.Servicios)

    def calcular_IVA(self):
        return self.calcular_Subtotal() * self.IVA

    def calcular_Total(self):
        return self.calcular_Subtotal() + self.calcular_IVA()

    @classmethod
    def guardar_Facturas_xml(cls, ruta):
        raiz = ET.Element("facturas")
        for fac in cls.facturas:
            nodo = ET.SubElement(raiz, "cita", id=str(fac.ID_cita))
            ET.SubElement(nodo, "fecha").text = str(fac.Fecha_Cita)
            ET.SubElement(nodo, "estado").text = "Cancelado" if fac.Cancelado else "Pendiente"
            mn = ET.SubElement(nodo, "menor", id=str(fac.Menor.ID_menorEdad))
            ET.SubElement(mn, "nombre").text = fac.Menor.Nombre
            ET.SubElement(mn, "primer_apellido").text = fac.Menor.Primer_Apellido
            ET.SubElement(mn, "segundo_apellido").text = fac.Menor.Segundo_Apellido
            ET.SubElement(mn, "sexo").text = fac.Menor.Sexo
            ET.SubElement(mn, "fecha_nacimiento").text = str(fac.Menor.Fecha_Nacimiento)
            fn = ET.SubElement(nodo, "funcionario", id=str(fac.Funcionario.ID_funcionario))
            ET.SubElement(fn, "usuario").text = fac.Funcionario.Usuario
            ET.SubElement(fn, "nombre_completo").text = fac.Funcionario.Nombre_Completo
            sn = ET.SubElement(nodo, "servicios")
            for ser in fac.Servicios:
                s = ET.SubElement(sn, "servicio", id=ser.ID_Servicio)
                ET.SubElement(s, "nombre_servicio").text = ser.Nombre_Servicio
                ET.SubElement(s, "costo").text = str(ser.Costo)
                ET.SubElement(s, "descripcion").text = ser.Descripcion
        ET.ElementTree(raiz).write(ruta, encoding="utf-8", xml_declaration=True)

    @classmethod
    def cargar_Facturas_xml(cls, ruta):
        cls.facturas.clear()
        cls.consecutivo = 0
        try:
            raiz = ET.parse(ruta).getroot()
            for nodo in raiz.findall("cita"):
                mn = nodo.find("menor")
                menor = MenorEdad(mn.get("id", ""), mn.findtext("nombre") or "", mn.findtext("primer_apellido") or "",
                                   mn.findtext("segundo_apellido") or "", mn.findtext("sexo") or "",
                                   date.fromisoformat(mn.findtext("fecha_nacimiento")))
                fn = nodo.find("funcionario")
                fun = Funcionario(fn.get("id", ""), fn.findtext("usuario") or "", fn.findtext("nombre_completo") or "", True)
                fac = cls(menor, fun, date.fromisoformat(nodo.findtext("fecha")), nodo.get("id"))
                fac.Cancelado = nodo.findtext("estado") == "Cancelado"
                servicios = nodo.find("servicios")
                if servicios is not None:
                    for sn in servicios.findall("servicio"):
                        fac.Servicios.append(ServiciosDisponibles(sn.get("id", ""), sn.findtext("nombre_servicio") or "",
                                                                 float(sn.findtext("costo") or 0), sn.findtext("descripcion") or ""))
                cls.facturas.append(fac)
        except (FileNotFoundError, ET.ParseError, ValueError, AttributeError):
            pass


class ServiciosDisponibles:

    def __init__(self, ID_Servicio, Nombre_Servicio, Costo, Descripcion=""):
        self.ID_Servicio = str(ID_Servicio).strip()
        self.Nombre_Servicio = str(Nombre_Servicio).strip()
        self.Costo = float(Costo)
        self.Descripcion = str(Descripcion).strip()
        if not self.ID_Servicio or not self.Nombre_Servicio:
            raise ValueError("Código y nombre del servicio son obligatorios.")
        if self.Costo < 0:
            raise ValueError("El costo no puede ser negativo.")

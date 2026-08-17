
class Encargado:
    def __init__(self, ID_encargado, Nombre_Completo, Identificacion, Provincia, Canton, Distrito,Direccion, Telefono, Correo_Electronico):
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
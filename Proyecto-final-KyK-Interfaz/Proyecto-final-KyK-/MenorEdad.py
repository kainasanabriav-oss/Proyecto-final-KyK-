from datetime import date, datetime


class MenorEdad:
    def __init__(self, ID_menorEdad, Nombre, Primer_Apellido, Segundo_Apellido, Sexo, Fecha_Nacimiento):
        self.ID_menorEdad = ID_menorEdad
        self.Nombre = Nombre
        self.Primer_Apellido = Primer_Apellido
        self.Segundo_Apellido = Segundo_Apellido
        self.Sexo = Sexo
        self.Fecha_Nacimiento = Fecha_Nacimiento

    @property
    def ID_menorEdad(self):
        return self.__ID_menorEdad

    @ID_menorEdad.setter
    def ID_menorEdad(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("La identificación del niño no puede estar vacía.")
        self.__ID_menorEdad = valor

    @property
    def Nombre(self):
        return self.__Nombre

    @Nombre.setter
    def Nombre(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self.__Nombre = valor

    @property
    def Primer_Apellido(self):
        return self.__Primer_Apellido

    @Primer_Apellido.setter
    def Primer_Apellido(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El primer apellido no puede estar vacío.")
        self.__Primer_Apellido = valor

    @property
    def Segundo_Apellido(self):
        return self.__Segundo_Apellido

    @Segundo_Apellido.setter
    def Segundo_Apellido(self, valor):
        self.__Segundo_Apellido = str(valor).strip()

    @property
    def Sexo(self):
        return self.__Sexo

    @Sexo.setter
    def Sexo(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("Debe seleccionar el sexo.")
        self.__Sexo = valor

    @property
    def Fecha_Nacimiento(self):
        return self.__Fecha_Nacimiento

    @Fecha_Nacimiento.setter
    def Fecha_Nacimiento(self, valor):
        if isinstance(valor, str):
            valor = datetime.strptime(valor, "%Y-%m-%d").date()
        if valor > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")
        self.__Fecha_Nacimiento = valor

    def calculo_Edad_Menor(self):
        hoy = date.today()
        return hoy.year - self.Fecha_Nacimiento.year - ((hoy.month, hoy.day) < (self.Fecha_Nacimiento.month, self.Fecha_Nacimiento.day))

    @property
    def nombre_completo(self):
        return f"{self.Nombre} {self.Primer_Apellido} {self.Segundo_Apellido}".strip()

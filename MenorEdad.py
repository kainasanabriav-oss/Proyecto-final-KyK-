from datetime import date


class MenorEdad:
    def __init__(self, ID_menorEdad:int, Nombre:str, Primer_Apellido:str, Segundo_Apellido:str, Sexo:str, Fecha_Nacimiento:date):
        self.__ID_menorEdad=ID_menorEdad
        self.__Nombre=Nombre
        self.__Primer_Apellido=Primer_Apellido
        self.__Segundo_Apellido=Segundo_Apellido
        self.__Sexo=Sexo
        self.__Fecha_Nacimiento=Fecha_Nacimiento
        
#============================================================= Getters n Setters =========================================================
    @property                  
    def ID_menorEdad(self):
        return self.__ID_menorEdad
    
    @ID_menorEdad.setter     
    def ID_menorEdad(self, valor):

        if not valor:
            raise ValueError("El ID no puede estar vacio")
        
        try:
            valor_prueba = int(valor)
        except ValueError:
            raise ValueError("El ID solo puede contener valores numericos menores a 8 digitos")
        
        if valor_prueba<=0:
            raise ValueError("El ID debe ser de un formato numerico aceptado.")
        if valor_prueba>99999999:
            raise ValueError("El ID debe tener un maximo de 8 digitos")
    
        self.__ID_menorEdad= valor_prueba

    @property                  
    def Nombre(self):
        return self.__Nombre
    
    @Nombre.setter     
    def Nombre(self, valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        self.__Nombre= valor

    @property                  
    def Primer_Apellido(self):
        return self.__Primer_Apellido
    
    @Primer_Apellido.setter     
    def Primer_Apellido(self, valor):
        if not valor:
            raise ValueError("El apellido no puede estar vacio")
        self.__Primer_Apellido= valor

    @property                  
    def Segundo_Apellido(self):
        return self.__Segundo_Apellido
    
    @Segundo_Apellido.setter     
    def Segundo_Apellido(self, valor):
        if not valor:
            raise ValueError("El apellido no puede estar vacio")
        self.__Segundo_Apellido= valor

    @property                  
    def Sexo(self):
        return self.__Sexo
    
    @Sexo.setter     
    def Sexo(self, valor):
        if not valor:
            raise ValueError("El sexo no puede estar vacio") 
        self.__Sexo= valor

    @property                  
    def Fecha_Nacimiento(self):
        return self.__Fecha_Nacimiento
    
    @Fecha_Nacimiento.setter     
    def Fecha_Nacimiento(self, valor):
        if not valor:
            raise ValueError("La fecha de nacimiento no puede estar vacia.")
        if not isinstance (valor,date): #is instance lo que hace es verificar si los datos corresponden al formato de date. Significa que la unica manera de que sea aceptado, es que tenga el formato especifico YYYY-MM-DD
            raise TypeError ("La fecha debe cumplir con el formato establecido.") #TypeError es para cuando hay info pero el dato es correcto (dato, tipo dato)
        self.__Fecha_Nacimiento= valor

    def calculo_Edad_Menor(self):
        fecha_actual = date.today() #date nos permite saber la fecha del dia de hoy, asi calculamos la edad
        edad = fecha_actual.year - self.__Fecha_Nacimiento.year# para la edad calculamos los anhos, restamos el anho actual a la fecha de nacimiento

        if(fecha_actual.month,fecha_actual.day)<(self.__Fecha_Nacimiento.month, self.__Fecha_Nacimiento.day): #si la fecha de nacimiento en meses y dias es mayor, o sea
            edad-=1 #si estamos antes del cumpleanhos en dicho anho, tiene -1 de edad, no los ha cumplido
        return edad #Kaina come caca
    
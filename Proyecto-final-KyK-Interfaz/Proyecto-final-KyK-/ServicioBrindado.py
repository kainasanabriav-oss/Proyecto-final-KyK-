from datetime import date
from ServiciosDisponibles import ServiciosDisponibles
from MenorEdad import MenorEdad
from Funcionario import Funcionario


class ServicioBrindado:
    IVA = 0.02

    def __init__(self, ID_cita, Menor, Fecha_Cita, Cancelado, Servicios):
        self.ID_cita = ID_cita
        self.Menor = Menor         
        self.Fecha_Cita = Fecha_Cita
        self.Cancelado = Cancelado
        self.Servicios = Servicios  

    def calcular_Subtotal(self):
        return sum(s.Costo for s in self.Servicios)

    def calcular_IVA(self):
        return self.calcular_Subtotal() * self.IVA

    def calcular_Total(self):
        return self.calcular_Subtotal() + self.calcular_IVA()

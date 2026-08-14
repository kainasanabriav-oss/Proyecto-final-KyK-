"""
ARCHIVO PRINCIPAL DEL PROYECTO 2 - HAPPY TEETH

Ejecutar este archivo para iniciar la interfaz gráfica.
Por ahora conserva XML únicamente como almacenamiento temporal del Proyecto 1.
Cuando se realice la parte de SQL Server, las llamadas de cargar/guardar XML se
reemplazarán por consultas a la base de datos sin tener que rediseñar las ventanas.
"""
import os
import tkinter as tk
from Funcionario import Funcionario
from Encargado import Encargado
from ServiciosDisponibles import ServiciosDisponibles
from ServicioBrindado import ServicioBrindado
from interfaz.InterfazLogin import InterfazLogin
from interfaz.InterfazMenu import InterfazMenu

BASE = os.path.dirname(os.path.abspath(__file__))


def ruta(nombre):
    return os.path.join(BASE, nombre)


def cargar_datos_temporales():
    Funcionario.cargar_Funcionarios_xml(ruta("funcionarios.xml"))
    Encargado.cargar_Encargados_xml(ruta("encargados.xml"))
    ServiciosDisponibles.cargar_Servicios_xml(ruta("servicios.xml"))
    ServicioBrindado.cargar_Facturas_xml(ruta("facturas.xml"))

    # El Proyecto 1 no almacenaba contraseña. Para que la pantalla de login pueda
    # probarse, los funcionarios antiguos usan temporalmente la contraseña 1234.
    for funcionario in Funcionario.funcionarios:
        if not getattr(funcionario, "Contrasena", None):
            funcionario.Contrasena = "1234"


def guardar_datos_temporales():
    Funcionario.guardar_Funcionarios_xml(ruta("funcionarios.xml"))
    Encargado.guardar_Encargados_xml(ruta("encargados.xml"))
    ServiciosDisponibles.guardar_Servicios_xml(ruta("servicios.xml"))
    ServicioBrindado.guardar_Facturas_xml(ruta("facturas.xml"))


def iniciar_menu(funcionario):
    InterfazMenu(raiz, funcionario, guardar_datos_temporales, mostrar_login)


def mostrar_login():
    Funcionario.usuario_Actual = None
    InterfazLogin(raiz, iniciar_menu)


def cerrar_programa():
    guardar_datos_temporales()
    raiz.destroy()


if __name__ == "__main__":
    cargar_datos_temporales()
    raiz = tk.Tk()
    raiz.protocol("WM_DELETE_WINDOW", cerrar_programa)
    mostrar_login()
    raiz.mainloop()

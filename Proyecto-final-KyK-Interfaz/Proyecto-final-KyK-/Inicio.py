"""
ARCHIVO PRINCIPAL DEL PROYECTO 2 - HAPPY TEETH

Ejecutar este archivo para iniciar la interfaz gráfica.
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

def guardar_datos_temporales():
    Encargado.guardar_Encargados_xml(ruta("encargados.xml"))
    ServiciosDisponibles.guardar_Servicios_xml(ruta("servicios.xml"))
    ServicioBrindado.guardar_Facturas_xml(ruta("facturas.xml"))

def cargar_datos_temporales():
    Encargado.cargar_Encargados_xml(ruta("encargados.xml"))
    ServiciosDisponibles.cargar_Servicios_xml(ruta("servicios.xml"))
    ServicioBrindado.cargar_Facturas_xml(ruta("facturas.xml"))


def iniciar_menu(conn, funcionario):
    InterfazMenu(raiz, conn, funcionario, guardar_datos_temporales,mostrar_login)


def mostrar_login():
    Funcionario.usuario_Actual = None
    InterfazLogin(raiz, iniciar_menu)


def cerrar_programa():
    raiz.destroy()


if __name__ == "__main__":
    cargar_datos_temporales()
    raiz = tk.Tk()
    raiz.protocol("WM_DELETE_WINDOW", cerrar_programa)
    mostrar_login()
    raiz.mainloop()

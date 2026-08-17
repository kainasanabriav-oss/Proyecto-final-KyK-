"""
ARCHIVO PRINCIPAL DEL PROYECTO 2 - HAPPY TEETH

Ejecutar este archivo para iniciar la interfaz gráfica.
"""
import os
import tkinter as tk
from Funcionario import Funcionario
from interfaz.InterfazLogin import InterfazLogin
from interfaz.InterfazMenu import InterfazMenu

BASE = os.path.dirname(os.path.abspath(__file__))


def ruta(nombre):
    return os.path.join(BASE, nombre)

def iniciar_menu(conn, funcionario):
    InterfazMenu(raiz, conn, funcionario,mostrar_login)


def mostrar_login():
    Funcionario.usuario_Actual = None
    InterfazLogin(raiz, iniciar_menu)


def cerrar_programa():
    raiz.destroy()

if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.protocol("WM_DELETE_WINDOW", cerrar_programa)
    mostrar_login()
    raiz.mainloop()

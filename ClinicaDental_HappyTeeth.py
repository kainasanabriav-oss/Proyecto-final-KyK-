# CLASES asociadas al codigo
from Funcionario import Funcionario as fun #clase funcionario
from Encargado import Encargado as enc #clase encargado
from ServiciosDisponibles import ServiciosDisponibles as sd
from ServicioBrindado import ServicioBrindado as sb

import os #usado para la limpieza del menu
import time #usado para timers de tiempo para que las acciones no sean inmediatas y se aprecie la captura de datos, entre otros
import xml.etree.ElementTree as ET #para usar archivos xml


#declaracion de variables globales, listas del sistema O XML
os.chdir(os.path.dirname(os.path.abspath(__file__))) #esto es algo especial que si busque, es para que cuando el usuario abra el archivo sin compilador sino abriendolo de python, mientras los archivos esten en la misma carpeta, se va a poder accederla
fun.cargar_Funcionarios_xml("funcionarios.xml")
enc.cargar_Encargados_xml("encargados.xml")
sd.cargar_Servicios_xml("servicios.xml")
sb.cargar_Facturas_xml("facturas.xml")
time.sleep(2)

#metodos y logica del programa
def limpiar_Pantalla():
    os.system("cls" if os.name == "nt" else "clear") #metodo os para limpiar la pantalla

#============================================================= Menus Principales =========================================================

def inicio_Sesion(): #Inicio de sesion incluye la generacion de nueva cuenta de funcionario (funciona para datos por Dr, y para iniciar sesion)
    limpiar_Pantalla() #limpia pantalla al entrar en este menu
    print(("="*60), "\nInicio de Sesion\n")
    opcion_Sesion = input("\n1)Iniciar Sesion\n2)Crear Nueva Cuenta\n0)Atras\n\nElija la accion que desea realizar: ")
    match opcion_Sesion:
        case "1":
            print(("="*60), "\nIngreso a la Cuenta\nUsuarios Actuales:")
            fun.mostrar_Funcionarios()
            id_funcionario = input("\nDigite el ID del funcionario para iniciar sesion: ")
            for fu in fun.funcionarios:
                if (id_funcionario==fu.ID_funcionario):    #si concuerdan los datos, se encuentra el usuario y se asigna
                    if(fu.Estado == False): #pero si el estado esta inactivo, no se puede usar
                        time.sleep(1)
                        print("El usuario seleccionado esta inactivo. Ingrese con un usuario activo o cree uno nuevo. ")
                        time.sleep(1)
                        return
                    fun.usuario_Actual = fu.Usuario #si todo esta bien, el usuario_Actual es el que se selecciona
                    time.sleep(3) #timer para apreciar datos
                    print(f"Se ha encontrado exitosamente la cuenta {fun.usuario_Actual}.")
                    time.sleep(1)
                    return
            time.sleep(1)            
            print("No se ha encontrado el usuario. Por favor intente de nuevo") #sino, no se encuentra
            time.sleep(2)  
            return
        case "2":
            fun.creacion_Cuenta()
        case "0":
            return
        case _:
            print("Opcion no valida.")
    
def mantenimiento_Funcionarios (): #menu principal del mantenimiento a los funcionarios
    limpiar_Pantalla() #limpia pantalla al entrar en este menu
    print(("="*60), "\nMantenimiento y Edicion de Funcionarios\n")
    opcion_Sesion = input("\n1)Mostrar Informacion de Funcionarios\n2)Editar Cuenta Funcionario\n3)Eliminar Funcionario\n0)Atras\nElija la accion que desea realizar: " )
    match opcion_Sesion:
        case "1":
            fun.mostrar_Funcionarios() #metodo de clase
            input("\nDigite cualquier tecla para volver al menu principal.")
        case "2":
            fun.editar_Funcionarios() #metodo de clase
        case "3":
            fun.eliminar_Usuario() #metodo de clase
        case "0":
            return
        case _:
            print("La opcion digitada no corresponde a ninguna opcion del menu.")

def mantenimiento_Pacientes(): #menu principal de los pacientes, encargados
    limpiar_Pantalla()
    print(("="*60), "\nMantenimiento y Edicion de los Pacientes\n")
    opcion_Sesion = input("\n1)Nuevo Paciente \n2)Ver Encargados\n3)Agregar Paciente Menor a Encargado\n4)Editar Informacion de Pacientes\n5)Eliminar Paciente o Encargado\n0)Atras\nElija la accion que desea realizar: " )
    match opcion_Sesion:
        case "1":
            enc.creacion_Paciente()    #limpiar consola, agregar primero el encargado (uno), agregar al hijo despues (pueden ser varios)
        case "2":
            enc.mostrar_Encargados()  # mostrar encargados 
            input("Digite cualquier tecla para salir. ")
        case "3":
            enc.agregar_menorEdad()   # se agrega un@ hij@ a un encargado ya existente, se selecciona el encargado y se agrega el nuevo 
        case "4":
            enc.editar_Encargados_o_Menores()      #se edita a partir de solicitar el padre, se pregunta  cual desea, y edita el padre o hij@
        case "5":
            enc.eliminar_encargado_o_menor()        #eliminar padre o hij@, si se elimina al encargado se borran los hijos tambien (confirmar), si no, se borra un hij@
        case "0":
            return
        case _:
            print("La opcion digitada no corresponde a ninguna opcion del menu.")

def mantenimiento_Servicios(): #menu principal de los servicios
    limpiar_Pantalla()
    print(("="*60), "\nMantenimiento y edicion de los servicios\n")
    opcion_Servicio = input("\n1)Agregar Nuevo Servicio \n2)Ver Informacion de los Servicios\n3)Editar Informacion de un Servicio\n4)Eliminar Servicio\n5)Atras\nElija la accion que desea realizar: " )
    match opcion_Servicio:
        case "1":
            sd.agregar_Servicios() 
        case "2":
            sd.mostrar_Servicios()
        case "3":
            sd.editar_Servicios()
        case "4":
            sd.eliminar_Servicio()  
        case "5":
            return
        case _:
            print("La opcion digitada no corresponde a ninguna opcion del menu.")

def mantenimiento_Citas(): #menu principal para la confeccion de citas
    limpiar_Pantalla()
    print(("="*60), "\nMantenimiento y Edicion de las Citas\n")
    opcion_Servicio = input("\n1)Agregar Nueva Cita \n2)Editar Cita Existente \n0)Atras\nElija la accion que desea realizar: " )
    match opcion_Servicio:
        case "1":
            sb.creacion_Cita()
        case "2":
            sb.editar_Cita()
        case "0":
            return
        case _: 
            print("El valor digitado no corresponde a las opciones del menu. Intente de nuevo.")
            time.sleep(1)

def no_es_posible_entrar(): #para no repetir codigo, se hizo este metodo utilizado 
    print("\nNo es posible acceder sin un usuario. Intente de nuevo.")
    time.sleep(2)

# Menu principal
def main():
    menuP = True
    while(menuP): #el menu es constante hasta que se decida salir del programa
        limpiar_Pantalla()
        print(("="*60),"\nBienvenido a Clínica Dental Infantil Happy Teeth")
        print(("="*60))
        print("|1. Iniciar Sesion de Funcionario\n|2. Registro de Cita Medica.\n|3. Consulta de Servicios Brindados.\n|4. Mantenimiento Funcionarios.\n|5. Mantenimiento de Pacientes.\n|6. Mantenimiento de Servicios" \
        "\n|7. Pago de Servicios\n|0. Salir")
        print(("="*60))

        if not fun.usuario_Actual:
            print("Usuario actual: No Seleccionado")
        else:
            print(f"Usuario actual: {fun.usuario_Actual}") #zona de prints del menu, incluyendo la posibilidad de ver si existe un usuario actual. Si no hay usuario actual, no se puede acceder a lo demas

        menuOpcion = input("Digite la accion que desea realizar: ") #el menu debe tener las validaciones antes de correr las funciones
        match menuOpcion:
            case "1":#terminado
                inicio_Sesion() 
            case "2": #terminado
                if not fun.usuario_Actual:
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    mantenimiento_Citas()
            case "3":#terminado
                if not fun.usuario_Actual:
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    limpiar_Pantalla()
                    sd.mostrar_Servicios_Principal()

            case "4":#terminado
                if not fun.usuario_Actual: 
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    mantenimiento_Funcionarios()
            case "5":#terminado
                if not fun.usuario_Actual:
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    mantenimiento_Pacientes()
            case "6":#terminado
                if not fun.usuario_Actual:
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    mantenimiento_Servicios()
            case "7": #terminado
                if not fun.usuario_Actual:
                    no_es_posible_entrar()
                    time.sleep(1)  
                else:
                    sb.cancelar_Cita()
            case "0":
                limpiar_Pantalla()
                eleccion = input("Esta seguro que desea salir del sistema?\n1)Si\n2)No\n")
                match eleccion:
                    case "1": #los xml se van a guardar cuando nos salimos, la informacion al final es la informacion que se genera
                        print("Entendido. Saliendo del sistema...\n")
                        fun.guardar_Funcionarios_xml("funcionarios.xml")
                        enc.guardar_Encargados_xml ("encargados.xml")
                        sd.guardar_Servicios_xml ("servicios.xml")
                        sb.guardar_Facturas_xml("facturas.xml")
                        time.sleep(2)
                        menuP=False
                    case"2":
                        continue
                    case _:
                        print("\nLa opcion digitada no es valida, vuelvalo a intentar")
            case _:
                print("\nLa opcion digitada no es valida, vuelvalo a intentar")

if __name__ == "__main__":
    main()
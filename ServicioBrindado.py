from ServiciosDisponibles import ServiciosDisponibles as sd
from Funcionario import Funcionario as fun
from MenorEdad import MenorEdad as men
from Encargado import Encargado as enc

import os
import time
from datetime import date
import xml.etree.ElementTree as ET

class ServicioBrindado:

    facturas = []
    consecutivo = 0 #reemplazar con XML
    IVA= 0.02 #Equivalente al IVA del 2% por servicio medico, (0.02 * total)+total para conseguir el monto final


    def __init__(self, Menor: men, Funcionario: fun, Fecha_Cita, id_externo=None):
        self.__Menor = Menor #menor individuo, porque es de un ninho por factura
        self.__Funcionario = Funcionario #igual aca, solo un funcionario atiende
        self.__Fecha_Cita = Fecha_Cita #fecha utilizando datetime para validaciones
        self.__Servicios = [] #pero servicios si son una lista basada en los servicios que ofrecemos, ya que pueden ser varios por cita medica
        self.__Cancelado = False #comienza falso y se cambia hasta que paguen

        if id_externo is not None:
            self.__ID_cita=id_externo
        else:
            ServicioBrindado.consecutivo+=1 # Consecutivo aumenta una unidad cada vez que se autogenera, para cumplir con el requi8sito y que el ID de cita nunca se repita
            self.__ID_cita = ServicioBrindado.consecutivo #entonces, ID cita depende de consecutivo

#============================================================= Getters n Setters =========================================================
    @property
    def ID_cita (self):
        return self.__ID_cita
    
    @property
    def Menor(self):
        return self.__Menor
    
    @property
    def Funcionario(self):
        return self.__Funcionario
    
    @property
    def Fecha_Cita(self):
        return self.__Fecha_Cita
    
    @Fecha_Cita.setter
    def Fecha_Cita(self,valor):
        if not valor:
            raise ValueError("La fecha de nacimiento no puede estar vacia.")
        if not isinstance (valor,date): #is instance lo que hace es verificar si los datos corresponden al formato de date. Significa que la unica manera de que sea aceptado, es que tenga el formato especifico YYYY-MM-DD
            raise TypeError ("La fecha debe cumplir con el formato establecido.") #TypeError es para cuando hay info pero el dato es correcto (dato, tipo dato)
        self.__Fecha_Cita=valor

    @property
    def Cancelado(self):
        return self.__Cancelado
    
    @Cancelado.setter
    def Cancelado (self, valor):
        self.__Cancelado = valor

    @property
    def Servicios(self):
        return self.__Servicios
    #estos de aca son equivalentes alos setter, pero sin reemplazar el valor completo del atributo, ya que es una lista.

    def agregar_Servicio(self, servicio:sd): #toma los datos de 
        if self.__Cancelado:
            raise ValueError("La cita ya fue cancelada, no se permiten realizar cambios.")
        self.__Servicios.append(servicio)
    
    def eliminar_Servicio(self, servicio:sd):
        if self.__Cancelado:
            raise ValueError("La cita ya fue cancelada, no se permiten realizar cambios.")
        if servicio not in self.__Servicios:
            raise ValueError("El servicio no es parte actualmente de la cita.")
        self.__Servicios.remove(servicio)

    @staticmethod
    def lp():
        os.system("cls" if os.name =="nt" else"clear")

    #============================================================= Metodos ===================================================================

    @classmethod
    def mostrar_Citas(cls):
        if not cls.facturas:
            print("No existen citas registradas en el sistema actualmente. ")
            return
        
        print("Citas registradas en el sistema: \n")
        for cita in cls.facturas:
            estado = "Cancelado" if cita.Cancelado else "Pendiente" #como es booleano, le asignamos un String descriptivo dependiendo del true o false

            print(f"{'ID':<15} {'Menor':<20} {'Funcionario':<20} {'Fecha':<15} {'Estado':<12}")
            print("-"*100)
            print(f"{cita.ID_cita:<15} {cita.Menor.Nombre:<20} {cita.Funcionario.Usuario:<20} {str(cita.Fecha_Cita):<15} {estado:<12}")

            print("Servicios brindados: \n")
            print(f"{'ID':<15} {'Nombre':<25} {'Costo':<15}")
            print("-"*55)
            for ser in cita.Servicios: #se imprime primero los datos iniciales de la cita, y luego todos los servicios proporcionados
                print(f"{ser.ID_Servicio:<15} {ser.Nombre_Servicio:<25} {ser.Costo:<15}")
            print("="*100)

        input("\nDigite cualquier tecla para salir: \n")
    
    @classmethod
    def mostrar_Citas_No_Canceladas(cls):
        if not cls.facturas:
            print("No existen citas registradas en el sistema actualmente. ")
            return
        
        print("Citas registradas en el sistema: \n")
        for cita in cls.facturas:
            estado = "Cancelado" if cita.Cancelado else "Pendiente" #como es booleano, le asignamos un String descriptivo dependiendo del true o false
            if(estado=="Pendiente"):
                print(f"{'ID':<15} {'Menor':<20} {'Funcionario':<20} {'Fecha':<15} {'Estado':<12}")
                print("-"*100)
                print(f"{cita.ID_cita:<15} {cita.Menor.Nombre:<20} {cita.Funcionario.Usuario:<20} {str(cita.Fecha_Cita):<15} {estado:<12}")

                print("Servicios brindados: \n")
                print(f"{'ID':<15} {'Nombre':<25} {'Costo':<15}")
                print("-"*100)
                for ser in cita.Servicios: #se imprime primero los datos iniciales de la cita, y luego todos los servicios proporcionados
                    print(f"{ser.ID_Servicio:<15} {ser.Nombre_Servicio:<25} {ser.Costo:<15}")
                print("="*80)
        input("\nDigite cualquier tecla para salir: \n")


    @classmethod
    def creacion_Cita(cls):
        cls.lp()
        print(("="*60), "\nSistema de citas de la Clinica Dental\nAsegurese de digitar correctamente los datos solicitados para evitar rehacer el proceso.\n")
        funcionario = fun.usuario_Actual
        funcionario_encontrado=False #bandera

        for f in fun.funcionarios:
            if(funcionario==f.Usuario):
                creacion=True
                funcionario_encontrado=True
                while(creacion):
                    try:
                        print("Funcionario activo encontrado. Por favor elija el encargado del menor: \n")
                        encargado_encontrado=False
                        enc.mostrar_Encargados()

                        encargado = input("Digite el ID de la persona encargada: ")
                        for e in enc.encargados:
                            if(encargado==e.ID_encargado):
                                encargado_encontrado=True
                                print("Encargado encontrado. Menores de edad asociados: \n")
                                for m in e.menoresEdad:
                                    print(f"{m.ID_menorEdad} | {m.Nombre} | Edad: {m.calculo_Edad_Menor()}")
                                
                                
                                menor=input("Digite el ID del menor de edad a atender: ")
                                menor_seleccionado = None #validacion tipo bandera
                                for m in e.menoresEdad:
                                    if(menor==m.ID_menorEdad):
                                        menor_seleccionado= m #el objeto completo es adjudicada
                                        break
                                if not menor_seleccionado:
                                    print("Menor de edad no encontrado. Vuelva a intentar.")
                                    continue
                                fecha_comprobacion = input("Digite la fecha de la cita. Utilice solamente el formato aceptado (AAAA-MM-DD): ")
                                fecha_cita = date.fromisoformat(fecha_comprobacion) #comprobacion por si acaso no pone la fecha correctamente

                                nueva_cita = cls(menor_seleccionado, f, fecha_cita) #se asignan primero todo lo que no sean los servicios.

                                print("Menor de edad encontrado. Proceda a agregar los servicios realizados al menor.\n")
                                sd.mostrar_Servicios()
                                eleccion_servicios= True
                                while(eleccion_servicios):
                                    id_servicio= input("\nDigite el ID del servicio brindado, o digite '0' para terminar.")
                                    if(id_servicio=="0"):
                                        eleccion_servicios=False
                                        continue
                                    servicio_encontrado=False #validacion tipo bandera
                                    for ser in sd.servicios:
                                        if(id_servicio==ser.ID_Servicio):
                                            servicio_encontrado=True
                                            nueva_cita.agregar_Servicio(ser)
                                            print(f"Servicio {ser.Nombre_Servicio} agregado correctamente.")
                                            break
                                    if not servicio_encontrado:
                                        print("El servicio no pudo ser encontrado. Intente de nuevo.")
                                
                                cls.facturas.append(nueva_cita)# ahora si, cuando ya esta todo, se agrega a facturas desde nueva_cita, que nos funciono para guardar los datos temporalmente
                                print(f"La cita ha sido registrada correctamente con el consecutivo: {nueva_cita.ID_cita}")
                                time.sleep(2)
                                creacion=False
                                return
                        
                        if not encargado_encontrado:
                            print("Encargado no encontrado. Vuelva a intentar de nuevo digitando el ID correctamente.")
                            continue

                    except UnboundLocalError as ule: #try catch por si se encuentra valores no esperados y no se caiga
                        print(f"El dato no puede ser accesado: {ule}")        
                    except ValueError as ve:
                        print(f"Los digitos colocados no corresponden a un numero valido. Solo digite formatos aceptados: {ve}")
                    except Exception as e:
                        print(f"ERROR: {e}")
                break
        if not funcionario_encontrado:    
            print("Error inesperado. El usuario actual no ha sido encontrado, vuelva a iniciar sesion.")
            time.sleep(2)
            return


    @classmethod
    def editar_Cita(cls):
        cls.lp()
        print(("="*60), "\nEditar cita existente. Recuerde que no se pueden editar citas ya canceladas.\nCitas actuales en el sistema:")
        
        if not cls.facturas:
            print("No existen citas registradas en el sistema actualmente. ")
            return
        
        cls.mostrar_Citas()

        cita_edicion = input("\nColoque el ID de la cita que desea editar datos.")
        for cita in cls.facturas:
            if(cita_edicion == str(cita.ID_cita)): # se tuvo que pasar a string porque sino era una comaparacion de dos diferentes tipos
                if(cita.Cancelado):
                    print("La cita ya fue cancelada. No se permiten cambios.")
                    time.sleep(2)
                    return
                
                seleccion = input("Cita encontrada. Que desea realizar?\n1)Editar servicios\n2)Eliminar cita\nSeleccion: ")
                
                if(seleccion=="1"):
                    edicion=True
                    while(edicion):
                        try: #pequenha impresion rapida de los servicios actuales
                            print("\nServicios actuales en la cita:\n")
                            print(f"{'ID':<15} {'Nombre':<25} {'Costo':<15}")
                            print("-"*55)
                            for ser in cita.Servicios:
                                print(f"{ser.ID_Servicio:<15} {ser.Nombre_Servicio:<25} {ser.Costo:<15}")
                            
                            accion = input("\n1)Agregar servicio\n2)Quitar servicio\n0)Salir\nSeleccion: ")
                            if(accion=="1"):
                                sd.mostrar_Servicios_Principal()
                                id_servicio = input("\nDigite el ID del servicio que desea agregar: ")
                                servicio_encontrado=False #bandera
                                for ser in sd.servicios:
                                    if(id_servicio==ser.ID_Servicio):
                                        servicio_encontrado=True
                                        cita.agregar_Servicio(ser)
                                        print(f"Servicio {ser.Nombre_Servicio} agregado correctamente.")
                                        break
                                if not servicio_encontrado:
                                    print("\nEl servicio no fue encontrado. Intente de nuevo.")

                            elif(accion=="2"):
                                id_servicio = input("\nDigite el ID del servicio a quitar: ")
                                servicio_encontrado=False
                                for ser in cita.Servicios:
                                    if(id_servicio==ser.ID_Servicio):
                                        servicio_encontrado=True
                                        cita.eliminar_Servicio(ser)
                                        print(f"Servicio {ser.Nombre_Servicio} eliminado correctamente.")
                                        break
                                if not servicio_encontrado:
                                    print("\nEl servicio no fue encontrado en la cita.")

                            elif(accion=="0"):
                                edicion=False
                            else:
                                print("Opcion no valida. Intente de nuevo.")

                        except ValueError as ve:
                            print(f"Error: {ve}")
                        except Exception as e:
                            print(f"Error inesperado: {e}")

                if(seleccion=="2"): #si quiere eliminar, se borra del todo
                    aceptar = input("Esta seguro que desea eliminar la cita?\n1)Si\n2)No\nRespuesta: ")
                    if(aceptar=="1"):
                        cls.facturas.remove(cita)
                        print("La cita ha sido eliminada correctamente.")
                        time.sleep(2)
                        return
                    if(aceptar=="2"):
                        print("La eliminacion no ha sido efectuada.")
                        time.sleep(2)
                        return
                return
                    
        print("No se ha encontrado la cita con el consecutivo digitado. Intente de nuevo.")
        time.sleep(2)

    @classmethod
    def cancelar_Cita(cls):
        cls.lp()
        print(("="*60), "\nCancelar cita existente. Solo accione luego de realizar el pago .\nCitas actuales en el sistema:")
        cls.mostrar_Citas_No_Canceladas() #solo aparecen las NO CANCELADAS, las canceladas no se muestran pero estan en la base de datos

        seleccionar_Cita= input("Proporciona el ID de la cita que desea cancelar. Recuerde que al cancelar una cita, no se pueden realizar mas cambios.")
        cita_encontrada = False
        for fac in cls.facturas:
            if(seleccionar_Cita==str(fac.ID_cita)):
                cita_encontrada=True
                print(f"Esta seguro que desea cancelar la cita #{fac.ID_cita}? Costo total con IVA: {fac.calcular_Total()}.\nAl cancelarla, no se permiten hacer nuevos cambios.\n1)Si\n2)No\n")
                eleccion = input("Opcion elegida: ")
                match eleccion:
                    case "1":
                        time.sleep(1)
                        print("Se ha generado el pago correspondiente. Generando la informacion...")
                        fac.Cancelado=True #fac es donde esta el iterador
                        print("...")
                        time.sleep(1)
                        print("...")
                        time.sleep(1)
                        print("...")
                        time.sleep(1)
                        fac.calcular_Factura() #calculo de factura aca
                        input("\nDigite cualquier tecla para salir. \n")
                    case "2":
                        print("El pago no ha sido efectuado. Saliendo de la opcion")
                        time.sleep(2)
                        return
                    case _:
                        print("La opcion digitada no corresponde a las opciones proporcionadas. Vuelva a intentarlo")
                        time.sleep(2)
                        return
                break
        if not cita_encontrada:
            print("No se ha encontrado la cita. Intente de nuevo")
            time.sleep(2)
        return
        
    def calcular_Factura(self): #este metodo es puro informativo, tiene un disenho similar a una factura.
        print(f"\n{'='*70}")
        print(f" Factura de servicios - Clinica Dental Happy Teeth")
        print(f" Consecutivo #{self.__ID_cita}  |  Fecha: {self.__Fecha_Cita}")
        print(f"{'='*70}")
        print(f" {'Funcionario:':<20} {self.__Funcionario.Nombre_Completo}")
        print(f" {'Menor atendido:':<20} {self.__Menor.Nombre} {self.__Menor.Primer_Apellido} {self.__Menor.Segundo_Apellido}  |  Edad: {self.__Menor.calculo_Edad_Menor()} años")
        print(f"{'-'*70}")
        print(f"{'Servicio':<35} {'Sin IVA':>15} {'Con IVA (2%)':>15}")
        print(f"{'-'*70}")
        
        total_con_iva = 0
        total_sin_iva = 0
        for ser in self.__Servicios: #hay que acceder al privado especifico de la instancia, con __ de privado
            precio_con_iva = ser.Costo + (ser.Costo * self.IVA)
            total_sin_iva +=ser.Costo
            total_con_iva += precio_con_iva
            print(f"{ser.Nombre_Servicio+' '+ser.ID_Servicio:<35} {ser.Costo:<15,.2f} {precio_con_iva:<15,.2f}") #formatos para calculo
        
        print("-"*70)
        print(f"{'Subtotal sin IVA:':<35} {total_sin_iva:<31,.2f}")
        print(f"{'IVA (2%):':<35} {total_sin_iva * ServicioBrindado.IVA:<31,.2f}")
        print(f"{'Total a cancelar:':<35} {total_con_iva:<31,.2f}")
        print(f"{'='*70}\n")
        return total_con_iva
                                #Consulta factura, es lo que guarda XML y se presenta en su totalidad con el metodo

    def calcular_Total(self): #solo esta hecho para imprimir el total a pagar antes de confirmar, es lo mismo que hace calcular_Factura pero solo con el monto que nos interesa
        total = 0
        for ser in self.__Servicios:
            total += ser.Costo + (ser.Costo*self.IVA)
        return total
    #================================================================ Calculos de XML ============================================================================


    @classmethod
    def guardar_Facturas_xml(cls, ruta):
        try:
            raiz = ET.Element("facturas")
            for fac in cls.facturas:
                # datos generales de la cita/factura
                nodo = ET.SubElement(raiz, "cita", id=str(fac.ID_cita))
                ET.SubElement(nodo, "fecha").text = str(fac.Fecha_Cita)
                ET.SubElement(nodo, "estado").text = "Cancelado" if fac.Cancelado else "Pendiente"
                # datos asociados al menor de edad
                menor_nodo = ET.SubElement(nodo, "menor", id=str(fac.Menor.ID_menorEdad))
                ET.SubElement(menor_nodo, "nombre").text = str(fac.Menor.Nombre)
                ET.SubElement(menor_nodo, "primer_apellido").text = str(fac.Menor.Primer_Apellido)
                ET.SubElement(menor_nodo, "segundo_apellido").text = str(fac.Menor.Segundo_Apellido)
                ET.SubElement(menor_nodo, "sexo").text = str(fac.Menor.Sexo)
                ET.SubElement(menor_nodo, "fecha_nacimiento").text = str(fac.Menor.Fecha_Nacimiento)
                # datos asociados al funcionario
                func_nodo = ET.SubElement(nodo, "funcionario", id=str(fac.Funcionario.ID_funcionario))
                ET.SubElement(func_nodo, "usuario").text = str(fac.Funcionario.Usuario)
                ET.SubElement(func_nodo, "nombre_completo").text = str(fac.Funcionario.Nombre_Completo)

                # servicios proporcionados en la cita
                servicios_nodo = ET.SubElement(nodo, "servicios")
                for ser in fac.Servicios: #necesita recorrerse ya que una cita puede tener varios servios
                    ser_nodo = ET.SubElement(servicios_nodo, "servicio", id=str(ser.ID_Servicio))
                    ET.SubElement(ser_nodo, "nombre_servicio").text = str(ser.Nombre_Servicio)
                    ET.SubElement(ser_nodo, "costo").text = str(ser.Costo)
                    ET.SubElement(ser_nodo, "descripcion").text = str(ser.Descripcion)

            arbol = ET.ElementTree(raiz)
            arbol.write(ruta, encoding="utf-8", xml_declaration=True)
            print("Facturas guardadas correctamente.")
        except Exception as e:
            print(f"Error inesperado al guardar las facturas: {e}")

    @classmethod
    def cargar_Facturas_xml(cls, ruta):
        try:
            arbol = ET.parse(ruta)
            raiz = arbol.getroot()
            id_maximo = 0

            for f in raiz.findall("cita"):
                id_cita = int(f.get("id"))  # convertir a int para comparar
                fecha_cita = date.fromisoformat(f.find("fecha").text)
                cancelado = f.find("estado").text == "Cancelado"

                # datos del menor
                menor_nodo = f.find("menor")
                fecha_nacimiento = date.fromisoformat(menor_nodo.find("fecha_nacimiento").text)
                menor = men(
                    menor_nodo.get("id"),
                    menor_nodo.find("nombre").text,
                    menor_nodo.find("primer_apellido").text,
                    menor_nodo.find("segundo_apellido").text,
                    menor_nodo.find("sexo").text,
                    fecha_nacimiento
                )

                # datos del funcionario
                func_nodo = f.find("funcionario")
                funcionario = fun(
                    func_nodo.get("id"),
                    func_nodo.find("usuario").text,
                    func_nodo.find("nombre_completo").text,
                    True
                )

                # creacion de la cita
                cita = cls(menor, funcionario, fecha_cita, id_externo=id_cita)

                # servicios, se recorren porque son varios
                servicios_nodo = f.find("servicios")
                for ser in servicios_nodo.findall("servicio"):
                    servicio = sd(
                        ser.get("id"),
                        ser.find("nombre_servicio").text,
                        float(ser.find("costo").text),
                        ser.find("descripcion").text
                    )
                    cita.agregar_Servicio(servicio)
                cita.Cancelado = cancelado

                cls.facturas.append(cita)

                if id_cita > id_maximo:
                    id_maximo = id_cita

            cls.consecutivo = id_maximo
            print("Citas cargadas correctamente.")

        except FileNotFoundError:
            print("Archivo de citas no encontrado. Se iniciara con lista vacia.")
        except ET.ParseError:
            print("ERROR: El archivo XML de citas esta mal formado.")
        except Exception as e:
            print(f"Error inesperado al cargar citas: {e}")


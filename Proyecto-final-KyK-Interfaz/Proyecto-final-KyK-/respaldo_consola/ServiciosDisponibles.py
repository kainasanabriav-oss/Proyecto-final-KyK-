from datetime import date

import os
import time
import xml.etree.ElementTree as ET

class ServiciosDisponibles:

    servicios = []

    def __init__(self, ID_Servicio:str, Nombre_Servicio:str, Costo:float, Descripcion:str):
        self.__ID_Servicio=ID_Servicio
        self.__Nombre_Servicio=Nombre_Servicio
        self.__Costo=Costo
        self.__Descripcion=Descripcion

#============================================================= Getters n Setters =========================================================
    @property
    def ID_Servicio(self):
        return self.__ID_Servicio
    
    @ID_Servicio.setter
    def ID_Servicio(self,valor):
        if not valor:
            raise ValueError("El ID no puede estar vacio")
        self.__ID_Servicio=valor


    @property
    def Nombre_Servicio(self):
        return self.__Nombre_Servicio
    
    @Nombre_Servicio.setter
    def Nombre_Servicio(self,valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        self.__Nombre_Servicio=valor

    @property
    def Costo(self):
        return self.__Costo
    
    @Costo.setter
    def Costo (self, valor):
        if not valor:
            raise ValueError("El costo no puede estar vacio")
        try:
            valor_prueba = float(valor)
        except ValueError:
            raise ValueError("El costo solo puede contener valores numericos.")
        if valor_prueba<=0:
            raise ValueError("El costo debe ser de un formato numerico aceptado.")
        self.__Costo=valor_prueba

    @property
    def Descripcion(self):
        return self.__Descripcion
    
    @Descripcion.setter
    def Descripcion(self,valor):
        self.__Descripcion=valor

    @staticmethod
    def lp():
        os.system("cls" if os.name =="nt" else"clear")

    #============================================================= Metodos ===================================================================

    @classmethod
    def agregar_Servicios(cls): #realmente aca es la misma logica de otros objetos, varian sus caracteristicas pero para preguntar,editar o eliminar son similares
        cls.lp()
        print(("="*60), "\nCreacion de un nuevo servicio\nAsegurese de digitar correctamente los datos solicitados para evitar rehacer el proceso.\n")

        agregar=True
        while(agregar):
            try:
                id_Servicio = input("Digite el ID del servicio ofrecido. El ID puede consistir de 3 digitos alfabeticos de la especializacion, y digitos numericos para diferenciarlos:  ")
                for ser in cls.servicios:
                    if(id_Servicio==ser.ID_Servicio):
                        print("El ID ya se encuentra actualmente ocupado. Intente de nuevo.\n")
                        time.sleep(2)
                        agregar=False
                        return
                    
                nombre_servicio = input("Digite el nombre del servicio ofrecido a los pacientes:  ")
                for ser in cls.servicios:    
                    if(nombre_servicio==ser.Nombre_Servicio):
                        print("El nombre del servicio ya se encuentra actualmente ocupado. Intente de nuevo.\n")
                        time.sleep(2)
                        agregar=False
                        return

                costo = float(input ("Digite el costo en colones que va a tener el servicio. No debe incluir IVA:  "))

                descripcion= input("Coloque informacion relevante o describa el servicio ofrecido: ")

                time.sleep(1)
                print("Revisando los datos para comprobar que se hayan generado correctamente...")
                time.sleep(2)

                cls.servicios.append(cls(id_Servicio, nombre_servicio, costo, descripcion))
                print(f"El nuevo servicio que se ha agregado, {nombre_servicio} ha sido guardado exitosamente. \n")
                time.sleep(2)
                agregar=False
            except UnboundLocalError as ule: #try catch por si se encuentra valores no esperados y no se caiga
                print(f"El servicio no puede ser accesado: {ule}")        
            except ValueError as ve:
                print(f"Los digitos colocados no corresponden a un ID valido. Solo digite formatos aceptados: {ve}")
            except Exception as e:
                print(f"Error no esperado: {e}")

    @classmethod
    def mostrar_Servicios(cls): #uno tiene mas datos
        print("Servicios actuales: \n")
        print(f"{'Nombre':<40} {'Precio':<15} {'ID':<15} {'Descripcion':<40}")
        print("-"*100)

        for ser in cls.servicios:
            print(f"{ser.Nombre_Servicio:<40} {ser.Costo:<15} {ser.ID_Servicio:<15} {ser.Descripcion:<40}")
        input("\nDigite cualquier tecla para salir: \n")

    @classmethod
    def mostrar_Servicios_Principal(cls): #otro es mas resumido
        print("Servicios brindados actualmente por la Clinica: \n")
        print(f"{'Nombre':<25} {'Precio':<15}")
        print("-"*55)

        for ser in cls.servicios:
            print(f"{ser.Nombre_Servicio:<25} {ser.Costo:<15}")
        input("\nDigite cualquier tecla para salir: \n")

#============================================================= Metodos ===================================================================

    @classmethod
    def editar_Servicios(cls):
        cls.lp() #limpieza de pantalla
        print(("="*60), "\nEditar informacion de los servicios\n") 
        cls.mostrar_Servicios()
        servicio_Seleccionado= input("Digite el ID correspondiente al servicio que desea modificar: ")
        for ser in cls.servicios:
            if(servicio_Seleccionado==ser.ID_Servicio):
                print("Servicio encontrado. Se procedera a editarlo")
                time.sleep(1)
                cls.lp() #se limpia la pantalla de nuevo
                edicion=True
                while(edicion):
                    try:
                        nombre_Comprobacion="" #variable de uso dependiendo de lo que pasa
                        print(f"Nombre actual del servicio: {ser.Nombre_Servicio} \n")
                        nuevo_Nombre = input("Digite el nombre al que se debe actualizar. Si no desea actualizarlo, digite 'mantener': ")
                        if(nuevo_Nombre=="mantener"): #si quiere mantener, entonces se mantiene y asigna la variable
                            print("El nombre se va a mantener.")
                            nombre_Comprobacion = ser.Nombre_Servicio
                        else:
                            print(f"Nombre actualizado correctamente a: {nuevo_Nombre}") #sino, se le cambia al nuevo en caso que no digite mantener
                            nombre_Comprobacion= nuevo_Nombre       

                        
                        precio_Comprobacion= ""
                        print(f"Precio actual del servicio:  {ser.Costo}")
                        nuevo_Precio = input("Digite el nuevo precio que debe tener el servicio. Asegurese de usar el formato correcto, en colones.\nSi no desea actualizarlo, digite 'mantener': ")
                        if(nuevo_Precio=="mantener"): #si quiere mantener, entonces se mantiene y asigna la variable
                            print("El precio se va a mantener.")
                            precio_Comprobacion = ser.Costo
                        else:
                            print(f"Nombre actualizado correctamente a: {nuevo_Precio}") #sino, se le cambia al nuevo en caso que no digite mantener
                            precio_Comprobacion= nuevo_Precio   

                        descripcion_Comprobacion= ""
                        print(f"Descripcion actual del servicio:  {ser.Descripcion}")
                        nueva_Descripcion = input("Digite la nueva descripcion que debe tener el servicio.\nSi no desea actualizarlo, digite 'mantener': ")
                        if(nueva_Descripcion=="mantener"): #si quiere mantener, entonces se mantiene y asigna la variable
                            print("La descripcion se va a mantener.")
                            descripcion_Comprobacion = ser.Descripcion
                        else:
                            print(f"Descripcion actualizada correctamente a: {nueva_Descripcion}") #sino, se le cambia al nuevo en caso que no digite mantener
                            descripcion_Comprobacion= nueva_Descripcion                           

                        ID_Comprobacion = ""
                        print(f"ID asociado actual del servicio {ser.ID_Servicio} \n")
                        nuevo_ID = input("Digite el nuevo ID asociado del servicio. Asegurese de usar el formato correcto (3 digitos alfabeticos de la especializacion, y digitos numericos para diferenciarlos).\nSi no desea actualizarlo, digite 'mantener': ")
                        if(nuevo_ID=="mantener"): 
                            print("La identificacion se va a mantener.")
                            ID_Comprobacion = ser.ID_Servicio
                        else:
                            ID_Duplicado=False
                            for s in cls.servicios:
                                if (nuevo_ID==s.ID_Servicio):    
                                    print("El ID del servicio ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                                    time.sleep(1)
                                    ID_Duplicado=True
                                    break
                            if (ID_Duplicado):
                                continue
                            print(f"ID actualizado correctamente a: {nuevo_ID}") 
                            ID_Comprobacion= nuevo_ID

                        time.sleep(2)
                        print("El encargado seleccionado ahora se ha actualizado con los siguientes datos:")
                        print(f"ID: {ID_Comprobacion} | Nombre: {nombre_Comprobacion} | Precio: {precio_Comprobacion} | Descripcion {descripcion_Comprobacion}")

                        #Aceptas los datos que has colocado?
                        opcion_Aceptar=True
                        while(opcion_Aceptar):
                            aceptar = input("Esta seguro que desea continuar con los datos digitados?\n1)Si\n2)No\n") #Menu de confirmacion, se asignan solo y solo si se acepta
                            if(aceptar=="1"):
                                time.sleep(1)
                                print("\nAsegurando de que el proceso haya sido exitoso...")
                                time.sleep(1)

                                ser.ID_Servicio = ID_Comprobacion 
                                ser.Nombre_Servicio = nombre_Comprobacion
                                ser.Costo= precio_Comprobacion
                                ser.Descripcion = descripcion_Comprobacion
                                    
                                time.sleep(1)
                                print("El proceso ha sido exitoso.")
                                time.sleep(2)
                                opcion_Aceptar=False #se cierra el menu
                                return
                            elif(aceptar=="2"):
                                print(f"El cambio se ha cancelado. Los datos del servicio {ser.Nombre_Servicio} no han sido actualizados")#Se cancela el cambio 
                                time.sleep(2)
                                opcion_Aceptar=False #se cierra el menu
                                return
                            else:
                                print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.") #se entra al bucle a menos que elija las opciones correctas
                        time.sleep(2)
                        edicion=False
                    except UnboundLocalError as ule: #la validacion dentro de los parametros de clase hacia que se cayera el sistema, entonces, se agrearon el while principal con try catch
                        print(f"El funcionario no puede ser accesado: {ule}")        
                    except ValueError as ve:
                        print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
                    except Exception as e:
                        print(f"Error inesperado: {e}")                    

        time.sleep(2)
        print("No se ha encontrado el servicio con el ID colocado. Intente de nuevo.")
        time.sleep(1)


    @classmethod
    def eliminar_Servicio(cls):
        cls.lp()
        print(("="*55), "\nEliminar servicio del centro dental.\n")
        cls.mostrar_Servicios()
        id_servicio_eleccion = input("Digite el ID del servicio que desea eliminar del sistema.")
        for ser in cls.servicios:
            if(id_servicio_eleccion==ser.ID_Servicio):
                opcion_Aceptar=True
                while(opcion_Aceptar):
                    time.sleep(1)
                    aceptar = input("Servicio encontrado. Esta seguro que desea continuar con la eliminacion?\n1)Si\n2)No\n")
                    if(aceptar=="1"):
                        cls.servicios.remove(ser)
                        time.sleep(1)
                        print("La eliminacion del servicio ha sido realizada correctamente.")
                        time.sleep(2)
                        opcion_Aceptar=False
                    elif(aceptar=="2"):
                        print(f"La eliminacion no ha sido efectuada.\n")
                        time.sleep(2)
                        opcion_Aceptar=False #se sale del menu
                    else:
                        print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.")
                        continue
        time.sleep(2)
        print("No se ha encontrado el servicio con el ID proporcionado. Intente de nuevo")
        time.sleep(1)

    #============================================= XML para los servicios ==================================================

    @classmethod
    def guardar_Servicios_xml(cls,ruta):
        try:
            raiz=ET.Element("servicios")
            for ser in cls.servicios:
                nodo = ET.SubElement(raiz, "servicio", id=str(ser.ID_Servicio))
                ET.SubElement(nodo, "nombre_servicio").text = str(ser.Nombre_Servicio)
                ET.SubElement(nodo, "costo").text = str(ser.Costo)
                ET.SubElement(nodo, "descripcion").text = str(ser.Descripcion)

            arbol = ET.ElementTree(raiz)
            arbol.write(ruta, encoding="utf-8", xml_declaration=True)
            print("Los funcionarios han sido guardados correctamente.")

        except Exception as e:
            print(f"Error inesperado al guardar los funcionarios: {e}")

    @classmethod
    def cargar_Servicios_xml(cls,ruta):
        try:
            arbol = ET.parse(ruta)
            raiz= arbol.getroot()

            for s in raiz.findall("servicio"):
                id_servicio = s.get("id")
                nombre_servicio = s.find("nombre_servicio").text
                costo = float(s.find("costo").text)
                descripcion = s.find("descripcion").text
                cls.servicios.append(cls(id_servicio,nombre_servicio,costo,descripcion))
            
            print("Funcionarios cargados correctamente.")

        except FileNotFoundError:
            print("Archivo de servicios no encontrado. Se iniciara con lista vacia.")
        except ET.ParseError:
            print("ERROR: El archivo XML de servicios esta mal formado.")
        except Exception as e:
            print(f"Error inesperado al cargar servicios: {e}") #los exception agarran cualquier error que encontremos
        
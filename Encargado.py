from MenorEdad import MenorEdad 
from datetime import date

import os
import time
import xml.etree.ElementTree as ET


class Encargado: 

    encargados=[] #lista de encargados esta aca

    def __init__(self, ID_encargado:int, Nombre:str, Primer_Apellido:str,Segundo_Apellido:str,Identificacion:int, 
                Direccion: str, Provincia:str, Codigo_Postal:int, Telefono:int, Correo_Electronico:str): #Deje los tipos para mi referencia
        self.__ID_encargado=ID_encargado
        self.__Nombre= Nombre
        self.__Primer_Apellido= Primer_Apellido
        self.__Segundo_Apellido= Segundo_Apellido
        self.__Identificacion= Identificacion
        self.__Direccion= Direccion
        self.__Provincia= Provincia
        self.__Codigo_Postal= Codigo_Postal
        self.__Telefono= Telefono
        self.__Correo_Electronico= Correo_Electronico
        self.__menoresEdad= []         #menor de edad esta dentro del encargado, ya que es a raiz de este que se genera las citas 

    @staticmethod
    def lp():
        os.system("cls" if os.name == "nt" else "clear") #metodo os para limpiar la pantalla

#============================================================= Getters n Setters =========================================================
    @property
    def ID_encargado(self):
        return self.__ID_encargado
    
    @ID_encargado.setter
    def ID_encargado(self, valor):
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
        
        self.__ID_encargado = valor_prueba
        
    @property
    def Nombre(self):
        return self.__Nombre
    
    @Nombre.setter
    def Nombre(self, valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        self.__Nombre = valor

    @property
    def Primer_Apellido(self):
        return self.__Primer_Apellido
    
    @Primer_Apellido.setter
    def Primer_Apellido (self,valor):
        if not valor:
            raise ValueError("El apellido no puede estar vacio")
        self.__Primer_Apellido=valor

    @property
    def Segundo_Apellido(self):
        return self.__Segundo_Apellido

    @Segundo_Apellido.setter
    def Segundo_Apellido(self, valor):
        if not valor:
            raise ValueError("El apellido no puede estar vacio")
        self.__Segundo_Apellido=valor

    @property
    def Identificacion(self):
        return self.__Identificacion

    @Identificacion.setter
    def Identificacion(self, valor):
        if not valor:
            raise ValueError("La identificacion no puede estar vacia")
        
        try:
            valor_prueba = int(valor)
        except ValueError:
            raise ValueError("La identificacion solo puede contener valores numericos aceptados, de 9 digitos")
        
        if valor_prueba<=100000001:             #las identificaciones siempre inician en 1 por SJ, y debe tener 9 digitos siempre, cuando se incluyen 0's en id viejos
            raise ValueError("La identificacion debe ser de un formato numerico aceptado de 9 digitos.")
        if valor_prueba>999999999:
            raise ValueError("El ID debe tener no mas de 9 digitos")
        
        self.__Identificacion=valor_prueba

    @property    
    def Direccion(self):
        return self.__Direccion

    @Direccion.setter
    def Direccion(self, valor):
        if not valor:
            raise ValueError("La direccion no puede estar vacia")
        self.__Direccion=valor

    @property    
    def Provincia(self):
        return self.__Provincia

    @Provincia.setter
    def Provincia(self, valor):
        if not valor:
            raise ValueError("La provincia no puede estar vacia")
        self.__Provincia=valor
    
    @property    #voy a usar codigo postal para saber donde se encuentran. Codigos postales nos dan el distrito y demas informacion, agregar provincia fue un plus
    def Codigo_Postal(self):
        return self.__Codigo_Postal

    @Codigo_Postal.setter
    def Codigo_Postal(self, valor):
        if not valor:
            raise ValueError("El codigo postal no puede estar vacio")
        
        try:
            valor_prueba = int(valor)
        except ValueError:
            raise ValueError("El codigo postal solo puede contener valores numericos aceptados, con 5 digitos")
        
        if valor_prueba<=10101:  #minimo de codigo postal es 10101, Carmen        
            raise ValueError("El codigo postal debe ser de un formato numerico aceptado.")
        if valor_prueba>70605: #maximo de codigo postal es 70605, Duacari
            raise ValueError("El codigo postal debe tener un maximo de 5 digitos")
        self.__Codigo_Postal=valor_prueba

    @property    
    def Telefono(self):
        return self.__Telefono

    @Telefono.setter
    def Telefono(self, valor):
        if not valor:
            raise ValueError("El numero telefonico no puede estar vacio")
        try:
            valor_prueba = int(valor)
        except ValueError:
            raise ValueError("El numero telefonico solo puede contener valores numericos aceptados, con 8 digitos")
        
        if valor_prueba<=10000000:      
            raise ValueError("El numero telefonico debe ser de un formato numerico aceptado.")
        if valor_prueba>99999999: 
            raise ValueError("El numero telefonico debe tener un maximo de 8 digitos")
        
        self.__Telefono=valor_prueba

    @property    
    def Correo_Electronico(self):
        return self.__Correo_Electronico

    @Correo_Electronico.setter
    def Correo_Electronico(self, valor):
        if not valor:
            raise ValueError("El correo no puede estar vacio. ")
        if "@" not in valor:
            raise ValueError("El correo electronico debe contener un @ para tener el formato necesario para ser aceptado. ")
        self.__Correo_Electronico=valor

    @property    
    def menoresEdad(self):
        return self.__menoresEdad
#============================================================= Metodos ===================================================================


    @classmethod
    def agregar_menorEdad(cls,id_encargado=None): #definirlo como None nos permite algo: Si agregar_menorEdad viene del menu principal (sin ID seleccionado) hay que seleccionarlo, pero si viene de agregar_paciente, entonces el ID se agrega automatico
        cls.lp()
        if not id_encargado:
            print("Actualmente se encuentran los siguientes encargados en la base: ")
            cls.mostrar_Encargados()
            id_seleccionado= input("Digite el ID correspondiente al encargado al cual debemos asignarle un menor de edad: ")
        else:
            id_seleccionado = id_encargado

        for e in cls.encargados:
            if(id_seleccionado== e.ID_encargado):    
                comprobacion_ame=True
                time.sleep(1)
                print("ID encargado encontrado. Se procedera a agregar uno o mas menores de edad a la persona seleccionada.\n")
                time.sleep(1)
                while(comprobacion_ame):
                    try:
                        id_menor=input ("Digite el ID correspondiente al menor de edad:  ")
                        id_duplicado = False
                        for men in e.menoresEdad:
                            if(id_menor==men.ID_menorEdad):
                                print("El ID ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                                time.sleep(2)
                                id_duplicado=True
                                break
                                
                        if id_duplicado:
                            continue        #para volver al inicio en caso de que ya haya sido usado
                        
                        nombre_menor = input("\nDigite el nombre de la persona menor de edad: ")
                        primer_apellido_menor = input("\nDigite el primer apellido de la persona menor de edad encargada: ")
                        segundo_apellido_menor = input("\nDigite el segundo apellido de la persona menor de edad: ")

                        sexo_comprob = input("\nDigite el sexo de la persona menor de edad. Se permiten las siguientes denominaciones 'Masculino', 'Femenino', 'No Definido': ")
                        sexo = ''
                        match sexo_comprob:
                            case "Masculino":
                                sexo="Masculino"
                            case "Femenino":
                                sexo = "Femenino"
                            case "No Definido":
                                sexo = "No Definido"
                            case _:
                                print("El sexo digitado no esta contemplado como parte de las opciones. Digite unicamente las opciones proporcionadas.")
                                time.sleep(2)
                                continue
                            
                        fecha_comprob = input("\nProporcione la fecha de nacimiento de la persona menor de edad. Debe estar unicamente en el formato: AAAA-MM-DD para evitar ser rechazado. \nDigite la fecha:   ")
                        
                        fecha_nacimiento = date.fromisoformat(fecha_comprob)
                        time.sleep(2)
                        e.menoresEdad.append(MenorEdad(id_menor,nombre_menor, primer_apellido_menor, segundo_apellido_menor, sexo, fecha_nacimiento))
                            
                        print(f"El nuevo menor de edad {nombre_menor} ha sido registrado correctamente.\n¿Desea agregar otro menor de edad?\n1)Si\n2)No")
                        seleccion_repeticion= input()
                        match seleccion_repeticion:
                            case "1":
                                print("El proceso se repetira para generar un nuevo menor de edad.")
                                time.sleep(2)
                                continue
                            case "2":
                                print("El proceso de agregar un hijo ha sido exitoso. Volviendo al menu principal.")
                                time.sleep(2)
                                comprobacion_ame=False
                                return
                            case _:
                                print("La opcion digitada no corresponde a las opciones. No se agregara un nuevo menor de edad asociado.")
                                time.sleep(2)
                                comprobacion_ame=False
                                return
                        
                    except UnboundLocalError as ule: 
                        print(f"El funcionario no puede ser accesado: {ule}")        
                    except ValueError as ve:
                        print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
                    except Exception as e:
                        print(f"Error inesperado: {e}")
                return
            
        print("No se ha encontrado el encargado con el ID digitado. Vuelvalo a intentar")
        time.sleep(2)
        return



    @classmethod
    def creacion_Paciente (cls):
        #creacion del padre va primero
        cls.lp()
        print(("="*60), "\nNuevo paciente en la base de datos\n\nAsegurese de digitar correctamente los datos solicitados para evitar rehacer el proceso.\n")
        comprobacion = True
        while(comprobacion):
            try:
                id_encargado= input("Digite el ID de la persona encargada. Debe ser numerico aceptado, no mayor a mas de 8 digitos:  ")
                for e in cls.encargados:
                    if(id_encargado== e.ID_encargado):
                        print("El ID ya se encuentra ocupado. Intente de nuevo ")
                        time.sleep(2)
                        comprobacion=False
                        return
                nombre_encargado = input("\nDigite el nombre de la persona encargada:  ") #estos son los datos asociados con el encargado.
                primer_apellido_encargado = input("\nDigite el primer apellido de la persona encargada:  ")
                segundo_apellido_encargado = input("\nDigite el segundo apellido de la persona encargada:  ")

                iden = input("\nDigite la identificacion correspondiente al encargado. La misma debe tener 8 digitos, incluyendo los 0 sin guiones:  ")
                for e in cls.encargados:
                    if(iden == e.Identificacion):
                        print("El ID ya se encuentra ocupado. Intente de nuevo ")
                        time.sleep(2)
                        comprobacion=False
                        return
                direccion = input("\nColoque su direccion actual completa:\n")
                provincia = input("\nDigite la provincia en la cual recide actualmente:  ")
                codigo = input("\nDigite el codigo postal correspondiente de su lugar de residencia. Debe ser de 5 digitos:  ")
                telefono = input("\nDigite su numero telefonico. Debe ser de 8 digitos sin uso de lineas o separadores:  ")
                correo= input("\nDigite un correo electronico personal de preferencia: ")

                print("Revisando los datos para comprobar que se hayan generado correctamente...") #si todo aparenta bien, se deja continuar y guardar
                time.sleep(2)
                cls.encargados.append(cls(id_encargado, nombre_encargado, primer_apellido_encargado, segundo_apellido_encargado, iden, direccion,provincia, codigo, telefono, correo))

                print(f"El nuevo encargado {nombre_encargado} ha sido guardado exitosamente.\n")
                time.sleep(2)
                comprobacion=False

            except UnboundLocalError as ule: #try catch por si se encuentra valores no esperados y no se caiga
                print(f"El funcionario no puede ser accesado: {ule}")        
            except ValueError as ve:
                print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
            except Exception as e:
                print(f"Error inesperado: {e}")
        seleccion = input("\n¿Desea agregar un paciente asociado al encargado de una vez?\n1)Aceptar\n2)Denegar\nSeleccion:  ")
        match seleccion:
            case "1":
                cls.agregar_menorEdad(id_encargado)
                time.sleep(1)
            case "2":
                print("Se procedera sin guardar un menor de edad para el encargado. Para agregar uno, vuelva a realizar el proceso y elija la opcion correspondiente\n")
                time.sleep(2)
                return
            case _:
                print("La opcion no corresponde a las opciones dentro del menu")
                time.sleep(2)

    @classmethod
    def mostrar_Encargados (cls):
        print("Encargados o padres de familia actuales:\n")
        print(f"{'ID':<8} {'Nombre':<15} {'Primer Apellido':<18} {'Segundo Apellido':<18} {'Cedula':<12} {'Direccion':<40} \
            {'Provincia':<12} {'Codigo':<8} {'Telefono':<12} {'Correo':<25}")
        print("-"*200)

        for enc in cls.encargados:
            print(f"{enc.ID_encargado:<8}{enc.Nombre:<15}{enc.Primer_Apellido:<18}{enc.Segundo_Apellido:<18}{enc.Identificacion:<12}\
                {enc.Direccion:<40}{enc.Provincia:<12}{enc.Codigo_Postal:<8}{enc.Telefono:<12}{enc.Correo_Electronico:<25}")
            #for men in cls.menoresEdad: tengo que crear algo para que se vean los menores de edad tambien


    @classmethod
    def editar_Encargados_o_Menores (cls):
        cls.lp()
        print(("="*55), "\nEditar informacion de paciente o encargado.\n")
        cls.mostrar_Encargados()
        ID_encargado_eleccion = input("Digite el ID de la persona encargada:  ")
        
        encargado_encontrado = False
        for enc in cls.encargados:
            if(ID_encargado_eleccion==enc.ID_encargado):
                encargado_encontrado=True
                time.sleep(1)
                seleccion_editar = input("\nPersona encargada encontrada. Seleccione si desea modificar el encargado o a un menor de edad asociado:\n1)Encargado\n2)Menor de edad\nSeleccion:  ") 
                time.sleep(1)
                if(seleccion_editar=="1"):
                    modificar_encargado=True
                    while(modificar_encargado):
                        try:
                            time.sleep(1)
                            cls.lp()
                            print(("="*55), "Modificacion de encargado") #todo lo que viene abajo es similar en logica a lo ya visto. Son variables del objeto y es largo
                            nombre_Comprobacion= ""
                            print(f"Nombre actual del encargado: {enc.Nombre}")
                            nuevo_Nombre= input("\nDigite el nombre al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Nombre=="mantener"): 
                                print("\nEl nombre se va a mantener.")
                                nombre_Comprobacion = enc.Nombre
                            else:
                                print(f"\nNombre actualizado correctamente a: {nuevo_Nombre}") 
                                nombre_Comprobacion= nuevo_Nombre
                            
                            Primer_Apellido_Comprobacion= ""
                            print(f"Primer apellido actual del encargado: {enc.Primer_Apellido}")
                            nuevo_Primer_Apellido= input("\nDigite el primer apellido al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Primer_Apellido=="mantener"): 
                                print("\nEl primer apellido se va a mantener.")
                                Primer_Apellido_Comprobacion = enc.Primer_Apellido
                            else:
                                print(f"\nPrimer apellido actualizado correctamente a: {nuevo_Primer_Apellido}") 
                                Primer_Apellido_Comprobacion= nuevo_Primer_Apellido

                            Segundo_Apellido_Comprobacion= ""
                            print(f"Segundo apellido actual del encargado: {enc.Segundo_Apellido}")
                            nuevo_Segundo_Apellido= input("\nDigite el segundo apellido al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Segundo_Apellido=="mantener"): 
                                print("\nEl segundo apellido se va a mantener.")
                                Segundo_Apellido_Comprobacion = enc.Segundo_Apellido
                            else:
                                print(f"\nSegundo apellido actualizado correctamente a: {nuevo_Segundo_Apellido}") 
                                Segundo_Apellido_Comprobacion= nuevo_Segundo_Apellido


                            Identificacion_Comprobacion = ""
                            print(f"Identificacion actual del encargado {enc.Identificacion} \n")
                            nueva_Identificacion = input("\nDigite la nueva identificacion de la persona encargada. Asegurese de usar el formato correcto (9 digitos numericos).\nSi no desea actualizarlo, digite 'mantener': ")
                            if(nueva_Identificacion=="mantener"): 
                                print("\nLa identificacion se va a mantener.")
                                Identificacion_Comprobacion = enc.Identificacion
                            else:
                                Identificacion_Duplicada=False #esta bandera nos permite usar continue, que salta cuando hay un usuario o ID duplicado. Si esta duplicado, vuelve al inicio del bucle while, pero sabiendo que el ID matcheo
                                for e in cls.encargados:
                                    if (nueva_Identificacion==e.Identificacion):    
                                        print("La identificacion ya se encuentra actualmente ocupada. Intente de nuevo.\n") 
                                        time.sleep(1)
                                        Identificacion_Duplicada=True
                                        break
                                if (Identificacion_Duplicada):
                                    continue
                                print(f"\nIdentificacion actualizada correctamente a: {nueva_Identificacion}") 
                                Identificacion_Comprobacion= nueva_Identificacion

                            Direccion_Comprobacion= ""
                            print(f"Direccion actual del encargado: {enc.Direccion}")
                            nuevo_Direccion= input("\nDigite la direccion al cual que se debe actualizar. Si no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Direccion=="mantener"): 
                                print("\nLa direccion se va a mantener.")
                                Direccion_Comprobacion = enc.Direccion
                            else:
                                print(f"\nDireccion actualizado correctamente a: {nuevo_Direccion}") 
                                Direccion_Comprobacion= nuevo_Direccion

                            Provincia_Comprobacion= ""
                            print(f"Provincia actual del encargado: {enc.Provincia}")
                            nueva_Provincia= input("\nDigite la provincia al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                            if(nueva_Provincia=="mantener"): 
                                print("\nLa provincia se va a mantener.")
                                Provincia_Comprobacion = enc.Provincia
                            else:
                                print(f"\nProvincia actualizada correctamente a: {nueva_Provincia}") 
                                Provincia_Comprobacion= nueva_Provincia

                            Codigo_Comprobacion = ""
                            print(f"Codigo postal actual del encargado {enc.Codigo_Postal} \n")
                            nuevo_Codigo = input("\nDigite el nuevo codigo postal de la persona encargada. Asegurese de usar el formato correcto (5 digitos numericos correspondientes al distrito).\nSi no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Codigo=="mantener"): 
                                print("\nEl codigo postal se va a mantener.")
                                Codigo_Comprobacion = enc.Codigo_Postal
                            else:
                                print(f"\nCodigo postal actualizado correctamente a: {nuevo_Codigo}") 
                                Codigo_Comprobacion= nuevo_Codigo

                            Telefono_Comprobacion = ""
                            print(f"Telefono actual del encargado {enc.Telefono} \n")
                            nuevo_Telefono = input("\nDigite el nuevo telefono de la persona encargada. Asegurese de usar el formato correcto (8 digitos numericos).\nSi no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Telefono=="mantener"): 
                                print("\nEl telefono se va a mantener.")
                                Telefono_Comprobacion = enc.Telefono
                            else:
                                print(f"\nTelefono actualizado correctamente a: {nuevo_Telefono}") 
                                Telefono_Comprobacion= nuevo_Telefono

                            Correo_Comprobacion = ""
                            print(f"Correo actual del encargado {enc.Correo_Electronico} \n")
                            nuevo_Correo= input("\nDigite el nuevo correo de la persona encargada. Asegurese de usar el formato correcto.\nSi no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_Correo=="mantener"): 
                                print("\nEl correo electronico se va a mantener.")
                                Correo_Comprobacion = enc.Correo_Electronico
                            else:
                                print(f"\nCorreo electronico actualizado correctamente a: {nuevo_Correo}") 
                                Correo_Comprobacion= nuevo_Correo

                            ID_Comprobacion = ""
                            print(f"ID asociado actual del encargado {enc.ID_encargado} \n")
                            nuevo_ID = input("\nDigite el nuevo ID asociado de la persona encargada. Asegurese de usar el formato correcto (8 digitos).\nSi no desea actualizarlo, digite 'mantener': ")
                            if(nuevo_ID=="mantener"): 
                                print("La identificacion se va a mantener.")
                                ID_Comprobacion = enc.ID_encargado
                            else:
                                ID_Duplicado=False
                                for e in cls.encargados:
                                    if (nuevo_ID==e.ID_encargado):    
                                        print("El ID asociado ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                                        time.sleep(1)
                                        ID_Duplicado=True
                                        break
                                if (ID_Duplicado):
                                    continue
                                print(f"\nID actualizado correctamente a: {nuevo_ID}") 
                                ID_Comprobacion= nuevo_ID

                            time.sleep(2)
                            print("El encargado seleccionado ahora se ha actualizado con los siguientes datos:") #queremos que el usuario vea los datos nuevos, se concatena la comprobacion antes de aceptarla para asegurar que los datos sean correctos y evitar errores del usuario
                            print(f"ID: {ID_Comprobacion} | Nombre: {nombre_Comprobacion} | Primer Apellido: {Primer_Apellido_Comprobacion} | Segundo Apellido {Segundo_Apellido_Comprobacion}| Identificacion: {Identificacion_Comprobacion} | Direccion: {Direccion_Comprobacion} | \
                                Provincia: {Provincia_Comprobacion} | Codigo Postal: {Codigo_Comprobacion} | Telefono: {Telefono_Comprobacion} | Correo: {Correo_Comprobacion} ")
                            
                            #Aceptas los datos que has colocado?
                            opcion_Aceptar=True
                            while(opcion_Aceptar):
                                aceptar = input("Esta seguro que desea continuar?\n1)Si\n2)No\n") #Menu de confirmacion, se asignan solo y solo si se acepta
                                if(aceptar=="1"):
                                    time.sleep(1)
                                    print("\nAsegurando de que el proceso haya sido exitoso...")
                                    time.sleep(1)

                                    enc.ID_encargado = ID_Comprobacion
                                    enc.Nombre = nombre_Comprobacion
                                    enc.Primer_Apellido = Primer_Apellido_Comprobacion
                                    enc.Segundo_Apellido = Segundo_Apellido_Comprobacion
                                    enc.Identificacion = Identificacion_Comprobacion
                                    enc.Direccion = Direccion_Comprobacion
                                    enc.Provincia = Provincia_Comprobacion
                                    enc.Codigo_Postal = Codigo_Comprobacion
                                    enc.Telefono = Telefono_Comprobacion
                                    enc.Correo_Electronico = Correo_Comprobacion
                                    
                                    time.sleep(1)
                                    print("\nEl proceso ha sido exitoso.")
                                    time.sleep(2)
                                    opcion_Aceptar=False #se cierra el menu
                                    return
                                elif(aceptar=="2"):
                                    print(f"El cambio se ha cancelado. Los datos del encargado {enc.Nombre +" "+ enc.Primer_Apellido} no han sido actualizados")#Se cancela el cambio 
                                    time.sleep(2)
                                    opcion_Aceptar=False #se cierra el menu
                                    return
                                else:
                                    print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.") #se entra al bucle a menos que elija las opciones correctas
                            time.sleep(2)
                            modificar_encargado=False

                        except UnboundLocalError as ule: 
                            print(f"El funcionario no puede ser accesado: {ule}")        
                        except ValueError as ve:
                            print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
                        except Exception as e:
                            print(f"Error inesperado: {e}")
                elif(seleccion_editar=="2"):
                    modificar_menor=True
                    while(modificar_menor):
                        try:
                            time.sleep(1)
                            cls.lp()
                            print(("="*100), "Modificacion de menor de edad")
                            print("\nInformacion actual de los menores asociados a la persona encargada:\n")
                            print(f"{'ID':<8} {'Nombre':<15} {'Primer Apellido':<18} {'Segundo Apellido':<18} {'Sexo':<12} {'Fecha de Nacimiento':<18} {'Edad':<6}")
                            print("-"*100)
                            for m in enc.menoresEdad:
                                    print(f"{m.ID_menorEdad:<8}{m.Nombre:<15}{m.Primer_Apellido:<18}{m.Segundo_Apellido:<18}{m.Sexo:<12} {str(m.Fecha_Nacimiento):<18} {m.calculo_Edad_Menor():<6}")

                            menor_edad_busqueda= input("\nDigite el ID del menor de edad asociado a la persona encargada:  ")
                            menor_encontrado=False
                            for men in enc.menoresEdad:
                                if(menor_edad_busqueda==men.ID_menorEdad): #similar a encargados, editar es largo pero toda la validacion es repetitiva
                                    menor_encontrado=True
                                    print("Menor de edad asociado al encargado de familia encontrado. Informacion puede ser editada.\n")
                                    time.sleep(1)
                                    cls.lp()

                                    nombre_Comprobacion= ""
                                    print(f"\nNombre actual del menor de edad : {men.Nombre}")
                                    nuevo_Nombre= input("\nDigite el nombre al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                                    if(nuevo_Nombre=="mantener"): 
                                        print("\nEl nombre se va a mantener.")
                                        nombre_Comprobacion = men.Nombre
                                    else:
                                        print(f"\nNombre actualizado correctamente a: {nuevo_Nombre}") 
                                        nombre_Comprobacion= nuevo_Nombre
                                    
                                    Primer_Apellido_Comprobacion= ""
                                    print(f"Primer apellido actual del menor de edad: {men.Primer_Apellido}")
                                    nuevo_Primer_Apellido= input("\nDigite el primer apellido al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                                    if(nuevo_Primer_Apellido=="mantener"): 
                                        print("\nEl primer apellido se va a mantener.")
                                        Primer_Apellido_Comprobacion = men.Primer_Apellido
                                    else:
                                        print(f"\nPrimer apellido actualizado correctamente a: {nuevo_Primer_Apellido}") 
                                        Primer_Apellido_Comprobacion= nuevo_Primer_Apellido

                                    Segundo_Apellido_Comprobacion= ""
                                    print(f"Segundo apellido actual del menor de edad: {men.Segundo_Apellido}")
                                    nuevo_Segundo_Apellido= input("\nDigite el segundo apellido al cual que se deba actualizar. Si no desea actualizarlo, digite 'mantener': ")
                                    if(nuevo_Segundo_Apellido=="mantener"): 
                                        print("\nEl segundo apellido se va a mantener.")
                                        Segundo_Apellido_Comprobacion = men.Segundo_Apellido
                                    else:
                                        print(f"\nSegundo apellido actualizado correctamente a: {nuevo_Segundo_Apellido}") 
                                        Segundo_Apellido_Comprobacion= nuevo_Segundo_Apellido

                                    Sexo_Comprobacion = ""
                                    print(f"Sexo biologico actual de la persona menor de edad: {men.Sexo}")
                                    nuevo_Sexo = input("\nDigite el sexo actualizado de la persona menor de edad. \nSe permiten las siguientes denominaciones 'Masculino', 'Femenino', 'No Definido'. Si no desea actualizarlo, digite 'mantener': ")
                                    if(nuevo_Sexo=="mantener"): 
                                        print("\nEl sexo se va a mantener.")
                                        Sexo_Comprobacion = men.Sexo
                                    else:
                                        match nuevo_Sexo:
                                            case "Masculino":
                                                Sexo_Comprobacion = nuevo_Sexo
                                                print(f"Segundo apellido actualizado correctamente a: {nuevo_Sexo}") 
                                            case "Femenino":
                                                Sexo_Comprobacion = nuevo_Sexo
                                                print(f"Segundo apellido actualizado correctamente a: {nuevo_Sexo}") 
                                            case "No Definido":
                                                Sexo_Comprobacion = nuevo_Sexo
                                                print(f"Segundo apellido actualizado correctamente a: {nuevo_Sexo}") 
                                            case _:
                                                print("El sexo digitado no esta contemplado como parte de las opciones. Digite unicamente las opciones proporcionadas. \nNo se realizaran los cambios en el sexo biologico.")
                        
                                        Fecha_Comprobacion = ""
                                        print(f"\nFecha de nacimiento actual de la persona menor de edad: {men.Fecha_Nacimiento}")
                                        Nueva_Fecha = input("\nProporcione la nueva fecha de nacimiento de la persona menor de edad. Debe estar unicamente en el formato: AAAA-MM-DD para evitar ser rechazado. \nDigite la fecha. Si no desea actualizarlo, digite 'mantener':  ")
                                        if(Nueva_Fecha=="mantener"): 
                                            print("\nLa fecha de nacimiento se va a mantener.")
                                            Fecha_Comprobacion = men.Fecha_Nacimiento
                                        else:
                                            Fecha_Comprobacion = date.fromisoformat(Nueva_Fecha)
                                            print(f"\nFecha de comprobacion actualizado correctamente a: {Nueva_Fecha}") 
                                        
                                        
                                        ID_Comprobacion = ""
                                        print(f"ID asociado actual del menor de edad {men.ID_menorEdad} \n")
                                        nuevo_ID = input("\nDigite el nuevo ID asociado de la persona menor de edad. Asegurese de usar el formato correcto (8 digitos).\nSi no desea actualizarlo, digite 'mantener': ")
                                        if(nuevo_ID=="mantener"): 
                                            print("\nEl ID se va a mantener.")
                                            ID_Comprobacion = men.ID_menorEdad
                                        else:
                                            ID_Duplicado=False #bandera de duplicado para que no se repitan
                                            for m in enc.menoresEdad:
                                                if (nuevo_ID==m.ID_menorEdad):    
                                                    print("El ID asociado ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                                                    time.sleep(1)
                                                    ID_Duplicado=True
                                                    break
                                            if (ID_Duplicado):
                                                continue
                                            print(f"\nID actualizado correctamente a: {nuevo_ID}") 
                                            ID_Comprobacion = nuevo_ID
                                                
                                        time.sleep(1)
                                        print("El menor de edad seleccionado ahora se ha actualizado con los siguientes datos:") #queremos que el usuario vea los datos nuevos, se concatena la comprobacion antes de aceptarla para asegurar que los datos sean correctos y evitar errores del usuario
                                        print(f"ID: {ID_Comprobacion} | Nombre: {nombre_Comprobacion} | Primer Apellido: {Primer_Apellido_Comprobacion} | Segundo Apellido: {Segundo_Apellido_Comprobacion} | Sexo: {Sexo_Comprobacion} | Fecha de Nacimiento:{Fecha_Comprobacion} | Edad: {men.calculo_Edad_Menor()}")
                                        
                                        #Aceptas los datos que has colocado?
                                        opcion_Aceptar=True
                                        while(opcion_Aceptar):
                                            aceptar = input("Esta seguro que desea continuar?\n1)Si\n2)No\n") #Menu de confirmacion, se asignan solo y solo si se acepta
                                            if(aceptar=="1"):
                                                time.sleep(1)
                                                print("\nAsegurando de que el proceso haya sido exitoso...")
                                                time.sleep(1)
                                                #se aprueban los datos y se guardan
                                                men.ID_menorEdad= ID_Comprobacion
                                                men.Nombre= nombre_Comprobacion
                                                men.Primer_Apellido= Primer_Apellido_Comprobacion
                                                men.Segundo_Apellido=Segundo_Apellido_Comprobacion
                                                men.Sexo= Sexo_Comprobacion
                                                men.Fecha_Nacimiento=Fecha_Comprobacion

                                                time.sleep(1)
                                                print("El proceso ha sido exitoso.")
                                                time.sleep(2)
                                                modificar_menor=False #se cierra el menu
                                                return
                                            elif(aceptar=="2"):
                                                print(f"El cambio se ha cancelado. Los datos del menor de edad {enc.Nombre +" "+ enc.Primer_Apellido} no han sido actualizados")#Se cancela el cambio 
                                                time.sleep(2)
                                                modificar_menor=False #se cierra el menu
                                                return
                                            else:
                                                print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.") #se entra al bucle a menos que elija las opciones correctas
                            if not menor_encontrado:            
                                time.sleep(2)
                                print("No se ha encontrado el menor de edad con el ID colocado. Intente de nuevo.")
                                time.sleep(1)
                                modificar_menor=False

                        except UnboundLocalError as ule: 
                            print(f"El funcionario no puede ser accesado: {ule}")        
                        except ValueError as ve:
                            print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
                        except Exception as e:
                            print(f"Error inesperado: {e}")
                else:
                    print("\nSe ha digitado una opcion no contemplada en el menu. Intentelo de nuevo.")
                    time.sleep(2)
                    return
        if not encargado_encontrado:
            time.sleep(2)
            print("\nNo se ha encontrado la persona encargada con el ID colocado. Intente de nuevo.")
            time.sleep(1)



    @classmethod
    def eliminar_encargado_o_menor(cls):
        cls.lp()
        print(("="*55), "\nEliminar paciente o encargado.\n")
        cls.mostrar_Encargados()
        ID_encargado_eleccion = input("\nDigite el ID de la persona encargada:  ")
        
        encargado_encontrado=False
        for enc in cls.encargados:
            if(ID_encargado_eleccion==enc.ID_encargado):
                encargado_encontrado=True
                time.sleep(1)
                seleccion_eliminar = input("Persona encargada encontrada. Seleccione si desea eliminar el encargado o a un menor de edad asociado:\n1)Encargado\n2)Menor de edad\nSeleccion:  ")
                
                if(seleccion_eliminar=="1"):
                    opcion_Aceptar= True
                    while(opcion_Aceptar):
                        time.sleep(1)
                        aceptar = input("Se eliminara el encargado y los menores de edad asociados. Esta seguro que desea continuar?\n1)Si\n2)No\nRespuesta: ")
                        if(aceptar=="1"):
                            cls.encargados.remove(enc) #remove eliminar todo el objeto directamente, en este caso, no lo pasamos a inactivo como es el caso de 
                            time.sleep(1)
                            print("Se ha eliminado el funcionario correctamente.")
                            time.sleep(2)
                            opcion_Aceptar=False #se sale del menu
                        elif(aceptar=="2"):
                            print(f"La eliminacion no ha sido efectuada\n")
                            time.sleep(2)
                            opcion_Aceptar=False #se sale del menu
                        else:
                            print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.")
                            continue

                elif(seleccion_eliminar=="2"):
                    print(("="*100), "Eliminacion de menor de edad")
                    print("\nInformacion actual de los menores asociados a la persona encargada:\n")
                    print(f"{'ID':<8} {'Nombre':<15} {'Primer Apellido':<18} {'Segundo Apellido':<18} {'Sexo':<12} {'Fecha de Nacimiento':<18} {'Edad':<6}")
                    print("-"*100)
                    for m in enc.menoresEdad:
                        print(f"{m.ID_menorEdad:<8}{m.Nombre:<15}{m.Primer_Apellido:<18}{m.Segundo_Apellido:<18}{m.Sexo:<12} {str(m.Fecha_Nacimiento):<18} {m.calculo_Edad_Menor():<6}")
                    menor_edad_busqueda= input("\nDigite el ID del menor de edad asociado a la persona encargada:  ")
                    
                    menor_encontrado=False
                    for men in enc.menoresEdad:
                        if(menor_edad_busqueda==men.ID_menorEdad):
                            menor_encontrado=True
                            opcion_Aceptar=True
                            while(opcion_Aceptar):    
                                aceptar=input("\nMenor de edad asociado al encargado de familia encontrado. Toda informacion sera eliminada. Esta seguro que desea continuar?\n1)Si\n2)No\nRespuesta:")
                                if(aceptar=="1"):
                                    enc.menoresEdad.remove(men) #remove eliminar todo el objeto directamente, en este caso, no lo pasamos a inactivo como es el caso de 
                                    time.sleep(1)
                                    print("Se ha eliminado el menor de edad correctamente.")
                                    time.sleep(2)
                                    opcion_Aceptar=False #se sale del menu
                                elif(aceptar=="2"):
                                    print(f"La eliminacion no ha sido efectuada\n")
                                    time.sleep(2)
                                    opcion_Aceptar=False #se sale del menu
                                else:
                                    print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.")
                                    continue                            
                    if not menor_encontrado:
                        time.sleep(2)
                        print("No se ha encontrado la persona menor de edad con el ID que ha colocado. Intente de nuevo.")
                        time.sleep(1)     
                else:
                    print("Se ha digitado una opcion no contemplada en el menu. Intentelo de nuevo.")
                    time.sleep(2)
                    return
        if not encargado_encontrado:
            time.sleep(2)
            print("No se ha encontrado la persona encargada con el ID colocado. Intente de nuevo.")
            time.sleep(1)
#======================================== XML de encargados y menores ===========================================

    @classmethod
    def guardar_Encargados_xml(cls,ruta):
        try:
            raiz= ET.Element("encargados") #nombre principal de la clase o el array donde se guarda
            for enc in cls.encargados:
                encargados_nodo= ET.SubElement(raiz, "encargado", id=str(enc.ID_encargado))
                ET.SubElement(encargados_nodo, "nombre").text = str(enc.Nombre)
                ET.SubElement(encargados_nodo, "primer_apellido").text = str(enc.Primer_Apellido)
                ET.SubElement(encargados_nodo, "segundo_apellido").text = str(enc.Segundo_Apellido)
                ET.SubElement(encargados_nodo, "identificacion").text = str(enc.Identificacion)
                ET.SubElement(encargados_nodo, "direccion").text = str(enc.Direccion)
                ET.SubElement(encargados_nodo, "provincia").text = str(enc.Provincia)
                ET.SubElement(encargados_nodo, "codigo_postal").text = str(enc.Codigo_Postal)
                ET.SubElement(encargados_nodo, "telefono").text = str(enc.Telefono)
                ET.SubElement(encargados_nodo, "correo").text = str(enc.Correo_Electronico)

                #guardado de los menores asociados a cada encargado
                menores_nodo = ET.SubElement(encargados_nodo, "menores") #subelemento de nodo de encargados
                for men in enc.menoresEdad:
                    menor_nodo= ET.SubElement(menores_nodo, "menor", id=str(men.ID_menorEdad)) #aca menores, abajo menor, variables diferentes por cada menor
                    ET.SubElement(menor_nodo, "nombre").text = str(men.Nombre)
                    ET.SubElement(menor_nodo, "primer_apellido").text = str(men.Primer_Apellido)
                    ET.SubElement(menor_nodo, "segundo_apellido").text = str(men.Segundo_Apellido)
                    ET.SubElement(menor_nodo, "sexo").text = str(men.Sexo)
                    ET.SubElement(menor_nodo, "fecha_nacimiento").text = str(men.Fecha_Nacimiento)
            arbol = ET.ElementTree(raiz)
            arbol.write(ruta, encoding="utf-8", xml_declaration=True)
            print("Encargados y menores de edad guardados correctamente.")

        except Exception as e:
            print(f"Error inesperado al guardar la informacion de los encargados: {e}")
    
    @classmethod
    def cargar_Encargados_xml(cls,ruta):
        try:
            arbol = ET.parse(ruta)
            raiz = arbol.getroot()

            for fun in raiz.findall("encargado"):
                id_encargado = fun.get("id")
                nombre = fun.find("nombre").text
                primer_apellido = fun.find("primer_apellido").text
                segundo_apellido = fun.find("segundo_apellido").text
                identificacion = fun.find("identificacion").text
                direccion = fun.find("direccion").text
                provincia = fun.find("provincia").text
                codigo_postal = fun.find("codigo_postal").text
                telefono = fun.find("telefono").text
                correo = fun.find("correo").text

                encargado = cls(id_encargado, nombre, primer_apellido,segundo_apellido,identificacion,direccion,provincia,codigo_postal, telefono, correo)
                #menores asociados al encargado

                menores_nodo = fun.find("menores") #fun es por cada encargado asignado
                if menores_nodo is not None: #mientras existan menores, que entre
                    for m in menores_nodo.findall("menor"):#menor individual, encontrarlo
                        id_menor = m.get("id")
                        nombre_menor = m.find("nombre").text
                        primer_apellido_menor = m.find("primer_apellido").text
                        segundo_apellido_menor = m.find("segundo_apellido").text
                        sexo = m.find("sexo").text
                        fecha_nacimiento = m.find("fecha_nacimiento").text
                            #como fecha de nacimiento es de tipo date, se valida que este bien escrito.
                        fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
                        encargado.menoresEdad.append(MenorEdad(id_menor, nombre_menor, primer_apellido_menor, segundo_apellido_menor, sexo, fecha_nacimiento ))

                cls.encargados.append(encargado)
            print("Encargados cargados correctamente.")
        except FileNotFoundError:
            print("Archivo de encargados no encontrado. Se iniciará con lista vacía.")
        except ET.ParseError:
            print("ERROR: El archivo XML de encargados está mal formado.")
        except Exception as e:
            print(f"Error inesperado al cargar encargados: {e}")
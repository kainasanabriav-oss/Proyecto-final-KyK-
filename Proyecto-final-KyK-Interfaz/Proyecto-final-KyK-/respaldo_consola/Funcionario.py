import os #usado para la limpieza del menu
import time #usado para timers de tiempo para que las acciones no sean inmediatas y se aprecie la captura de datos, entre otros
import xml.etree.ElementTree as ET

#Clase funcionario, la cual va a ser necesaria validar para poder acceder a las demas acciones del programa

class Funcionario: #

    funcionarios=[] #listas creadas a partir de las clases
    usuario_Actual= ""

    def __init__(self, ID_funcionario, Usuario, Nombre_Completo, Estado): # mi manera de construir las clases va a ser similar a mi enfoque de Java, las validaciones se haran desde dentro
        self.__ID_funcionario=ID_funcionario
        self.__Usuario=Usuario
        self.__Nombre_Completo=Nombre_Completo
        self.__Estado=Estado
        #tipos de variables que vamos a encontrar dentro de funcionario, las vamos a encapsular

    #============================================================= Getters n Setters =========================================================
    @staticmethod
    def lp():
        os.system("cls" if os.name == "nt" else "clear") #metodo os para limpiar la pantalla

    @property                   #getter de python
    def ID_funcionario(self):
        return self.__ID_funcionario
    
    @ID_funcionario.setter      #setter de python
    def ID_funcionario(self, valor):
        if not valor: 
            raise ValueError("El ID no puede estar vacio") #raise es una variable aprendida, dispira excepciones manualmente cuando yo detecto el error, contrario a try except, que lo detecta el sistema
        self.__ID_funcionario= valor

    @property                   #getter de python
    def Usuario(self):
        return self.__Usuario
    
    @Usuario.setter      #setter de python
    def Usuario(self, valor):
        if not valor: 
            raise ValueError("El codigo usuario no puede estar vacio")
        self.__Usuario= valor

    @property                   #getter de python
    def Nombre_Completo(self):
        return self.__Nombre_Completo
    
    @Nombre_Completo.setter      #setter de python
    def Nombre_Completo(self, valor):
        if not valor: 
            raise ValueError("El nombre no puede estar vacio")
        self.__Nombre_Completo=valor

    @property                   #getter de python
    def Estado(self):
        return self.__Estado
    
    @Estado.setter      #setter de python
    def Estado(self, valor):
        self.__Estado= valor       

#============================================================= Metodos ===================================================================

    @classmethod
    def creacion_Cuenta(cls): #usado en el inicio de Sesion, cls es self o se hace referencia a si mismo
        print(("="*60), "\nCreacion de una nueva cuenta para funcionarios.\nAsegurese de digitar correctamente los datos solicitados para evitar rehacer el proceso.\n")
        comprobacion = True
        while(comprobacion):
            try:                                                         #se ingresaan posibles fallos y se hacen validaciones basicas, otras validaciones estan dentro de las clases
                id_funcionario = input("\nDigite el ID que va a tener el nuevo funcionario: ")
                for f in cls.funcionarios:
                    if (id_funcionario==f.ID_funcionario):    
                        print("El ID ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                        time.sleep(2)
                        comprobacion=False
                        return        
                user= input("Digite el codigo usuario que va a tener el nuevo funcionario: ")
                for f in cls.funcionarios:
                    if (user==f.Usuario):    
                        print("El usuario ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                        time.sleep(2)
                        comprobacion=False
                        return
                nombre_completo= input("Digite el nombre completo que va a tener el nuevo funcionario: ")
                estado = True #si es un nuevo usuario, va a estar activo si o si
                time.sleep(2)
                cls.funcionarios.append(cls(id_funcionario,user,nombre_completo,estado)) #si todo aparenta estar bien, se permite pasar adelante

                time.sleep(1)
                print(f"El nuevo usuario {user} fue registrado existosamente.") #se avisa que el registro fue bueno
                time.sleep(2)
                comprobacion=False

            except UnboundLocalError as ule: #try catch por si se encuentra valores no esperados y no se caiga
                print(f"El funcionario no puede ser accesado: {ule}")        
            except ValueError as ve:
                print(f"Los digitos colocados no corresponden a un ID valido. Solo digite formatos aceptados: {ve}")
            except Exception as e:
                print(f"ERROR: {e}")

    @classmethod
    def mostrar_Funcionarios (cls): #metodo de clase
        print ("Funcionarios actuales:\n")
        print(f"{'ID':<15} {'Nombre':<30} {'Usuario':<20}") #en  python, para formatear podemos usar la variable + :<cantidad de espacio
        print("-"*80)
        
        for fun in cls.funcionarios:
            if (fun.Estado):
                print(f"{fun.ID_funcionario:<15} {fun.Nombre_Completo:<30} {fun.Usuario:<20}") #se mantiene el formato y se concatena

    @classmethod
    def editar_Funcionarios(cls): #editar funcionario tiene varias comprobaciones
        cls.lp() #limpieza de pantalla
        print(("="*60), "\nEditar informacion de funcionario\n") 
        cls.mostrar_Funcionarios()#se llama a mostrar funcionarios para tenerlos en cuenta
        usuario_Seleccionado= input("Digite el ID correspondiente al funcionario que desea modificar: ") 
        encontrado = False #bandera
        for fun in cls.funcionarios:
            if(usuario_Seleccionado==fun.ID_funcionario): #si ya existe ese ID, se procede a edtiar, sino, se sale del bucle y se avisa que no se encontro
                encontrado = True #lo encontro? ahora es true
                comprobacion= True
                while(comprobacion): #la unica forma de salirse es digitar bien los datos, en caso de que agregue datos vacios (todos son String aca)
                    try:                          # para evitar que se caiga, se agrega un try except
                        if(fun.Estado == False): #pero si el estado esta inactivo, no se puede usar
                            time.sleep(1)
                            print("El usuario seleccionado esta inactivo. Ingrese con un usuario activo o cree uno nuevo. ")
                            time.sleep(2)
                            return
                    
                        print("Usuario encontrado. Se procedera a editarlo")
                        time.sleep(2)
                        cls.lp() #se limpia la pantalla de nuevo

                        #Edicion de funcionario
                        nombre_Comprobacion="" #variable de uso dependiendo de lo que pasa
                        print(f"Nombre actual del funcionario: {fun.Nombre_Completo} \n")
                        nuevo_Nombre = input("Digite el nombre al que se debe actualizar. Si no desea actualizarlo, digite 'mantener': ")
                        if(nuevo_Nombre=="mantener"): #si quiere mantener, entonces se mantiene y asigna la variable
                            print("El nombre se va a mantener.")
                            nombre_Comprobacion = fun.Nombre_Completo
                        else:
                            print(f"Nombre actualizado correctamente a: {nuevo_Nombre}") #sino, se le cambia al nuevo en caso que no digite mantener
                            nombre_Comprobacion= nuevo_Nombre

                        usuario_Comprobacion= "" #misma logica para usuario y ID
                        print(f"Usuario actual del funcionario: {fun.Usuario} \n")
                        nuevo_Usuario = input("Digite el usuario que se debe actualizar. Si no desea actualizarlo, digite 'mantener': ")
                        if(nuevo_Usuario=="mantener"):
                            print("El usuario se va a mantener.")
                            usuario_Comprobacion= fun.Usuario
                        else:
                            usuario_Duplicado=False #esta bandera nos permite usar continue, que salta cuando hay un usuario o ID duplicado. Si esta duplicado, vuelve al inicio del bucle while, pero sabiendo que el ID matcheo
                            for fu in cls.funcionarios:
                                if (nuevo_Usuario==fu.Usuario):    
                                    print("El usuario ya se encuentra actualmente ocupado. Intente de nuevo.\n") #igualmente si el nuevo usuario ya existe, se manda error
                                    time.sleep(1)
                                    usuario_Duplicado=True
                                    break
                            if (usuario_Duplicado):
                                continue
                            print(f"Usuario actualizado correctamente a: {nuevo_Usuario}")
                            usuario_Comprobacion= nuevo_Usuario
                        
                        ID_Comprobacion=""
                        print(f"ID actual del funcionario: {fun.ID_funcionario} \n")
                        nuevo_ID = input("Digite el ID que se debe actualizar. Si no desea actualizarlo, digite mantener: ") 
                        if(nuevo_ID=="mantener"):
                            print("El ID se va a mantener.")
                            ID_Comprobacion= fun.ID_funcionario
                        else:
                            ID_Duplicado= False
                            for fu in cls.funcionarios: #aca igual, no pueden existir dos ID iguales
                                if (nuevo_ID==fu.ID_funcionario):    
                                    print("El ID ya se encuentra actualmente ocupado. Intente de nuevo.\n") 
                                    time.sleep(1)
                                    ID_Duplicado=True
                                    break   
                            if(ID_Duplicado):
                                continue
                            print(f"ID actualizado correctamente a: {nuevo_ID}")
                            ID_Comprobacion= nuevo_ID
                        time.sleep(1)
                        print("El usuario seleccionado ahora se a actualizado con los siguientes datos:") #queremos que el usuario vea los datos nuevos, se concatena la comprobacion antes de aceptarla para asegurar que los datos sean correctos y evitar errores del usuario
                        print(f"Nombre: {nombre_Comprobacion} | Usuario: {usuario_Comprobacion} | ID: {ID_Comprobacion}")
                        
                        #Aceptas los datos que has colocado?
                        opcion_Aceptar=True
                        while(opcion_Aceptar):
                            aceptar = input("Esta seguro que desea continuar?\n1)Si\n2)No\n") #Menu de confirmacion, se asignan solo y solo si se acepta
                            if(aceptar=="1"):
                                if(fun.Usuario==cls.usuario_Actual): #si el usuario actual es el que se edita, el usuario actual se sale.
                                    cls.usuario_Actual= None
                                    print("El usuario actual ha sido actualizado. Debe ingresar al sistema de nuevo.\n")
                                    time.sleep(1)
                                fun.Nombre_Completo = nombre_Comprobacion
                                fun.Usuario = usuario_Comprobacion
                                fun.ID_funcionario= ID_Comprobacion
                                time.sleep(1)
                                print("El proceso ha sido exitoso.")
                                time.sleep(2)
                                opcion_Aceptar=False #se cierra el menu
                                return
                            elif(aceptar=="2"):
                                print(f"El cambio se ha cancelado. Los datos del funcionario {fun.Usuario} no han sido actualizados")#Se cancela el cambio 
                                time.sleep(2)
                                opcion_Aceptar=False #se cierra el menu
                                return
                            else:
                                print("La opcion digitada no corresponde a las opciones del menu. Los cambios no han sido realizados. Intentelo de nuevo.") #se entra al bucle a menos que elija las opciones correctas
                        time.sleep(2)
                        comprobacion=False
                    except UnboundLocalError as ule: #la validacion dentro de los parametros de clase hacia que se cayera el sistema, entonces, se agrearon el while principal con try catch
                        print(f"El funcionario no puede ser accesado: {ule}")        
                    except ValueError as ve:
                        print(f"Los digitos colocados no corresponden a un formato valido. Solo digite formatos aceptados: {ve}")
                    except Exception as e:
                        print(f"Error inesperado: {e}")
        if not encontrado:
            time.sleep(1)
            print("No se ha encontrado el funcionario con el ID que ha colocado. Intente de nuevo.")
            time.sleep(2)

        
    @classmethod
    def eliminar_Usuario(cls):
        cls.lp()
        print(("="*60), "\nEliminar funcionario de base de datos\n")
        cls.mostrar_Funcionarios()
        usuario_Seleccionado= input("Digite el ID correspondiente al funcionario que desea eliminar: ")
        for fun in cls.funcionarios: #si no lo encuentra, se manda error
            if(usuario_Seleccionado==fun.ID_funcionario):#si lo encuentra, se pone false a activo. Queda en memoria, pero no se muestra
                if(fun.Estado == False): #pero si el estado esta inactivo, no se puede usar
                    time.sleep(1)
                    print("El usuario seleccionado esta inactivo. Ingrese con un usuario activo o cree uno nuevo. ")
                    time.sleep(2)
                    return
                
                opcion_Aceptar=True
                while(opcion_Aceptar):
                    aceptar = input("\nFuncionario encontrado. Esta seguro que desea continuar?\n1)Si\n2)No\n")
                    if(aceptar=="1"):
                        if(fun.Usuario==cls.usuario_Actual):
                            cls.usuario_Actual= None
                        fun.Estado=False
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
                return        #si se encuentra la persona, se debe salir del bucle
            
    #============================ metodos para XML ====================================

    @classmethod
    def guardar_Funcionarios_xml(cls,ruta): #cuando se pasa al menu principal, se pone el nombre del archivo que tendremos
        try:
            raiz = ET.Element("funcionarios")#nombre principal de la clase, crea nodo raiz(root), es el nodo padre que va a contentener
            for f in cls.funcionarios: 
                nodo = ET.SubElement(raiz, "funcionario", id=str(f.ID_funcionario)) #funcionario individual, no de la clase. #ET lo estamos importando en la parte superior. Funcionarios->funcionario->usuario,nombre,estado
                ET.SubElement(nodo, "usuario").text = str(f.Usuario) #subelementos del nodo
                ET.SubElement(nodo, "nombre_completo").text = str(f.Nombre_Completo)
                ET.SubElement(nodo, "estado").text = str(f.Estado)

            arbol = ET.ElementTree(raiz)  #que haga un arbol
            arbol.write(ruta, encoding="utf-8", xml_declaration=True) #hace la magia en python
            print("Funcionarios guardados correctamente.")
        except Exception as e:
            print(f"Error inesperado al guardar los funcionarios: {e}")

    @classmethod
    def cargar_Funcionarios_xml(cls,ruta): #ruta igual se define en el main cuando se llama, para el xml. El ejemplo del profe cargar y mostrar son diferentes, para nosotros, no.
        try:     #se cargan los datos y se guardan acorde
            arbol = ET.parse(ruta) #lee xml y construye en memoria el arbol, con jerarquia de nodos e hijos
            raiz = arbol.getroot() #para mostrar, agarra la raiz de este arbol, el nodo padre principal. Parse abre el libro, getroot inicia al inicio

            for f in raiz.findall("funcionario"): #recorremos los datos del xml, los vamos acomodando segun las partes del objeto definidas, findall para que no quede nada sin lectura desde el nodo funcionario
                id_funcionario=f.get("id") #OJO hay que fijarse en el nombre que pusimos cuando guardamos, porque si no no lo lee bien. Es nodo, el ID identificador o llave primaria
                usuario = f.find("usuario").text
                nombre=f.find("nombre_completo").text
                estado=f.find("estado").text =="True" #de string de estado a un booleano dentro de la logica del programa
                cls.funcionarios.append(cls(id_funcionario,usuario,nombre,estado))
            print("Funcionarios cargados correctamente. ")
        except FileNotFoundError:
            print("Archivo de funcionarios no encontrado. Se iniciara con lista vacia.")
        except ET.ParseError:
            print("ERROR: El archivo XML de funcionarios esta mal formado.")
        except Exception as e:
            print(f"Error inesperado al cargar funcionarios: {e}") #los exception agarran cualquier error que encontremos
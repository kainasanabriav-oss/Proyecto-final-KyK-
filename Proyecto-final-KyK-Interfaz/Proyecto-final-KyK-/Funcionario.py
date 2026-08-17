
class Funcionario:
    usuario_Actual = None ##esto se usa para cosas como impedir que una persona elimine su propio funcionario mientras tiene la sesión abierta

    def __init__(self, ID_funcionario, Usuario, Nombre_Completo, Contrasena, Estado=True): #ahora las clases solamente van a tener constructores+setter,getter, sin metodos de clase
        self.ID_funcionario = ID_funcionario
        self.Usuario = Usuario
        self.Nombre_Completo = Nombre_Completo
        self.Contrasena = Contrasena
        self.Estado = Estado

    @property
    def ID_funcionario(self):
        return self.__ID_funcionario

    @ID_funcionario.setter
    def ID_funcionario(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El ID del funcionario no puede estar vacío.")
        self.__ID_funcionario = valor

    @property
    def Usuario(self):
        return self.__Usuario

    @Usuario.setter
    def Usuario(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El usuario no puede estar vacío.")
        self.__Usuario = valor

    @property
    def Nombre_Completo(self):
        return self.__Nombre_Completo

    @Nombre_Completo.setter
    def Nombre_Completo(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self.__Nombre_Completo = valor

    @property
    def Estado(self):
        return self.__Estado

    @Estado.setter
    def Estado(self, valor):
        self.__Estado = bool(valor)

    @property
    def Contrasena(self):
        return self.__Contrasena

    @Contrasena.setter
    def Contrasena (self,valor):
        if not valor:
            raise ValueError("La contraseña no puede estar vacía.")
        self.__Contrasena= valor
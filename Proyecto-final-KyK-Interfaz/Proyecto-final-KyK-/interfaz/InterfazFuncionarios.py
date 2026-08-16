import tkinter as tk
from tkinter import ttk, messagebox
from Funcionario import Funcionario
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, pasos, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS
import odbc_conexion as conexion



class InterfazFuncionarios:
    def __init__(self, master, conn): #conn viene de sql
        self.conn = conn
        self.ventana = tk.Toplevel(master)
        configurar_estilos(); preparar_ventana(self.ventana, "Funcionarios", 1020, 640) #configuraciones de la ventana segun el estilo
        self.seleccionado = None
        self.funcionarios_cache = {}# en lugar de volver a consultar, vamos a guardar lo que ya se trajo en memoria interna.
        self.crear_interfaz(); self.cargar_tabla()

    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo=tk.Frame(self.ventana,bg=COLOR_FONDO); cuerpo.pack(fill="both",expand=True)
        tarjeta=tk.Frame(cuerpo,bg=COLOR_BLANCO,highlightbackground=COLOR_BORDE,highlightthickness=1)
        tarjeta.pack(fill="both",expand=True,padx=28,pady=22)
        interior=tk.Frame(tarjeta,bg=COLOR_BLANCO,padx=25,pady=16); interior.pack(fill="both",expand=True)
        pasos(interior,["Información","Acceso","Estado","Resumen"],1)
        tk.Label(interior,text="Mantenimiento de Funcionarios",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",18,"bold")).pack(pady=(0,12))
        tk.Label(interior,text="Los funcionarios inactivos no pueden ingresar al sistema.",bg=COLOR_BLANCO,fg=COLOR_GRIS,font=("Segoe UI",9)).pack(pady=(0,10))
        form=tk.Frame(interior,bg=COLOR_BLANCO); form.pack(fill="x")
        campos=["ID funcionario","Nombre completo","Usuario","Contraseña"]
        self.entradas={}
        for i,campo in enumerate(campos):
            fila,col=divmod(i,2)
            tk.Label(form,text=campo+":",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).grid(row=fila,column=col*2,padx=(0,8),pady=7,sticky="w")
            e=ttk.Entry(form,width=31,show="*" if campo=="Contraseña" else ""); e.grid(row=fila,column=col*2+1,padx=(0,18),pady=7,sticky="ew"); self.entradas[campo]=e
        tk.Label(form,text="Estado:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).grid(row=2,column=0,padx=(0,8),pady=7,sticky="w")
        self.cbo_estado=ttk.Combobox(form,values=["Activo","Inactivo"],state="readonly",width=28); self.cbo_estado.grid(row=2,column=1,padx=(0,18),pady=7,sticky="ew"); self.cbo_estado.set("Activo")
        form.columnconfigure(1,weight=1); form.columnconfigure(3,weight=1)
        acciones=tk.Frame(interior,bg=COLOR_BLANCO); acciones.pack(fill="x",pady=10)
        ttk.Button(acciones,text="Nuevo / Limpiar",command=self.limpiar).pack(side="left")
        ttk.Button(acciones,text="Guardar",command=self.guardar,style="Menta.TButton").pack(side="left",padx=7)
        ttk.Button(acciones,text="Modificar",command=self.modificar).pack(side="left")
        ttk.Button(acciones,text="Eliminar",command=self.eliminar,style="Peligro.TButton").pack(side="left",padx=7)
        ttk.Button(acciones,text="Cerrar",command=self.ventana.destroy).pack(side="right")
        tk.Label(interior,text="Funcionarios registrados",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(4,5))
        cols=("id","nombre","correo","estado"); self.tabla=ttk.Treeview(interior,columns=cols,show="headings",height=9)
        for c,t,w in [("id","ID",100),("nombre","Nombre completo",240),("correo","Usuario",260),("estado","Estado",100)]: self.tabla.heading(c,text=t); self.tabla.column(c,width=w)
        self.tabla.pack(fill="both",expand=True); self.tabla.bind("<<TreeviewSelect>>",self.seleccionar)

    #aca la parte de logica: 
    def cargar_tabla(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        self.funcionarios_cache = {}
        for id_f, usuario, nombre, estado, clave in conexion.listar_funcionarios(self.conn): #llama a conexion de odbc, la opcion de listar que construimos alli
            self.funcionarios_cache[id_f] = (id_f, usuario, nombre, estado, clave) #el que esta en el cache o usandose ahorita
            self.tabla.insert("", "end", values=(id_f, nombre, usuario, "Activo" if estado else "Inactivo")) #activo o no segun booleano

    def seleccionar(self, _=None):
        sel = self.tabla.selection() #el que se seleccione, va a mostrar/generar los datos.
        if not sel:
            return
        ident = str(self.tabla.item(sel[0], "values")[0])
        fila = self.funcionarios_cache.get(ident)
        if not fila:
            return
        self.seleccionado = ident
        id_f, usuario, nombre, estado, clave = fila
        for e, v in zip(self.entradas.values(), [id_f, nombre, usuario, clave]):
            e.delete(0, "end")
            e.insert(0, v)
        self.cbo_estado.set("Activo" if estado else "Inactivo")

    def limpiar(self):
        self.seleccionado = None
        for e in self.entradas.values():
            e.delete(0, "end")
        self.cbo_estado.set("Activo") #limpia la pantalla cuando se necesite

    def _datos(self):
        vals = [e.get().strip() for e in self.entradas.values()]
        if not all(vals):
            raise ValueError("Complete todos los campos.")
        ident, nombre, usuario, clave = vals
        return {
            "id_funcionario": ident,
            "usuario": usuario,
            "nombre_completo": nombre,
            "estado": self.cbo_estado.get() == "Activo",
            "contrasena": clave,
        }

    def guardar(self):
        try:
            data = self._datos() #llama a datos guardados en esta clase
            if data["id_funcionario"] in self.funcionarios_cache: #agarra los funcionarios dentro del cache
                raise ValueError("Ya existe ese ID de funcionario.")
            if conexion.obtener_funcionario_por_usuario(self.conn, data["usuario"]): #no puede tener mismo usuario/id
                raise ValueError("Ya existe ese usuario.")
            conexion.crear_funcionario(self.conn, data)
            self.cargar_tabla(); self.limpiar()
            messagebox.showinfo("Guardado", "Funcionario registrado.")
        except Exception as e:
            messagebox.showerror("No se pudo guardar", str(e))

    def modificar(self): #no permitimos el cambio de id ya que ahora esta ligado con sql
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un funcionario."); return
        try:
            data = self._datos()
            if data["id_funcionario"] != self.seleccionado:
                raise ValueError("El ID de funcionario no se puede modificar.")
            otro = conexion.obtener_funcionario_por_usuario(self.conn, data["usuario"])
            if otro and otro[0] != self.seleccionado:
                raise ValueError("Ese usuario ya está ocupado.") #comprobacion
            conexion.actualizar_funcionario(self.conn, self.seleccionado, data)
            self.cargar_tabla()
            messagebox.showinfo("Modificado", "Funcionario actualizado.")
        except Exception as e:
            messagebox.showerror("No se pudo modificar", str(e))

    def eliminar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un funcionario."); return #debe seleccionar uno para borrar
        actual = Funcionario.usuario_Actual
        if actual and self.seleccionado == actual.ID_funcionario: #el que tiene la sesion abierta no puede eliminarse
            messagebox.showwarning("No permitido", "No puede eliminar el funcionario con la sesión abierta."); return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar el funcionario seleccionado?"):
            conexion.eliminar_funcionario(self.conn, self.seleccionado) #se acciona el eliminar que hicimos en odbc pasandole el que se selecciono
            self.cargar_tabla(); self.limpiar()
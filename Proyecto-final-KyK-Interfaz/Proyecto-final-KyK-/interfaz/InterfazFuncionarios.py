import tkinter as tk
from tkinter import ttk, messagebox
from Funcionario import Funcionario
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, pasos, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS

class InterfazFuncionarios:
    def __init__(self, master, guardar_cambios):
        self.guardar_cambios=guardar_cambios; self.ventana=tk.Toplevel(master)
        configurar_estilos(); preparar_ventana(self.ventana,"Funcionarios",1020,640)
        self.seleccionado=None; self.crear_interfaz(); self.cargar_tabla()

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

    def cargar_tabla(self):
        for x in self.tabla.get_children(): self.tabla.delete(x)
        for f in Funcionario.funcionarios: self.tabla.insert("","end",values=(f.ID_funcionario,f.Nombre_Completo,f.Usuario,"Activo" if f.Estado else "Inactivo"))
    def seleccionar(self,_=None):
        sel=self.tabla.selection()
        if not sel:return
        ident=str(self.tabla.item(sel[0],"values")[0]); self.seleccionado=next((f for f in Funcionario.funcionarios if f.ID_funcionario==ident),None)
        if not self.seleccionado:return
        vals=[self.seleccionado.ID_funcionario,self.seleccionado.Nombre_Completo,self.seleccionado.Usuario,self.seleccionado.Contrasena]
        for e,v in zip(self.entradas.values(),vals): e.delete(0,"end"); e.insert(0,v)
        self.cbo_estado.set("Activo" if self.seleccionado.Estado else "Inactivo")
    def limpiar(self):
        self.seleccionado=None
        for e in self.entradas.values(): e.delete(0,"end")
        self.cbo_estado.set("Activo")
    def _datos(self):
        vals=[e.get().strip() for e in self.entradas.values()]
        if not all(vals): raise ValueError("Complete todos los campos.")
        return vals+[self.cbo_estado.get()=="Activo"]
    def guardar(self):
        try:
            ident,nombre,correo,clave,estado=self._datos()
            if any(f.ID_funcionario==ident for f in Funcionario.funcionarios): raise ValueError("Ya existe ese ID de funcionario.")
            if Funcionario.buscar_por_usuario(correo): raise ValueError("Ya existe ese usuario.")
            Funcionario.funcionarios.append(Funcionario(ident,correo,nombre,estado,clave)); self.guardar_cambios(); self.cargar_tabla(); self.limpiar(); messagebox.showinfo("Guardado","Funcionario registrado.")
        except Exception as e: messagebox.showerror("No se pudo guardar",str(e))
    def modificar(self):
        if not self.seleccionado: messagebox.showwarning("Seleccione","Seleccione un funcionario."); return
        try:
            ident,nombre,correo,clave,estado=self._datos()
            if any(f.ID_funcionario==ident and f is not self.seleccionado for f in Funcionario.funcionarios): raise ValueError("Ese ID ya está ocupado.")
            if any(f.Usuario.lower()==correo.lower() and f is not self.seleccionado for f in Funcionario.funcionarios): raise ValueError("Ese usuario ya está ocupado.")
            self.seleccionado.ID_funcionario=ident; self.seleccionado.Nombre_Completo=nombre; self.seleccionado.Usuario=correo; self.seleccionado.Contrasena=clave; self.seleccionado.Estado=estado
            self.guardar_cambios(); self.cargar_tabla(); messagebox.showinfo("Modificado","Funcionario actualizado.")
        except Exception as e: messagebox.showerror("No se pudo modificar",str(e))
    def eliminar(self):
        if not self.seleccionado: messagebox.showwarning("Seleccione","Seleccione un funcionario."); return
        if self.seleccionado is Funcionario.usuario_Actual: messagebox.showwarning("No permitido","No puede eliminar el funcionario con la sesión abierta."); return
        if messagebox.askyesno("Confirmar","¿Desea eliminar el funcionario seleccionado?"):
            Funcionario.funcionarios.remove(self.seleccionado); self.guardar_cambios(); self.cargar_tabla(); self.limpiar()

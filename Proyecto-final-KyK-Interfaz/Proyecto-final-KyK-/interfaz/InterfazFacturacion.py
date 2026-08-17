import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from Encargado import Encargado
from ServiciosDisponibles import ServiciosDisponibles
from ServicioBrindado import ServicioBrindado
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, pasos, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS


class InterfazFacturacion:
    def __init__(self,master,funcionario,guardar_cambios):
        self.funcionario=funcionario; self.guardar_cambios=guardar_cambios
        self.ventana=tk.Toplevel(master); configurar_estilos(); preparar_ventana(self.ventana,"Atención / Facturación",1020,640)
        self.servicios_agregados=[]; self.crear_interfaz(); self.cargar_datos()

    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo=tk.Frame(self.ventana,bg=COLOR_FONDO); cuerpo.pack(fill="both",expand=True)
        tarjeta=tk.Frame(cuerpo,bg=COLOR_BLANCO,highlightbackground=COLOR_BORDE,highlightthickness=1)
        tarjeta.pack(fill="both",expand=True,padx=28,pady=22)
        interior=tk.Frame(tarjeta,bg=COLOR_BLANCO,padx=25,pady=16); interior.pack(fill="both",expand=True)

        pasos(interior,["Datos de la Atención","Servicios","Resumen","Confirmación"],1)
        tk.Label(interior,text="Nueva Atención / Facturación",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",18,"bold")).pack(pady=(0,12))

        datos=tk.Frame(interior,bg=COLOR_BLANCO); datos.pack(fill="x",pady=(0,10))
        tk.Label(datos,text="Fecha:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).grid(row=0,column=0,padx=(0,6),pady=6,sticky="w")
        # Campo visual para la fecha, sin cambiar la lógica existente.
        self.txt_fecha=ttk.Entry(datos,width=16); self.txt_fecha.grid(row=0,column=1,padx=(0,15),pady=6); self.txt_fecha.insert(0,str(date.today())); self.txt_fecha.config(state="readonly")
        tk.Label(datos,text="Consecutivo:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).grid(row=0,column=2,padx=(0,6),pady=6,sticky="w")
        self.lbl_consecutivo=ttk.Label(datos,text="Automático",style="SubtituloCard.TLabel"); self.lbl_consecutivo.grid(row=0,column=3,padx=(0,15),pady=6,sticky="w")
        tk.Label(datos,text="Niño:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).grid(row=0,column=4,padx=(0,6),pady=6,sticky="w")
        self.cbo_nino=ttk.Combobox(datos,state="readonly",width=31); self.cbo_nino.grid(row=0,column=5,pady=6,sticky="ew")
        datos.columnconfigure(5,weight=1)

        servicio_fila=tk.Frame(interior,bg=COLOR_BLANCO); servicio_fila.pack(fill="x",pady=(0,8))
        tk.Label(servicio_fila,text="Servicio:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).pack(side="left")
        self.cbo_servicio=ttk.Combobox(servicio_fila,state="readonly",width=42); self.cbo_servicio.pack(side="left",padx=8)
        ttk.Button(servicio_fila,text="+ Agregar Servicio",command=self.agregar,style="Menta.TButton").pack(side="left")
        ttk.Button(servicio_fila,text="Quitar",command=self.quitar,style="Peligro.TButton").pack(side="left",padx=7)

        tk.Label(interior,text="Servicios seleccionados",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(4,5))
        cols=("codigo","servicio","siniva","iva","total")
        self.tabla=ttk.Treeview(interior,columns=cols,show="headings",height=9)
        for c,t,w in [("codigo","Código",90),("servicio","Descripción",250),("siniva","Costo",125),("iva","IVA (2%)",105),("total","Total",125)]:
            self.tabla.heading(c,text=t); self.tabla.column(c,width=w)
        self.tabla.pack(fill="both",expand=True)

        resumen=tk.Frame(interior,bg=COLOR_AZUL_CLARO,highlightbackground=COLOR_BORDE,highlightthickness=1,padx=15,pady=10)
        resumen.pack(fill="x",pady=10)
        tk.Label(resumen,text="Total a Pagar:",bg=COLOR_AZUL_CLARO,fg=COLOR_AZUL,font=("Segoe UI",10,"bold")).pack(side="left")
        self.lbl_total=tk.Label(resumen,text="₡0.00",bg=COLOR_AZUL_CLARO,fg=COLOR_MENTA,font=("Segoe UI",16,"bold")); self.lbl_total.pack(side="right")

        pie=tk.Frame(interior,bg=COLOR_BLANCO); pie.pack(fill="x")
        ttk.Button(pie,text="Cancelar / Limpiar",command=self.limpiar).pack(side="left")
        ttk.Button(pie,text="Guardar y Facturar",command=self.guardar,style="Principal.TButton").pack(side="right")
        ttk.Button(pie,text="Cerrar",command=self.ventana.destroy).pack(side="right",padx=8)

    def cargar_datos(self):
        self.ninos={f"{m.ID_menorEdad} - {m.nombre_completo} ({m.calculo_Edad_Menor()} años)":m for _,m in Encargado.todos_los_menores()}; self.cbo_nino["values"]=list(self.ninos.keys())
        self.servicios={f"{s.ID_Servicio} - {s.Nombre_Servicio}":s for s in ServiciosDisponibles.servicios}; self.cbo_servicio["values"]=list(self.servicios.keys())

    def agregar(self):
        s=self.servicios.get(self.cbo_servicio.get())
        if not s: messagebox.showwarning("Servicio","Seleccione un servicio."); return
        self.servicios_agregados.append(s); self.refrescar()

    def quitar(self):
        sel=self.tabla.selection()
        if not sel:return
        idx=self.tabla.index(sel[0]); self.servicios_agregados.pop(idx); self.refrescar()

    #Esto sirve principalmente para actualizar visualmente la tabla y el total mientras el usuario agrega servicios
    def refrescar(self):
        for x in self.tabla.get_children(): self.tabla.delete(x)
        total=0
        for s in self.servicios_agregados:
            iva=s.Costo*.02; total+=s.Costo+iva; self.tabla.insert("","end",values=(s.ID_Servicio,s.Nombre_Servicio,f"₡{s.Costo:,.2f}",f"₡{iva:,.2f}",f"₡{s.Costo+iva:,.2f}"))
        self.lbl_total.config(text=f"₡{total:,.2f}")

    def limpiar(self):
        self.cbo_nino.set(""); self.cbo_servicio.set(""); self.servicios_agregados.clear(); self.refrescar()
    #Creacion de factura
    def guardar(self):
        menor=self.ninos.get(self.cbo_nino.get())#verifica que haya niño
        if not menor: messagebox.showwarning("Niño","Seleccione un niño."); return
        if not self.servicios_agregados: messagebox.showwarning("Servicios","Agregue al menos un servicio."); return
        fac=ServicioBrindado(menor,self.funcionario,date.today())
        for s in self.servicios_agregados: fac.agregar_Servicio(s)
        ServicioBrindado.facturas.append(fac); self.guardar_cambios(); messagebox.showinfo("Atención guardada",f"Factura/consecutivo #{fac.ID_cita} guardado como Pendiente.\nTotal: ₡{fac.calcular_Total():,.2f}"); self.limpiar()

import tkinter as tk
from tkinter import ttk, messagebox
from ServicioBrindado import ServicioBrindado
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS

class InterfazConsultaFacturas:
    def __init__(self,master,guardar_cambios):
        self.guardar_cambios=guardar_cambios; self.ventana=tk.Toplevel(master); configurar_estilos(); preparar_ventana(self.ventana,"Consulta de Facturas",1020,640); self.factura=None; self.crear_interfaz(); self.cargar_tabla()
    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo=tk.Frame(self.ventana,bg=COLOR_FONDO); cuerpo.pack(fill="both",expand=True)
        tarjeta=tk.Frame(cuerpo,bg=COLOR_BLANCO,highlightbackground=COLOR_BORDE,highlightthickness=1); tarjeta.pack(fill="both",expand=True,padx=28,pady=22)
        interior=tk.Frame(tarjeta,bg=COLOR_BLANCO,padx=25,pady=16); interior.pack(fill="both",expand=True)
        tk.Label(interior,text="Consulta y Pago de Factura",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",18,"bold")).pack(anchor="w")
        tk.Label(interior,text="Seleccione una factura para ver sus servicios y registrar el pago.",bg=COLOR_BLANCO,fg=COLOR_GRIS,font=("Segoe UI",9)).pack(anchor="w",pady=(3,12))
        b=tk.Frame(interior,bg=COLOR_BLANCO); b.pack(fill="x",pady=(0,10))
        tk.Label(b,text="Buscar factura:",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",9,"bold")).pack(side="left")
        self.txt_buscar=ttk.Entry(b,width=34); self.txt_buscar.pack(side="left",padx=8)
        ttk.Button(b,text="Buscar",command=self.cargar_tabla,style="Principal.TButton").pack(side="left")
        ttk.Button(b,text="Mostrar todas",command=self.todos).pack(side="left",padx=7)
        cols=("consecutivo","fecha","nino","edad","total","estado"); self.tabla=ttk.Treeview(interior,columns=cols,show="headings",height=8)
        for c,t,w in [("consecutivo","Consecutivo",100),("fecha","Fecha",100),("nino","Niño",220),("edad","Edad",65),("total","Total",125),("estado","Estado",95)]: self.tabla.heading(c,text=t); self.tabla.column(c,width=w)
        self.tabla.pack(fill="x",pady=(0,10)); self.tabla.bind("<<TreeviewSelect>>",self.seleccionar)
        detalle=tk.Frame(interior,bg=COLOR_BLANCO,highlightbackground=COLOR_BORDE,highlightthickness=1); detalle.pack(fill="both",expand=True)
        tk.Label(detalle,text="Detalle de la factura seleccionada",bg=COLOR_BLANCO,fg=COLOR_AZUL,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=12,pady=(10,4))
        self.txt_detalle=tk.Text(detalle,height=8,font=("Consolas",10),state="disabled",bd=0,bg=COLOR_BLANCO,fg=COLOR_AZUL); self.txt_detalle.pack(fill="both",expand=True,padx=12,pady=(0,8))
        pie=tk.Frame(interior,bg=COLOR_BLANCO); pie.pack(fill="x",pady=(10,0))
        self.lbl_estado=tk.Label(pie,text="Seleccione una factura",bg=COLOR_BLANCO,fg=COLOR_MENTA,font=("Segoe UI",10,"bold")); self.lbl_estado.pack(side="left")
        ttk.Button(pie,text="Registrar Pago",command=self.pagar,style="Menta.TButton").pack(side="right")
        ttk.Button(pie,text="Cerrar",command=self.ventana.destroy).pack(side="right",padx=8)
    def todos(self): self.txt_buscar.delete(0,"end"); self.cargar_tabla()
    def cargar_tabla(self):
        for x in self.tabla.get_children(): self.tabla.delete(x)
        q=self.txt_buscar.get().strip().lower()
        for f in ServicioBrindado.facturas:
            if q and q not in str(f.ID_cita).lower() and q not in f.Menor.nombre_completo.lower() and q not in str(f.Menor.ID_menorEdad).lower(): continue
            self.tabla.insert("","end",values=(f.ID_cita,f.Fecha_Cita,f.Menor.nombre_completo,f.Menor.calculo_Edad_Menor(),f"₡{f.calcular_Total():,.2f}","Cancelado" if f.Cancelado else "Pendiente"))
    def seleccionar(self,_=None):
        sel=self.tabla.selection()
        if not sel:return
        ident=int(self.tabla.item(sel[0],"values")[0]); self.factura=next((f for f in ServicioBrindado.facturas if f.ID_cita==ident),None)
        if not self.factura:return
        lineas=[f"Factura #{self.factura.ID_cita} - {self.factura.Fecha_Cita}",f"Niño: {self.factura.Menor.nombre_completo} - Edad: {self.factura.Menor.calculo_Edad_Menor()} años","","Servicio                         Sin IVA        IVA 2%        Total","-"*70]
        for s in self.factura.Servicios: lineas.append(f"{s.Nombre_Servicio:<30} ₡{s.Costo:>10,.2f}  ₡{s.Costo*.02:>9,.2f}  ₡{s.Costo*1.02:>10,.2f}")
        lineas += ["-"*70,f"Subtotal: ₡{self.factura.calcular_Subtotal():,.2f}",f"IVA: ₡{self.factura.calcular_IVA():,.2f}",f"TOTAL: ₡{self.factura.calcular_Total():,.2f}"]
        self.txt_detalle.config(state="normal"); self.txt_detalle.delete("1.0","end"); self.txt_detalle.insert("1.0","\n".join(lineas)); self.txt_detalle.config(state="disabled")
        self.lbl_estado.config(text=f"Estado: {'Cancelado' if self.factura.Cancelado else 'Pendiente'}")
    def pagar(self):
        if not self.factura: messagebox.showwarning("Seleccione","Seleccione una factura."); return
        if self.factura.Cancelado: messagebox.showinfo("Sin cambios","Esta factura ya está Cancelada y solo puede consultarse."); return
        if messagebox.askyesno("Confirmar pago",f"¿Registrar el pago por ₡{self.factura.calcular_Total():,.2f}?\nDespués no se permitirán cambios en la factura."):
            self.factura.Cancelado=True; self.guardar_cambios(); self.cargar_tabla(); self.lbl_estado.config(text="Estado: Cancelado"); messagebox.showinfo("Pago registrado","La factura quedó en estado Cancelado.")

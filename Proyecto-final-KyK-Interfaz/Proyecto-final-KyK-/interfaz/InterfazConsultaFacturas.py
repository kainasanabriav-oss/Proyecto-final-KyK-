import tkinter as tk
from tkinter import ttk, messagebox
import odbc_conexion as conexion
from MenorEdad import MenorEdad

from .Estilos import preparar_ventana, configurar_estilos, barra_superior, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS

class InterfazConsultaFacturas:
    def __init__(self, master, conn):
        self.conn = conn
        self.ventana = tk.Toplevel(master); configurar_estilos(); preparar_ventana(self.ventana, "Consulta de Facturas", 1020, 640)
        self.factura = None
        self.crear_interfaz(); self.cargar_tabla()

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

    def todos(self): self.txt_buscar.delete(0, "end"); self.cargar_tabla()


    def cargar_tabla(self):
        for x in self.tabla.get_children(): self.tabla.delete(x)
        q = self.txt_buscar.get().strip()
        for id_cita, fecha_cita, cancelado, id_menor, nombre, ap1, ap2, fecha_nac, sexo in conexion.listar_citas(self.conn, q):
            menor = MenorEdad(nombre, ap1, ap2, sexo, fecha_nac)
            servicios = conexion.obtener_servicios_de_cita(self.conn, id_cita)
            _, _, total = conexion.calcular_totales(servicios)
            self.tabla.insert("", "end", iid=str(id_cita), values=(
                id_cita, fecha_cita, menor.nombre_completo, menor.calculo_Edad_Menor(),
                f"₡{total:,.2f}", "Cancelado" if cancelado else "Pendiente",
            ))

    def seleccionar(self, _=None):
        sel = self.tabla.selection()
        if not sel: return
        id_cita = int(sel[0])
        fila = next((f for f in conexion.listar_citas(self.conn) if f[0] == id_cita), None)
        if not fila: return
        _, fecha_cita, cancelado, id_menor, nombre, ap1, ap2, fecha_nac, sexo = fila
        menor = MenorEdad(nombre, ap1, ap2, sexo, fecha_nac)
        servicios = conexion.obtener_servicios_de_cita(self.conn, id_cita)
        subtotal, iva, total = conexion.calcular_totales(servicios)
        self.factura = {"id_cita": id_cita, "cancelado": cancelado}
        lineas = [f"Factura #{id_cita} - {fecha_cita}", f"Niño: {menor.nombre_completo} - Edad: {menor.calculo_Edad_Menor()} años", "",
                    "Servicio                         Sin IVA        IVA 2%        Total", "-"*70]
        for id_s, nombre_s, costo in servicios:
            lineas.append(f"{nombre_s:<30} ₡{costo:>10,.2f}  ₡{costo*.02:>9,.2f}  ₡{costo*1.02:>10,.2f}")
        lineas += ["-"*70, f"Subtotal: ₡{subtotal:,.2f}", f"IVA: ₡{iva:,.2f}", f"TOTAL: ₡{total:,.2f}"]
        self.txt_detalle.config(state="normal"); self.txt_detalle.delete("1.0", "end"); self.txt_detalle.insert("1.0", "\n".join(lineas)); self.txt_detalle.config(state="disabled")
        self.lbl_estado.config(text=f"Estado: {'Cancelado' if cancelado else 'Pendiente'}")

    def pagar(self):
        if not self.factura: messagebox.showwarning("Seleccione", "Seleccione una factura."); return
        if self.factura["cancelado"]: messagebox.showinfo("Sin cambios", "Esta factura ya está Cancelada y solo puede consultarse."); return
        servicios = conexion.obtener_servicios_de_cita(self.conn, self.factura["id_cita"])
        _, _, total = conexion.calcular_totales(servicios)
        if messagebox.askyesno("Confirmar pago", f"¿Registrar el pago por ₡{total:,.2f}?\nDespués no se permitirán cambios en la factura."):
            conexion.registrar_pago(self.conn, self.factura["id_cita"])
            self.cargar_tabla(); self.lbl_estado.config(text="Estado: Cancelado")
            messagebox.showinfo("Pago registrado", "La factura quedó en estado Cancelado.")
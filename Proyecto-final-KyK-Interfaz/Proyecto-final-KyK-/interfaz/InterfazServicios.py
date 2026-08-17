import tkinter as tk
from tkinter import ttk, messagebox
from ServiciosDisponibles import ServiciosDisponibles
import odbc_conexion as conexion
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, pasos, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS, COLOR_AZUL_CLARO


class InterfazServicios:
    def __init__(self, master, conn):
        self.conn = conn
        self.ventana = tk.Toplevel(master)
        configurar_estilos()
        preparar_ventana(self.ventana, "Servicios", 1020, 640)
        self.seleccionado = None
        self.servicios_cache = {}
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo = tk.Frame(self.ventana, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True)

        tarjeta = tk.Frame(cuerpo, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(fill="both", expand=True, padx=24, pady=18)
        interior = tk.Frame(tarjeta, bg=COLOR_BLANCO, padx=22, pady=18)
        interior.pack(fill="both", expand=True)

        pasos(interior, ["Información", "Detalles", "Confirmación"], 1)
        tk.Label(interior, text="Registro y Mantenimiento de Servicio", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(interior, text="Administra de forma más cómoda los servicios disponibles en la clínica.",
                 bg=COLOR_BLANCO, fg=COLOR_GRIS, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 14))

        form_card = tk.LabelFrame(interior, text="Datos del servicio", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                  font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        form_card.pack(fill="x", pady=(0, 12))
        form = tk.Frame(form_card, bg=COLOR_BLANCO, padx=14, pady=14)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Código del servicio:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.txt_codigo = ttk.Entry(form, width=28)
        self.txt_codigo.grid(row=0, column=1, sticky="ew", padx=(0, 18), pady=6)

        tk.Label(form, text="Nombre / descripción:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 8), pady=6)
        self.txt_nombre = ttk.Entry(form, width=34)
        self.txt_nombre.grid(row=0, column=3, sticky="ew", pady=6)

        tk.Label(form, text="Costo sin IVA:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.txt_costo = ttk.Entry(form, width=28)
        self.txt_costo.grid(row=1, column=1, sticky="ew", padx=(0, 18), pady=6)

        tk.Label(form, text="Detalle opcional:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", padx=(0, 8), pady=6)
        self.txt_desc = ttk.Entry(form, width=34)
        self.txt_desc.grid(row=1, column=3, sticky="ew", pady=6)

        info = tk.Frame(form, bg=COLOR_AZUL_CLARO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        info.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        tk.Label(info, text="El IVA médico del 2% se aplica automáticamente al momento de facturar.",
                 bg=COLOR_AZUL_CLARO, fg=COLOR_GRIS, font=("Segoe UI", 8)).pack(anchor="w", padx=10, pady=8)

        for col in (1, 3):
            form.columnconfigure(col, weight=1)

        acciones = tk.Frame(interior, bg=COLOR_BLANCO)
        acciones.pack(fill="x", pady=(0, 10))
        ttk.Button(acciones, text="Nuevo / Limpiar", command=self.limpiar).pack(side="left")
        ttk.Button(acciones, text="Guardar", command=self.guardar, style="Menta.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Modificar", command=self.modificar).pack(side="left")
        ttk.Button(acciones, text="Eliminar", command=self.eliminar, style="Peligro.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Volver al menú", command=self.ventana.destroy).pack(side="right")

        tabla_card = tk.LabelFrame(interior, text="Servicios registrados", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                   font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        tabla_card.pack(fill="both", expand=True)
        tabla_wrap = tk.Frame(tabla_card, bg=COLOR_BLANCO, padx=10, pady=10)
        tabla_wrap.pack(fill="both", expand=True)

        cols = ("codigo", "nombre", "costo", "iva", "total")
        self.tabla = ttk.Treeview(tabla_wrap, columns=cols, show="headings", height=10)
        for c, t, w in [("codigo", "Código", 110), ("nombre", "Servicio", 280), ("costo", "Costo sin IVA", 130), ("iva", "IVA 2%", 110), ("total", "Precio final", 130)]:
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=w)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_tabla(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        self.servicios_cache = {}
        for id_s, nombre, costo, desc in conexion.listar_servicios(self.conn):
            self.servicios_cache[id_s] = (id_s, nombre, costo, desc)
            iva = costo * .02
            self.tabla.insert("", "end", iid=id_s,values=(id_s, nombre, f"₡{costo:,.2f}", f"₡{iva:,.2f}", f"₡{costo+iva:,.2f}"))

    def seleccionar(self, _=None):
        sel = self.tabla.selection()
        if not sel:
            return
        fila = self.servicios_cache.get(sel[0])
        if not fila:
            return
        self.seleccionado = sel[0]
        id_s, nombre, costo, desc = fila
        for e, v in [(self.txt_codigo, id_s), (self.txt_nombre, nombre), (self.txt_costo, costo), (self.txt_desc, desc)]:
            e.delete(0, "end")
            e.insert(0, v)

    def limpiar(self):
        self.seleccionado = None
        for e in [self.txt_codigo, self.txt_nombre, self.txt_costo, self.txt_desc]:
            e.delete(0, "end")

    def _datos(self):
        return {
            "id_servicio": self.txt_codigo.get().strip(),
            "nombre_servicio": self.txt_nombre.get().strip(),
            "costo": float(self.txt_costo.get().strip()),
            "descripcion": self.txt_desc.get().strip(),
        }

    def guardar(self):
        try:
            data = self._datos()
            if conexion.obtener_servicio(self.conn, data["id_servicio"]):
                raise ValueError("Ya existe ese código de servicio.")
            conexion.crear_servicio(self.conn, data)
            self.cargar_tabla(); self.limpiar()
            messagebox.showinfo("Guardado", "Servicio registrado.")
        except Exception as e:
            messagebox.showerror("No se pudo guardar", str(e))

    def modificar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un servicio.")
            return
        try:
            data = self._datos()
            if data["id_servicio"] != self.seleccionado:
                raise ValueError("El código de servicio no se puede modificar.")
            conexion.actualizar_servicio(self.conn, self.seleccionado, data)
            self.cargar_tabla()
            messagebox.showinfo("Modificado", "Servicio actualizado.")
        except Exception as e:
            messagebox.showerror("No se pudo modificar", str(e))

    def eliminar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un servicio.")
            return
        citas = conexion.contar_citas_de_servicio(self.conn, self.seleccionado)
        if citas > 0:
            messagebox.showwarning("No permitido", f"Este servicio tiene {citas} cita(s) registrada(s) y no puede eliminarse.")
            return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar el servicio seleccionado?"):
            conexion.eliminar_servicio(self.conn, self.seleccionado)
            self.cargar_tabla(); self.limpiar()

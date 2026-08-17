import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Encargado import Encargado
from MenorEdad import MenorEdad
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, pasos, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS, COLOR_AZUL_CLARO
import odbc_conexion as conexion 

class InterfazNinos:
    def __init__(self, master, conn):
        self.conn = conn
        self.ventana = tk.Toplevel(master)
        configurar_estilos()
        preparar_ventana(self.ventana, "Niños", 1020, 640)
        self.seleccionado = None
        self.menores_cache = {}
        self.crear_interfaz()
        self.cargar_padres()
        self.cargar_tabla()

    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo = tk.Frame(self.ventana, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True)

        tarjeta = tk.Frame(cuerpo, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(fill="both", expand=True, padx=24, pady=18)

        interior = tk.Frame(tarjeta, bg=COLOR_BLANCO, padx=22, pady=18)
        interior.pack(fill="both", expand=True)

        pasos(interior, ["Información", "Padre", "Datos", "Revisión", "Resumen"], 1)
        tk.Label(interior, text="Registro y Mantenimiento de Niño", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(interior, text="Aquí puedes registrar, editar, buscar y eliminar niños de forma más ordenada.",
                 bg=COLOR_BLANCO, fg=COLOR_GRIS, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 14))

        superior = tk.Frame(interior, bg=COLOR_BLANCO)
        superior.pack(fill="x", pady=(0, 12))

        busqueda_card = tk.LabelFrame(superior, text="Búsqueda", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                      font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        busqueda_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        busq_cont = tk.Frame(busqueda_card, bg=COLOR_BLANCO, padx=12, pady=10)
        busq_cont.pack(fill="both", expand=True)
        tk.Label(busq_cont, text="Buscar niño por nombre o identificación:", bg=COLOR_BLANCO, fg=COLOR_GRIS,
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.txt_buscar = ttk.Entry(busq_cont, width=34)
        self.txt_buscar.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        bot_busq = tk.Frame(busq_cont, bg=COLOR_BLANCO)
        bot_busq.grid(row=1, column=1, padx=(10, 0))
        ttk.Button(bot_busq, text="Buscar", command=self.cargar_tabla, style="Principal.TButton").pack(side="left")
        ttk.Button(bot_busq, text="Todos", command=self.buscar_todos).pack(side="left", padx=6)
        busq_cont.columnconfigure(0, weight=1)

        edad_card = tk.LabelFrame(superior, text="Edad calculada", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                  font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        edad_card.pack(side="left", fill="y")
        edad_cont = tk.Frame(edad_card, bg=COLOR_AZUL_CLARO, padx=24, pady=20)
        edad_cont.pack(fill="both", expand=True, padx=12, pady=10)
        tk.Label(edad_cont, text="Edad actual", bg=COLOR_AZUL_CLARO, fg=COLOR_GRIS,
                 font=("Segoe UI", 9)).pack()
        self.lbl_edad = tk.Label(edad_cont, text="-- años", bg=COLOR_AZUL_CLARO, fg=COLOR_MENTA,
                                 font=("Segoe UI", 20, "bold"))
        self.lbl_edad.pack(pady=(8, 0))

        form_card = tk.LabelFrame(interior, text="Datos del niño", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                  font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        form_card.pack(fill="x", pady=(0, 12))
        form = tk.Frame(form_card, bg=COLOR_BLANCO, padx=14, pady=14)
        form.pack(fill="both", expand=True)

        self.entradas = {}
        tk.Label(form, text="Padre / encargado:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.cbo_padre = ttk.Combobox(form, state="readonly", width=34)
        self.cbo_padre.grid(row=0, column=1, sticky="ew", padx=(0, 18), pady=6)

        tk.Label(form, text="Identificación niño:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 8), pady=6)
        self.entradas["Identificación niño"] = ttk.Entry(form, width=28)
        self.entradas["Identificación niño"].grid(row=0, column=3, sticky="ew", pady=6)

        labels = [
            ("Nombre", 1, 0),
            ("Primer apellido", 1, 2),
            ("Segundo apellido", 2, 0),
            ("Fecha nacimiento (AAAA-MM-DD)", 2, 2),
        ]
        for campo, fila, col in labels:
            tk.Label(form, text=campo + ":", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=fila, column=col, sticky="w", padx=(0, 8), pady=6)
            self.entradas[campo] = ttk.Entry(form, width=28)
            self.entradas[campo].grid(row=fila, column=col+1, sticky="ew", padx=(0, 18), pady=6)

        tk.Label(form, text="Sexo:", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.cbo_sexo = ttk.Combobox(form, values=["Masculino", "Femenino", "Otro"], state="readonly", width=26)
        self.cbo_sexo.grid(row=3, column=1, sticky="ew", padx=(0, 18), pady=6)

        ayuda = tk.Frame(form, bg=COLOR_AZUL_CLARO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        ayuda.grid(row=3, column=2, columnspan=2, sticky="ew", pady=6)
        tk.Label(ayuda, text="La edad se calcula automáticamente al seleccionar o guardar.", bg=COLOR_AZUL_CLARO,
                 fg=COLOR_GRIS, font=("Segoe UI", 8)).pack(anchor="w", padx=10, pady=8)

        for col in (1, 3):
            form.columnconfigure(col, weight=1)

        acciones = tk.Frame(interior, bg=COLOR_BLANCO)
        acciones.pack(fill="x", pady=(0, 10))
        ttk.Button(acciones, text="Nuevo / Limpiar", command=self.limpiar).pack(side="left")
        ttk.Button(acciones, text="Guardar", command=self.guardar, style="Menta.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Modificar", command=self.modificar).pack(side="left")
        ttk.Button(acciones, text="Eliminar", command=self.eliminar, style="Peligro.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Volver al menú", command=self.ventana.destroy).pack(side="right")

        tabla_card = tk.LabelFrame(interior, text="Niños registrados", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                                   font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        tabla_card.pack(fill="both", expand=True)
        tabla_wrap = tk.Frame(tabla_card, bg=COLOR_BLANCO, padx=10, pady=10)
        tabla_wrap.pack(fill="both", expand=True)

        cols = ("id", "nombre", "padre", "fecha", "edad", "sexo")
        self.tabla = ttk.Treeview(tabla_wrap, columns=cols, show="headings", height=8)
        for c, t, w in [("id", "Identificación", 120), ("nombre", "Nombre completo", 220), ("padre", "Padre", 220), ("fecha", "F. nacimiento", 120), ("edad", "Edad", 70), ("sexo", "Sexo", 90)]:
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=w)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_padres(self):
        self.padre_map = {
            f"{ident} - {nombre}": id_enc
            for id_enc, nombre, ident, *_ in conexion.listar_encargados(self.conn)
        }
        self.cbo_padre["values"] = list(self.padre_map.keys())

    def buscar_todos(self):
        self.txt_buscar.delete(0, "end")
        self.cargar_tabla()

    def cargar_tabla(self):
        self.cargar_padres()
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        self.menores_cache = {}
        criterio = self.txt_buscar.get().strip()
        for fila in conexion.listar_menores(self.conn, criterio):
            id_m, nombre, ap1, ap2, sexo, fecha_nac, id_enc, nombre_enc, ident_enc = fila
            self.menores_cache[id_m] = fila
            edad = MenorEdad(nombre, ap1, ap2, sexo, fecha_nac, id_enc, id_m).calculo_Edad_Menor()
            nombre_completo = f"{nombre} {ap1} {ap2}".strip()
            self.tabla.insert("", "end", iid=str(id_m), values=(id_m, nombre_completo, nombre_enc, fecha_nac, edad, sexo))

    def seleccionar(self, _=None):
        sel = self.tabla.selection()
        if not sel:
            return
        id_m = int(sel[0])
        fila = self.menores_cache.get(id_m)
        if not fila:
            return
        _, nombre, ap1, ap2, sexo, fecha_nac, id_enc, nombre_enc, ident_enc = fila
        self.seleccionado = id_m
        clave_padre = next((k for k, v in self.padre_map.items() if v == id_enc), "")
        self.cbo_padre.set(clave_padre)
        vals = [nombre, ap1, ap2, str(fecha_nac)]
        for e, v in zip(self.entradas.values(), vals):
            e.delete(0, "end")
            e.insert(0, v)
        self.cbo_sexo.set(sexo)
        self.lbl_edad.config(text=f"{MenorEdad(nombre, ap1, ap2, sexo, fecha_nac).calculo_Edad_Menor()} años")

    def limpiar(self):
        self.seleccionado = None
        self.cbo_padre.set("")
        self.cbo_sexo.set("")
        for e in self.entradas.values():
            e.delete(0, "end")
        self.lbl_edad.config(text="-- años")

    def _datos(self):
        if self.cbo_padre.get() not in self.padre_map:
            raise ValueError("Seleccione un padre o encargado.")
        vals = [e.get().strip() for e in self.entradas.values()]
        fecha = datetime.strptime(vals[3], "%Y-%m-%d").date()
        if not self.cbo_sexo.get():
            raise ValueError("Seleccione el sexo.")
        return {
            "id_encargado": self.padre_map[self.cbo_padre.get()],
            "nombre": vals[0], "primer_apellido": vals[1], "segundo_apellido": vals[2],
            "sexo": self.cbo_sexo.get(), "fecha_nacimiento": fecha,
        }

    def guardar(self):
        try:
            data = self._datos()
            conexion.crear_menor(self.conn, data)
            self.cargar_tabla(); self.limpiar()
            messagebox.showinfo("Guardado", "Niño registrado correctamente.")
        except Exception as e:
            messagebox.showerror("No se pudo guardar", str(e))

    def modificar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un niño de la tabla.")
            return
        try:
            data = self._datos()
            conexion.actualizar_menor(self.conn, self.seleccionado, data)
            self.cargar_tabla()
            self.lbl_edad.config(text=f"{MenorEdad(**{**data, 'ID_encargado': data['id_encargado']}).calculo_Edad_Menor()} años" if False else self.lbl_edad.cget("text"))
            messagebox.showinfo("Modificado", "Datos del niño actualizados.")
        except Exception as e:
            messagebox.showerror("No se pudo modificar", str(e))

    def eliminar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione", "Seleccione un niño de la tabla.")
            return
        citas = conexion.contar_citas_de_menor(self.conn, self.seleccionado)
        if citas > 0:
            messagebox.showwarning("No permitido", f"Este niño tiene {citas} cita(s) registrada(s) y no puede eliminarse.")
            return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar el niño seleccionado?"):
            conexion.eliminar_menor(self.conn, self.seleccionado)
            self.cargar_tabla(); self.limpiar()

import tkinter as tk
from tkinter import ttk, messagebox
from Encargado import Encargado
from .Estilos import (preparar_ventana, configurar_estilos, barra_superior, pasos,
                      COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA,
                      COLOR_BORDE, COLOR_GRIS)


class InterfazPadres:
    def __init__(self, master, guardar_cambios):
        self.guardar_cambios = guardar_cambios
        self.ventana = tk.Toplevel(master)
        configurar_estilos()
        preparar_ventana(self.ventana, "Padres / Encargados", 1020, 640)
        self.seleccionado = None
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        barra_superior(self.ventana)
        cuerpo = tk.Frame(self.ventana, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True)

        tarjeta = tk.Frame(cuerpo, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(fill="both", expand=True, padx=28, pady=22)
        interior = tk.Frame(tarjeta, bg=COLOR_BLANCO, padx=25, pady=18)
        interior.pack(fill="both", expand=True)

        pasos(interior, ["Información Personal", "Dirección", "Contacto", "Resumen"], 1)
        tk.Label(interior, text="Registro y Mantenimiento de Padre", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                 font=("Segoe UI", 18, "bold")).pack(pady=(0, 14))

        buscar = tk.Frame(interior, bg=COLOR_BLANCO)
        buscar.pack(fill="x", pady=(0, 12))
        tk.Label(buscar, text="Buscar por nombre o identificación:", bg=COLOR_BLANCO, fg=COLOR_GRIS,
                 font=("Segoe UI", 9)).pack(side="left")
        self.txt_buscar = ttk.Entry(buscar, width=32)
        self.txt_buscar.pack(side="left", padx=8)
        ttk.Button(buscar, text="Buscar", command=self.cargar_tabla, style="Principal.TButton").pack(side="left")
        ttk.Button(buscar, text="Todos", command=self.limpiar_busqueda).pack(side="left", padx=6)

        form = tk.Frame(interior, bg=COLOR_BLANCO)
        form.pack(fill="x", pady=(4, 8))
        campos = ["Identificación", "Nombre completo", "Provincia", "Cantón", "Distrito", "Otras señas", "Teléfono", "Correo electrónico"]
        self.entradas = {}
        for i, campo in enumerate(campos):
            fila, col = divmod(i, 2)
            tk.Label(form, text=campo + ":", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                     font=("Segoe UI", 9, "bold")).grid(row=fila, column=col*2, sticky="w", padx=(0, 8), pady=7)
            entrada = ttk.Entry(form, width=31)
            entrada.grid(row=fila, column=col*2+1, sticky="ew", padx=(0, 20), pady=7)
            self.entradas[campo] = entrada
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        acciones = tk.Frame(interior, bg=COLOR_BLANCO)
        acciones.pack(fill="x", pady=10)
        ttk.Button(acciones, text="Nuevo / Limpiar", command=self.limpiar_formulario).pack(side="left")
        ttk.Button(acciones, text="Guardar", command=self.guardar, style="Menta.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Modificar", command=self.modificar).pack(side="left")
        ttk.Button(acciones, text="Eliminar", command=self.eliminar, style="Peligro.TButton").pack(side="left", padx=7)
        ttk.Button(acciones, text="Cerrar", command=self.ventana.destroy).pack(side="right")

        tk.Label(interior, text="Padres registrados", bg=COLOR_BLANCO, fg=COLOR_AZUL,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(5, 5))
        columnas = ("identificacion", "nombre", "telefono", "correo")
        self.tabla = ttk.Treeview(interior, columns=columnas, show="headings", height=7)
        for c, texto, ancho in [("identificacion", "Identificación", 130), ("nombre", "Nombre completo", 260),
                                ("telefono", "Teléfono", 120), ("correo", "Correo", 230)]:
            self.tabla.heading(c, text=texto)
            self.tabla.column(c, width=ancho)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def limpiar_busqueda(self):
        self.txt_buscar.delete(0, "end")
        self.cargar_tabla()

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        criterio = self.txt_buscar.get().strip().lower()
        for enc in Encargado.encargados:
            if criterio and criterio not in enc.Nombre_Completo.lower() and criterio not in enc.Identificacion.lower():
                continue
            self.tabla.insert("", "end", iid=str(id(enc)), values=(enc.Identificacion, enc.Nombre_Completo, enc.Telefono, enc.Correo_Electronico))

    def seleccionar(self, _evento=None):
        sel = self.tabla.selection()
        if not sel:
            return
        item = self.tabla.item(sel[0], "values")
        self.seleccionado = Encargado.buscar_por_identificacion(item[0])
        if not self.seleccionado:
            return
        datos = [self.seleccionado.Identificacion, self.seleccionado.Nombre_Completo, self.seleccionado.Provincia,
                 self.seleccionado.Canton, self.seleccionado.Distrito, self.seleccionado.Direccion,
                 self.seleccionado.Telefono, self.seleccionado.Correo_Electronico]
        for entrada, valor in zip(self.entradas.values(), datos):
            entrada.delete(0, "end")
            entrada.insert(0, valor)

    def limpiar_formulario(self):
        self.seleccionado = None
        for entrada in self.entradas.values():
            entrada.delete(0, "end")

    def _datos(self):
        return [e.get().strip() for e in self.entradas.values()]

    def guardar(self):
        try:
            identificacion, nombre, provincia, canton, distrito, direccion, telefono, correo = self._datos()
            if Encargado.buscar_por_identificacion(identificacion):
                raise ValueError("Ya existe un padre con esa identificación.")
            nuevo = Encargado(str(len(Encargado.encargados)+1), nombre, identificacion, provincia, canton, distrito, direccion, telefono, correo)
            Encargado.encargados.append(nuevo)
            self.guardar_cambios()
            self.cargar_tabla(); self.limpiar_formulario()
            messagebox.showinfo("Guardado", "Padre/encargado registrado correctamente.")
        except Exception as e:
            messagebox.showerror("No se pudo guardar", str(e))

    def modificar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione un registro", "Seleccione un padre de la tabla.")
            return
        try:
            identificacion, nombre, provincia, canton, distrito, direccion, telefono, correo = self._datos()
            otro = Encargado.buscar_por_identificacion(identificacion)
            if otro and otro is not self.seleccionado:
                raise ValueError("Esa identificación ya pertenece a otro padre.")
            self.seleccionado.Identificacion = identificacion
            self.seleccionado.Nombre_Completo = nombre
            self.seleccionado.Provincia, self.seleccionado.Canton, self.seleccionado.Distrito = provincia, canton, distrito
            self.seleccionado.Direccion, self.seleccionado.Telefono, self.seleccionado.Correo_Electronico = direccion, telefono, correo
            self.guardar_cambios(); self.cargar_tabla()
            messagebox.showinfo("Modificado", "Datos actualizados correctamente.")
        except Exception as e:
            messagebox.showerror("No se pudo modificar", str(e))

    def eliminar(self):
        if not self.seleccionado:
            messagebox.showwarning("Seleccione un registro", "Seleccione un padre de la tabla.")
            return
        if self.seleccionado.menoresEdad:
            mensaje = "Este padre tiene niños registrados. Si lo elimina también se eliminarán de su registro. ¿Continuar?"
        else:
            mensaje = "¿Desea eliminar el padre seleccionado?"
        if messagebox.askyesno("Confirmar eliminación", mensaje):
            Encargado.encargados.remove(self.seleccionado)
            self.guardar_cambios(); self.cargar_tabla(); self.limpiar_formulario()

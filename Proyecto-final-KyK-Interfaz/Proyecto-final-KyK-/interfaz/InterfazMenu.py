import tkinter as tk
from tkinter import messagebox
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS, COLOR_AZUL_CLARO, COLOR_TEXTO, COLOR_CIAN
from .InterfazPadres import InterfazPadres
from .InterfazNinos import InterfazNinos
from .InterfazFuncionarios import InterfazFuncionarios
from .InterfazServicios import InterfazServicios
from .InterfazFacturacion import InterfazFacturacion
from .InterfazConsultaFacturas import InterfazConsultaFacturas

class InterfazMenu:
    def __init__(self, root,conn, funcionario, cerrar_sesion):
        self.root = root
        self.conn = conn
        self.funcionario = funcionario
        self.cerrar_sesion = cerrar_sesion
        configurar_estilos()
        preparar_ventana(root, "Menú principal", 1020, 640)
        root.resizable(True, True)
        self.crear_interfaz()

    def _tarjeta_acceso(self, parent, icono, titulo, detalle, color_icono, comando):
        tarjeta = tk.Frame(parent, bg=COLOR_BLANCO, width=220, height=150,
                           highlightbackground=COLOR_BORDE, highlightthickness=1,
                           cursor="hand2")
        tarjeta.grid_propagate(False)

        # Vuelve a usar los íconos bonitos, pero con un espacio un poco mayor
        # y fuente de emoji para que se vean completos.
        icon_bg = tk.Frame(tarjeta, bg=COLOR_AZUL_CLARO, width=62, height=62,
                           highlightbackground=COLOR_BORDE, highlightthickness=1,
                           cursor="hand2")
        icon_bg.pack(pady=(16, 8))
        icon_bg.pack_propagate(False)
        tk.Label(icon_bg, text=icono, bg=COLOR_AZUL_CLARO, fg=color_icono,
                 font=("Segoe UI Emoji", 21), cursor="hand2").pack(expand=True)

        tk.Label(tarjeta, text=titulo, bg=COLOR_BLANCO, fg=COLOR_AZUL,
                 font=("Segoe UI", 12, "bold"), cursor="hand2").pack()
        tk.Label(tarjeta, text=detalle, bg=COLOR_BLANCO, fg=COLOR_GRIS,
                 font=("Segoe UI", 8), wraplength=180, justify="center",
                 cursor="hand2").pack(pady=(4, 0))

        def abrir(_e=None):
            comando()

        # Hace clickeable TODA la tarjeta, incluso widgets dentro de otros frames.
        def enlazar_recursivo(widget):
            widget.bind("<Button-1>", abrir)
            for hijo in widget.winfo_children():
                enlazar_recursivo(hijo)

        # Pequeño efecto visual al pasar el mouse.
        def entrar(_e=None):
            tarjeta.config(highlightbackground=COLOR_MENTA, highlightthickness=2)

        def salir(_e=None):
            tarjeta.config(highlightbackground=COLOR_BORDE, highlightthickness=1)

        def enlazar_hover(widget):
            widget.bind("<Enter>", entrar)
            widget.bind("<Leave>", salir)
            for hijo in widget.winfo_children():
                enlazar_hover(hijo)

        enlazar_recursivo(tarjeta)
        enlazar_hover(tarjeta)
        return tarjeta

    def _btn_sidebar(self, parent, texto, comando, activo=False):
        bg = COLOR_MENTA if activo else COLOR_BLANCO
        fg = "#FFFFFF" if activo else COLOR_TEXTO
        btn = tk.Button(parent, text=texto, command=comando, bg=bg, fg=fg, activebackground=COLOR_AZUL_CLARO,
                        activeforeground=COLOR_AZUL, bd=0, relief="flat", anchor="w", padx=16, pady=10,
                        font=("Segoe UI", 10, "bold" if activo else "normal"), cursor="hand2")
        btn.pack(fill="x", pady=4)
        return btn

    def crear_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        barra_superior(self.root)

        cont = tk.Frame(self.root, bg=COLOR_FONDO)
        cont.pack(fill="both", expand=True)

        sidebar = tk.Frame(cont, bg=COLOR_BLANCO, width=240, highlightbackground=COLOR_BORDE, highlightthickness=1)
        sidebar.pack(side="left", fill="y", padx=(18, 10), pady=18)
        sidebar.pack_propagate(False)

        main = tk.Frame(cont, bg=COLOR_FONDO)
        main.pack(side="left", fill="both", expand=True, padx=(0, 18), pady=18)

        tk.Label(sidebar, text="Happy Teeth", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=18, pady=(20, 2))
        tk.Label(sidebar, text="Clínica Dental Infantil", bg=COLOR_BLANCO, fg=COLOR_CIAN, font=("Segoe UI", 10)).pack(anchor="w", padx=18)

        info = tk.Frame(sidebar, bg=COLOR_AZUL_CLARO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        info.pack(fill="x", padx=18, pady=18)
        tk.Label(info, text="Usuario activo", bg=COLOR_AZUL_CLARO, fg=COLOR_GRIS, font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(10, 0))
        tk.Label(info, text=self.funcionario.Nombre_Completo, bg=COLOR_AZUL_CLARO, fg=COLOR_AZUL, font=("Segoe UI", 10, "bold"), wraplength=180, justify="left").pack(anchor="w", padx=12, pady=(2, 0))
        tk.Label(info, text=f"@{self.funcionario.Usuario}", bg=COLOR_AZUL_CLARO, fg=COLOR_CIAN, font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(2, 10))

        nav = tk.Frame(sidebar, bg=COLOR_BLANCO)
        nav.pack(fill="x", padx=18)
        opciones = [

        ]
        for texto, comando, activo in opciones:
            self._btn_sidebar(nav, texto, comando, activo)

        tk.Button(sidebar, text="Cerrar sesión", command=self.confirmar_salida, bg="#EF4444", fg="#FFFFFF",
                  activebackground="#DC2626", activeforeground="#FFFFFF", bd=0, relief="flat",
                  font=("Segoe UI", 10, "bold"), cursor="hand2", pady=10).pack(side="bottom",fill="x", padx=18, pady=18)

        hero = tk.Frame(main, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        hero.pack(fill="x")
        tk.Label(hero, text="Menú Principal", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=24, pady=(20, 0))
        tk.Label(hero, text="Selecciona la opción que deseas abrir.",
                 bg=COLOR_BLANCO, fg=COLOR_GRIS, font=("Segoe UI", 10)).pack(anchor="w", padx=24, pady=(4, 18))

        accesos_wrap = tk.Frame(main, bg=COLOR_FONDO)
        accesos_wrap.pack(fill="both", expand=True, pady=(16, 0))
        accesos = [
            ("👨‍👩‍👧", "Padres", "Registrar, buscar y editar padres o encargados.", "#60A5FA", lambda: InterfazPadres(self.root, self.conn)),
            ("🧒", "Niños", "Registrar niños y visualizar su edad calculada.", "#34D399", lambda: InterfazNinos(self.root, self.conn)),
            ("🦷", "Servicios", "Administrar los servicios dentales disponibles.", "#F472B6", lambda: InterfazServicios(self.root, self.conn)),
            ("📝", "Atenciones", "Crear nuevas atenciones y facturas.", "#FBBF24", lambda: InterfazFacturacion(self.root, self.funcionario, self.conn)),
            ("💳", "Facturación", "Consultar facturas y registrar pagos.", "#22D3EE", lambda: InterfazConsultaFacturas(self.root, self.conn)),
            ("👤", "Funcionarios", "Gestionar usuarios y personal de la clínica.", "#A78BFA", lambda: InterfazFuncionarios(self.root, self.conn)),
        ]
        for i, data in enumerate(accesos):
            card = self._tarjeta_acceso(accesos_wrap, *data)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
        for c in range(3):
            accesos_wrap.columnconfigure(c, weight=1)
        for r in range(2):
            accesos_wrap.rowconfigure(r, weight=1)

    def mostrar_inicio(self):
        self.crear_interfaz()

    def confirmar_salida(self):
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión actual?"):
            self.cerrar_sesion()

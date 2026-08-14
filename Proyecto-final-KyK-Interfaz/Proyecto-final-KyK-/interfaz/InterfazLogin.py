import tkinter as tk
from tkinter import ttk, messagebox
from Funcionario import Funcionario
from .Estilos import preparar_ventana, configurar_estilos, barra_superior, COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_MENTA, COLOR_BORDE, COLOR_GRIS, COLOR_TEXTO, COLOR_AZUL_CLARO, COLOR_CIAN


class InterfazLogin:
    def __init__(self, root, al_ingresar):
        self.root = root
        self.al_ingresar = al_ingresar
        configurar_estilos()
        preparar_ventana(root, "Inicio de sesión", 560, 660)
        root.resizable(False, False)
        self.crear_interfaz()

    def crear_interfaz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        barra_superior(self.root)
        fondo = tk.Frame(self.root, bg=COLOR_FONDO)
        fondo.pack(fill="both", expand=True)

        tk.Label(fondo, text="Bienvenido a Happy Teeth", bg=COLOR_FONDO, fg=COLOR_AZUL, font=("Segoe UI", 23, "bold")).pack(pady=(26, 4))
        tk.Label(fondo, text="Ingresa con tu usuario para acceder al sistema de la clínica.", bg=COLOR_FONDO, fg=COLOR_GRIS, font=("Segoe UI", 10)).pack()

        tarjeta = tk.Frame(fondo, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tarjeta.pack(padx=55, pady=24, fill="both", expand=False)

        top = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        top.pack(fill="x", padx=28, pady=(22, 10))

        logo = tk.Canvas(top, width=110, height=95, bg=COLOR_BLANCO, highlightthickness=0)
        logo.pack()
        logo.create_oval(22, 10, 83, 71, fill=COLOR_AZUL_CLARO, outline=COLOR_CIAN, width=3)
        logo.create_arc(25, 28, 80, 92, start=200, extent=140, style="arc", outline=COLOR_CIAN, width=3)
        logo.create_oval(40, 38, 44, 42, fill=COLOR_AZUL, outline=COLOR_AZUL)
        logo.create_oval(61, 38, 65, 42, fill=COLOR_AZUL, outline=COLOR_AZUL)
        logo.create_arc(46, 43, 60, 55, start=200, extent=140, style="arc", outline=COLOR_AZUL, width=2)
        logo.create_line(83, 20, 95, 10, fill=COLOR_MENTA, width=3)
        logo.create_line(89, 12, 96, 18, fill=COLOR_MENTA, width=3)

        tk.Label(top, text="Inicio de Sesión", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=("Segoe UI", 18, "bold")).pack(pady=(6, 0))
        tk.Label(top, text="Usa tu usuario y contraseña registrados.", bg=COLOR_BLANCO, fg=COLOR_GRIS, font=("Segoe UI", 9)).pack(pady=(4, 0))

        formulario = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        formulario.pack(fill="x", padx=34, pady=(8, 10))

        tk.Label(formulario, text="Usuario", bg=COLOR_BLANCO, fg=COLOR_TEXTO, anchor="w", font=("Segoe UI", 9, "bold")).pack(fill="x")
        self.txt_usuario = ttk.Entry(formulario)
        self.txt_usuario.pack(fill="x", pady=(6, 14), ipady=2)

        tk.Label(formulario, text="Contraseña", bg=COLOR_BLANCO, fg=COLOR_TEXTO, anchor="w", font=("Segoe UI", 9, "bold")).pack(fill="x")
        self.txt_contrasena = ttk.Entry(formulario, show="*")
        self.txt_contrasena.pack(fill="x", pady=(6, 8), ipady=2)

        opciones = tk.Frame(formulario, bg=COLOR_BLANCO)
        opciones.pack(fill="x", pady=(0, 14))
        self.mostrar_clave = tk.BooleanVar(value=False)
        tk.Checkbutton(opciones, text="Mostrar contraseña", variable=self.mostrar_clave, command=self.alternar_clave,
                       bg=COLOR_BLANCO, fg=COLOR_GRIS, activebackground=COLOR_BLANCO, selectcolor=COLOR_BLANCO,
                       activeforeground=COLOR_GRIS, font=("Segoe UI", 8)).pack(side="left")
        tk.Label(opciones, text="Acceso de funcionarios", bg=COLOR_BLANCO, fg=COLOR_CIAN, font=("Segoe UI", 8, "bold")).pack(side="right")

        tk.Button(formulario, text="Iniciar Sesión", command=self.validar, bg=COLOR_MENTA, fg="#FFFFFF", activebackground=COLOR_MENTA,
                  activeforeground="#FFFFFF", bd=0, font=("Segoe UI", 11, "bold"), pady=10, cursor="hand2").pack(fill="x")

        nota = tk.Frame(tarjeta, bg=COLOR_AZUL_CLARO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        nota.pack(fill="x", padx=28, pady=(8, 22))
        tk.Label(nota, text="Tip: si algo falla, verifica que el usuario esté activo y que la contraseña sea correcta.",
                 bg=COLOR_AZUL_CLARO, fg=COLOR_GRIS, font=("Segoe UI", 8), wraplength=420, justify="left").pack(anchor="w", padx=12, pady=10)

        self.txt_usuario.focus_set()
        self.root.bind("<Return>", lambda _e: self.validar())

    def alternar_clave(self):
        self.txt_contrasena.config(show="" if self.mostrar_clave.get() else "*")

    def validar(self):
        usuario = self.txt_usuario.get().strip()
        contrasena = self.txt_contrasena.get().strip()
        if not usuario or not contrasena:
            messagebox.showwarning("Datos faltantes", "Digite el usuario y la contraseña.")
            return
        funcionario = Funcionario.buscar_por_usuario(usuario)
        if funcionario is None:
            messagebox.showerror("Acceso denegado", "El usuario no existe.")
            return
        if not funcionario.Estado:
            messagebox.showerror("Acceso denegado", "El funcionario está inactivo.")
            return
        if funcionario.Contrasena != contrasena:
            messagebox.showerror("Acceso denegado", "La contraseña es incorrecta.")
            return
        Funcionario.usuario_Actual = funcionario
        self.root.unbind("<Return>")
        self.al_ingresar(funcionario)

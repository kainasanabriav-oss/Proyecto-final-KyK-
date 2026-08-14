import tkinter as tk
from tkinter import ttk
import sys

# ------------------------------------------------------------
# TEMA GENERAL
# Solo existen dos modos: oscuro y claro.
# Los colores de acento (turquesa, verde, azul, etc.) se conservan.
# ------------------------------------------------------------

MODO_ACTUAL = "oscuro"

TEMA_OSCURO = {
    "FONDO": "#0B1020",
    "TARJETA": "#151B2F",
    "TEXTO_TITULO": "#F8FAFC",
    "SUPERFICIE": "#1D2640",
    "TEXTO": "#E5E7EB",
    "GRIS": "#9CA3AF",
    "BORDE": "#2C3659",
    "BARRA": "#090E1A",
    "SIDEBAR": "#0F1528",
    "HOVER": "#273352",
    "DISABLED": "#11172A",
    "TREE_HEADING": "#21304F",
    "TREE_SELECTED": "#233A4B",
    "PANEL_RESUMEN": "#1D2640",
}

TEMA_CLARO = {
    "FONDO": "#F4F7FB",
    "TARJETA": "#FFFFFF",
    "TEXTO_TITULO": "#172033",
    "SUPERFICIE": "#EEF3F8",
    "TEXTO": "#273244",
    "GRIS": "#6B7280",
    "BORDE": "#D5DEE9",
    "BARRA": "#FFFFFF",
    "SIDEBAR": "#FFFFFF",
    "HOVER": "#E7EDF5",
    "DISABLED": "#E9EEF4",
    "TREE_HEADING": "#E8EFF7",
    "TREE_SELECTED": "#CFF7F1",
    "PANEL_RESUMEN": "#EAF8F6",
}

# El color de acento se mantiene igual en ambos modos.
COLOR_ACENTO = "#22D3EE"
COLOR_ROJO = "#F87171"
COLOR_VERDE = "#34D399"


def _tema():
    return TEMA_OSCURO if MODO_ACTUAL == "oscuro" else TEMA_CLARO


def _aplicar_variables():
    global COLOR_FONDO, COLOR_BLANCO, COLOR_AZUL, COLOR_AZUL_CLARO
    global COLOR_TEXTO, COLOR_GRIS, COLOR_BORDE, COLOR_MENTA
    global COLOR_CIAN, COLOR_MENTA_CLARO, COLOR_LILA, COLOR_LILA_OSCURO

    t = _tema()
    COLOR_FONDO = t["FONDO"]
    COLOR_BLANCO = t["TARJETA"]
    COLOR_AZUL = t["TEXTO_TITULO"]
    COLOR_AZUL_CLARO = t["SUPERFICIE"]
    COLOR_TEXTO = t["TEXTO"]
    COLOR_GRIS = t["GRIS"]
    COLOR_BORDE = t["BORDE"]
    COLOR_MENTA = COLOR_ACENTO
    COLOR_CIAN = COLOR_ACENTO
    COLOR_MENTA_CLARO = t["SUPERFICIE"]
    COLOR_LILA = COLOR_MENTA_CLARO
    COLOR_LILA_OSCURO = COLOR_AZUL


_aplicar_variables()


def _actualizar_variables_en_modulos():
    valores = {
        "COLOR_FONDO": COLOR_FONDO,
        "COLOR_BLANCO": COLOR_BLANCO,
        "COLOR_AZUL": COLOR_AZUL,
        "COLOR_AZUL_CLARO": COLOR_AZUL_CLARO,
        "COLOR_TEXTO": COLOR_TEXTO,
        "COLOR_GRIS": COLOR_GRIS,
        "COLOR_BORDE": COLOR_BORDE,
        "COLOR_MENTA": COLOR_MENTA,
        "COLOR_CIAN": COLOR_CIAN,
        "COLOR_MENTA_CLARO": COLOR_MENTA_CLARO,
        "COLOR_LILA": COLOR_LILA,
        "COLOR_LILA_OSCURO": COLOR_LILA_OSCURO,
    }
    for nombre, modulo in list(sys.modules.items()):
        if not nombre.startswith("interfaz.") or modulo is None:
            continue
        for variable, valor in valores.items():
            if hasattr(modulo, variable):
                setattr(modulo, variable, valor)


def configurar_estilos():
    t = _tema()
    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure("TFrame", background=COLOR_FONDO)
    estilo.configure("Card.TFrame", background=COLOR_BLANCO)
    estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=("Segoe UI", 10))
    estilo.configure("Card.TLabel", background=COLOR_BLANCO, foreground=COLOR_TEXTO, font=("Segoe UI", 10))
    estilo.configure("Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_AZUL, font=("Segoe UI", 18, "bold"))
    estilo.configure("TituloCard.TLabel", background=COLOR_BLANCO, foreground=COLOR_AZUL, font=("Segoe UI", 17, "bold"))
    estilo.configure("Subtitulo.TLabel", background=COLOR_FONDO, foreground=COLOR_ACENTO, font=("Segoe UI", 11, "bold"))
    estilo.configure("SubtituloCard.TLabel", background=COLOR_BLANCO, foreground=COLOR_ACENTO, font=("Segoe UI", 11, "bold"))
    estilo.configure("Info.TLabel", background=COLOR_FONDO, foreground=COLOR_GRIS, font=("Segoe UI", 9))
    estilo.configure("InfoCard.TLabel", background=COLOR_BLANCO, foreground=COLOR_GRIS, font=("Segoe UI", 9))

    estilo.configure("TEntry", padding=7, fieldbackground=COLOR_AZUL_CLARO, foreground=COLOR_TEXTO,
                     insertcolor=COLOR_TEXTO, bordercolor=COLOR_BORDE)
    estilo.map("TEntry", fieldbackground=[("disabled", t["DISABLED"])])

    estilo.configure("TCombobox", padding=6, fieldbackground=COLOR_AZUL_CLARO, foreground=COLOR_TEXTO,
                     arrowcolor=COLOR_TEXTO, insertcolor=COLOR_TEXTO, bordercolor=COLOR_BORDE)
    estilo.map("TCombobox", fieldbackground=[("readonly", COLOR_AZUL_CLARO)],
               selectbackground=[("readonly", COLOR_AZUL_CLARO)],
               selectforeground=[("readonly", COLOR_TEXTO)])

    estilo.configure("TButton", font=("Segoe UI", 10), padding=(12, 7), foreground=COLOR_TEXTO,
                     background=COLOR_AZUL_CLARO, bordercolor=COLOR_BORDE)
    estilo.map("TButton", background=[("active", t["HOVER"])])

    estilo.configure("Principal.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8),
                     foreground="#071018", background=COLOR_ACENTO, bordercolor=COLOR_ACENTO)
    estilo.map("Principal.TButton", background=[("active", COLOR_ACENTO)])

    estilo.configure("Menta.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8),
                     foreground="#071018", background=COLOR_ACENTO, bordercolor=COLOR_ACENTO)
    estilo.map("Menta.TButton", background=[("active", COLOR_ACENTO)])

    estilo.configure("Peligro.TButton", font=("Segoe UI", 10), padding=(12, 7), foreground="#FFE7E7",
                     background="#7F1D1D", bordercolor="#991B1B")
    estilo.map("Peligro.TButton", background=[("active", "#991B1B")])

    estilo.configure("TLabelframe", background=COLOR_BLANCO, bordercolor=COLOR_BORDE, relief="solid")
    estilo.configure("TLabelframe.Label", background=COLOR_BLANCO, foreground=COLOR_ACENTO, font=("Segoe UI", 10, "bold"))

    estilo.configure("Treeview", background=COLOR_AZUL_CLARO, fieldbackground=COLOR_AZUL_CLARO, foreground=COLOR_TEXTO,
                     font=("Segoe UI", 9), rowheight=27, bordercolor=COLOR_BORDE)
    estilo.configure("Treeview.Heading", background=t["TREE_HEADING"], foreground=COLOR_AZUL,
                     font=("Segoe UI", 9, "bold"), padding=6)
    estilo.map("Treeview", background=[("selected", t["TREE_SELECTED"])], foreground=[("selected", COLOR_TEXTO)])


def _recolorear_widget(widget, mapa):
    opciones = ("background", "foreground", "activebackground", "activeforeground", "highlightbackground")
    for opcion in opciones:
        try:
            valor = str(widget.cget(opcion)).lower()
            if valor in mapa:
                widget.configure(**{opcion: mapa[valor]})
        except (tk.TclError, AttributeError):
            pass

    for hijo in widget.winfo_children():
        _recolorear_widget(hijo, mapa)


def cambiar_modo(ventana, boton=None):
    """Alterna solamente entre modo oscuro y modo claro."""
    global MODO_ACTUAL

    tema_anterior = dict(_tema())
    MODO_ACTUAL = "claro" if MODO_ACTUAL == "oscuro" else "oscuro"
    tema_nuevo = dict(_tema())

    mapa = {str(tema_anterior[k]).lower(): tema_nuevo[k] for k in tema_anterior}

    _aplicar_variables()
    _actualizar_variables_en_modulos()
    configurar_estilos()

    raiz = ventana._root() if hasattr(ventana, "_root") else ventana.winfo_toplevel()
    _recolorear_widget(raiz, mapa)

    try:
        raiz.configure(bg=COLOR_FONDO)
    except tk.TclError:
        pass

    if boton is not None:
        boton.config(text="☀  Modo claro" if MODO_ACTUAL == "oscuro" else "☾  Modo oscuro")


def preparar_ventana(ventana, titulo, ancho=930, alto=600):
    ventana.title(f"Clínica Dental Infantil - Happy Teeth | {titulo}")
    ventana.geometry(f"{ancho}x{alto}")
    ventana.minsize(min(ancho, 820), min(alto, 540))
    ventana.configure(bg=COLOR_FONDO)


def barra_superior(ventana, titulo="Clínica Dental Infantil - Happy Teeth"):
    t = _tema()
    barra = tk.Frame(ventana, bg=t["BARRA"], height=38)
    barra.pack(fill="x")
    barra.pack_propagate(False)

    tk.Label(barra, text="✦  " + titulo, bg=t["BARRA"], fg=COLOR_AZUL,
             font=("Segoe UI", 9, "bold")).pack(side="left", padx=12)

    texto = "☀  Modo claro" if MODO_ACTUAL == "oscuro" else "☾  Modo oscuro"
    boton = tk.Button(barra, text=texto,
                      bg=COLOR_AZUL_CLARO, fg=COLOR_TEXTO,
                      activebackground=t["HOVER"], activeforeground=COLOR_AZUL,
                      bd=0, relief="flat", padx=12, font=("Segoe UI", 8, "bold"), cursor="hand2")
    boton.config(command=lambda: cambiar_modo(ventana, boton))
    boton.pack(side="right", padx=10, pady=5)
    return barra


def encabezado(contenedor, titulo, subtitulo=""):
    caja = ttk.Frame(contenedor)
    caja.pack(fill="x", padx=28, pady=(22, 10))
    ttk.Label(caja, text=titulo, style="Titulo.TLabel").pack(anchor="w")
    if subtitulo:
        ttk.Label(caja, text=subtitulo, style="Info.TLabel").pack(anchor="w", pady=(4, 0))
    return caja


def tarjeta(contenedor, padx=18, pady=15):
    marco = tk.Frame(contenedor, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
    marco.pack(fill="x", padx=28, pady=8)
    interior = tk.Frame(marco, bg=COLOR_BLANCO, padx=padx, pady=pady)
    interior.pack(fill="both", expand=True)
    return interior


def pasos(contenedor, etiquetas, activo=1):
    fila = tk.Frame(contenedor, bg=COLOR_BLANCO)
    fila.pack(fill="x", pady=(0, 14))
    for i, etiqueta in enumerate(etiquetas, 1):
        color = COLOR_ACENTO if i == activo else COLOR_AZUL_CLARO
        borde = COLOR_ACENTO if i <= activo else COLOR_BORDE
        fg = "#071018" if i == activo else COLOR_TEXTO
        circulo = tk.Label(fila, text=str(i), width=2, height=1, bg=color, fg=fg,
                           font=("Segoe UI", 9, "bold"), highlightbackground=borde, highlightthickness=1)
        circulo.grid(row=0, column=(i-1)*2, padx=3)
        tk.Label(fila, text=etiqueta, bg=COLOR_BLANCO, fg=COLOR_ACENTO if i == activo else COLOR_GRIS,
                 font=("Segoe UI", 8, "bold" if i == activo else "normal")).grid(row=1, column=(i-1)*2, pady=(4,0))
        if i < len(etiquetas):
            tk.Frame(fila, bg=COLOR_BORDE, height=1, width=55).grid(row=0, column=(i-1)*2+1, padx=2)
    return fila


def botonera(contenedor, botones):
    marco = ttk.Frame(contenedor)
    marco.pack(fill="x", padx=28, pady=12)
    for _i, (texto, comando) in enumerate(botones):
        estilo = "Principal.TButton" if texto.lower().startswith(("guardar", "nuevo")) else "TButton"
        if "eliminar" in texto.lower():
            estilo = "Peligro.TButton"
        ttk.Button(marco, text=texto, command=comando, style=estilo).pack(side="left", padx=(0, 8))
    return marco

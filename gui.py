import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import lexer as lexico
import sintactico

# Paleta
AZUL = "#14437a"
AZUL_BTN = "#1f5fa8"
AZUL_CLARO = "#e3ecf7"
FONDO = "#eef3f9"
BORDE = "#cfdbe9"
TEXTO = "#1d2b3a"
APAGADO = "#6b7a8c"
NARANJA_BG = "#fdf1e3"
NARANJA_BORDE = "#f0c99a"
NARANJA_FG = "#b4572b"
VERDE = "#2e7d4f"
VERDE_BG = "#e8f5ee"

FUENTE = ("DejaVu Sans", 10)
FUENTE_NEGRITA = ("DejaVu Sans", 10, "bold")
FUENTE_CHICA = ("DejaVu Sans", 9)
FUENTE_CODIGO = ("DejaVu Sans Mono", 11)

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

SUGERENCIAS = {
    "Fin de archivo inesperado": "Revise que el código esté completo: puede faltar un ';' o cerrar una llave o paréntesis.",
    "Token inesperado": "Revise la sintaxis cerca de ese token; puede faltar un ';' al final de la instrucción anterior.",
    "Caracter no reconocido": "Elimine o reemplace el carácter, no pertenece al lenguaje.",
    "Cadena sin cerrar": "Cierre la cadena con comillas dobles.",
    "Caracter mal formado": "Un carácter se escribe entre comillas simples, por ejemplo 'a'.",
}


def ejecutar_lexico(codigo):
    """Devuelve (tokens, errores_lexicos)."""
    return lexico.analizar(codigo)


def ejecutar_sintactico(codigo):
    """Devuelve (tokens, errores_lexicos, errores_sintacticos)."""
    tokens, err_lex = lexico.analizar(codigo)
    sintactico.errores_sintacticos.clear()
    # El parser consume el mismo lexer global, por eso se reinicia la entrada.
    lexico.lexer.lineno = 1
    sintactico.parser.parse(codigo, lexer=lexico.lexer)
    return tokens, err_lex, list(sintactico.errores_sintacticos)


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador de Código C#")
        self.geometry("1180x720")
        self.minsize(960, 600)
        self.configure(bg=FONDO)
        self.archivo = None
        self.botones_analisis = {}
        self.pestanas = {}
        self._construir_estilos()
        self._construir_cabecera()
        self._construir_barra()
        self._construir_cuerpo()
        self._construir_diagnosticos()
        self._construir_estado()
        self._actualizar_numeros()
        self._marcar_analisis(None)

    def report_callback_exception(self, tipo, valor, traza):
        # Tkinter oculta las excepciones de los callbacks; las mostramos.
        messagebox.showerror("Error interno", f"{tipo.__name__}: {valor}")

    # ------------------------------------------------------------ helpers
    def _panel(self, padre, **kw):
        return tk.Frame(padre, bg="white", highlightbackground=BORDE,
                        highlightthickness=1, **kw)

    def _boton(self, padre, texto, comando, activo=False):
        return tk.Button(
            padre, text=texto, command=comando, font=FUENTE_NEGRITA,
            bg=AZUL_BTN if activo else "white",
            fg="white" if activo else AZUL_BTN,
            activebackground=AZUL if activo else AZUL_CLARO,
            activeforeground="white" if activo else AZUL,
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=AZUL_BTN, highlightcolor=AZUL_BTN,
            padx=9, pady=4, cursor="hand2")

    def _enlace(self, padre, texto, comando):
        e = tk.Label(padre, text=texto, font=FUENTE_NEGRITA, fg=AZUL_BTN,
                     bg="white", cursor="hand2")
        e.bind("<Button-1>", lambda _e: comando())
        return e

    # ------------------------------------------------------------ UI
    def _construir_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=30, font=FUENTE_CHICA, background="white",
                         fieldbackground="white", foreground=TEXTO, borderwidth=0)
        estilo.map("Treeview", background=[("selected", AZUL_CLARO)],
                   foreground=[("selected", AZUL)])
        estilo.configure("Treeview.Heading", font=FUENTE_NEGRITA, background="white",
                         foreground=TEXTO, relief="flat", borderwidth=0, padding=(6, 8))
        estilo.map("Treeview.Heading", background=[("active", "white")])
        estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    def _construir_cabecera(self):
        cab = tk.Frame(self, bg=AZUL)
        cab.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(cab, text="C#", bg="white", fg=AZUL, font=("DejaVu Sans", 9, "bold"),
                 padx=5, pady=1).pack(side="left", padx=(14, 10), pady=12)
        tk.Label(cab, text="Analizador de Código C#", bg=AZUL, fg="white",
                 font=("DejaVu Sans", 14, "bold")).pack(side="left")
        tk.Label(cab, text="PROTOTIPO DE INTERFAZ", bg=AZUL, fg="#c9d8ec",
                 font=("DejaVu Sans", 8)).pack(side="right", padx=16)

    def _construir_barra(self):
        barra = self._panel(self)
        barra.pack(fill="x", padx=10, pady=10)
        interior = tk.Frame(barra, bg="white")
        interior.pack(fill="x", padx=12, pady=10)

        for texto, cmd in (("Nuevo", self.nuevo), ("Abrir .cs", self.abrir),
                           ("Guardar", self.guardar), ("Limpiar", self.limpiar)):
            self._boton(interior, texto, cmd).pack(side="left", padx=(0, 5))

        tk.Label(interior, text="Analizar:", bg="white", fg=TEXTO,
                 font=FUENTE).pack(side="left", padx=(6, 6))
        for clave, texto, cmd in (("lexico", "Léxico", self.analizar_lexico),
                                  ("sintactico", "Sintáctico", self.analizar_sintactico),
                                  ("semantico", "Semántico", self.analizar_semantico),
                                  ("completo", "Completo", self.analizar_completo)):
            b = self._boton(interior, texto, cmd)
            b.pack(side="left", padx=(0, 5))
            self.botones_analisis[clave] = b

        self._enlace(interior, "Ayuda", self.ayuda).pack(side="left", padx=(14, 0))
        tk.Label(interior, text="|", bg="white", fg=APAGADO).pack(side="left", padx=6)
        self._enlace(interior, "Ver logs", self.ver_logs).pack(side="left")
        # El orden visual es "Ver logs | Ayuda"; se reordena empaquetando al reves
        hijos = interior.pack_slaves()
        ayuda, sep, logs = hijos[-3], hijos[-2], hijos[-1]
        for w in (ayuda, sep, logs):
            w.pack_forget()
        logs.pack(side="left", padx=(8, 0))
        sep.pack(side="left", padx=6)
        ayuda.pack(side="left")

    def _marcar_analisis(self, clave):
        """Resalta el boton del analisis ejecutado (relleno azul)."""
        for k, b in self.botones_analisis.items():
            activo = k == clave
            b.configure(bg=AZUL_BTN if activo else "white",
                        fg="white" if activo else AZUL_BTN,
                        activebackground=AZUL if activo else AZUL_CLARO,
                        activeforeground="white" if activo else AZUL)

    def _construir_cuerpo(self):
        cuerpo = tk.Frame(self, bg=FONDO)
        cuerpo.pack(fill="both", expand=True, padx=10)
        cuerpo.columnconfigure(0, weight=11, uniform="c")
        cuerpo.columnconfigure(1, weight=10, uniform="c")
        cuerpo.rowconfigure(0, weight=1)

        # ---- Panel izquierdo: editor
        izq = self._panel(cuerpo)
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        cab = tk.Frame(izq, bg=AZUL_CLARO)
        cab.pack(fill="x")
        tk.Label(cab, text="Código fuente (C#)", bg=AZUL_CLARO, fg=AZUL,
                 font=FUENTE_NEGRITA).pack(side="left", padx=12, pady=8)
        self.etiqueta_archivo = tk.Label(cab, text="archivo: sin título", bg=AZUL_CLARO,
                                         fg=APAGADO, font=FUENTE_CHICA)
        self.etiqueta_archivo.pack(side="right", padx=12)

        marco = tk.Frame(izq, bg="white")
        marco.pack(fill="both", expand=True)
        self.numeros = tk.Text(marco, width=4, padx=8, pady=8, state="disabled",
                               bg="white", fg="#9aa7b6", relief="flat", bd=0,
                               font=FUENTE_CODIGO, takefocus=0, cursor="arrow",
                               highlightthickness=0)
        self.numeros.tag_configure("der", justify="right")
        self.numeros.pack(side="left", fill="y")
        self.editor = tk.Text(marco, wrap="none", undo=True, font=FUENTE_CODIGO,
                              relief="flat", bd=0, padx=8, pady=8, fg=TEXTO,
                              highlightthickness=0, insertbackground=TEXTO)
        self.editor.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(marco, command=self._scroll_conjunto)
        scroll.pack(side="right", fill="y")
        self.editor.configure(yscrollcommand=lambda a, b: self._sync_scroll(scroll, a, b))
        self.editor.tag_configure("error", background="#fff6e5", relief="solid",
                                  borderwidth=1, foreground=NARANJA_FG)
        self.editor.bind("<<Modified>>", self._al_modificar)

        # ---- Panel derecho: pestanas
        der = self._panel(cuerpo)
        der.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        barra_tabs = tk.Frame(der, bg=AZUL_CLARO)
        barra_tabs.pack(fill="x")
        self.contenido_tabs = tk.Frame(der, bg="white")
        self.contenido_tabs.pack(fill="both", expand=True)

        self.tabla_tokens = self._pestana(barra_tabs, "tokens", "Tokens",
                                          ("Token", "Lexema", "Línea", "Columna"),
                                          (150, 150, 70, 80))
        self.tabla_simbolos = self._pestana(barra_tabs, "simbolos", "Símbolos",
                                            ("Identificador", "Primera línea", "Apariciones"),
                                            (180, 120, 110))
        self.tabla_errores = self._pestana(barra_tabs, "errores", "Errores",
                                           ("Fase", "Descripción", "Lexema", "Línea", "Columna"),
                                           (90, 190, 90, 60, 70))
        self.texto_resumen = tk.Text(self.contenido_tabs, state="disabled", relief="flat",
                                     padx=14, pady=14, font=FUENTE, bg="white", fg=TEXTO,
                                     highlightthickness=0)
        self._registrar_pestana(barra_tabs, "resumen", "Resumen", self.texto_resumen)
        self._mostrar_pestana("tokens")

    def _pestana(self, barra, clave, titulo, columnas, anchos):
        marco = tk.Frame(self.contenido_tabs, bg="white")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for c, ancho in zip(columnas, anchos):
            tabla.heading(c, text=c, anchor="w")
            tabla.column(c, width=ancho, anchor="w")
        tabla.tag_configure("par", background="#f6f9fd")
        sb = ttk.Scrollbar(marco, command=tabla.yview)
        tabla.configure(yscrollcommand=sb.set)
        tabla.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        tabla.bind("<Double-1>", lambda e, t=tabla: self._ir_a_linea(t))
        self._registrar_pestana(barra, clave, titulo, marco)
        return tabla

    def _registrar_pestana(self, barra, clave, titulo, contenido):
        boton = tk.Button(barra, text=titulo, font=FUENTE_NEGRITA, relief="flat", bd=0,
                          padx=18, pady=6, cursor="hand2",
                          command=lambda: self._mostrar_pestana(clave))
        boton.pack(side="left", padx=(8 if not self.pestanas else 0, 6), pady=8)
        self.pestanas[clave] = (boton, contenido)

    def _mostrar_pestana(self, clave):
        for k, (boton, contenido) in self.pestanas.items():
            if k == clave:
                boton.configure(bg=AZUL, fg="white", activebackground=AZUL,
                                activeforeground="white")
                contenido.pack(fill="both", expand=True)
            else:
                boton.configure(bg="white", fg=AZUL_BTN, activebackground=AZUL_CLARO,
                                activeforeground=AZUL)
                contenido.pack_forget()

    def _construir_diagnosticos(self):
        panel = self._panel(self)
        panel.pack(fill="x", padx=10, pady=10)
        cab = tk.Frame(panel, bg="white")
        cab.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(cab, text="Diagnósticos", bg="white", fg=AZUL,
                 font=("DejaVu Sans", 11, "bold")).pack(side="left")
        tk.Label(cab, text="El código se valida; no se ejecuta.", bg="white",
                 fg=APAGADO, font=FUENTE_CHICA).pack(side="left", padx=12)

        self.caja_diag = tk.Frame(panel, bg=NARANJA_BG, highlightthickness=1,
                                  highlightbackground=NARANJA_BORDE)
        self.caja_diag.pack(fill="x", padx=14, pady=(0, 12))
        self.insignia = tk.Label(self.caja_diag, text="INFO", font=("DejaVu Sans", 9, "bold"),
                                 fg="white", bg=APAGADO, padx=12, pady=6)
        self.insignia.pack(side="left", padx=14, pady=12, anchor="n")
        textos = tk.Frame(self.caja_diag, bg=NARANJA_BG)
        textos.pack(side="left", fill="x", expand=True, pady=10)
        self.diag_mensaje = tk.Label(textos, anchor="w", justify="left", bg=NARANJA_BG,
                                     fg=TEXTO, font=FUENTE_NEGRITA)
        self.diag_mensaje.pack(fill="x")
        self.diag_sugerencia = tk.Label(textos, anchor="w", justify="left", bg=NARANJA_BG,
                                        fg=APAGADO, font=FUENTE_CHICA)
        self.diag_sugerencia.pack(fill="x", pady=(2, 0))
        self.caja_diag.bind("<Configure>", self._ajustar_texto)
        self._diagnostico("INFO", "Aún no se ha ejecutado ningún análisis.",
                          "Escriba o abra código C# y elija un tipo de análisis.", "info")

    def _ajustar_texto(self, evento):
        ancho = max(evento.width - 170, 200)
        self.diag_mensaje.configure(wraplength=ancho)
        self.diag_sugerencia.configure(wraplength=ancho)

    def _diagnostico(self, tipo, mensaje, sugerencia, nivel):
        bg, borde, insignia = {
            "error": (NARANJA_BG, NARANJA_BORDE, NARANJA_FG),
            "ok": (VERDE_BG, "#b7dcc7", VERDE),
            "info": ("#f3f6fa", BORDE, APAGADO),
        }[nivel]
        self.caja_diag.configure(bg=bg, highlightbackground=borde)
        self.insignia.configure(text=tipo, bg=insignia)
        self.caja_diag.winfo_children()[1].configure(bg=bg)
        self.diag_mensaje.configure(text=mensaje, bg=bg)
        self.diag_sugerencia.configure(text=sugerencia, bg=bg)

    def _construir_estado(self):
        marco = tk.Frame(self, bg=AZUL_CLARO, highlightbackground=BORDE, highlightthickness=1)
        marco.pack(fill="x", padx=10, pady=(0, 10), side="bottom")
        self.estado = tk.Label(marco, text="Estado: listo", anchor="w", bg=AZUL_CLARO,
                               fg=TEXTO, font=FUENTE_CHICA)
        self.estado.pack(side="left", padx=12, pady=6)
        tk.Label(marco, text="Resultado ilustrativo", bg=AZUL_CLARO, fg=APAGADO,
                 font=FUENTE_CHICA).pack(side="right", padx=12)

    # ------------------------------------------------- numeros de linea
    def _scroll_conjunto(self, *args):
        self.editor.yview(*args)
        self.numeros.yview(*args)

    def _sync_scroll(self, scroll, a, b):
        scroll.set(a, b)
        self.numeros.yview_moveto(a)

    def _al_modificar(self, _evento):
        if self.editor.edit_modified():
            self._actualizar_numeros()
            self.editor.edit_modified(False)

    def _actualizar_numeros(self):
        total = int(self.editor.index("end-1c").split(".")[0])
        self.numeros.configure(state="normal")
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(i) for i in range(1, total + 1)), "der")
        self.numeros.configure(state="disabled")

    # ------------------------------------------------------- archivo
    def nuevo(self):
        self.archivo = None
        self.limpiar()

    def limpiar(self):
        self.editor.delete("1.0", "end")
        self._vaciar_resultados()
        self._marcar_analisis(None)
        self._diagnostico("INFO", "Aún no se ha ejecutado ningún análisis.",
                          "Escriba o abra código C# y elija un tipo de análisis.", "info")
        self.estado.configure(text="Estado: listo")
        self._nombre_archivo()

    def _nombre_archivo(self):
        nombre = os.path.basename(self.archivo) if self.archivo else "sin título"
        self.etiqueta_archivo.configure(text=f"archivo: {nombre}")

    def abrir(self):
        ruta = filedialog.askopenfilename(filetypes=[("C#", "*.cs"), ("Todos", "*.*")])
        if not ruta:
            return
        with open(ruta, encoding="utf-8") as f:
            contenido = f.read()
        self.archivo = ruta
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", contenido)
        self._vaciar_resultados()
        self._nombre_archivo()

    def guardar(self):
        ruta = self.archivo or filedialog.asksaveasfilename(
            defaultextension=".cs", filetypes=[("C#", "*.cs")])
        if not ruta:
            return
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", "end-1c"))
        self.archivo = ruta
        self._nombre_archivo()
        self.estado.configure(text=f"Estado: guardado en {ruta}")

    def ver_logs(self):
        if not os.path.isdir(CARPETA_LOGS):
            messagebox.showinfo("Logs", "Todavía no existe la carpeta de logs.")
            return
        subprocess.Popen(["xdg-open", CARPETA_LOGS])

    def ayuda(self):
        messagebox.showinfo(
            "Ayuda",
            "1. Escriba o abra un archivo .cs.\n"
            "2. Elija Léxico, Sintáctico o Completo.\n"
            "3. Revise las pestañas y los diagnósticos.\n\n"
            "Doble clic en un error para saltar a su línea.\n"
            "El código se valida; no se ejecuta.")

    # ------------------------------------------------------ analisis
    def _codigo(self):
        return self.editor.get("1.0", "end-1c")

    def analizar_lexico(self):
        tokens, err_lex = ejecutar_lexico(self._codigo())
        self._mostrar(tokens, err_lex, [], "léxico", "lexico")

    def analizar_sintactico(self):
        tokens, err_lex, err_sin = ejecutar_sintactico(self._codigo())
        self._mostrar(tokens, err_lex, err_sin, "sintáctico", "sintactico")

    def analizar_completo(self):
        # El semantico aun no existe; "completo" encadena lo disponible.
        tokens, err_lex, err_sin = ejecutar_sintactico(self._codigo())
        self._mostrar(tokens, err_lex, err_sin, "completo", "completo")

    def analizar_semantico(self):
        messagebox.showinfo("Semántico", "El análisis semántico aún no está implementado.")

    # ------------------------------------------------------ resultados
    def _vaciar_resultados(self):
        for tabla in (self.tabla_tokens, self.tabla_simbolos, self.tabla_errores):
            tabla.delete(*tabla.get_children())
        self.editor.tag_remove("error", "1.0", "end")

    def _insertar(self, tabla, filas):
        for i, valores in enumerate(filas):
            tabla.insert("", "end", values=valores, tags=("par",) if i % 2 else ())

    def _mostrar(self, tokens, err_lex, err_sin, modo, clave):
        self._vaciar_resultados()
        self._marcar_analisis(clave)

        codigo = self._codigo()
        self._insertar(self.tabla_tokens, [
            (t.type, t.value, t.lineno, t.lexpos - codigo.rfind("\n", 0, t.lexpos))
            for t in tokens])

        simbolos = {}
        for t in tokens:
            if t.type == "ID":
                primera, cuenta = simbolos.get(t.value, (t.lineno, 0))
                simbolos[t.value] = (primera, cuenta + 1)
        self._insertar(self.tabla_simbolos,
                       [(n, l, c) for n, (l, c) in simbolos.items()])

        errores = [("Léxico", "LÉXICO", e) for e in err_lex] + \
                  [("Sintáctico", "SINTAXIS", e) for e in err_sin]
        self._insertar(self.tabla_errores, [
            (fase, e["descripcion"], e["lexema"], e["linea"], e["columna"])
            for fase, _, e in errores])
        for _, _, e in errores:
            self.editor.tag_add("error", f"{e['linea']}.0", f"{e['linea']}.end")

        if errores:
            _, insignia, e = errores[0]
            self._diagnostico(
                insignia,
                f"Línea {e['linea']}, columna {e['columna']}: "
                f"{e['descripcion']} '{e['lexema']}'.",
                "Sugerencia: " + SUGERENCIAS.get(
                    e["descripcion"], "Revise el código cerca de esa posición."),
                "error")
            self._mostrar_pestana("errores")
        else:
            self._diagnostico("OK", f"Análisis {modo} sin errores.",
                              "El código cumple las reglas validadas.", "ok")

        resumen = (f"Análisis {modo}\n\nTokens: {len(tokens)}\n"
                   f"Símbolos distintos: {len(simbolos)}\n"
                   f"Errores léxicos: {len(err_lex)}\n"
                   f"Errores sintácticos: {len(err_sin)}\n")
        self.texto_resumen.configure(state="normal")
        self.texto_resumen.delete("1.0", "end")
        self.texto_resumen.insert("1.0", resumen)
        self.texto_resumen.configure(state="disabled")

        plural = lambda n: f"{n} error" if n == 1 else f"{n} errores"
        self.estado.configure(
            text=f"Estado: análisis {modo} con {plural(len(err_sin))}  •  "
                 f"Léxico: {plural(len(err_lex))}")

    def _ir_a_linea(self, tabla):
        sel = tabla.selection()
        if not sel:
            return
        valores = tabla.item(sel[0], "values")
        columnas = tabla["columns"]
        if "Línea" in columnas:
            linea = valores[columnas.index("Línea")]
            self.editor.see(f"{linea}.0")
            self.editor.mark_set("insert", f"{linea}.0")
            self.editor.focus_set()


if __name__ == "__main__":
    Aplicacion().mainloop()

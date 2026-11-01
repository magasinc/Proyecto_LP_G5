import ply.lex as lex
import os
from datetime import datetime

# =========================================================
# INICIO APORTE: Mateo Gallegos - magasinc (Analizador Léxico)
# =========================================================

# 1. Palabras reservadas asignadas
reserved_magasinc = {
    'var': 'VAR',
    'const': 'CONST',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'bool': 'BOOL_TYPE',
    'char': 'CHAR_TYPE',
    'string': 'STRING_TYPE',
    'true': 'BOOL',
    'false': 'BOOL'
}

# Lista de tokens asignados (Debe llamarse 'tokens' para PLY)
tokens = [
    'ID', 'INT', 'DOUBLE', 'STRING', 'CHAR',
    'LBRACKET', 'RBRACKET', 'ASSIGN', 'SEMICOLON', 'LBRACE', 'RBRACE', 'COMMA'
] + list(reserved_magasinc.values())

# 2. Reglas de expresiones regulares para tokens simples
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_ignore = ' \t'  # Ignorar espacios en blanco y tabulaciones


# 3. Reglas complejas (Funciones en orden de prioridad)

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_CHAR(t):
    r'\'[^\']\''
    return t

def t_ID(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_magasinc.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass  # Ignorar comentarios en el análisis

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: Carácter no reconocido '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================

# Inicializar lexer
lexer = lex.lex()

# ---------------------------------------------------------
# LECTURA Y GENERACIÓN DE LOGS (Avance 1)
# ---------------------------------------------------------
ruta_algoritmo = os.path.join("algoritmos", "algoritmo1_G.cs")

if os.path.exists(ruta_algoritmo):
    with open(ruta_algoritmo, "r", encoding="utf-8") as f:
        codigo_csharp = f.read()

    lexer.input(codigo_csharp)

    if not os.path.exists("logs"):
        os.makedirs("logs")

    fecha_hora_str = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-MateoGallegos-{fecha_hora_str}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    salida_log = [
        "==================================================",
        "LOG DE ANÁLISIS LÉXICO",
        "Desarrollador: Mateo Gallegos (magasinc)",
        f"Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "Archivo analizado: algoritmo1_G.cs",
        "=================================================="
    ]

    print("\n--- TOKENS RECONOCIDOS ---")
    for tok in lexer:
        linea = f"[Línea {tok.lineno}] TOKEN: {tok.type} | Valor: {tok.value}"
        print(linea)
        salida_log.append(linea)

    salida_log.append("==================================================")
    salida_log.append("Análisis finalizado exitosamente.")

    with open(ruta_log, "w", encoding="utf-8") as f_log:
        f_log.write("\n".join(salida_log))

    print(f"\n¡Log generado con éxito en: {ruta_log}")
else:
    print(f"Error: No se encontró {ruta_algoritmo}")
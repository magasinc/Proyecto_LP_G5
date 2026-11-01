import ply.lex as lex
import os
from datetime import datetime
import sys
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


# Lista para guardar los errores de cada prueba
errores_lexicos = []

def t_error(t):
    columna = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)

    mensaje = (
        f"Error lexico: Caracter no reconocido "
        f"'{t.value[0]}' en linea {t.lineno}, "
        f"columna {columna}"
    )

    errores_lexicos.append(mensaje)
    print(mensaje)
    t.lexer.skip(1)


# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================

# Steven Avelino - savelinop
# Analizador léxico: operadores, delimitadores y listas

# 1. TOKENS ASIGNADOS A STEVEN AVELINO

tokens += [
    # Operadores aritmeticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'INCREMENT',
    'DECREMENT',

    # Operadores logicos
    'AND',
    'OR',
    'NOT',

    # Operadores relacionales
    'EQUAL',
    'NOT_EQUAL',
    'LESS',
    'GREATER',
    'LESS_EQUAL',
    'GREATER_EQUAL',

    # Delimitadores
    'LPAREN',
    'RPAREN',
    'DOT',

    # Estructura de datos
    'LIST'
]

# 2. REGLAS DE OPERADORES ARITMETICOS

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# 3. REGLAS DE OPERADORES LOGICOS

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# 4. REGLAS DE OPERADORES RELACIONALES

t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='

# 5. REGLAS DE DELIMITADORES

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'

# 6. RECONOCIMIENTO DE LISTAS GENERICAS



# Aprovechamos la funcion t_ID existente de Mateo
# para reconocer List como un token independiente.

reserved_magasinc['List'] = 'LIST'

# Verificar que LIST este registrado
# APORTE: Steven Avelino
if 'LIST' not in tokens:
    tokens.append('LIST')



# Inicializar lexer
lexer = lex.lex()


# ---------------------------------------------------------
# LECTURA Y GENERACION DE LOGS (AVANCE 1)
# Adaptacion para pruebas de cada integrante
# ---------------------------------------------------------

# Seleccionar el algoritmo a analizar
ruta_algoritmo = (
    sys.argv[1] if len(sys.argv) > 1
    else os.path.join("algoritmos", "algoritmo1_G.cs")
)

# Identificar al integrante que realiza la prueba
desarrollador = (
    sys.argv[2] if len(sys.argv) > 2
    else "MateoGallegos"
)

if os.path.exists(ruta_algoritmo):

    # Leer el codigo C#
    with open(ruta_algoritmo, "r", encoding="utf-8") as archivo:
        codigo_csharp = archivo.read()

    # Reiniciar el analizador
    errores_lexicos.clear()
    lexer.lineno = 1
    lexer.input(codigo_csharp)

    # Crear carpeta de logs
    os.makedirs("logs", exist_ok=True)

    # Nombre del log
    ahora = datetime.now()
    fecha = ahora.strftime("%d-%m-%Y-%Hh%Mm%Ss")

    nombre_log = f"lexico-{desarrollador}-{fecha}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    # Informacion inicial
    salida_log = [
        "==========================================",
        "ANALISIS LEXICO - C#",
        f"Desarrollador: {desarrollador}",
        f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}",
        f"Archivo: {os.path.basename(ruta_algoritmo)}",
        "==========================================",
        "",
        "TOKENS RECONOCIDOS:"
    ]

    print("\n--- TOKENS RECONOCIDOS ---")

    # Recorrer los tokens
    contador = 0

    for tok in lexer:
        linea = (
            f"[Linea {tok.lineno}] "
            f"TOKEN: {tok.type} | Valor: {tok.value}"
        )

        print(linea)
        salida_log.append(linea)
        contador += 1

    # Agregar resultados
    salida_log.append("")
    salida_log.append("ERRORES LEXICOS:")

    if errores_lexicos:
        salida_log.extend(errores_lexicos)
    else:
        salida_log.append("Sin errores lexicos")

    salida_log.append("")
    salida_log.append(f"Total tokens: {contador}")
    salida_log.append(
        f"Total errores: {len(errores_lexicos)}"
    )

    # Guardar archivo log
    with open(ruta_log, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(salida_log))

    print("\n--- RESULTADO ---")
    print(f"Tokens reconocidos: {contador}")
    print(f"Errores lexicos: {len(errores_lexicos)}")
    print(f"Log generado: {ruta_log}")

else:
    print(f"Error: No se encontro {ruta_algoritmo}")

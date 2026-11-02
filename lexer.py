import ply.lex as lex
import os
import re
from datetime import datetime
import sys
# =========================================================
# INICIO APORTE: Mateo Gallegos - magasinc (Analizador Léxico)
# =========================================================

# 1. Palabras reservadas asignadas
reserved = {
    'var': 'VAR',
    'const': 'CONST',
    'int': 'INT',
    'double': 'DOUBLE',
    'bool': 'BOOL',
    'char': 'CHAR',
    'string': 'STRING',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Lista de tokens asignados (Debe llamarse 'tokens' para PLY)
tokens = [
    'ID',
    'INT_LIT',
    'DOUBLE_LIT',
    'STRING_LIT',
    'CHAR_LIT',
    'LBRACKET', 
    'RBRACKET', 
    'ASSIGN', 
    'SEMICOLON', 
    'LBRACE', 
    'RBRACE', 
    'COMMA'
] + list(reserved.values())

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
def t_DOUBLE_LIT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Geovanny: estas dos reglas de error van antes para atrapar el 
# lexema si está implementado.
def t_ERROR_DECIMAL(t):
    r'\d+\.(?!\d)'
    registrar_error(t, "Numero decimal mal formado", t.value)

def t_ERROR_IDENTIFICADOR(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    registrar_error(t, "Identificador mal formado", t.value)

def t_INT_LIT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LIT(t):
    r'"[^"\n]*"'
    return t

def t_CHAR_LIT(t):
    r'\'[^\']\''
    return t

def t_ID(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    # Los comentarios multilinea tambien deben contar sus saltos de linea
    t.lexer.lineno += t.value.count('\n')

# Geovanny: Error si el comentario no esta cerrado.
def t_ERROR_COMMENT(t):
    r'/\*[\s\S]*'
    registrar_error(t, "Comentario sin cerrar", "/*")
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



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

reserved['List'] = 'LIST'

# Verificar que LIST este registrado
# APORTE: Steven Avelino
if 'LIST' not in tokens:
    tokens.append('LIST')

# =========================================================
# Geovanny Diaz - g30dl (Analizador Léxico)
# Analizador léxico: estructuras de datos y errores
# =========================================================

reserved.update({
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "break": "BREAK",
    "continue": "CONTINUE",
    "void": "VOID",
    "static": "STATIC",
    "new": "NEW",
    "Dictionary": "DICTIONARY",
})

tokens += [
    "IF",
    "ELSE",
    "WHILE",
    "FOR",
    "RETURN",
    "BREAK",
    "CONTINUE",
    "VOID",
    "STATIC",
    "NEW",
    "DICTIONARY"
]

# Lista para guardar los errores de cada prueba. Cada error es un dict
# con: descripcion, lexema, linea y columna (la GUI los usa por separado).
errores_lexicos = []

def calcular_columna(t):
    return t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)

def formatear_error(error):
    return (
        f"Error lexico: {error['descripcion']} "
        f"'{error['lexema']}' en linea {error['linea']}, "
        f"columna {error['columna']}"
    )

def registrar_error(t, descripcion, lexema):
    error = {
        "descripcion": descripcion,
        "lexema": lexema,
        "linea": t.lineno,
        "columna": calcular_columna(t),
    }
    errores_lexicos.append(error)
    print(formatear_error(error))



 # PLY llama a t_error cuando ninguna regla coincide.
def t_error(t):
    primero = t.value[0]

    if primero == '"':
        resto = re.match(r'"[^"\n]*', t.value).group()
        registrar_error(t, "Cadena sin cerrar", resto)
        t.lexer.skip(len(resto))

    elif primero == "'":
        resto = re.match(r"'[^'\n]*'?", t.value).group()
        registrar_error(t, "Caracter mal formado", resto)
        t.lexer.skip(len(resto))
        
    else:
        registrar_error(t, "Caracter no reconocido", primero)
        t.lexer.skip(1)


# =========================================================
# Geovanny Diaz - g30dl (Analizador Léxico)
# =========================================================


# Inicializar lexer
lexer = lex.lex()


# ---------------------------------------------------------
# LECTURA Y GENERACION DE LOGS (AVANCE 1)
# Adaptacion para pruebas de cada integrante
# ---------------------------------------------------------

def analizar(codigo):
    """Analiza el codigo C# y devuelve (tokens, errores)."""
    errores_lexicos.clear()
    lexer.lineno = 1
    lexer.input(codigo)
    lista_tokens = list(lexer)
    return lista_tokens, list(errores_lexicos)


def main():
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

    if not os.path.exists(ruta_algoritmo):
        print(f"Error: No se encontro {ruta_algoritmo}")
        return

    # Leer el codigo C#
    with open(ruta_algoritmo, "r", encoding="utf-8") as archivo:
        codigo_csharp = archivo.read()

    print("\n--- TOKENS RECONOCIDOS ---")
    tokens_reconocidos, errores = analizar(codigo_csharp)

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

    # Recorrer los tokens
    for tok in tokens_reconocidos:
        linea = (
            f"[Linea {tok.lineno}] "
            f"TOKEN: {tok.type} | Valor: {tok.value}"
        )

        print(linea)
        salida_log.append(linea)

    # Agregar resultados
    salida_log.append("")
    salida_log.append("ERRORES LEXICOS:")

    if errores:
        salida_log.extend(formatear_error(e) for e in errores)
    else:
        salida_log.append("Sin errores lexicos")

    salida_log.append("")
    salida_log.append(f"Total tokens: {len(tokens_reconocidos)}")
    salida_log.append(f"Total errores: {len(errores)}")

    # Guardar archivo log
    with open(ruta_log, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(salida_log))

    print("\n--- RESULTADO ---")
    print(f"Tokens reconocidos: {len(tokens_reconocidos)}")
    print(f"Errores lexicos: {len(errores)}")
    print(f"Log generado: {ruta_log}")


if __name__ == "__main__":
    main()

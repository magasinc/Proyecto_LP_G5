import ply.yacc as yacc
from lexer import tokens, errores_lexicos
import lexer as lexico

# =========================================================
# Geovanny Diaz - g30dl (Analizador Sintactico)
# Analizador sintactico:
# =========================================================

# Errores encontrados en cada analisis; main.py los lee para el log.
# Cada error es un dict con: descripcion, lexema, linea y columna.
errores_sintacticos = []

def p_programa(p):
    """programa : instrucciones 
    """

def p_instrucciones(p):
    """instrucciones : instruccion instrucciones
                     | instruccion
    """

def p_instruccion(p):
    """instruccion : asignacion_variable
                   | imprimir  
                   | while
                   | diccionario
                   | funcion
    """ #añadir mas instrucciones aqui

def p_asignacion_variable_constante(p):
    """asignacion_variable : CONST tipo ID ASSIGN valor SEMICOLON
    """

def p_tipo_variable(p):
    """tipo : INT
            | DOUBLE
            | STRING
            | BOOL
            | CHAR
    """
def p_valor(p):
    """valor : INT_LIT
            | DOUBLE_LIT
            | STRING_LIT
            | CHAR_LIT
            | TRUE
            | FALSE
            
    """

def p_imprimir(p):
    """imprimir : ID DOT ID LPAREN condicion RPAREN SEMICOLON
                |  tipo ID ASSIGN ID DOT ID LPAREN condicion RPAREN SEMICOLON
    
    """

def p_while(p):
    """while : WHILE LPAREN condicion RPAREN LBRACE instrucciones RBRACE
    """


def p_diccionario(p):
    """diccionario : DICTIONARY LESS tipo COMMA tipo GREATER ID ASSIGN NEW DICTIONARY LESS tipo COMMA tipo GREATER LPAREN RPAREN SEMICOLON
    """ #Dictionary<tipo,tipo> dic = new Dictionary<tipo,tipo>();

def p_funcion(p):
    """funcion : tipo ID LPAREN parametros RPAREN LBRACE instrucciones RBRACE
    """

def p_condicion(p):
    """condicion : valor operador_logico valor
                 | valor
    """

def p_operador_logico(p):
    """operador_logico : LESS
                       | GREATER
                       | LESS_EQUAL
                       | GREATER_EQUAL
                       | NOT_EQUAL
    """
def p_parametros(p):
    """parametros : tipo ID COMMA parametros
                  | tipo ID
                  | empty
    """

def p_vacio(p):
    """empty : 
    """

# PLY llama a p_error cuando un token no encaja en ninguna regla.
# Si p es None, el archivo termino antes de lo esperado.
def p_error(p):
    if p is None:
        datos = lexico.lexer.lexdata
        error = {
            "descripcion": "Fin de archivo inesperado",
            "lexema": "EOF",
            "linea": lexico.lexer.lineno,
            "columna": len(datos) - datos.rfind('\n', 0, len(datos)),
        }
    else:
        error = {
            "descripcion": "Token inesperado",
            "lexema": p.value,
            "linea": p.lineno,
            "columna": lexico.calcular_columna(p),
        }

    errores_sintacticos.append(error)
    print(formatear_error(error))

def formatear_error(error):
    return (
        f"Error sintactico: {error['descripcion']} "
        f"'{error['lexema']}' en linea {error['linea']}, "
        f"columna {error['columna']}"
    )
# =========================================================
# Geovanny Diaz - g30dl (Analizador Sintactico)
# Analizador sintactico:
# =========================================================

parser = yacc.yacc()
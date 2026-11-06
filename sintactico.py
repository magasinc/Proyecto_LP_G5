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
                   | funcion_estatica
                   | lectura

                   | BREAK SEMICOLON
                   | CONTINUE SEMICOLON 
                   | RETURN SEMICOLON
                   | RETURN operando SEMICOLON
                   
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

def registrar_error(descripcion, lexema, linea, lexpos):
    datos = lexico.lexer.lexdata
    error = {
        "descripcion": descripcion,
        "lexema": lexema,
        "linea": linea,
        "columna": lexpos - datos.rfind('\n', 0, lexpos),
    }
    errores_sintacticos.append(error)
    print(formatear_error(error))

def p_imprimir(p):
    """imprimir : ID DOT ID LPAREN condicion RPAREN SEMICOLON
    """
    # Validamos que sea Console.WriteLine(...)
    if p[1] != "Console":
        registrar_error("Se esperaba 'Console'", p[1], p.lineno(1), p.lexpos(1))
    if p[3] != "WriteLine":
        registrar_error("Se esperaba 'WriteLine'", p[3], p.lineno(3), p.lexpos(3))

def p_lectura(p):
    """lectura : tipo ID ASSIGN ID DOT ID LPAREN RPAREN SEMICOLON
               | tipo ID ASSIGN tipo DOT ID LPAREN ID DOT ID LPAREN RPAREN RPAREN SEMICOLON
    """
    # Validamos Console.ReadLine() o Tipo.Parse(Console.ReadLine())
    if len(p) == 10:
        clase, metodo = 4, 6
    else:
        clase, metodo = 8, 10
        if p[6] != "Parse":
            registrar_error("Se esperaba 'Parse'", p[6], p.lineno(6), p.lexpos(6))
    
    if p[clase] != "Console":
        registrar_error("Se esperaba 'Console'", p[clase], p.lineno(clase), p.lexpos(clase))
    if p[metodo] != "ReadLine":
        registrar_error("Se esperaba 'ReadLine'", p[metodo], p.lineno(metodo), p.lexpos(metodo))

def p_while(p):
    """while : WHILE LPAREN condicion RPAREN cuerpo_funciones
    """

def p_cuerpo_funciones(p):
    """cuerpo_funciones : LBRACE instrucciones RBRACE
                        | LBRACE RBRACE
    """

def p_diccionario(p):
    """diccionario : DICTIONARY LESS tipo COMMA tipo GREATER ID ASSIGN NEW DICTIONARY LESS tipo COMMA tipo GREATER LPAREN RPAREN SEMICOLON
    """ 
    #Dictionary<tipo,tipo> dic = new Dictionary<tipo,tipo>();

def p_funcion_estatica(p):
    """funcion_estatica : STATIC tipo_retorno_funcion ID LPAREN parametros RPAREN cuerpo_funciones
    """

def p_tipo_retorno_funcion(p):
    """tipo_retorno_funcion : tipo
                            | VOID
    """

def p_condicion(p):
    """condicion : operando operador_logico operando
                 | operando
    """

def p_operando(p):
    """operando : ID
                | valor
    """

def p_operador_logico(p):
    """operador_logico : LESS
                       | GREATER
                       | LESS_EQUAL
                       | GREATER_EQUAL
                       | NOT_EQUAL
                       | EQUAL
    """

def p_parametros(p):
    """parametros : lista_parametros
                  | empty
    """

def p_lista_parametros(p):
    """lista_parametros : parametro COMMA lista_parametros
                        | parametro
    """

def p_parametro(p):
    """parametro : tipo ID
                 | tipo ID ASSIGN valor
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
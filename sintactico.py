import ply.yacc as yacc
from lexer import tokens, errores_lexicos
import lexer as lexico


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'COMPARACION'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),
)

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
                   | declaracion_var
                   | imprimir  
                   | while
                   | diccionario
                   | funcion_estatica
                   | lectura
                   | declaracion_variable
                   | asignacion_basica
                   | if_else
                   | arreglo
                   | funcion_con_retorno
                                       | for
                   | incremento_decremento
                   | lista_generica
                   | llamada_funcion

                   | BREAK SEMICOLON
                   | CONTINUE SEMICOLON 
                   | RETURN SEMICOLON
                   | RETURN expresion SEMICOLON
                   
                   
    """ #añadir mas instrucciones aqui


def p_asignacion_variable_constante(p):
    """asignacion_variable : CONST tipo ID ASSIGN valor SEMICOLON
    """
# Declaracion de variables con tipo explicito.
# Ejemplos:
# int edad = 21;
# double promedio = 8.5;
# bool activo = true;

def p_declaracion_tipada_compartida(p):
    """asignacion_variable : tipo ID ASSIGN expresion SEMICOLON
    """

# Asignacion a variables existentes.
# Ejemplos:
# edad = 22;
# promedio = promedio + 1;
# activo = edad >= 18;

def p_asignacion_simple_compartida(p):
    """asignacion_variable : ID ASSIGN expresion SEMICOLON
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
    """condicion : expresion
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


# =========================================================
# Mateo Gallegos - magasinc (Analizador Sintactico)
# =========================================================

# 1. Declaración de Variables: Declaración explícita con inicialización
def p_declaracion_variable(p):
    """declaracion_variable : tipo ID ASSIGN operando SEMICOLON
                            | tipo ID ASSIGN operacion_aritmetica SEMICOLON
    """

# 1b. Asignación a una variable existente
def p_asignacion_basica(p):
    """asignacion_basica : ID ASSIGN operando SEMICOLON
                         | ID ASSIGN operacion_aritmetica SEMICOLON
    """

def p_operacion_aritmetica(p):
    """operacion_aritmetica : operando PLUS operando
                            | operando MINUS operando
                            | operando TIMES operando
                            | operando DIVIDE operando
    """

# 2. Estructuras de Control: if / else
def p_if_else(p):
    """if_else : IF LPAREN condicion RPAREN cuerpo_funciones
               | IF LPAREN condicion RPAREN cuerpo_funciones ELSE cuerpo_funciones
    """

# 3. Estructuras de Datos: Arreglo
def p_arreglo(p):
    """arreglo : tipo LBRACKET RBRACKET ID ASSIGN LBRACE elementos_arreglo RBRACE SEMICOLON
    """

def p_elementos_arreglo(p):
    """elementos_arreglo : valor COMMA elementos_arreglo
                         | valor
    """

# 4. Declaraciones de Funciones: Función con retorno y varios parámetros
def p_funcion_con_retorno(p):
    """funcion_con_retorno : STATIC tipo ID LPAREN lista_parametros RPAREN cuerpo_funciones
    """

# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================


# =========================================================
# Mateo Gallegos - magasinc (Analizador Sintactico)
# =========================================================

# 1. Declaración de Variables: Declaración explícita con inicialización

# 1b. Asignación a una variable existente


# 2. Estructuras de Control: if / else

# 3. Estructuras de Datos: Arreglo


# 4. Declaraciones de Funciones: Función con retorno y varios parámetros

# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================



# =========================================================
# Steven Avelino - savelinop
# Avance 2 - Analizador Sintactico

# Regla 1: Declaracion de variables con tipo inferido (var)
# Ejemplos:
# var edad = 21;
# var nombre = "Carlos";
# var activo = true;

def p_declaracion_var(p):
    """declaracion_var : VAR ID ASSIGN expresion SEMICOLON
    """

# =========================================================

# Regla 2: Expresiones aritmeticas
# =========================================================

# Suma y resta
def p_expresion(p):
    """expresion : expresion PLUS termino
                 | expresion MINUS termino
                 | termino
    """

# Multiplicacion, division y modulo
def p_termino(p):
    """termino : termino TIMES factor
               | termino DIVIDE factor
               | termino MOD factor
               | factor
    """

# Valores, identificadores y agrupacion con parentesis
def p_factor(p):
    """factor : operando
              | LPAREN expresion RPAREN
    """
# Regla 3: Expresiones booleanas
# =========================================================

# Conectores logicos AND (&&) y OR (||)
def p_expresion_conectores(p):
    """expresion : expresion AND expresion
                 | expresion OR expresion
    """

# Comparaciones: >, <, >=, <=, ==, !=
# Reutiliza operador_logico definido por Geovanny.
def p_expresion_comparacion(p):
    """expresion : expresion operador_logico expresion %prec COMPARACION
    """

# Negacion logica (!)
def p_expresion_negacion(p):
    """expresion : NOT expresion
    """


# Regla 4: Estructura de control FOR
# =========================================================

# Estructura principal del ciclo for
def p_for_steven(p):
    """for : FOR LPAREN inicio_for SEMICOLON condicion SEMICOLON actualizacion_for RPAREN cuerpo_funciones
    """

# Inicializacion del ciclo
def p_inicio_for(p):
    """inicio_for : tipo ID ASSIGN expresion
                  | VAR ID ASSIGN expresion
                  | ID ASSIGN expresion
                  | empty
    """

# Actualizacion del contador
def p_actualizacion_for(p):
    """actualizacion_for : ID INCREMENT
                         | ID DECREMENT
                         | INCREMENT ID
                         | DECREMENT ID
                         | ID ASSIGN expresion
    """

# Incremento y decremento como instrucciones
def p_incremento_decremento(p):
    """incremento_decremento : ID INCREMENT SEMICOLON
                             | ID DECREMENT SEMICOLON
                             | INCREMENT ID SEMICOLON
                             | DECREMENT ID SEMICOLON
    """

# Regla 5: Estructura de datos List<T>
# =========================================================

# Declaracion de listas genericas en C#
# Ejemplo 1: List<int> numeros = new List<int>();
# Ejemplo 2: List<int> numeros = new List<int> {1, 2, 3};

def p_lista_generica(p):
    """lista_generica : LIST LESS tipo GREATER ID ASSIGN NEW LIST LESS tipo GREATER LPAREN RPAREN SEMICOLON
                      | LIST LESS tipo GREATER ID ASSIGN NEW LIST LESS tipo GREATER LBRACE elementos_lista RBRACE SEMICOLON
    """

# Permite listas vacias o con varios elementos
def p_elementos_lista(p):
    """elementos_lista : expresion
                       | elementos_lista COMMA expresion
                       | empty
    """

# Regla 7: Llamadas a funciones
# =========================================================

# Llamada a funcion como instruccion
def p_llamada_funcion(p):
    """llamada_funcion : llamada SEMICOLON
    """

# Nombre de funcion y sus argumentos
def p_llamada(p):
    """llamada : ID LPAREN argumentos RPAREN
    """

# Argumentos opcionales
def p_argumentos(p):
    """argumentos : lista_argumentos
                  | empty
    """

# Uno o varios argumentos separados por coma
def p_lista_argumentos(p):
    """lista_argumentos : expresion
                        | lista_argumentos COMMA expresion
    """

# Permite llamadas dentro de expresiones:
# var resultado = Sumar(3, 4);
def p_factor_llamada(p):
    """factor : llamada
    """


# Ejemplos:
# static void Saludar() {
#     Console.WriteLine("Hola");
# }
#
# static void MostrarNombre(string nombre) {
#     Console.WriteLine(nombre);
# }

# Reutilizamos las reglas del grupo:
# - parametros
# - cuerpo_funciones
# - imprimir
#
# Esto permite funciones con y sin parametros.

# Reutilizamos:
# - LIST: definido por Steven en el lexer
# - NEW: definido por Geovanny en el lexer
# - tipo: definido en el sintactico del grupo
# - expresion: reglas aritmeticas y booleanas de Steven
# - empty: regla existente del proyecto



# Las expresiones booleanas tambien permiten
# operaciones aritmeticas y agrupaciones.
#
# Ejemplos:
# edad >= 18
# edad >= 18 && activo
# activo || autorizado
# !activo
# (edad >= 18 && activo) || autorizado

# =================================

# Se reutiliza la regla 'operando' de Geovanny.
# La estructura de la gramatica respeta la precedencia:
# 1. Parentesis
# 2. Multiplicacion, division y modulo
# 3. Suma y resta

# =========================================================




parser = yacc.yacc()
import ply.yacc as yacc
from lexer import tokens, errores_lexicos
import lexer as lexico

#GD-AnalizadorSemantico
tabla_simbolos = {
    "variables":{},
    "tipos":{ 
        "funciones_definidas":["Console", "WriteLine", "ReadLine", "Parse"],
        "tipos_numericos":["int", "double", "char"] },
    "funciones":{
        "retorno_bucles": ["break", "continue"],
        "retorno_funciones": ["return"]
    },
    "contexto":{"bucles":0, "funciones":0}
    }
#Añadir mas elementos a la tabla de simbolos segun se requiera

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
    
    #GD-AnalizadorSemantico
    # Saber si una instruccion es un break o continue y si esta dentro de un bucle.
    nombre = p[1]
    if nombre in tabla_simbolos["funciones"]["retorno_bucles"]:
        if tabla_simbolos["contexto"]["bucles"] == 0:
            registrar_error_semantico(
                "Sentencia fuera de un bucle", p[1], p.lineno(1), p.lexpos(1))

    if nombre in tabla_simbolos["funciones"]["retorno_funciones"]:
        if tabla_simbolos["contexto"]["funciones"] == 0:
            registrar_error_semantico(
                "Sentencia fuera de una funcion", p[1], p.lineno(1), p.lexpos(1))

def p_asignacion_variable_constante(p):
    """asignacion_variable : CONST tipo ID ASSIGN expresion SEMICOLON
    """
    registrar_variable(p[3], p[2], True)  #GD-AnalizadorSemantico
# Declaracion de variables con tipo explicito.
# Ejemplos:
# int edad = 21;
# double promedio = 8.5;
# bool activo = true;

def p_declaracion_tipada_compartida(p):
    """asignacion_variable : tipo ID ASSIGN expresion SEMICOLON
    """
    registrar_variable(p[2], p[1], False)  #GD-AnalizadorSemantico
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
    p[0] = p[1]  #GD-AnalizadorSemantico

def p_valor(p):
    """valor : INT_LIT
            | DOUBLE_LIT
            | STRING_LIT
            | CHAR_LIT
            | TRUE
            | FALSE    
    """
    #GD-AnalizadorSemantico
    if p.slice[1].type == "INT_LIT":
        p[0] = "int"
    elif p.slice[1].type == "DOUBLE_LIT":
        p[0] = "double"
    elif p.slice[1].type == "STRING_LIT":
        p[0] = "string"
    elif p.slice[1].type == "CHAR_LIT":
        p[0] = "char"
    else:
        p[0] = "bool"      # TRUE o FALSE

#GD-AnalizadorSemantico
def registrar_variable(nombre, tipo, constante):
    tabla_simbolos["variables"][nombre] = {"tipo": tipo, "const": constante}

def p_imprimir(p):
    """imprimir : ID DOT ID LPAREN condicion RPAREN SEMICOLON
    """

    # Los nombres de Console.WriteLine(...) deben estar definidos en la tabla de simbolos
    for i in (1, 3):
        if p[i] not in tabla_simbolos["tipos"]["funciones_definidas"]:
            registrar_error("Funcion no definida", p[i], p.lineno(i), p.lexpos(i))

def p_lectura(p):
    """lectura : tipo ID ASSIGN ID DOT ID LPAREN RPAREN SEMICOLON
               | tipo ID ASSIGN tipo DOT ID LPAREN ID DOT ID LPAREN RPAREN RPAREN SEMICOLON
    """

    # Los nombres de Console.ReadLine() o Tipo.Parse(Console.ReadLine()) deben estar en la tabla
    nombres = (4, 6) if len(p) == 10 else (6, 8, 10)
    for i in nombres:
        if p[i] not in tabla_simbolos["tipos"]["funciones_definidas"]:
            registrar_error("Funcion no definida", p[i], p.lineno(i), p.lexpos(i))
    # La variable leida queda declarada con el tipo indicado.
    registrar_variable(p[2], p[1], False)  #GD-AnalizadorSemantico

def p_while(p):
    """while : WHILE LPAREN condicion RPAREN cuerpo_bucle
    """
    tabla_simbolos["contexto"]["bucles"] -= 1  #GD-AnalizadorSemantico

#GD-AnalizadorSemantico
def p_cuerpo_bucle(p):
    """cuerpo_bucle : LBRACE abrir_bucle instrucciones RBRACE
                    | LBRACE abrir_bucle RBRACE
    """
#while(condicion){ }

#GD-AnalizadorSemantico
def p_abrir_bucle(p):
    """abrir_bucle : """
    tabla_simbolos["contexto"]["bucles"] += 1

#GD-AnalizadorSemantico
def p_cuerpo_funciones(p):
    """cuerpo_funciones : LBRACE abrir_funcion instrucciones RBRACE
                        | LBRACE abrir_funcion RBRACE
    """

#GD-AnalizadorSemantico
def p_abrir_funcion(p):
    """abrir_funcion : """
    tabla_simbolos["contexto"]["funciones"] += 1
    
def p_diccionario(p):
    """diccionario : DICTIONARY LESS tipo COMMA tipo GREATER ID ASSIGN NEW DICTIONARY LESS tipo COMMA tipo GREATER LPAREN RPAREN SEMICOLON
    """ 
    #Dictionary<tipo,tipo> dic = new Dictionary<tipo,tipo>();

def p_funcion_estatica(p):
    """funcion_estatica : STATIC tipo_retorno_funcion ID LPAREN parametros RPAREN cuerpo_funciones
    """
    tabla_simbolos["contexto"]["funciones"] -= 1  #GD-AnalizadorSemantico

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
    #GD-AnalizadorSemantico
    # Un literal trae su tipo; un ID lo trae de la tabla.
    if p.slice[1].type == "ID":
        variable = tabla_simbolos["variables"].get(p[1])
        if variable is not None:
            p[0] = variable["tipo"]
        else:
            p[0] = None
    else:
        p[0] = p[1]

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

# Cada error es un dict con: descripcion, lexema, linea y columna.
errores_sintacticos = []

# PLY llama a p_error cuando un token no encaja en ninguna regla.
# Si p es None, el archivo termino antes de lo esperado.
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

#GD-AnalizadorSemantico
# Errores semanticos: misma estructura que los sintacticos
# (descripcion, lexema, linea y columna).
errores_semanticos = []

def reiniciar_semantico():
    """Limpia errores y contexto; un error de sintaxis dentro de un bucle deja el contador sucio."""
    errores_semanticos.clear()
    tabla_simbolos["variables"].clear()
    tabla_simbolos["contexto"]["bucles"] = 0
    tabla_simbolos["contexto"]["funciones"] = 0

def registrar_error_semantico(descripcion, lexema, linea, lexpos):
    datos = lexico.lexer.lexdata
    error = {
        "descripcion": descripcion,
        "lexema": lexema,
        "linea": linea,
        "columna": lexpos - datos.rfind('\n', 0, lexpos),
    }
    errores_semanticos.append(error)
    print(formatear_error_semantico(error))

def formatear_error_semantico(error):
    return (
        f"Error semantico: {error['descripcion']} "
        f"'{error['lexema']}' en linea {error['linea']}, "
        f"columna {error['columna']}"
    )

#GD-AnalizadorSemantico
def p_casting(p):
    """factor : LPAREN tipo RPAREN factor
    """
    destino, origen = p[2], p[4]
    
    # Si el tipo del operando no se conoce todavia (None) no se marca error.
    if origen is not None and origen != destino:
        if not (origen in tabla_simbolos["tipos"]["tipos_numericos"] and destino in tabla_simbolos["tipos"]["tipos_numericos"]):
            registrar_error_semantico(
                f"No se puede convertir explicitamente '{origen}' a '{destino}' mediante casting", destino, p.lineno(1), p.lexpos(1))
    p[0] = destino

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
    registrar_variable(p[2], p[1], False)  #GD-AnalizadorSemantico

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
    """funcion_con_retorno : tipo_retorno_funcion ID LPAREN lista_parametros RPAREN cuerpo_funciones
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
    #GD-AnalizadorSemantico
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
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
    """for : FOR LPAREN inicio_for SEMICOLON condicion SEMICOLON actualizacion_for RPAREN cuerpo_bucle
    """
    tabla_simbolos["contexto"]["bucles"] -= 1  #GD-AnalizadorSemantico

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
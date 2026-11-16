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

start = "programa"
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
    # Steven Avelino - savelinop
    # Propagar el retorno de las instrucciones
    # =========== Steven Avelino ===========
    p[0] = bool(p[1]) or (
        bool(p[2]) if len(p) == 3 else False
    )
    # ============== Steven Avelino ==================

def p_instruccion(p):
    """instruccion : asignacion_variable
                   | declaracion_var
                   | imprimir  
                   | while
                   | diccionario
                   | funcion_estatica
                   | lectura
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
    
    # Steven Avelino - savelinop
    # Avance 3: Verificar el tipo de cada return

    # =========== Steven Avelino ===========
    if p.slice[1].type == "RETURN":
        p[0] = True

        if pila_funciones:
            funcion = pila_funciones[-1]
            tipo_esperado = funcion["tipo"]
            tiene_valor = len(p) == 4
            tipo_devuelto = p[2] if tiene_valor else None

            if tipo_esperado == "void" and tiene_valor:
                registrar_error_semantico(
                    "[Retorno de funciones] Una funcion 'void' "
                    "no puede devolver un valor",
                    p[1], p.lineno(1), p.lexpos(1)
                )

            elif tipo_esperado != "void" and not tiene_valor:
                registrar_error_semantico(
                    f"[Retorno de funciones] La funcion "
                    f"'{funcion['nombre']}' debe retornar un "
                    f"valor de tipo '{tipo_esperado}'",
                    p[1], p.lineno(1), p.lexpos(1)
                )

            elif (tipo_esperado != "void"
                  and tiene_valor
                  and tipo_devuelto is not None
                  and not compatible_retorno(
                      tipo_esperado, tipo_devuelto
                  )):
                registrar_error_semantico(
                    f"[Retorno de funciones] La funcion "
                    f"'{funcion['nombre']}' debe retornar "
                    f"'{tipo_esperado}', pero devolvio "
                    f"'{tipo_devuelto}'",
                    p[1], p.lineno(1), p.lexpos(1)
                )
    else:
        p[0] = p[1] if isinstance(p[1], bool) else False
    # ============== Steven Avelino ==================
        

def p_asignacion_variable_constante(p):
    """asignacion_variable : CONST tipo ID ASSIGN expresion SEMICOLON
    """
    registrar_variable(p[3], p[2], True)  #GD-AnalizadorSemantico

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
    validar_condicion_bool(p[3], p[1], p.lineno(1), p.lexpos(1))  #GD-AnalizadorSemantico

#GD-AnalizadorSemantico
def p_cuerpo_funciones(p):
    """cuerpo_funciones : LBRACE abrir_funcion instrucciones RBRACE
                        | LBRACE abrir_funcion RBRACE
    """

    # Steven Avelino - savelinop
    # =========== Steven Avelino ===========
    p[0] = bool(p[3]) if len(p) == 5 else False
    # ============== Steven Avelino ==================

def p_diccionario(p):
    """diccionario : DICTIONARY LESS tipo COMMA tipo GREATER ID ASSIGN NEW DICTIONARY LESS tipo COMMA tipo GREATER LPAREN RPAREN SEMICOLON
    """ 
    #Dictionary<tipo,tipo> dic = new Dictionary<tipo,tipo>();

def p_funcion_estatica(p):
    """funcion_estatica : STATIC tipo_retorno_funcion ID LPAREN parametros RPAREN preparar_funcion cuerpo_funciones
    """

    # Geovanny Diaz: cerrar el contexto de la funcion
    tabla_simbolos["contexto"]["funciones"] -= 1

    # Steven Avelino - savelinop (Avance 3)
    # Comprobar el retorno de la funcion
    # =========== Steven Avelino ===========
    finalizar_funcion(
        p[8],
        p.lineno(3),
        p.lexpos(3)
    )
    # ============== Steven Avelino ==================

def p_tipo_retorno_funcion(p):
    """tipo_retorno_funcion : tipo
                            | VOID
    """
    # Steven Avelino - savelinop (Avance 3)
    # Guardar el tipo de retorno declarado
    # =========== Steven Avelino ===========
    p[0] = p[1]
    # ============== Steven Avelino ==================

def p_condicion(p):
    """condicion : expresion
    """
    p[0] = p[1]  #GD-AnalizadorSemantico

def p_operando(p):
    """operando : ID
                | valor
    """
    # Regla 1: Verificación de identificadores no declarados
    if p.slice[1].type == "ID":
        variable = tabla_simbolos["variables"].get(p[1])
        if variable is not None:
            p[0] = variable["tipo"]
        else:
            # =========== Mateo Gallegos ===========
            registrar_error_semantico(
                f"[Identificadores] El identificador '{p[1]}' no existe en el contexto actual", 
                p[1], p.lineno(1), p.lexpos(1)
            )
            # ============== Mateo Gallegos ==================
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

    # Steven Avelino - savelinop (Avance 3)
    # Enviar el operador y su posicion a nuestra validacion
    # =========== Steven Avelino ===========
    p[0] = p[1]
    p.set_lineno(0, p.lineno(1))
    p.set_lexpos(0, p.lexpos(1))
    # ============== Steven Avelino ==================

def p_parametros(p):
    """parametros : lista_parametros
                  | empty
    """
    # Steven Avelino - savelinop (Avance 3)
    # =========== Steven Avelino ===========
    p[0] = p[1] or []
    # ============== Steven Avelino ==================

def p_lista_parametros(p):
    """lista_parametros : parametro COMMA lista_parametros
                        | parametro
    """
    # Steven Avelino - savelinop (Avance 3)
    # =========== Steven Avelino ===========
    p[0] = [p[1]] + (p[3] if len(p) == 4 else [])
    # ============== Steven Avelino ==================

def p_parametro(p):
    """parametro : tipo ID
                 | tipo ID ASSIGN valor
    """
    # Steven Avelino - savelinop (Avance 3)
    # Guardar nombre y tipo del parametro
    # =========== Steven Avelino ===========
    p[0] = (p[2], p[1])
    # ============== Steven Avelino ==================

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

# =========================================================
# Geovanny Diaz - g30dl (Analizador Sintactico)
# Analizador sintactico:
# =========================================================

# =========================================================
# Geovanny Diaz - g30dl (Analizador Semantico)
# Analizador Semantico:
# =========================================================

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
def p_abrir_funcion(p):
    """abrir_funcion : """
    tabla_simbolos["contexto"]["funciones"] += 1
    

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
    # =========== Steven Avelino ===========
    pila_funciones.clear()
    # ============== Steven Avelino ==================

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
def validar_condicion_bool(tipo, estructura, linea, lexpos):
    """Regla 5: la condicion de if y while debe ser bool. Un tipo desconocido (None) no se marca."""
    if tipo is not None and tipo != "bool":
        registrar_error_semantico(
            f"[Estructuras de Control] La condicion de la estructura '{estructura}' "
            f"debe ser de tipo 'bool', se proporciono '{tipo}'",
            estructura, linea, lexpos)

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
# Geovanny Diaz - g30dl (Analizador Semantico)
# Analizador Semantico:
# =========================================================

# =========================================================
# INICIO APORTE: Mateo Gallegos - magasinc (Analizador Sintactico)
# =========================================================

# Declaracion de variables con tipo explicito.
# Ejemplos:
# int edad = 21;
# double promedio = 8.5;
# bool activo = true;
'''def p_declaracion_tipada_compartida(p):
    """asignacion_variable : tipo ID ASSIGN expresion SEMICOLON
    """
    registrar_variable(p[2], p[1], False)  #GD-AnalizadorSemantico
# Asignacion a variables existentes.
# Ejemplos:
# edad = 22;
# promedio = promedio + 1;
# activo = edad >= 18;'''

'''def p_asignacion_simple_compartida(p):
    """asignacion_variable : ID ASSIGN expresion SEMICOLON
    """'''

def p_declaracion_tipada_compartida(p):
    """asignacion_variable : tipo ID ASSIGN expresion SEMICOLON
    """
    tipo_destino = p[1]
    nombre_var = p[2]
    tipo_origen = p[4]
    
    # Regla 1: Validar identificador (No duplicados)
    registrar_variable(nombre_var, tipo_destino, False, p, 2)
    # Regla 2: Validar pérdida de información
    validar_asignacion(tipo_destino, tipo_origen, nombre_var, p.lineno(2), p.lexpos(2))

def p_asignacion_simple_compartida(p):
    """asignacion_variable : ID ASSIGN expresion SEMICOLON
    """
    nombre_var = p[1]
    tipo_origen = p[3]
    
    variable = tabla_simbolos["variables"].get(nombre_var)
    if variable is None:
        # Regla 1: La variable debe existir
        registrar_error_semantico(
            f"[Identificadores] La variable '{nombre_var}' no esta declarada en el contexto actual", 
            nombre_var, p.lineno(1), p.lexpos(1)
        )
    else:
        if variable["const"]:
            registrar_error_semantico(
                f"[Constantes] No se puede reasignar un valor a la constante '{nombre_var}'", 
                nombre_var, p.lineno(1), p.lexpos(1)
            )
        else:
            # Regla 2: Validar pérdida de información
            tipo_destino = variable["tipo"]
            validar_asignacion(tipo_destino, tipo_origen, nombre_var, p.lineno(1), p.lexpos(1))

# 1. Declaración y asignación básica
'''def p_declaracion_variable(p):
    """declaracion_variable : tipo ID ASSIGN expresion SEMICOLON
    """
    tipo_destino = p[1]
    nombre_var = p[2]
    tipo_origen = p[4]
    
    # Regla 1: Validar identificador (No duplicados)
    registrar_variable(nombre_var, tipo_destino, False, p, 2)
    # Regla 2: Validar pérdida de información
    validar_asignacion(tipo_destino, tipo_origen, nombre_var, p.lineno(2), p.lexpos(2))'''

# Regla para soportar a + b + c + ...
# 2. Estructuras de Control: if / else (Con soporte else if)
def p_if_else(p):
    """if_else : IF LPAREN condicion RPAREN cuerpo_funciones
               | IF LPAREN condicion RPAREN cuerpo_funciones ELSE cuerpo_funciones
               | IF LPAREN condicion RPAREN cuerpo_funciones ELSE if_else
    """

    # =========== Geovanny Diaz ===========
    validar_condicion_bool(p[3], p[1], p.lineno(1), p.lexpos(1))  #GD-AnalizadorSemantico
    # ============== Geovanny Diaz ==================

    # Steven Avelino - savelinop
    # Avance 3: Verificar retorno en todas las rutas

    # =========== Steven Avelino ===========
    if len(p) == 8:
        # Tanto el if como el else deben garantizar retorno
        p[0] = bool(p[5]) and bool(p[7])
    else:
        # Un if sin else no garantiza retorno
        p[0] = False
    # ============== Steven Avelino ==================

# 1. Declaración y asignación básica
# Regla para soportar a + b + c + ...
# 2. Estructuras de Control: if / else
'''def p_if_else(p):
    """if_else : IF LPAREN condicion RPAREN cuerpo_funciones
               | IF LPAREN condicion RPAREN cuerpo_funciones ELSE cuerpo_funciones
               | IF LPAREN condicion RPAREN cuerpo_funciones ELSE if_else
    """
    if len(p) == 8:
        p[0] = bool(p[5]) and bool(p[7])
    else:
        p[0] = False'''

# 3. Estructuras de Datos: Arreglo
def p_arreglo(p):
    """arreglo : tipo LBRACKET RBRACKET ID ASSIGN LBRACE elementos_arreglo RBRACE SEMICOLON
    """

def p_elementos_arreglo(p):
    """elementos_arreglo : valor COMMA elementos_arreglo
                         | valor
    """

# 4. Declaraciones de Funciones: Función con retorno
def p_funcion_con_retorno(p):
    """funcion_con_retorno : tipo_retorno_funcion ID LPAREN lista_parametros RPAREN preparar_funcion cuerpo_funciones
    """
    # =========== Geovanny Diaz ===========
    tabla_simbolos["contexto"]["funciones"] -= 1
    # ============== Geovanny Diaz ==================
    finalizar_funcion(p[7], p.lineno(2), p.lexpos(2))

# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================

# =========================================================
# INICIO APORTE: Mateo Gallegos - magasinc (Analizador Semantico)
# =========================================================

def validar_asignacion(tipo_destino, tipo_origen, lexema, linea, lexpos):
    """Regla 2: Compatibilidad de tipos y pérdida de información."""
    if tipo_destino is None or tipo_origen is None or tipo_destino == tipo_origen:
        return

    # C# permite conversiones implícitas seguras (ej. int a double o char a int/double)
    if tipo_destino == "double" and tipo_origen in ["int", "char"]:
        return
    if tipo_destino == "int" and tipo_origen == "char":
        return

    # Cualquier otro caso genera error (ej. double a int pierde decimales)
    registrar_error_semantico(
        f"[Compatibilidad de Tipos] No se puede convertir implicitamente '{tipo_origen}' a '{tipo_destino}'. Posible perdida de informacion",
        lexema, linea, lexpos
    )

def registrar_variable(nombre, tipo, constante, p_obj=None, p_index=1):
    """Regla 1: Identificadores. Evita variables duplicadas en el mismo contexto."""
    if nombre in tabla_simbolos["variables"]:
        if p_obj:
            registrar_error_semantico(
                f"[Identificadores] La variable '{nombre}' ya esta declarada en este contexto", 
                nombre, p_obj.lineno(p_index), p_obj.lexpos(p_index)
            )
    else:
        # =========== Geovanny Diaz ===========
        tabla_simbolos["variables"][nombre] = {"tipo": tipo, "const": constante}
        # ============== Geovanny Diaz ==================

# =========================================================
# FIN APORTE: Mateo Gallegos - magasinc
# =========================================================

# =========================================================
# INICIO APORTE: Steven Avelino - savelinop (Analizador Sintactico)
# =========================================================

# 3. Estructuras de Datos: Arreglo
# 4. Declaraciones de Funciones: Función con retorno y varios parámetros




# 1. Declaración de Variables: Declaración explícita con inicialización

# 1b. Asignación a una variable existente


# 2. Estructuras de Control: if / else

# 3. Estructuras de Datos: Arreglo


# 4. Declaraciones de Funciones: Función con retorno y varios parámetros




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
    # Steven Avelino - savelinop (Avance 3)
    # Guardar el tipo inferido de la variable
    registrar_variable(p[2], p[4], False)

# Regla 2: Expresiones aritmeticas


# Steven Avelino - savelinop
# Avance 3: Validacion semantica de suma y resta
def p_expresion(p):
    """expresion : expresion PLUS termino
                 | expresion MINUS termino
                 | termino
    """

    if len(p) == 4:
        p[0] = validar_operacion(
            p[2],
            p[1],
            p[3],
            p.lineno(2),
            p.lexpos(2)
        )
    else:
        p[0] = p[1]

# Steven Avelino - savelinop
# Avance 3: Validacion de multiplicacion, division y modulo
def p_termino(p):
    """termino : termino TIMES factor
               | termino DIVIDE factor
               | termino MOD factor
               | factor
    """

    if len(p) == 4:
        p[0] = validar_operacion(
            p[2],
            p[1],
            p[3],
            p.lineno(2),
            p.lexpos(2)
        )
    else:
        p[0] = p[1]

# Valores, identificadores y agrupacion con parentesis
def p_factor(p):
    """factor : operando
              | LPAREN expresion RPAREN
    """
    #GD-AnalizadorSemantico
    # =========== Geovanny Diaz ===========
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    # ============== Geovanny Diaz ==================

# Regla 3: Expresiones booleanas


# Steven Avelino - savelinop
# Avance 3: Validacion de operadores logicos AND y OR
def p_expresion_conectores(p):
    """expresion : expresion AND expresion
                 | expresion OR expresion
    """

    p[0] = validar_operacion(
        p[2],
        p[1],
        p[3],
        p.lineno(2),
        p.lexpos(2)
    )

# Comparaciones: >, <, >=, <=, ==, !=
# Reutiliza operador_logico definido por Geovanny.

# Steven Avelino - savelinop
# Avance 3: Validacion de operadores relacionales
def p_expresion_comparacion(p):
    """expresion : expresion operador_logico expresion %prec COMPARACION
    """

    p[0] = validar_operacion(
        p[2],
        p[1],
        p[3],
        p.lineno(2),
        p.lexpos(2)
    )

# Steven Avelino - savelinop
# Avance 3: Validacion del operador NOT
def p_expresion_negacion(p):
    """expresion : NOT expresion
    """

    if p[2] is not None and p[2] != "bool":

        registrar_error_semantico(
            f"[Operaciones permitidas] El operador '!' "
            f"requiere 'bool', se recibio '{p[2]}'",
            p[1],
            p.lineno(1),
            p.lexpos(1)
        )

        p[0] = None

    else:
        p[0] = "bool" if p[2] is not None else None

# Regla 4: Estructura de control FOR

# Estructura principal del ciclo for
def p_for_steven(p):
    """for : FOR LPAREN inicio_for SEMICOLON condicion SEMICOLON actualizacion_for RPAREN cuerpo_bucle
    """
    # =========== Geovanny Diaz ===========
    tabla_simbolos["contexto"]["bucles"] -= 1  #GD-AnalizadorSemantico
    # ============== Geovanny Diaz ==================

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
    #GD-AnalizadorSemantico
    # Regla 6: una constante no se puede modificar, tampoco con ++ o --.
    # =========== Geovanny Diaz ===========
    indice = 1 if p.slice[1].type == "ID" else 2
    variable = tabla_simbolos["variables"].get(p[indice])
    if variable is not None and variable["const"]:
        registrar_error_semantico(
            f"[Constantes] No se puede modificar la constante '{p[indice]}'",
            p[indice], p.lineno(indice), p.lexpos(indice))
    # ============== Geovanny Diaz ==================

# Regla 5: Estructura de datos List<T>
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


# Se reutiliza la regla 'operando' de Geovanny.
# La estructura de la gramatica respeta la precedencia:
# 1. Parentesis
# 2. Multiplicacion, division y modulo
# 3. Suma y resta

# =========================================================
# FIN APORTE: Steven Avelino - savelinop
# =========================================================

# =========================================================
# INICIO APORTE: Steven Avelino - savelinop (Analizador Semantico)
# =========================================================

# AVANCE 3 - ANALIZADOR SEMANTICO
# Regla 3: Operaciones permitidas y compatibilidad de tipos
def validar_operacion(operador, izquierda, derecha, linea, lexpos):

    # No validar tipos que todavia no se conocen
    if izquierda is None or derecha is None:
        return None

    numericos = ("int", "double", "char")

    # Concatenacion de cadenas
    if operador == "+" and "string" in (izquierda, derecha):
        return "string"

    # Operaciones aritmeticas
    if operador in ("+", "-", "*", "/", "%"):
        if izquierda in numericos and derecha in numericos:
            if "double" in (izquierda, derecha):
                return "double"
            return "int"

    # Operaciones logicas
    elif operador in ("&&", "||"):
        if izquierda == derecha == "bool":
            return "bool"

    # Comparaciones relacionales
    elif operador in ("<", ">", "<=", ">="):
        if izquierda in numericos and derecha in numericos:
            return "bool"

    # Igualdad y desigualdad
    elif operador in ("==", "!="):
        if izquierda == derecha or (
            izquierda in numericos and derecha in numericos
        ):
            return "bool"

    # Si no cumple ninguna regla, registrar error
    registrar_error_semantico(
        f"[Operaciones permitidas] No se puede aplicar el operador '{operador}' "
        f"a los operandos de tipo '{izquierda}' y '{derecha}'",
        operador,
        linea,
        lexpos
    )

    return None

# AVANCE 3 - Regla 4: Retorno de funciones

# Guarda las funciones que se estan analizando
pila_funciones = []

def compatible_retorno(tipo_destino, tipo_origen):
    """
    Comprueba que el tipo retornado sea compatible
    con el tipo declarado de la funcion.
    """

    # Mismo tipo: permitido
    if tipo_destino == tipo_origen:
        return True

    # C# permite convertir int a double implicitamente
    if tipo_destino == "double" and tipo_origen == "int":
        return True

    # Los demas casos no son compatibles
    return False

def finalizar_funcion(garantiza_retorno, linea, lexpos):
    """
    Verifica si una funcion debe retornar un valor.
    """

    funcion = pila_funciones.pop()

    # Las funciones no void deben garantizar un retorno
    if funcion["tipo"] != "void" and not garantiza_retorno:

        registrar_error_semantico(
            f"[Retorno de funciones] La funcion "
            f"'{funcion['nombre']}' no retorna un valor "
            f"en todas las rutas de codigo",
            funcion["nombre"],
            linea,
            lexpos
        )

    # Restaurar las variables anteriores
    tabla_simbolos["variables"] = funcion["variables_anteriores"]

# Avance 3 - Regla 4: Preparar el contexto de la funcion
def p_preparar_funcion(p):
    """preparar_funcion : """

    # Obtener los datos de la funcion declarada
    tipo = p[-5]
    nombre = p[-4]
    parametros = p[-2] or []

    # Guardar el contexto de la funcion actual
    pila_funciones.append({
        "tipo": tipo,
        "nombre": nombre,
        "variables_anteriores": tabla_simbolos["variables"].copy()
    })

    # Registrar los parametros para reconocer sus tipos
    for nombre_parametro, tipo_parametro in parametros:
        registrar_variable(nombre_parametro, tipo_parametro, False)

# =========================================================
# FIN APORTE: Steven Avelino - savelinop
# =========================================================

parser = yacc.yacc()

import argparse
import os
import sys
from datetime import datetime

import lexer as lexico

SEPARADOR = "=" * 42


def leer_codigo(ruta_algoritmo):
    with open(ruta_algoritmo, "r", encoding="utf-8") as archivo:
        return archivo.read()


def encabezado(titulo, desarrollador, ruta_algoritmo, ahora):
    return [
        SEPARADOR,
        titulo,
        f"Desarrollador: {desarrollador}",
        f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M:%S')}",
        f"Archivo: {os.path.basename(ruta_algoritmo)}",
        SEPARADOR,
        "",
    ]


def guardar_log(prefijo, desarrollador, ahora, lineas):
    os.makedirs("logs", exist_ok=True)
    fecha = ahora.strftime("%d-%m-%Y-%Hh%Mm%Ss")
    ruta_log = os.path.join("logs", f"{prefijo}-{desarrollador}-{fecha}.txt")
    with open(ruta_log, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas))
    return ruta_log


def ejecutar_lexico(codigo, ruta_algoritmo, desarrollador):
    ahora = datetime.now()
    salida_log = encabezado(
        "ANALISIS LEXICO - C#", desarrollador, ruta_algoritmo, ahora
    )
    salida_log.append("TOKENS RECONOCIDOS:")

    print("\n--- TOKENS RECONOCIDOS ---")
    tokens_reconocidos, errores = lexico.analizar(codigo)

    for tok in tokens_reconocidos:
        linea = (
            f"[Linea {tok.lineno}] "
            f"TOKEN: {tok.type} | Valor: {tok.value}"
        )
        print(linea)
        salida_log.append(linea)

    salida_log.append("")
    salida_log.append("ERRORES LEXICOS:")

    if errores:
        salida_log.extend(lexico.formatear_error(e) for e in errores)
    else:
        salida_log.append("Sin errores lexicos")

    salida_log.append("")
    salida_log.append(f"Total tokens: {len(tokens_reconocidos)}")
    salida_log.append(f"Total errores: {len(errores)}")

    ruta_log = guardar_log("lexico", desarrollador, ahora, salida_log)

    print("\n--- RESULTADO ---")
    print(f"Tokens reconocidos: {len(tokens_reconocidos)}")
    print(f"Errores lexicos: {len(errores)}")
    print(f"Log generado: {ruta_log}")
    return 0


def cargar_sintactico():
    """Devuelve el modulo sintactico o None si aun no esta listo."""
    try:
        import sintactico
        sintactico.parser
        sintactico.errores_sintacticos
        sintactico.formatear_error
        return sintactico
    except Exception as error:
        print("El analizador sintactico aun no esta listo.")
        print(f"Motivo: {type(error).__name__}: {error}")
        print("sintactico.py debe definir 'parser', 'errores_sintacticos' "
              "y 'formatear_error'.")
        return None


def ejecutar_sintactico(codigo, ruta_algoritmo, desarrollador):
    sintactico = cargar_sintactico()
    if sintactico is None:
        return 1
    parser = sintactico.parser
    errores_sintacticos = sintactico.errores_sintacticos

    ahora = datetime.now()
    salida_log = encabezado(
        "ANALISIS SINTACTICO - C#", desarrollador, ruta_algoritmo, ahora
    )

    errores_sintacticos.clear()
    lexico.errores_lexicos.clear()
    lexico.lexer.lineno = 1

    print("\n--- ANALISIS SINTACTICO ---")
    parser.parse(codigo, lexer=lexico.lexer)

    salida_log.append("ERRORES SINTACTICOS:")
    if errores_sintacticos:
        salida_log.extend(
            sintactico.formatear_error(e) for e in errores_sintacticos
        )
    else:
        print("Sin errores sintacticos")
        salida_log.append("Sin errores sintacticos")

    salida_log.append("")
    salida_log.append("ERRORES LEXICOS ENCONTRADOS DURANTE EL ANALISIS:")
    if lexico.errores_lexicos:
        salida_log.extend(
            lexico.formatear_error(e) for e in lexico.errores_lexicos
        )
    else:
        salida_log.append("Sin errores lexicos")

    salida_log.append("")
    salida_log.append(f"Total errores sintacticos: {len(errores_sintacticos)}")
    salida_log.append(f"Total errores lexicos: {len(lexico.errores_lexicos)}")

    ruta_log = guardar_log("sintactico", desarrollador, ahora, salida_log)

    print("\n--- RESULTADO ---")
    print(f"Errores sintacticos: {len(errores_sintacticos)}")
    print(f"Errores lexicos: {len(lexico.errores_lexicos)}")
    print(f"Log generado: {ruta_log}")
    return 0


ANALISIS = {
    "lexico": ejecutar_lexico,
    "sintactico": ejecutar_sintactico,
}


def main():
    argumentos = argparse.ArgumentParser(
        description="Analizador de codigo C# (lexico y sintactico)."
    )
    argumentos.add_argument("analisis", choices=ANALISIS, help="analisis a ejecutar")
    argumentos.add_argument("archivo", help="ruta del algoritmo .cs")
    argumentos.add_argument("desarrollador", help="nombre para el log, ej. GeovannyDiaz")
    parametros = argumentos.parse_args()

    if not os.path.exists(parametros.archivo):
        print(f"Error: No se encontro {parametros.archivo}")
        return 1

    codigo = leer_codigo(parametros.archivo)
    return ANALISIS[parametros.analisis](
        codigo, parametros.archivo, parametros.desarrollador
    )


if __name__ == "__main__":
    sys.exit(main())

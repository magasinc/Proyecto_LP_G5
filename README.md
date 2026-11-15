# Analizador de Código C#

Compilador parcial para un subconjunto del lenguaje C#, desarrollado como proyecto académico para la materia **Ingeniería de Software II** (PAO 2 - 2026). El programa implementa las tres primeras fases de un compilador: análisis léxico, sintáctico y semántico.

## Integrantes (Grupo 10)

- Mateo Gallegos
- Steven Avelino
- Geovanny Díaz

## Descripción del Proyecto

El analizador recibe como entrada un archivo de código fuente en C# (`.cs`) y lo procesa en tres fases secuenciales:

### 1. Análisis Léxico (`lexer.py`)
Descompone el código fuente en **tokens** (las unidades mínimas del lenguaje). Reconoce:
- **Palabras reservadas**: `int`, `double`, `string`, `bool`, `char`, `var`, `const`, `if`, `else`, `while`, `for`, `return`, `break`, `continue`, `void`, `static`, `new`, `true`, `false`, `List`, `Dictionary`.
- **Literales**: enteros (`42`), decimales (`3.14`), cadenas (`"hola"`), caracteres (`'a'`).
- **Operadores**: aritméticos (`+`, `-`, `*`, `/`, `%`, `++`, `--`), lógicos (`&&`, `||`, `!`), relacionales (`==`, `!=`, `<`, `>`, `<=`, `>=`).
- **Delimitadores**: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `.`, `=`.
- **Identificadores**: nombres de variables y funciones.
- **Comentarios**: de línea (`//`) y de bloque (`/* */`).
- **Errores léxicos**: caracteres no reconocidos, cadenas sin cerrar, identificadores mal formados, decimales incompletos.

### 2. Análisis Sintáctico (`sintactico.py`)
Verifica que los tokens formen **estructuras gramaticalmente válidas** usando una gramática libre de contexto procesada con PLY (Python Lex-Yacc). Reglas soportadas:
- Declaración de variables con tipo explícito (`int x = 5;`) o inferido (`var x = 5;`).
- Declaración de constantes (`const double PI = 3.14;`).
- Asignación a variables existentes (`x = 10;`).
- Expresiones aritméticas encadenadas con precedencia (`a + b * c`).
- Expresiones booleanas con operadores lógicos y relacionales.
- Estructuras de control: `if / else / else if`, `while`, `for`.
- Funciones estáticas con parámetros opcionales y tipo de retorno.
- Entrada/salida: `Console.WriteLine(...)` y `Console.ReadLine()` / `Tipo.Parse(...)`.
- Estructuras de datos: arreglos (`int[] x = { 1, 2, 3 };`), `Dictionary<K,V>`, `List<T>`.
- Incremento y decremento (`i++`, `--j`).
- Llamadas a funciones como instrucciones y dentro de expresiones.

### 3. Análisis Semántico (`sintactico.py`)
Valida el **significado** del código durante el parseo mediante una tabla de símbolos. Reglas implementadas:
- **Compatibilidad de tipos en operaciones**: verifica que los operandos sean compatibles (ej: no sumar `bool + int`), soporta concatenación de cadenas con `+`, y promoción implícita de `int` a `double`.
- **Retorno de funciones**: verifica que las funciones no-void retornen un valor en todas las rutas, que el tipo retornado sea compatible con el declarado, y que las funciones `void` no retornen valores.
- **Contexto de estructuras de control**: `break` y `continue` solo dentro de bucles, `return` solo dentro de funciones.
- **Inmutabilidad de constantes**: las variables declaradas con `const` no se pueden reasignar.
- **Casting entre tipos**: solo se permite entre tipos numéricos (`int`, `double`, `char`).

## Requisitos

- Python 3.10 o superior
- Librería PLY (Python Lex-Yacc):
  ```bash
  pip install ply
  ```

## Uso

### Línea de comandos (`main.py`)

```bash
# Análisis léxico
python main.py lexico algoritmos/archivo.cs NombreDesarrollador

# Análisis sintáctico
python main.py sintactico algoritmos/archivo.cs NombreDesarrollador

# Análisis semántico
python main.py semantico algoritmos/archivo.cs NombreDesarrollador
```

Cada ejecución imprime los resultados en consola y genera un archivo de log en la carpeta `logs/`.

### Interfaz gráfica (`gui.py`)

```bash
python gui.py
```

La GUI permite abrir archivos `.cs`, editar código, ejecutar cualquier tipo de análisis y ver los resultados en pestañas de tokens, símbolos, errores y resumen.

## Estructura del Proyecto

```
Proyecto_LP_G10/
├── main.py                  # Punto de entrada por línea de comandos
├── gui.py                   # Interfaz gráfica con Tkinter
├── lexer.py                 # Analizador léxico (tokenización)
├── sintactico.py            # Analizador sintáctico y semántico
├── algoritmos/              # Archivos .cs de prueba
│   ├── algoritmo1_G.cs
│   ├── algoritmo_G_sintactico.cs
│   ├── algoritmo_G_semantico.cs
│   ├── algoritmo_GD_semantico.cs
│   ├── prueba_semantico_steven.cs
│   └── ...
├── logs/                    # Logs generados por cada ejecución
└── README.md
```

## Documento de Referencia

https://docs.google.com/document/d/1iiJ8Gs_BtlcygklOs9qubF6q8Om55HMMCtLZ1_hnIis/edit?usp=sharing

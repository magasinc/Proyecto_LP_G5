// Algoritmo de prueba - Geovanny Diaz (g30dl)
// Analizador Sintactico: constante, impresion y lectura, while,
// diccionario y funcion con parametro opcional.
//
// Parte 1: casos VALIDOS (0 errores sintacticos).
// Parte 2: casos INVALIDOS (cada uno debe reportar 1 error sintactico).
// Las variables no estan declaradas a proposito: eso es tema del semantico.
// Todo el archivo es lexicamente correcto (0 errores lexicos).

// ===================================================================
// PARTE 1: CASOS VALIDOS
// ===================================================================

// --- Regla 1: declaracion de constante ---
const double PI = 3.1416;
const int MAXIMO = 100;
const string SALUDO = "Hola";
const bool ACTIVO = true;
const char INICIAL = 'G';

// --- Regla 2: impresion y lectura ---
Console.WriteLine("Hola Mundo");
Console.WriteLine(total);
Console.WriteLine(a + b);
string entrada = Console.ReadLine();
int edad = int.Parse(Console.ReadLine());
double nota = double.Parse(Console.ReadLine());

// --- Regla 3: while, break y continue ---
while (contador < 5) {
    contador++;
}
while (true) {
    break;
}
while (contador < 10) {
    contador++;
    continue;
}
while (a < 3) {
    while (b < 3) {
        b++;
    }
    a++;
}

// --- Regla 4: diccionario generico ---
Dictionary<string, int> edades = new Dictionary<string, int>();
Dictionary<int, string> nombres = new Dictionary<int, string>();
Dictionary<string, double> precios = new Dictionary<string, double>();

// --- Regla 5: funcion con parametro opcional ---
static int Incrementar(int valor, int paso = 1) {
    return valor + paso;
}
static double Area(double ancho, double alto = 2.5) {
    return ancho * alto;
}
static string Saludar(string nombre, string saludo = "Hola") {
    return saludo;
}

// ===================================================================
// PARTE 2: CASOS INVALIDOS (cada linea marcada debe dar error sintactico)
// ===================================================================

// --- Constante ---
// INVALIDO C1: falta el '='
const double PI2 3.1416;
// INVALIDO C2: falta el tipo
const PI3 = 3.1416;
// INVALIDO C3: falta la expresion
const int MAXIMO2 = ;

// --- Impresion y lectura ---
// INVALIDO P1: falta ')' en WriteLine
Console.WriteLine("Hola";
// INVALIDO P2: ReadLine sin parentesis
string entrada2 = Console.ReadLine;
// INVALIDO P3: falta ')' en Parse
int edad2 = int.Parse(Console.ReadLine();
// INVALIDO P4: WriteLine sin parentesis
Console.WriteLine "Hola";

// --- while ---
// INVALIDO W1: condicion sin parentesis
while contador < 5 { contador++; }
// INVALIDO W2: condicion vacia
while () { contador++; }
// INVALIDO W3: sin llaves (valido en C#, pero la gramatica del PDF exige llaves)
while (contador < 5) contador++;
// INVALIDO W4: falta ';' despues de break
while (true) { break }

// --- Diccionario ---
// INVALIDO D1: falta la coma entre tipos
Dictionary<string int> d1 = new Dictionary<string, int>();
// INVALIDO D2: falta el '>' de cierre
Dictionary<string, int d2 = new Dictionary<string, int>();
// INVALIDO D3: falta el tipo del valor
Dictionary<string> d3 = new Dictionary<string>();
// INVALIDO D4: el constructor no tiene parentesis
Dictionary<string, int> d4 = new Dictionary<string, int>;

// --- Funcion con parametro opcional ---
// INVALIDO F1: parametro opcional sin valor por defecto
static int F1(int valor, int paso = ) { return valor; }
// INVALIDO F2: parametro opcional sin tipo
static int F2(int valor, paso = 1) { return valor; }
// INVALIDO F3: falta el tipo de retorno
static F3(int valor, int paso = 1) { return valor; }
// INVALIDO F4: falta la coma entre parametros
static int F4(int valor int paso = 1) { return valor; }
// INVALIDO F5: falta el nombre de la funcion
static int (int valor) { return valor; }
// INVALIDO F6: falta ';' despues de return
static int F6(int valor, int paso = 1) { return valor + paso }

// --- Fin de archivo inesperado ---
// INVALIDO X1: falta ';' al final del archivo (el error se reporta en el EOF)
const int LIMITE = 10

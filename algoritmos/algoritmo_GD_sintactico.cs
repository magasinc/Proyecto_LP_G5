// Algoritmo de prueba - Geovanny Diaz (g30dl)
// Analizador Sintactico: constante, impresion y lectura, while,
// diccionario y funcion con parametro opcional.
//
// Parte 1: casos VALIDOS (0 errores sintacticos).

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

// Algoritmo de prueba - Geovanny Diaz (g30dl)
// Analizador Semantico: Regla 5 (estructuras de control y contexto logico)
// y Regla 6 (conversion de tipos e inmutabilidad).
//
// Parte 1: casos VALIDOS (0 errores semanticos).
// Parte 2: casos INVALIDOS (cada caso marcado "ERROR" debe reportar 1 error semantico).
// Parte 3: casting entre tipos numericos (caso valido).
//
// Todo el archivo es lexica y sintacticamente correcto: el semantico asume sintaxis valida.
// Las variables no estan declaradas a proposito: eso es tema de la regla 1 (Mateo).

// ===================================================================
// PARTE 1: CASOS VALIDOS
// ===================================================================

// --- Regla 5: break y continue dentro de bucles ---
while (true) {
    break;
}
while (contador < 5) {
    contador++;
    continue;
}
for (int i = 0; i < 5; i++) {
    if (i == 2) {
        continue;
    }
    if (i == 4) {
        break;
    }
}
while (a < 3) {
    while (b < 3) {
        break;
    }
    break;
}

// --- Regla 5: condiciones booleanas en if y while ---
if (activo) {
    Console.WriteLine("Ok");
}
if (edad >= 18 && activo) {
    Console.WriteLine("Adulto");
} else {
    Console.WriteLine("Menor");
}
if (5 > 3) {
    Console.WriteLine("Comparacion");
}
while (!terminado) {
    break;
}

// --- Regla 6: constantes que solo se leen ---
const double PI = 3.14;
const int MAXIMO = 100;
double perimetro = PI * radio;
int limite = MAXIMO + 1;

// ===================================================================
// PARTE 2: CASOS INVALIDOS (cada linea marcada debe dar error semantico)
// ===================================================================

// --- Regla 5: la condicion debe ser bool ---
// ERROR E5: la condicion del if es int
if (5 + 3) {
    Console.WriteLine("Ok");
}
// ERROR E6: la condicion del while es int
while (10) {
    break;
}
// ERROR E7: la condicion del if es string
if ("hola") {
    Console.WriteLine("Ok");
}

// --- Regla 6: modificacion de una constante ---
const double GRAVEDAD = 9.8;
// ERROR E8: asignacion a una constante
GRAVEDAD = 10.5;
const int CAPACIDAD = 50;
// ERROR E9: incremento de una constante
CAPACIDAD++;

// ===================================================================
// PARTE 3: CASTING (regla 6)
// ===================================================================

// VALIDO: casting entre tipos numericos
double pi = 3.14;
int piEntero = (int)pi;
int entero = 7;
double decimalDeEntero = (double)entero;

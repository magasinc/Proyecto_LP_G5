// =====================================================================
// PRUEBA SEMANTICA CON ERRORES (Regla 1 y Regla 2 - Mateo Gallegos)
// Este archivo debe arrojar una cascada de errores semanticos.
// =====================================================================

// --- REGLA 1: Identificadores y Duplicados ---

int anio = 2026;
// ERROR: La variable 'anio' ya esta declarada en este contexto.
int anio = 2027; 

double presupuesto = 5000.00;
// ERROR: Intento de volver a declarar con un tipo diferente.
bool presupuesto = false;

// ERROR: 'precio' no existe en el contexto actual (Uso de variable fantasma).
precio = 99.99; 

// --- REGLA 2: Compatibilidad de Tipos y Perdida de Informacion ---

double distancia = 150.75;
// ERROR: Posible perdida de informacion (asignar un double a un int trunca los decimales).
int distanciaMetros = distancia; 

// ERROR: Tipos totalmente incompatibles (asignar un string a un entero).
int codigoSeguridad = "Secreto";

// ERROR: Tipos totalmente incompatibles (asignar un booleano a un double).
double factor = true;

// --- REGLA CONSTANTES ---

const int MAXIMO_ALUMNOS = 30;
// ERROR: No se puede reasignar un valor a una constante.
MAXIMO_ALUMNOS = 35;

// --- ERRORES COMBINADOS EN BLOQUES ---

if (anio > 2020) {
    // ERROR: 'descuento' no esta declarada en el contexto actual.
    // ERROR: 'total' tampoco esta declarada.
    total = total - descuento;
}
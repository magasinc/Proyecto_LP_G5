// =========================================================
// Algoritmo de prueba Avance 2 - Mateo Gallegos (magasinc)
// =========================================================

// ---------------------------------------------------------
// PARTE 1: CASOS VÁLIDOS (Código funcional)
// ---------------------------------------------------------

// 1. Declaración y asignación básica
int edadEstudiante = 17;
int limiteEdad = 18;
edadEstudiante = 19; // Reasignación

// 3. Estructura de Datos: Arreglo
int[] calificaciones = { 10, 8, 9 };

// 4. Declaración de Función con retorno y parámetros
static int SumarPuntos(int bono, int extra) {
    int resultado = bono + extra;
    return resultado;
}

// 2. Estructura de Control: if / else (con llamado a función y lógica)
if (edadEstudiante >= limiteEdad) {
    Console.WriteLine("Mayor");
} else {
    Console.WriteLine("Menor");
}

// ---------------------------------------------------------
// PARTE 2: CASOS INVÁLIDOS (Errores sintácticos intencionales)
// ---------------------------------------------------------

// ERROR A: Falta el punto y coma (;) al final
int puntaje = 100

// ERROR B: Falta el paréntesis de apertura en la condición del if
if edadEstudiante > 15) { Console.WriteLine("Error"); }

// ERROR C: Falta la coma (,) separadora en el arreglo
int[] valores = { 10 20 };
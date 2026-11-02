// Algoritmo de prueba - Geovanny Diaz (g30dl)
// Analizador Lexico: palabras reservadas y errores lexicos

// ===== PARTE 1: PALABRAS RESERVADAS =====

// if / else
if (activo) {

} else {

}

// while con continue y break
while (activo) {
    continue;
    break;
}

// for
for (;;) {
    break;
}

// Funciones: static, void y return
static void Saludar() {
    return;
}
static int Obtener() {
    return valor;
}

// new y Dictionary
Dictionary<string, int> edades = new Dictionary<string, int>();

// ===== PARTE 2: ERRORES LEXICOS =====
valor = 5 # 2;
cadena = "sin cerrar
letra = 'ab';
2abc = 1;
numero = 3.;

// El comentario sin cerrar debe ir al final: consume hasta el fin del archivo.
/* comentario sin cerrar

// Algoritmo de prueba con errores - Geovanny Diaz (g30dl)
// Analizador Semantico: Regla 5 (break, continue y return fuera de contexto)
// y Regla 6 (casting entre tipos incompatibles).
//
// Cada caso marcado "ERROR" debe reportar exactamente 1 error semantico.
// Todo el archivo es lexica y sintacticamente correcto: el semantico asume sintaxis valida.

// ===================================================================
// REGLA 5: break, continue y return fuera de su contexto
// ===================================================================

// ERROR E1: break fuera de un bucle
break;
// ERROR E2: continue fuera de un bucle
continue;
// ERROR E3: return fuera de una funcion
return 5;
// ERROR E4: break dentro de un if, pero sin bucle que lo contenga
if (activo) {
    break;
}
// ERROR E5: break dentro de una funcion, pero sin bucle
static void Detener() {
    break;
}

// ===================================================================
// REGLA 6: casting entre tipos incompatibles
// ===================================================================

string texto = "123";
int entero = 7;
// ERROR E6: casting incompatible, string a int
int num = (int)texto;
// ERROR E7: casting incompatible, int a bool
bool bandera = (bool)entero;
// ERROR E8: casting incompatible, literal bool a int
int desdeBool = (int)true;

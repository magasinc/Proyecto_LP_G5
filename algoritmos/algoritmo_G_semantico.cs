// =====================================================================
// PRUEBA SEMANTICA EXITOSA (Regla 1 y Regla 2 - Mateo Gallegos)
// Todo el codigo en este archivo debe pasar sin errores semanticos.
// =====================================================================

// 1. Declaraciones correctas sin duplicados (Regla 1)
int edad = 25;
double salario = 1500.50;
char inicial = 'M';
bool esValido = true;
string nombre = "Mateo";
const double PI = 3.14159;

// 2. Conversiones implicitas permitidas (Regla 2)
// C# permite pasar un 'int' a un 'double', y un 'char' a un 'int'
int codigoAscii = inicial; 
double salarioConBono = edad; 
double calculoDesdeChar = inicial;

// 3. Reasignaciones validas a variables existentes (Regla 1 y 2)
salario = 2000.75;
edad = 26;

// 4. Uso de identificadores correctamente declarados en expresiones y bloques
if (edad >= 18) {
    int bono = 250;
    
    // Todo existe y los tipos son compatibles
    salario = salario + bono;
    
    // Otra asignacion de int a double valida
    double totalAcumulado = bono; 
}
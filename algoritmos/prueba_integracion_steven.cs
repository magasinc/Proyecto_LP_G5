// Steven Avelino - Prueba final correcta
// Avance 2 - Analizador sintactico

// Variables
const int limite = 3;
int contador = 0;
bool activo = true;

var nombre = "Steven";
var total = (10 + 5) * 2;

// Expresiones booleanas
var autorizado = (total >= 20 && activo) || !activo;

// Lectura por teclado - Geovanny
string entrada = Console.ReadLine();
int edad = int.Parse(Console.ReadLine());

// Diccionario - Geovanny
Dictionary<string, int> edades = new Dictionary<string, int>();

// Lista generica - Steven
List<int> notas = new List<int> {8, 9, 10};
List<string> nombres = new List<string>();

// Funcion void - Steven
static void Mostrar(string texto) {
    Console.WriteLine(texto);
}

// Funcion con retorno y parametro opcional
static int Incrementar(int numero, int paso = 1) {
    return numero + paso;
}

// Ciclo for - Steven
for (int i = 0; i < limite; i++) {
    Console.WriteLine(i);
}

// Ciclo while - Geovanny
while (contador < limite && activo) {
    contador++;
}

// Llamadas a funciones
Mostrar(nombre);

int resultado = Incrementar(5, 2);

Console.WriteLine(resultado);
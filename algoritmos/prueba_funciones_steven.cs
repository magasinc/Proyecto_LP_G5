

// Funcion void con parametro
static void Saludar(string nombre) {
    Console.WriteLine(nombre);
}

// Funcion con retorno int
static int Sumar(int a, int b) {
    return a + b;
}

// Funcion con retorno double
static double Multiplicar(double a, double b) {
    return a * b;
}

// Funcion void sin parametros
static void MostrarMensaje() {
    Console.WriteLine("Analizador funcionando");
}

// Llamadas a las funciones
Saludar("Steven");

int resultado = Sumar(10, 5);

double producto = Multiplicar(2.5, 4.0);

MostrarMensaje();

Console.WriteLine(resultado);
Console.WriteLine(producto);
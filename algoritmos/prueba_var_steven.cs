var nombre = "Steven";
var edad = 21;
var promedio = 9.5;
var activo = true;
var letra = 'A';
var suma = 10 + 5;
var resta = 20 - 8;
var producto = 5 * 4;
var division = 20 / 2;
var residuo = 10 % 3;
var resultado = (10 + 5) * 2 - 4;
// Steven Avelino - Expresiones booleanas

var esMayor = edad >= 18;

var tieneAcceso = edad >= 18 && activo;

var esValido = activo || esMayor;

var noActivo = !activo;

var resultadoLogico = (edad >= 18 && activo) || !activo;

// Prueba de compatibilidad con el while de Geovanny
while (edad > 0 && activo) {
    Console.WriteLine("Condicion valida");
}

// Steven Avelino - Prueba de estructura FOR

// Ciclo con incremento
for (int i = 0; i < 5; i++) {
    Console.WriteLine(i);
}

// Ciclo con decremento
for (int j = 5; j > 0; j--) {
    Console.WriteLine(j);
}

// Ciclo con var
for (var k = 0; k < 3; k++) {
    Console.WriteLine(k);
}

// Ciclo con actualizacion por asignacion
for (int x = 0; x < 10; x = x + 2) {
    Console.WriteLine(x);
}


// Steven Avelino - Prueba de listas genericas

// Lista vacia de enteros
List<int> valores = new List<int>();

// Lista de nombres con elementos
List<string> nombres = new List<string> {
    "Steven", "Eddy", "Carlos"
};

// Lista de decimales
List<double> notas = new List<double> {
    8.5, 9.0, 10.0
};

// Lista de booleanos
List<bool> estados = new List<bool> {
    true, false, true
};
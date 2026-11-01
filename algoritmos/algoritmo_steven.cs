
using System;
using System.Collections.Generic;

// ==========================================
// Algoritmo de prueba - Steven Avelino
// Avance 1 - Analizador Lexico C#
// ==========================================

class Programa
{
    static void Main()
    {
        int a = 10;
        int b = 3;

        // Operadores aritmeticos
        int suma = a + b;
        int resta = a - b;
        int producto = a * b;
        int division = a / b;
        int residuo = a % b;

        a++;
        b--;

        // Operadores relacionales
        bool mayor = a > b;
        bool menor = a < b;
        bool mayorIgual = a >= b;
        bool menorIgual = a <= b;
        bool iguales = a == b;
        bool diferentes = a != b;

        // Operadores logicos
        bool resultado = (mayor && diferentes)
                         || !iguales;

        // Arreglos y listas
        int[] numeros = {1, 2, 3};
        List<int> lista = new List<int> {4, 5};

        // Mostrar resultados
        Console.WriteLine(suma);
        Console.WriteLine(resta);
        Console.WriteLine(producto);
        Console.WriteLine(division);
        Console.WriteLine(residuo);
        Console.WriteLine(resultado);
        Console.WriteLine(numeros[0] + lista[0]);
    }
}

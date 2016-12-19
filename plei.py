#!/usr/bin/python3.5

"""
    Author: Seykotron
    Date: 19/12/2016
    Title: PythonLispExpresionInterpreter
    Comment: This module solve Lisp Expresion giving the expresion as string and the values as dict "key": true|false

    Example usage:
    Python 3.5.2 (default, Nov 17 2016, 17:05:23)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from plei import Plei
    >>> expresionS = "(OR (NOT VAL1) (AND VAL1 VAL2) )"
    >>> operandos = { "VAL1" : True, "VAL2" : False }
    >>> a = Plei( expresionS, operandos )
    Expresion: (OR (NOT VAL1) (AND VAL1 VAL2) )
    Operandos:
    {'VAL1': True, 'VAL2': False}
    Solucion:
    ----------------------------------------------------------
    ['OR', 'NOT']
    VAL1
    NOT
    Operando el NOT sobre VAL1
    VAL1 vale True
    ['OR', False, 'AND', 'VAL1']
    VAL2
    VAL1
    AND
    Operando el AND sobre VAL1 y VAL2
    VAL1 vale True
    VAL2 vale False
    ['OR', False, False]
    False
    False
    OR
    Operando el OR sobre False y False
    ----------------------------------------------------------
    Resultado: False
"""
import types

class Plei:

    """
        Estos son los operadores definidos por defecto, se pueden agregar más agregando aquí una entrada y la
        correspondiente acción en el metodo operar()
    """
    operadores = [
        "AND",
    	"OR",
    	"NOT",
    	">",
    	"<",
    	">=",
    	"<=",
    	"=="
    ]

    """
        La pila se usa para ir almacenando los operadores y operandos en el orden en el que van llegando,
        esta pila se gestiona de manera LIFO para resolver la expresion LISP
    """
    pila = []

    def __init__(self, lisp, valores, verbose=True ):
        """
            Constructor de la clase
            por defecto el verbose está activado asi que mostrará por pantalla informacion
        """
        if len(lisp) == 0:
            print("La expresion LISP no puede estar vacía.")
            quit()
        if len(valores) == 0:
            print("Los valores de las variables no pueden estar vacíos")

        #Reinicio la pila
        self.pila = []
        self.lisp = lisp
        self.valores = valores
        self.verbose = verbose

        self.resultado = self.resolver()

    def getResultado( self ):
        """
            Devuelve el resultado de la operacion LISP si existe
        """
        return self.resultado

    def operar( self, op, operNombres):
        """
            Este metodo opera y agrega a la pila el resultado de la operacion,
            en operNombres esta el nombre de la variable que
            es la key del dict "valores" que se le da al constructor de la clase,
            op es la operación a realizar, y deberá existir en la lista de operadores
            Y la pila es la pila del programa en la que se van guardando las operaciones que se van realizando
        """
        self.pila.pop()
        if op == "AND" :
            self.log("Operando el AND sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 and val2 )
        elif op == "OR":
            self.log("Operando el OR sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 or val2 )
        elif op == "NOT":
            self.log("Operando el NOT sobre "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[0])
            self.pila.append( not val1 )
        elif op == ">":
            self.log("Operando el > sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 > val2 )
        elif op == "<":
            self.log("Operando el < sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 < val2 )
        elif op == ">=":
            self.log("Operando el >= sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 >= val2 )
        elif op == "<=":
            self.log("Operando el <= sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 <= val2 )
        elif op == "==":
            self.log("Operando el == sobre "+str(operNombres[1])+" y "+str(operNombres[0]) )
            val1 = self.getValor(operNombres[1])
            val2 = self.getValor(operNombres[0])
            self.pila.append( val1 == val2 )
        """
            Agregar aquí el código si se agregan más operadores con nuevas entradas de elif
        """

    def getValor( self, o ):
        """
            Si el valor es un boolean true o false, devuelve el valor pasado por parámetro,
            si el valor es un string lo busca en las claves del dict valores y devuelve su
            valor booleano (true o false)
        """
        if type(o) == bool:
            return o
        else:
            self.log( str(o)+" vale "+str(self.valores[o]))
            return self.valores[o]

    def log( self, texto ):
        """
            Este metodo escribe por pantalla si el verbose esta activado.
            Por defecto el verbose está activado
        """
        if self.verbose:
            print( texto )

    def resolver( self ):
        """
            Este metodo resuelve la expresion LISP dada al constructor de esta clase y retorna el valor solución
            si no obtiene el resultado devuelve None
        """
        if len(self.lisp) > 0:
            operandos = self.valores
            self.log("Expresion: "+self.lisp)
            self.log("Operandos:")
            self.log( operandos )
            self.log("Solucion: ")
            self.log("----------------------------------------------------------")

            #Seteo esta variable vacía
            palabra = ""

            #Itero por cada caracter de la expresion LISP
            for caracter in self.lisp:
                #Si es un caracter de apertura de parentesis o un espacio
                if caracter == "(" or caracter == " ":
                    #Si la palabra contiene algo
                    if len(palabra) > 0:
                        #Se agrega a la pila la palabra
                        self.pila.append(palabra)
                        #Se vacía la palabra
                        palabra = ""
                    #Si no es un caracter de abrir parentesis, espacio o cerrar parentesis entonces es un caracter perteneciente
                    #a una palabra
                elif caracter != "(" and caracter != " " and caracter != ")":
                    #concateno el caracter a la palabra
                    palabra += caracter
                #Si es un caracter de cierre de parentesis entonces hay que resolver la expresion contenida dentro de ese paréntesis
                elif caracter == ")":
                    #Imprimo la pila
                    self.log( self.pila )
                    #Si había una palabra almacenada, la agrego a la pila
                    if len(palabra) > 0:
                        self.pila.append( palabra )
                        palabra = ""

                    #Inicializo el array de los nombres de los operandos (los valores)
                    operNombres = []

                    #Por cada operacion en la pila (de manera reversa) es decir last in first out LIFO
                    for op in reversed(self.pila):
                        self.log( op )
                        #Si el operador de la pila no está en los operadores, entonces es un operando (un valor o variable)
                        if op not in self.operadores:
                            #Agrego el operando a la lista de nombres de operandos
                            operNombres.append(op)
                            #Extraigo dicho operando de la pila
                            self.pila.pop()
                        # Si el operador de la pila está en los operadores, entonces es una operación
                        # OJO las operaciones en LISP siempre van después de los operandos (viendo la pila en el orden en el que
                        # la estamos tratando, es decir de arriba abajo) por lo tanto los operandos ya deberían estar en su posicion
                        # en la lista de operandos.
                        else:
                            # Le pasamos al metodo operar los valores para que haga lo suyo
                            self.operar( op, operNombres )
                            # Interrumpimos el bucle para no contiunar resolviendo la expresion LISP
                            # ya que podríamos estar en el medio de esta y faltarnos valores para resolverla
                            break

            self.log( "----------------------------------------------------------" )

            if len(self.pila) == 1:
                self.log( "Resultado: "+str(self.pila[0]) )
                return self.pila[0]
            else:
                return None
        else:
            self.log("La Expresión no puede estar vacía")

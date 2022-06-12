# clases.py
# por Nadia Garcia y Sofia Vega (2022)
# Clases de apoyo que representan las estructuras de datos
# requeridas para el buen funcionamiento de nuestro compilador

from errores import *


# NODO ARREGLO
# Clase que representa la estructura de uno de los nodos generados
# por la linked list de representación de un arreglo
class NodoArreglo():

    def __init__(self, r=1, var="", ls=0, dim=1, dirLS=0):
        self.li = 0                 # Límite inferior, siempre empieza en 0
        self.ls = int(ls)           # Límite superior
        self.dim = dim              # Dimensión
        self.ultimoNodo = True      # Último nodo
        self.r = r                  # R
        self.var = var              # Valor casilla inferior (mdim o -k)
        self.siguienteNodo = None   # Siguiente nodo
        self.dirLS = dirLS          # Dirección del límite superior

    # SET NEXT NODE
    # Función que modifica el apuntador de siguiente nodo a el nodo siguiente
    def setNextNode(self, nodo):
        self.ultimoNodo = False
        self.siguienteNodo = nodo

    # CALC R
    # Función que calcula el valor de r y lo actualiza en el objeto
    def calcR(self):
        self.r = (self.ls + 1) * self.r

    # SET VAL
    # Función que actualiza el valor de var
    def setVal(self, val):
        self.val = val

    # IMPRIMIR
    # Función que imprime los datos calculados y necesarios de un nodo
    def imprimir(self):
        print("li " + str(self.li) + " ls " + str(self.ls) + " dim " +
              str(self.dim) + " ultimoNodo " + str(self.ultimoNodo))


# CLASE OPCIONES
# Clase que modela la estructura propia del lenguaje OPCIONES
class Opciones():

    def __init__(self):
        self.cap = ""  # capítulo en el que están las opciones
        self.strs = []
        self.caps = []
        self.saltos = []
        self.choice = 0

    # AGREGA OPCIÓN
    # Función que agrega la información de la opción a las pilas de atributos de las Opciones
    def agregaOpcion(self, str, opt, salto):
        self.strs.append(str)
        self.caps.append(opt)
        self.saltos.append(salto)


# TABLA DE CONSTANTES
# Clase que modela la tabla de constantes
class TablaConstantes():
    def __init__(self):
        self.mv = []            # Memoria virtual

    # ADD CTE
    # Función para agregar constante a tabla de constantes
    def addCte(self, val, dir):
        t = [dir, val]
        self.mv.append(t)

    # GET DIR
    # Función para obtener dirección de memoria virtual de una constante
    def getDir(self, val):
        for i in self.mv:
            if i[1] == val:
                return i[0]

    # TO TXT
    # Función para crear un archivo txt con la lista de constantes generadas
    def toTxt(self):
        f = open("tablaCtes.txt", "w")
        for m in self.mv:
            f.write(str(m[0])+' '+str(m[1]) + '\n')
        f.close()

# VARIABLE CLASS
# Clase que modela una variable y sus atributos


class VariableClass():
    '''
    Constructor de Variable

    Parámetros:
    - nameVar : string -> nombre de la variable
    - typeVar : string ->  tipo de la variable (numero, enunciado, bool, arreglo)
    - valueVar : [numero, bool, enunciado, arreglo] -> valor de la variable de acuerdo a su tipo
    - scopeVar : string -> scope de la variable
    - addressVar : int -> dirección de memoria virtual
    - isArray : bool
    - arrNode : la primera dimension del arreglo
    '''

    def __init__(self, nameVar, typeVar, valueVar='', addressVar=''):
        self.nameVar = nameVar
        self.typeVar = typeVar
        self.valueVar = valueVar
        self.addressVar = addressVar
        self.isArray = False
        self.arrNode = None

    # PRINT VAR
    # Función para imprimir la información pertinente de una variable
    def printvar(self):
        print("[nameVar: {} typeVar: {} valueVar: {} addressVar: {}]".format(
            self.nameVar, self.typeVar, self.valueVar, self.addressVar))

# FUNCTION CLASS
# Clase que modela una función y sus atributos pertinentes


class FunctionClass:
    '''
    Constructor de Function

    Parámetros:
    - nameFunc : string -> nombre de la función
    - typeFunc : string ->  tipo de retorno de la función (numero, enunciado, bool, arreglo, void)
    - paramsFunc : [] -> arreglo de parametros de tipo variable, o constante
    - scopeFunc : string -> scope de la función
    - addressFunc : int -> numero de cuádruplo donde inicia la función
    - quad_inicial: numero de cuádruplo donde inicia la función
    '''

    def __init__(self, nameFunc, typeFunc, paramTipos=[], scopeFunc="", addressFunc="", numParam=0, numVar=0, quad_inicial=0):
        self.nameFunc = nameFunc
        self.typeFunc = typeFunc
        self.paramTipos = paramTipos
        self.scopeFunc = scopeFunc
        self.addressFunc = addressFunc
        self.varsFunc = VariableTable()
        self.numParam = numParam
        self.numVar = numVar
        self.quad_inicial = quad_inicial
        self.keysParam = []

    # ADD PARAM
    # Función que agrega los parámetros a la tabla de variables de la función
    def addParam(self, tipo, id_param, address):
        # to do: los parametros se agregan como variables?
        var = VariableClass(id_param, tipo, addressVar=address)
        self.varsFunc.addVar(var)
        self.numParam = self.numParam + 1
        self.keysParam.append(id_param)
        # self.paramsFunc.append(var)

    # ADD VAR
    # Función que agrega variables a la tabla de variables de la función
    def addVar(self, varObject):
        self.varsFunc.addVar(varObject)
        self.numVar = self.numVar + 1

    # ADD TIPO
    # Función que agrega el tipo a la lista de tipos de los parámetros de la función
    def addTipo(self, tipo):
        self.paramTipos.append(tipo)

    # PRINT FUNC
    # Función que imprime la información pertinente de la función
    def printfunc(self):
        print("[nameFunc: {} typeFunc: {} paramTipos: {} scopeFunc: {} addressFunc: {}]".format(
            self.nameFunc, self.typeFunc, self.paramTipos, self.scopeFunc, self.addressFunc))
        print("variables")
        self.varsFunc.printTable()

# PROC DIRECTORY
# Clase Directorio de Procedimientos


class ProcDirectory:
    def __init__(self):
        self.procDirectory = {}     # Diccionario de procedimientos/funciones

    # ADD FUNC
    # Función que agrega una función al Directorio de Procedimientos
    # INPUT: Función a ser agregada
    def addFunc(self, funcObject):
        if not (self.checkDuplicate(funcObject.nameFunc)):
            self.procDirectory[funcObject.nameFunc] = funcObject
            print("Function added")

    # PRINT TABLE
    # Función que imprime el Directorio de Procedimientos
    def printTable(self):
        for item in self.procDirectory.items():
            print(item)
            item[1].printfunc()

    # FIND FUNCTION
    # Función que ayuda a encontrar la función deseada en el directorio de procedimientos
    # INPUT: nombre de la función como llave
    # OUTPUT: True o False, de acuerdo a si fue encontrada
    def findFunction(self, key):
        if key in self.procDirectory:
            return True
        else:
            return False

    # CHECK DUPLICATE
    # Función que revisa si la función ya fue agregada previamente
    # INPUT: Nombre de la función
    # OUTPUT: True si ya se encuentra registrada, False si no
    def checkDuplicate(self, key):
        if key in self.procDirectory:
            errorReFunc(key)
            return True
        else:
            return False

    # GET FUNC
    # Función que retorna la función del directorio
    # INPUT: nombre de la función
    def getFunc(self, name):
        return self.procDirectory[name]


# VARIABLE TABLE
# Clase que representa una tabla de variables
class VariableTable:
    def __init__(self):
        self.tablaVar = {}  # Diccionario que representa la tabla de variables

    # ADD VAR
    # Función que agrega una variable a la tabla de variables
    def addVar(self, varObject):
        if not (self.checkDuplicate(varObject.nameVar)):
            self.tablaVar[varObject.nameVar] = varObject

    # PRINT TABLE
    # Función que imprime la tabla de variables
    def printTable(self):
        for item in self.tablaVar.items():
            print(item)
            item[1].printvar()

    # CHECK DUPLICATE
    # Función que revisa si la variable a agregar sería un duplicado de una variable ya existente
    # INPUT: Nombre de la variable
    # OUTPUT: True si la función ya existe, o False si no
    def checkDuplicate(self, key):
        if key in self.tablaVar:
            errorReVar(key)
            return True
        else:
            return False

    # CHECK EXISTS
    # Función que revisa si una variable existe en el contexto actual
    # INPUT: Nombre de la variable
    # OUTPUT: True o False, dependiendo si fue encontrada
    def checkExists(self, key):
        if key in self.tablaVar:
            return True
        else:
            errorVariableNoExiste(key)
            return False

    # GET TYPE
    # Función que obtiene el tipo de una variable
    def getType(self, key):
        if key in self.tablaVar:
            return self.tablaVar[key].typeVar
        else:
            errorVariableNoExiste(key)
            return False


#   CLASE CUADRUPLOS
#   Un cuádruplo es una estructura de tipo registro con cuatro campos:
#   {operador, operando_izquierdo, operando_derecho, resultado}
#
#   Esta clase albergará todas las funciones relacionadas con esta estructura
class Cuadruplos():
    def __init__(self):
        self.cuadruplosID = []  # Lista de cuádruplos con identificadores
        self.cuadruplosMem = []  # Lista de cuádruplos con direcciones de memoria
        self.quad_pointer = 0   # Contador/Apuntador de cuádruplo

    #   GENERA ARCHIVOS
    #   Función que genera dos archivos de texto, uno con los cuádruplos con
    #   identificadores y otro con los cuádruplos con direcciones de memoria
    #   para ser interpretados por la máquina virtual
    def generaArchivos(self):
        f = open("cuadruplosID.txt", "w")
        for quad in self.cuadruplosID:
            f.write(str(quad)+'\n')
        f.close()

        f = open("cuadruplosMem.txt", "w")
        for quad in self.cuadruplosMem:
            f.write(str(quad)+'\n')
        f.close()

    def print_quad(self):
        print(self.quad_pointer + 1, self.cuadruplosID[-1])

    #   GENERATE QUAD
    #   Función que genera los cuádruplos con identificadores y los agrega a la
    #   lista de cuádruplos con identificadores
    def generate_quad(self, operator, left, right, result):
        cuadruplo = {"operator": operator, "left": left,
                     "right": right, "result": result}
        self.cuadruplosID.append(cuadruplo)
        self.quad_pointer = self.quad_pointer + 1

    def generate_quad_mem(self, operator, left, right, result):
        cuadruplo = {"operator": operator, "left": left,
                     "right": right, "result": result}
        self.cuadruplosMem.append(cuadruplo)

    #   FILL QUAD
    #   Función que regresa a un cuádruplo generado con identificadores con ____
    #   en la casilla de result para meter el número de cuádruplo al que tendrá
    #   que tiene que brincar
    #   Por lo general, para gotos
    def fill_quad(self, end, cont):
        self.cuadruplosID[end]["result"] = cont

    #   FILL QUAD MEM
    #   Función que regresa a un cuádruplo con direcciones de memoria virtuales
    #   con ____ en la casilla de result para meter el número de cuádruplo al
    #   que tendrá que tiene que brincar
    #
    #   Por lo general, para gotos
    def fill_quad_mem(self, end, cont):
        self.cuadruplosMem[end]["result"] = cont

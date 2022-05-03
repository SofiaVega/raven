# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Tabla de variables

# Clase Variable para la creación de variables y sus atributos
class VariableClass:
    '''
    Constructor de Variable

    Parámetros:
    - nameVar : string -> nombre de la variable
    - typeVar : string ->  tipo de la variable (numero, enunciado, bool, arreglo)
    - valueVar : [numero, bool, enunciado, arreglo] -> valor de la variable de acuerdo a su tipo
    - scopeVar : string -> scope de la variable
    - addressVar : int -> direccion de memoria virtual
    '''

    def __init__(self, nameVar, typeVar, valueVar, scopeVar, addressVar):
        self.nameVar = nameVar
        self.typeVar = typeVar
        self.valueVar = valueVar
        self.scopeVar = scopeVar
        self.addressVar = addressVar

    def printvar(self):
        print("[nameVar: {} typeVar: {} valueVar: {} scopeVar: {} addressVar: {}]".format(
            self.nameVar, self.typeVar, self.valueVar, self.scopeVar, self.addressVar))


# Tabla de Variables
class VariableTable:
    def __init__(self):
        self.tablaVar = {}

    def addVar(self, varObject):
        self.tablaVar[varObject.nameVar] = varObject
        print("Variable added")

    def printTable(self):
        for item in self.tablaVar.items():
            print(item)
            item[1].printvar()


# Clase Funcion para la creación de funciones y sus atributos
class FunctionClass:
    '''
    Constructor de Function

    Parámetros:
    - nameFunc : string -> nombre de la funcion
    - typeFunc : string ->  tipo de retorno de la funcion (numero, enunciado, bool, arreglo, void)
    - paramsFunc : [] -> arreglo de parametros de tipo variable, o constante
    - scopeFunc : string -> scope de la funcion
    - addressFunc : int -> numero de cuadruplo donde inicia la funcion
    '''

    def __init__(self, nameFunc, typeFunc, paramsFunc, scopeFunc, addressFunc):
        self.nameFunc = nameFunc
        self.typeFunc = typeFunc
        self.paramsFunc = paramsFunc
        self.scopeFunc = scopeFunc
        self.addressFunc = addressFunc
        self.varsFunc = VariableTable()

    def printfunc(self):
        print("[nameFunc: {} typeFunc: {} paramsFunc: {} scopeFunc: {} addressFunc: {}]".format(
            self.nameFunc, self.typeFunc, self.paramsFunc, self.scopeFunc, self.addressFunc))


# Directorio de procedimientos
class ProcDirectory:
    def __init__(self):
        self.procDirectory = {}

    def addFunc(self, funcObject):
        self.procDirectory[funcObject.nameFunc] = funcObject
        print("Function added")

    def printTable(self):
        for item in self.procDirectory.items():
            print(item)
            item[1].printfunc()

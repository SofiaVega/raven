# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Tabla de variables

# Clase Variable para la creación de variables y sus atributos
from lark import Visitor

id_Asignar = ""
pilaO = []
pOper = []
pSaltos = []



# Tabla de Variables
class VariableTable:
    def __init__(self):
        self.tablaVar = {}

    def addVar(self, varObject):
        self.tablaVar[varObject.nameVar] = varObject
        print("Variable added")

    def asignar(self, name, new_value):
        self.tablaVar[name]

    def printTable(self):
        for item in self.tablaVar.items():
            print(item)
            item[1].printvar()


#pilaO y poper
tabla_variables = VariableTable()



class VariableClass(Visitor):
    '''
    Constructor de Variable

    Parámetros:
    - nameVar : string -> nombre de la variable
    - typeVar : string ->  tipo de la variable (numero, enunciado, bool, arreglo)
    - valueVar : [numero, bool, enunciado, arreglo] -> valor de la variable de acuerdo a su tipo
    - scopeVar : string -> scope de la variable
    - addressVar : int -> direccion de memoria virtual
    '''
    '''
    def __init__(self, nameVar, typeVar, valueVar, scopeVar, addressVar):
        self.nameVar = nameVar
        self.typeVar = typeVar
        self.valueVar = valueVar
        self.scopeVar = scopeVar
        self.addressVar = addressVar
        '''

    def printvar(self):
        print("[nameVar: {} typeVar: {} valueVar: {} scopeVar: {} addressVar: {}]".format(self.nameVar, self.typeVar, self.valueVar, self.scopeVar, self.addressVar))
    def np_hola(self, tree):
        print("hola")

    def np_asignacion_1(self, tree):
        #revisar si existe en la tabla de variables
        id = tree.children[0].value
        id_Asignar = id
        if id in tabla_variables.tablaVar.keys():
            print("todo bien")

        else:
            print("ERROR")

        print("np 1")
    def np_asignacion_2(self, tree):
        #actualizar el valor
        print("np 2")
        print(tree.children[0].value)
        #tabla_variables.tablaVar[id_Asignar]. tree.children[0.value]
    '''
    def asignacion(self, tree):
        print("ASIGNACION")
        print(tree)
        print(tree.children[0].value)
        print(tree.children[0].line)
        print(tree.children[0])
        #print(tree.children[0])
    '''
    
    def idd(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        print("arbol en id")
        print(tree)
        print(tree.children)
        miid = tree.children[1].value
        print("mi id")
        print(miid)
        pilaO.append(miid)
    
    def f(self, tree):
        #2.- POper.Push(* or /)
        print("hijos de f")
        print(tree.children)
        signo = tree.children[0].value
        pOper.append(signo)

    def e(self, tree):
        # 3.- POper.Push(+ or - )
        print("hijos de e")
        print(tree.children)
        signo = tree.children[0].value
        pOper.append(signo)




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

# x = 5
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


class Test(Visitor):
    def printTree(self, tree):
        print(tree.pretty())

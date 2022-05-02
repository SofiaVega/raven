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

class NodoArreglo():
    """
    Nodo arreglo
        Limite inferior
        Limite Superior
        Dim
        SiguenteNodo
        val: mdim o -k
        ultimoNodo: booleano
        r

    """
    def __init__(self, r = 1, var = "", ls = 0, dim = 1):
        self.li = 0
        self.ls = int(ls)
        self.dim = dim
        self.ultimoNodo = True
        self.r = r
        self.var = var
        self.siguienteNodo = None

    def setNextNode(self, nodo):
        self.ultimoNodo = False
        self.siguienteNodo = nodo

    def calcR(self):
        print(self.ls)
        print(type(self.ls))
        self.r = (self.ls + 1) * self.r

    def setVal(self, val):
        self.val = val

    def imprimir(self):
        print("li " + str(self.li) + " ls " + str(self.ls) + " dim " + str(self.dim) + " ultimoNodo " + str(self.ultimoNodo))

class TablaConstantes():
    '''
    Atributos:
    - dirs: arreglo de memoria virtual
    - vals
    '''

    def __init__(self):
        self.mv = []
        print("tabla constantes")

    def addCte(self, val, dir):
        t = [dir, val]
        self.mv.append(t)

    def toTxt(self):
        f = open("tablaCtes.txt", "w")
        print(self.mv)
        for m in self.mv:
            f.write(str(m[0])+' '+str(m[1]) + '\n')
        f.close()


class VariableClass():
    '''
    Constructor de Variable

    Parámetros:
    - nameVar : string -> nombre de la variable
    - typeVar : string ->  tipo de la variable (numero, enunciado, bool, arreglo)
    - valueVar : [numero, bool, enunciado, arreglo] -> valor de la variable de acuerdo a su tipo
    - scopeVar : string -> scope de la variable
    - addressVar : int -> direccion de memoria virtual
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


    def printvar(self):
        print("[nameVar: {} typeVar: {} valueVar: {} addressVar: {}]".format(
            self.nameVar, self.typeVar, self.valueVar, self.addressVar))


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

    def addParam(self, tipo, id_param):
        # to do: los parametros se agregan como variables?
        var = VariableClass(id_param, tipo)
        self.varsFunc.addVar(var)
        self.numParam = self.numParam + 1
        # self.paramsFunc.append(var)

    def addVar(self, varObject):
        self.varsFunc.addVar(varObject)
        self.numVar = self.numVar + 1

    def addTipo(self, tipo):
        self.paramTipos.append(tipo)

    def printfunc(self):
        print("[nameFunc: {} typeFunc: {} paramTipos: {} scopeFunc: {} addressFunc: {}]".format(
            self.nameFunc, self.typeFunc, self.paramTipos, self.scopeFunc, self.addressFunc))
        print("variables")
        self.varsFunc.printTable()


class ProcDirectory:
    def __init__(self):
        self.procDirectory = {}

    def addFunc(self, funcObject):
        if not (self.checkDuplicate(funcObject.nameFunc)):
            self.procDirectory[funcObject.nameFunc] = funcObject
            print("Function added")

    def printTable(self):
        for item in self.procDirectory.items():
            print(item)
            item[1].printfunc()

    def findFunction(self, key):
        if key in self.procDirectory:
            return True
        else:
            return False

    def checkDuplicate(self, key):
        if key in self.procDirectory:
            print('Syntax error: redeclaration of function' + key)
            return True
        else:
            return False


class VariableTable:
    def __init__(self):
        self.tablaVar = {}

    def addVar(self, varObject):
        if not (self.checkDuplicate(varObject.nameVar)):
            self.tablaVar[varObject.nameVar] = varObject

    def asignar(self, name, new_value):
        self.tablaVar[name]

    def printTable(self):
        # print(len(self.tablaVar.items()))
        for item in self.tablaVar.items():
            print(item)
            item[1].printvar()

    def checkDuplicate(self, key):
        if key in self.tablaVar:
            print('Syntax error: redeclaration of variable' + key)
            return True
        else:
            return False

    def checkExists(self, key):
        if key in self.tablaVar:
            print("si existe " + key)
            return True
        else:
            print("aqui")
            print('Syntax error: variable ' + key + ' does not exist')
            return False

    def getType(self, key):
        if key in self.tablaVar:
            return self.tablaVar[key].typeVar
        else:
            print('Syntax error: variable ' + key + ' does not exist')
            return False


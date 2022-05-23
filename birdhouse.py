# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Tabla de variables

# Clase Variable para la creación de variables y sus atributos
from lark import Visitor
from cubo_semantico import cubo as cubo_semantico

id_Asignar = ""
pilaO = []
pOper = []
pilaT = []
pSaltos = []
temporales = []
avail = 0
quad_pointer = 0
cuadruplos = []


for i in range(0, 20):
    temporales.append("t" + str(i))


def generate_quad(operator, left, right, result):
    global quad_pointer
    cuadruplo = {"operator":operator, "left": left, "right": right, "result": result}
    cuadruplos.append(cuadruplo)
    print("cuadruplo agregado")
    print(cuadruplo)
    quad_pointer = quad_pointer + 1

def fill_quad(end, cont):
    cuadruplos[end]["result"] = cont

# Tabla de Variables


class VariableTable:
    def __init__(self):
        self.tablaVar = {}

    def addVar(self, varObject):
        if not (self.checkDuplicate(varObject.nameVar)):
            self.tablaVar[varObject.nameVar] = varObject
            print("Variable added")

    def asignar(self, name, new_value):
        self.tablaVar[name]

    def printTable(self):
        for item in self.tablaVar.items():
            print(item)
            item[1].printvar()

    def checkDuplicate(self, key):
        if key in self.tablaVar:
            print('Syntax error: redeclaration of variable' + key)
            return True
        else:
            return False

'''
class FunctionTable:
    def __init__(self):
        self.tablaFunc = {}
    def addFunction(self, funcObject):
        if not (self.checkDuplicate(funcObject.nameFunc)):
            self.tablaFunc[funcObject.nameFunc] = funcObject
            print("Function added")
    def checkDuplicate(self, key):
        if key in self.tablaFunc:
            print('Syntax error: redeclaration of function' + key)
            return True
        else:
            return False
'''
    
# Directorio de procedimientos


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

    def checkDuplicate(self, key):
        if key in self.procDirectory:
            print('Syntax error: redeclaration of function' + key)
            return True
        else:
            return False


# pilaO y poper
tabla_variables = VariableTable()
tabla_funciones = ProcDirectory()


class PuntosNeuralgicos(Visitor):
    def np_hola(self, tree):
        print("hola")

    def vars(self, tree):
        print("-----I will start adding variables to the table")
        type = tree.children[0].children[0].value
        name = tree.children[1].children[0].value
        # Logica para tambien agregar variables que se declaran en la misma linea
        # print(tree.children[2].children[0].children)

        var = VariableClass(name, type)
        tabla_variables.addVar(var)
        tabla_variables.printTable()

    def np_asignacion_1(self, tree):
        # revisar si existe en la tabla de variables
        id = tree.children[0].value
        id_Asignar = id
        if id in tabla_variables.tablaVar.keys():
            print("todo bien")

        else:
            print("ERROR")

        print("np 1")

    def np_asignacion_2(self, tree):
        # actualizar el valor
        # print("np 2")
        # print(tree.children[0].value)
        # tabla_variables.tablaVar[id_Asignar]. tree.children[0.value]
        '''
        def asignacion(self, tree):
            print("ASIGNACION")
            print(tree)
            print(tree.children[0].value)
            print(tree.children[0].line)
            print(tree.children[0])
            #print(tree.children[0])
        '''

    def guardar_id(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        tipo = tabla_variables.tablaVar[miid].typeVar
        pilaT.append(tipo)


    def guardar_num(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("num")

    def guardar_string(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("enunciado")

    def guardar_bool(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("bool")

    def termino_mult(self, tree):
        signo = tree.children[0].value
        pOper.append(signo)

    def exp_suma(self, tree):
        signo = tree.children[0].value
        pOper.append(signo)

    def cuadruplo_suma(self, tree):
        
        if pOper:
            if (pOper[-1] == "+") or (pOper[-1] == "-"):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                operator = pOper.pop()
                # TO-DO: agregar validacion semantica
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global avail
                    result = temporales[avail]
                    avail = avail+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def cuadruplo_mult_div(self, tree):
        '''
        If POper.top() == ‘+’ or ‘-‘ then
            right_operand= PilaO.Pop() left_operand=PilaO.Pop() let_Type=PTypes.Pop() operator= POper.Pop()
            result_Type= Semantics[left_Type,
            right_Type, operator] 
            if (result_Type != ERROR)
                result ßAVAIL.next() generate quad
                (operator, left_operand, right_operand, result) Quad.Push(quad)
                PilaO.Push(result) PTypes.Push(result_Type) If any operand were a temporal space,
                return it to AVAIL
            Else
                ERROR (“Type mismatch”)
        '''
        #print("hijos de exp")
        # print(pOper)
        # print(pilaO)
        # print(tree.children)
        if pOper:
            if (pOper[-1] == "*") or (pOper[-1] == "/"):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                operator = pOper.pop()
                if operator == "/":
                    if right_operand == "0" or tabla_variables.tablaVar[right_operand].value == 0:
                        print("Error: no se puede dividir entre 0")
                        exit()

                # TO-DO: agregar validacion semantica
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global avail
                    result = temporales[avail]
                    avail = avail+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def expresion_mayor(self, tree):
        # poper.push <, >, etc
        #print("hijos de g")
        # print(tree.children)
        signo = tree.children[0].value
        pOper.append(signo)

    def cuadruplo_expresion(self, tree):
        #print("llegamos a cuadruplo expresion")
        if pOper:
            if (pOper[-1] == ">") or (pOper[-1] == "<"):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                operator = pOper.pop()
                # TO-DO: agregar validacion semantica
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global avail
                    result = temporales[avail]
                    avail = avail+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def print_string(self, tree):
        # print("Escritura")
        # print(tree.children)
        # print(tree.children[-1].value)
        my_str = tree.children[-1].value
        pilaO.append(my_str)
        pilaT.append("enunciado")
        if pilaO:
            if pilaT.pop() == "enunciado":
                result = pilaO.pop()
                generate_quad("PRINT", None, None, result)

    def np_print_expresion(self, tree):
        if pilaO:
            result = pilaO.pop()
            if pilaT:
                pilaT.pop()
            generate_quad("PRINT", None, None, result)
            
            # Puntos neuralgicos del if
    # To do: probarlos con un ejemplo, necesitamos la tabla de variables

    def np_if(self, tree):
        global quad_pointer
        exp_type = pilaT.pop()
        if exp_type != "bool":
            print("Type mismatch")
            exit()
        else:
            result = pilaO.pop()
            generate_quad("GOTOF", result, None, "blank")
            pSaltos.append(quad_pointer - 1)

    def np_if_2(self, tree):
        end = pSaltos.pop()
        fill_quad(end, quad_pointer)
    
    def np_if_3(self, tree):
        generate_quad("GOTO", None, None, "blank")
        falso = pSaltos.pop()
        fill_quad(falso, quad_pointer)

    #Puntos neuralgicos para un while
    #Falta probarlos

    def np_while_1(self, tree):
        pSaltos.append(quad_pointer)

    def np_while_2(self, tree):
        global quad_pointer
        exp_type = pilaT.pop()
        if exp_type != "bool":
            print("Type mismatch")
            exit()
        else:
            result = pilaO.pop()
            generate_quad("GOTOF", result, None, "blank")
            pSaltos.append(quad_pointer - 1)

    def np_while_3(self, tree):
        end = pSaltos.pop()
        regreso = pSaltos.pop()
        generate_quad("GOTO", None, None, regreso)
        fill_quad(end, quad_pointer)

    #Puntos neuralgicos funciones

    def np_funciones_1(self, tree):
        # Insert Function name into the DirFunc table (and its type, if any), verify semantics.
        print("children mecanica")
        print(tree.children[0].children[0])
        tipo_funcion = tree.children[0].children[0]
        nombre_funcion = tree.children[1]
        func = FunctionClass(nombre_funcion, tipo_funcion)
        tabla_funciones.addFunc(func)
        tabla_funciones.printTable()
        



class VariableClass():
    '''
    Constructor de Variable

    Parámetros:
    - nameVar : string -> nombre de la variable
    - typeVar : string ->  tipo de la variable (numero, enunciado, bool, arreglo)
    - valueVar : [numero, bool, enunciado, arreglo] -> valor de la variable de acuerdo a su tipo
    - scopeVar : string -> scope de la variable
    - addressVar : int -> direccion de memoria virtual
    '''

    def __init__(self, nameVar, typeVar, valueVar='', addressVar=''):
        self.nameVar = nameVar
        self.typeVar = typeVar
        self.valueVar = valueVar
        self.addressVar = addressVar

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

    def __init__(self, nameFunc, typeFunc, paramsFunc = "", scopeFunc = "", addressFunc = ""):
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



class Test(Visitor):
    def printTree(self, tree):
        print(tree.pretty())

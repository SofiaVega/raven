# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Compilador

# Clase Variable para la creación de variables y sus atributos
from lark import Visitor
from cubo_semantico import cubo as cubo_semantico
from clases import *
from memoria import *

id_Asignar = ""
pilaO = []  # Operandos
pOper = []  # Operadores
pilaT = []  # Tipos
pSaltos = []  # Saltos (migaja de pan)
pilaDim = []
pilaMem = [] # Dirs de memoria de pilaO
temporalesNum = []  # Temporales
temporalesBool = []  # Temporales booleanos
temporalesString = []  # Temporales de string
temporalesPointer = []  # Temporales para Instruction Pointer
availNum = 0  # Contador de temporales (empieza en t0)
availBool = 0
availString = 0
availPointer = 0
quad_pointer = 0  # Contador de cuadruplos
cuadruplos = []  # Lista de cuadruplos
cuadruplosMem = []
pilaFunciones = []  # Pila de funciones: pilaFunciones[-1] es la funcion actual
pilaFunciones.append("global")
# pila de llamadas a funciones
# pila[-1] es la llamada actual
pilaLlamadas = []
# parameter counter
pilaK = []
tipo_arr_aux = ""  # Es el tipo con el que vamos a declarar un arreglo
# Necesitamos un auxiliar porque lo declaramos en 2 puntos diferentes
r = 1  # La r auxiliar para calcular las dimensiones de un arreglo
currNodo = NodoArreglo()  # Nodo auxiliar para recorrer los nodos de una matriz
headNodo = NodoArreglo()  # El primer nodo de la matriz que estamos declarando

# Generacion de los temporales
for i in range(0, 1000):
    temporalesNum.append("tN" + str(i))
    temporalesBool.append("tB" + str(i))
    temporalesString.append("tS" + str(i))
    temporalesPointer.append("tP" + str(i))


# Funcion para generar cuadruplos
# Es posible moverla a un objeto para refactorizar
def quad_ids(cuadruplos):
    f = open("cuadruplosID.txt", "w")
    for quad in cuadruplos:
        f.write(str(quad)+'\n')
    f.close()

# Pasa los cuadruplos con direcciones virtuales a un archivo de texto
def quad_mem(cuadruplos):
    f = open("cuadruplosMem.txt", "w")
    for quad in cuadruplosMem:
        f.write(str(quad)+'\n')
    f.close()

#Agrega una variable a la tabla de variables global o local
def addVar(var):
    if pilaFunciones[-1] == "global":
                tabla_variables.addVar(var)
    else:
        tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)

# Obtiene una variable a partir de su nombre y el contexto en el que estamos
# (global o una funcion)
def getVar(varID):
    if pilaFunciones[-1] == "global":
        var = tabla_variables.tablaVar[varID]
    else:
        var = tabla_funciones.procDirectory[pilaFunciones[-1]].tablaVar[varID]
    return var

# Revisa si el id corresponde a una variable del contexto actual
def checkExists_contexto(val):
    print(pilaFunciones[-1])
    tabla_variables.printTable()
    if pilaFunciones[-1] == "global":
        tabla_variables.checkExists(val)
        return True
    else:
        tabla_funciones.procDirectory[pilaFunciones[-1]].varsFunc.checkExists(val)
        return False

#Genera cuadruplos con los ids
def generate_quad(operator, left, right, result):
    global quad_pointer
    cuadruplo = {"operator": operator, "left": left,
                 "right": right, "result": result}
    cuadruplos.append(cuadruplo)
    print(quad_pointer + 1, ' ', operator, left, right, result)
    quad_pointer = quad_pointer + 1

# Genera cuadruplos con los valores de memoria
def generate_quad_mem(operator, left, right, result):
    cuadruplo = {"operator": operator, "left": left,
                 "right": right, "result": result}
    cuadruplosMem.append(cuadruplo)
    print("cuadruplo memoria")
    print(cuadruplo)

# Regresar a un cuadruplo con ____ para meter la linea a la que tiene que brincar
# Por lo general, para gotos
def fill_quad(end, cont):
    cuadruplos[end]["result"] = cont

def fill_quad_mem(end, cont):
    print("fill")
    print(cuadruplosMem[end])
    cuadruplosMem[end]["result"] = cont


tabla_variables = VariableTable()  # Tabla de variables
tabla_funciones = ProcDirectory()  # Tabla de funciones
tabla_ctes = TablaConstantes()


class PuntosNeuralgicos(Visitor):
    def huv_inicio(self, tree):
        print("Habia una vez", tree.children[1])
        generate_quad("GOTO", tree.children[1].value, None, "blank")
        # to do: poner memoria en vez de valor
        generate_quad_mem("GOTO", tree.children[1].value, None, "blank")
        pSaltos.append(quad_pointer-1)

    def titulo_asig(self, tree):
        val = tree.children[0].value
        pilaO.append(val)
        pilaT.append("enunciado")
        mem = memoria["cte"]["enunciado"]
        tabla_ctes.addCte(val, mem)
        memoria["cte"]["enunciado"] += 1
        pilaMem.append(mem)
        pOper.append(tree.children[1].value)
        val = tree.children[2].value
        pilaO.append(val)
        pilaT.append("enunciado")
        mem = memoria["cte"]["enunciado"]
        tabla_ctes.addCte(val, mem)
        memoria["cte"]["enunciado"] += 1
        pilaMem.append(mem)

    def np_cap(self, tree):
        print("AQUI")
        end = pSaltos.pop()
        print("capitulo " + str(end) + " " + str(quad_pointer))
        fill_quad(end, quad_pointer)
        fill_quad_mem(end, quad_pointer)

    # Funcion ayudante recursiva para agregar multiples asignaciones de variables del mismo tipo
    def inlineVar(self, inlineT, type):
        if(inlineT != []):
            name = inlineT[0].children[0].value
            inlineT = inlineT[1].children
            mem = memoria["global"][type]
            memoria["global"][type] += 1
            var = VariableClass(name, type, addressVar = mem)
            addVar(var)
            self.inlineVar(inlineT, type)
        else:
            return

    def np_vars(self, tree):
        # print(tree)
        type = tree.children[0].children[0].value
        name = tree.children[1].children[0].value
        mem = memoria["global"][type]
        memoria["global"][type] += 1
        var = VariableClass(name, type, addressVar=mem)
        addVar(var)
        # Logica para tambien agregar variables que se declaran en la misma linea
        self.inlineVar(tree.children[3].children, type)

    # Agrega ID a pila de operandos
    def np_asig(self, tree):
        val = tree.children[0].value
        print(tree)
        if (checkExists_contexto(val) == True):
            var = getVar(val)
            
            pilaO.append(val)
            tipo = var.typeVar
            mem = var.addressVar
            print(val)
            print("mem "+str(mem))
            pilaT.append(tipo)
            pilaMem.append(mem)
            try:
                pOper.append(tree.children[1].value)
            except:
                pOper.append(tree.children[2].value)
        else:
            print("no existe " + val)
            exit()

    def np_asig_quad(self, tree):
        print("asig quad")
        operator = pOper.pop()
        left_operand = pilaO.pop()
        right_operand = None
        left_mem = pilaMem.pop()
        result = pilaO.pop()
        print(pilaMem)
        res_mem = pilaMem.pop()
        generate_quad(operator, left_operand,
                      right_operand, result)
        generate_quad_mem(operator, left_mem, None, res_mem)

        #generate_quad("=", "value", None, tree.children[0].value)
    ''' 
    Guardado de constantes
    '''

    def guardar_id(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        # verificarlo con el len de children -1
        # 0 o -1?
        miid = tree.children[0].value
        pilaO.append(miid)
        var = getVar(miid)
        tipo = var.typeVar
        pilaT.append(tipo)
        mem = var.addressVar
        pilaMem.append(mem)

    def guardar_num(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("num")
        mem = memoria["cte"]["num"]
        memoria["cte"]["num"] += 1
        tabla_ctes.addCte(miid, mem)
        pilaMem.append(mem)

    def guardar_string(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("enunciado")
        mem = memoria["cte"]["enunciado"]
        memoria["cte"]["num"] += 1
        tabla_ctes.addCte(miid, mem)
        pilaMem.append(mem)

    def guardar_bool(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("bool")
        mem = memoria["cte"]["bool"]
        memoria["cte"]["bool"] += 1
        tabla_ctes.addCte(miid, mem)
        pilaMem.append(mem)

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
                right_mem = pilaMem.pop()
                left_mem = pilaMem.pop()
                operator = pOper.pop()
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    if result_type == "num":
                        global availNum
                        result = temporalesNum[availNum]
                        availNum = availNum+1
                    elif result_type == "enunciado":
                        global availString
                        result = temporalesString[availNum]
                        availString = availString+1
                    result_mem = memoria["temp"][result_type]
                    memoria["temp"][result_type] = memoria["temp"][result_type] + 1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    generate_quad_mem(operator, left_mem, right_mem, result_mem)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    pilaMem.append(result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def cuadruplo_mult_div(self, tree):
        if pOper:
            if (pOper[-1] == "*") or (pOper[-1] == "/"):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                right_mem = pilaMem.pop()
                left_mem = pilaMem.pop()
                operator = pOper.pop()
                if operator == "/":
                    var = getVar(right_operand)
                    # to do: en compilacion no sabemos el valor de las variables, asi que este check es incorrecto
                    if right_operand == "0" or var.value == 0:
                        print("Error: no se puede dividir entre 0")
                        exit()
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global availNum
                    result = temporalesNum[availNum]
                    availNum = availNum+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    result_mem = memoria["temp"][result_type]
                    pilaMem.append(result_mem)
                    memoria["temp"][result_type] = memoria["temp"][result_type] + 1
                    generate_quad_mem(operator, left_mem, right_mem, result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def expresion_mayor(self, tree):
        # poper.push <, >, etc
        signo = tree.children[0].value
        pOper.append(signo)

    def cuadruplo_expresion(self, tree):
        if pOper:
            if (pOper[-1] == ">") or (pOper[-1] == "<"):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                right_mem = pilaMem.pop()
                left_mem = pilaMem.pop()
                operator = pOper.pop()
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global availBool
                    result = temporalesBool[availBool]
                    availBool = availBool+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    result_mem = memoria["temp"][result_type]
                    pilaMem.append(result_mem)
                    memoria["temp"][result_type] = memoria["temp"][result_type] + 1
                    generate_quad_mem(operator, left_mem, right_mem, result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def print_string(self, tree):
        my_str = tree.children[-1].value
        pilaO.append(my_str)
        pilaT.append("enunciado")
        mem_str = memoria["cte"]["enunciado"]
        memoria["cte"]["enunciado"] += 1
        pilaMem.append(mem_str)
        #aqui habia un if pilaO pero creo que no es necesario
        if pilaT.pop() == "enunciado":
            result = pilaO.pop()
            pilaT.pop()
            generate_quad("PRINT", None, None, result)
            generate_quad_mem("PRINT", None, None, mem_str)
            tabla_ctes.addCte(result, mem_str)

    def np_print_expresion(self, tree):
        if pilaO:
            result = pilaO.pop()
            if pilaT:
                pilaT.pop()
            mem = pilaMem.pop()
            generate_quad("PRINT", None, None, result)
            generate_quad_mem("PRINT", None, None, mem)

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
            mem = pilaMem.pop()
            generate_quad("GOTOF", result, None, "blank")
            # to do: este cuadruplo de memoria tambien tiene que ir con blank?
            generate_quad_mem("GOTOF", result, None, "blank")
            pSaltos.append(quad_pointer - 1)

    def np_if_2(self, tree):
        end = pSaltos.pop()
        fill_quad(end, quad_pointer)
        fill_quad_mem(end, quad_pointer)

    def np_if_3(self, tree):
        generate_quad("GOTO", None, None, "blank")
        falso = pSaltos.pop()
        fill_quad(falso, quad_pointer)
        fill_quad_mem(falso, quad_pointer)

    # Puntos neuralgicos para un while

    def np_while_1(self, tree):
        # Migaja de pan
        # En cuanto encuentras el while
        pSaltos.append(quad_pointer)

    def np_while_2(self, tree):
        # Revisar que el tipo sea booleano
        global quad_pointer
        exp_type = pilaT.pop()
        if exp_type != "bool":
            print("Type mismatch")
            exit()
        else:
            result = pilaO.pop()
            mem = pilaMem.pop()
            generate_quad("GOTOF", result, None, "blank")
            generate_quad_mem("GOTOF", result, None, "blank")
            pSaltos.append(quad_pointer - 1)

    def np_while_3(self, tree):
        # Hacer un goto de regreso a la condicion del while
        # Llenar el gotoF vacio
        end = pSaltos.pop()
        regreso = pSaltos.pop()
        generate_quad("GOTO", None, None, regreso)
        generate_quad_mem("GOTO", None, None, regreso)
        fill_quad(end, quad_pointer)
        fill_quad_mem(end, quad_pointer)

    # Puntos neuralgicos funciones

    def np_funciones_1(self, tree):
        # Insert Function name into the DirFunc table (and its type, if any), verify semantics.
        tipo_funcion = tree.children[0].children[0]
        nombre_funcion = tree.children[1]
        func = FunctionClass(nombre_funcion, tipo_funcion)
        tabla_funciones.addFunc(func)
        pilaFunciones.append(nombre_funcion)
        tabla_funciones.printTable()
        # to do: verificar semanticas

    def mecanica2(self, tree):
        # 2 - Insert every parameter into the current (local) VarTable.
        if tree.children:
            # esto solo funciona con un parametro
            tipo = tree.children[0].children[0]
            id_param = tree.children[1]
            tabla_funciones.procDirectory[pilaFunciones[-1]
                                          ].addParam(tipo, id_param)
            tabla_funciones.procDirectory[pilaFunciones[-1]].addTipo(tipo)
            tabla_funciones.printTable()

    def mecanica3(self, tree):
        if tree.children:
            # otro parametro
            tipo = tree.children[0].children[0]
            id_param = tree.children[1]
            tabla_funciones.procDirectory[pilaFunciones[-1]
                                          ].addParam(tipo, id_param)
            tabla_funciones.procDirectory[pilaFunciones[-1]].addTipo(tipo)
            tabla_funciones.printTable()

    def cambiar_quad_pointer(self, tree):
        tabla_funciones.procDirectory[pilaFunciones[-1]
                                      ].quad_inicial = quad_pointer

    def fin_mecanica(self, tree):
        # varias cosas
        # release
        generate_quad("ENDFunc", None, None, None)
        generate_quad_mem("ENDFunc", None, None, None)
        # insert the number of temps

    # puntos neuralgicos para llamadas a funciones

    def np_llamada_funcion_1(self, tree):
        # verify that the function exists
        if tabla_funciones.findFunction(tree.children[0]):
            pilaLlamadas.append(tree.children[0])
        else:
            print("Error, esa funcion no existe")
            exit()

    def np_llamada_funcion_2(self, tree):
        # Generar cuadruplo ERA, nombreFuncion
        # Cuando se llama a una funcion
        generate_quad("ERA", pilaLlamadas[-1], None, None)
        generate_quad_mem("ERA", pilaLlamadas[-1], None, None)
        pilaK.append(0)

    def np_llamada_funcion_3(self, tree):
        # Argument= PilaO.Pop() ArgumentType= PTypes.Pop().
        # Verify ArgumentType against current Parameter (#k) in ParameterTable.
        # Generate action PARAMETER, Argument, Argument#k
        argument = pilaO[-1]
        argumentType = pilaT[-1]
        if argumentType == tabla_funciones.procDirectory[pilaLlamadas[-1]].paramTipos[pilaK[-1]]:
            print("parametro tipo compatible")
        else:
            print("El parametro no es del tipo correcto")
            exit()

    def np_llamada_funcion_4(self, tree):
        pilaK[-1] = pilaK[-1] + 1

    def np_llamada_funcion_5(self, tree):
        if pilaK[-1] == (tabla_funciones.procDirectory[pilaLlamadas[-1]].numParam - 1):
            print("right amount of params")
        else:
            print("Faltan parametros")
            exit()

    def np_llamada_funcion_6(self, tree):
        # to do: falta initial-address
        generate_quad("GOSUB", pilaLlamadas[-1], None, None)
        generate_quad_mem("GOSUB", pilaLlamadas[-1], None, None)

    def np_fin(self, tree):
        print("tabla de variables fin")
        tabla_variables.printTable()
        quad_ids(cuadruplos)
        quad_mem(cuadruplosMem)
        tabla_ctes.toTxt()

    # Arreglos
    def arreglo(self, tree):
        #vartable.add(id, type)
        global tipo_arr_aux
        tipo_arr_aux = tree.children[0].children[0].value

    def arr(self, tree):
        global currNodo
        global headNodo
        global r
        global tipo_arr_aux
        tipo = tipo_arr_aux
        thisID = tree.children[0]
        ls = tree.children[1]
        var = VariableClass(thisID, tipo)
        # np 2
        var.isArray = True
        # np 3
        r = 1
        currNodo = NodoArreglo(dim=1, r=1, ls=ls, var=thisID)
        var.arrNode = currNodo
        headNodo = var.arrNode
        addVar(var)

    def np_arr_5(self, tree):
        global currNodo
        currNodo.calcR()

    def np_arr_6(self, tree):
        # to do: ver si la referencia al objeto te permite funcionar como una linked list
        global currNodo
        dim = currNodo.dim + 1
        nuevoNodo = NodoArreglo(r=currNodo.r, var=currNodo.var, dim=dim)
        currNodo.siguienteNodo = nuevoNodo
        currNodo = nuevoNodo

    def np_arr_7(self, tree):
        global currNodo
        global r
        currNodo.ultimoNodo = True
        # tener un headNode y un currNode
        currNodo = headNodo
        dim = 1
        offset = 0
        size = currNodo.r
        # pasar r a variable global
        while currNodo != None:
            m = r / (currNodo.ls + 1)
            currNodo.val = m
            r = m
            if currNodo.ultimoNodo == True:
                currNodo.val = 0
            currNodo = currNodo.siguienteNodo

    # el siguiente cuadruplo es guardar una direccion virtual

    # cuadruplos de acceso a arreglos
    def np_acc_arr_1(self, tree):
        #este cuadruplo ya no hace nada
        print("es un arreglo")

    def np_acc_arr_2(self, tree):
        global currNodo
        idd = pilaO.pop()
        tipo = pilaT.pop()
        dim = 1
        pilaDim.append([idd, dim])
        var = getVar(idd)
        if var.isArray == False:
            print(idd + "no es un arreglo")
            exit()
        currNodo = var.arrNode
        # fondo falso
        pOper.append("[")
        print("curr nodo")
        currNodo.imprimir()
        
    def np_acc_arr_3(self, tree):
        global currNodo
        global availNum
        print("verificacion")
        generate_quad("VER", pilaO[-1], 0, currNodo.ls)
        generate_quad_mem("VER", pilaMem[-1], 0, currNodo.ls)
        if currNodo.ultimoNodo == False:
            aux = pilaO.pop()
            tipo = pilaT.pop()
            mem = pilaMem.pop()

            result = temporalesNum[availNum]
            availNum = availNum+1
            result_mem = memoria["temp"]["num"]
            memoria["temp"]["num"] +=1

            generate_quad("*", aux, currNodo.val, result)
            generate_quad_mem("*", mem, currNodo.val, result_mem)
            pilaO.append(result)
            pilaT.append("num")
            pilaMem.append(result_mem)
        dim = pilaDim[-1][1]
        if dim > 1:
            aux2 = pilaO.pop()
            t = pilaT.pop()
            mem2 = pilaMem.pop()
            aux1 = pilaO.pop()
            t = pilaT.pop()
            mem1 = pilaMem.pop()

            result = temporalesNum[availNum]
            availNum = availNum+1
            result_mem = memoria["temp"]["num"]
            memoria["temp"]["num"] +=1

            generate_quad("+", aux1, aux2, result)
            generate_quad_mem("*", mem, currNodo.val, result_mem)
            pilaO.append(result)
            pilaT.append("num")
            pilaMem.append(result_mem)

    def np_acc_arr_4(self, tree):
        global currNodo
        pilaDim[-1][1] = pilaDim[-1][1] + 1
        currNodo = currNodo.siguienteNodo

    def np_acc_arr_5(self, tree):
        global temporalesNum
        global availPointer
        print("ultimo arr")
        aux = pilaO.pop()
        t = pilaT.pop()
        mem = pilaMem.pop()
        result = temporalesPointer[availPointer]
        availPointer = availPointer+1
        result_mem = memoria["temp"]["pointer"]
        memoria["temp"]["pointer"] +=1

        generate_quad("+", aux, 0, result)
        generate_quad_mem("+", mem, 0, result_mem)
        # TO DO cambiar esto al pointer de result
        # esto tiene que pasar antes de asig quad
        pilaO.append(result)
        pilaT.append("pointer")
        pilaMem.append(result_mem)
        pOper.pop() # quita el fake bottom

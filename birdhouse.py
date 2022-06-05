# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Compilador

from lark import Visitor
from cubo_semantico import cubo as cubo_semantico
from clases import *
from memoria import *
from errores import *

# PILAS GENERALES
pilaO = []  # Pila de Operandos
pOper = []  # Pila de Operadores
pilaT = []  # Pila de Tipos
pSaltos = []  # Pila de Saltos (migaja de pan)
pilaDim = []  # Pila de dimensiones
pilaMem = []  # Dirs de memoria de pilaO

# TEMPORALES
temporalesNum = []  # Temporales para numeros
temporalesBool = []  # Temporales booleanos
temporalesString = []  # Temporales de string
temporalesPointer = []  # Temporales para Instruction Pointer
availNum = 0  # Contador de temporales para numero (empieza en t0)
availBool = 0  # Contador de temporales para booleanos (empieza en t0)
availString = 0  # Contador de temporales para strings (empieza en t0)
availPointer = 0  # Contador de temporales para iPointer (empieza en t0)

# CUADRUPLOS
cuadruplos = Cuadruplos()

# FUNCIONES
# Pila de funciones
# pilaFunciones[-1] es la funcion actual
pilaFunciones = []
pilaFunciones.append("global")
# pila de llamadas a funciones
# pila[-1] es la llamada actual
pilaLlamadas = []

# ARREGLOS
# Contador de parametros
pilaK = []
tipo_arr_aux = ""  # Es el tipo con el que vamos a declarar un arreglo
# Necesitamos un auxiliar porque lo declaramos en 2 puntos diferentes
r = 1  # La r auxiliar para calcular las dimensiones de un arreglo
currNodo = NodoArreglo()  # Nodo auxiliar para recorrer los nodos de una matriz
headNodo = NodoArreglo()  # El primer nodo de la matriz que estamos declarando

# Generacion de temporales
for i in range(0, 1000):
    temporalesNum.append("tN" + str(i))
    temporalesBool.append("tB" + str(i))
    temporalesString.append("tS" + str(i))
    temporalesPointer.append("tP" + str(i))

# Agrega una variable a la tabla de variables global o local


def getTemp(tipo):
    global availNum
    global availBool
    global availString
    global availPointer
    if tipo == "num":
        result = temporalesNum[availNum]
        availNum = availNum+1
    elif tipo == "enunciado":
        result = temporalesString[availString]
        availString += 1
    elif tipo == "bool":
        result = temporalesBool[availBool]
        availBool += 1
    elif tipo == "pointer":
        result = temporalesPointer[availPointer]
        availPointer += 1

    return result

# Agrega una variable a la tabla de variables global o local


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
        var = tabla_funciones.procDirectory[pilaFunciones[-1]
                                            ].varsFunc.tablaVar[varID]
    return var

# Revisa si el id corresponde a una variable del contexto actual


def checkExists_contexto(val):
    print(pilaFunciones[-1])
    tabla_variables.printTable()
    if pilaFunciones[-1] == "global":
        return tabla_variables.checkExists(val)
    else:
        return tabla_funciones.procDirectory[pilaFunciones[-1]].varsFunc.checkExists(val)


tabla_variables = VariableTable()  # Tabla de variables
tabla_funciones = ProcDirectory()  # Tabla de funciones
tabla_ctes = TablaConstantes()


class PuntosNeuralgicos(Visitor):
    def huv_inicio(self, tree):
        print("Habia una vez", tree.children[1])
        cuadruplos.generate_quad("GOTO", tree.children[1].value, None, "blank")
        # to do: poner memoria en vez de valor
        cuadruplos.generate_quad_mem(
            "GOTO", tree.children[1].value, None, "blank")
        pSaltos.append(cuadruplos.quad_pointer-1)

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
        print("capitulo " + str(end) + " " + str(cuadruplos.quad_pointer))
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    # Funcion ayudante recursiva para agregar multiples asignaciones de variables del mismo tipo
    def inlineVar(self, inlineT, type):
        if(inlineT != []):
            name = inlineT[0].children[0].value
            inlineT = inlineT[1].children
            mem = memoria["global"][type]
            memoria["global"][type] += 1
            # pasar esto a cuadruplos
            var = VariableClass(name, type, addressVar=mem)
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
        print(pilaFunciones[-1])
        print(checkExists_contexto(val))
        if (checkExists_contexto(val) == True):
            print("entra porque si existe")
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
        cuadruplos.generate_quad(operator, left_operand,
                                 right_operand, result)
        cuadruplos.generate_quad_mem(operator, left_mem, None, res_mem)

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
                    cuadruplos.generate_quad(operator, left_operand,
                                             right_operand, result)
                    cuadruplos.generate_quad_mem(operator, left_mem,
                                                 right_mem, result_mem)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    pilaMem.append(result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    errorTipos(operator, left_type, right_type)

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
                    cuadruplos.generate_quad(operator, left_operand,
                                             right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    result_mem = memoria["temp"][result_type]
                    pilaMem.append(result_mem)
                    memoria["temp"][result_type] = memoria["temp"][result_type] + 1
                    cuadruplos.generate_quad_mem(operator, left_mem,
                                                 right_mem, result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    errorTipos(operator, left_type, right_type)

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
                    cuadruplos.generate_quad(operator, left_operand,
                                             right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    result_mem = memoria["temp"][result_type]
                    pilaMem.append(result_mem)
                    memoria["temp"][result_type] = memoria["temp"][result_type] + 1
                    cuadruplos.generate_quad_mem(operator, left_mem,
                                                 right_mem, result_mem)
                    # revisar si uno de los operandos era un temporal
                else:
                    errorTipos(operator, left_type, right_type)

    def print_string(self, tree):
        my_str = tree.children[-1].value
        pilaO.append(my_str)
        pilaT.append("enunciado")
        mem_str = memoria["cte"]["enunciado"]
        memoria["cte"]["enunciado"] += 1
        pilaMem.append(mem_str)
        # aqui habia un if pilaO pero creo que no es necesario
        if pilaT.pop() == "enunciado":
            result = pilaO.pop()
            pilaT.pop()
            cuadruplos.generate_quad("PRINT", None, None, result)
            cuadruplos.generate_quad_mem("PRINT", None, None, mem_str)
            tabla_ctes.addCte(result, mem_str)

    def np_print_expresion(self, tree):
        if pilaO:
            result = pilaO.pop()
            if pilaT:
                pilaT.pop()
            mem = pilaMem.pop()
            cuadruplos.generate_quad("PRINT", None, None, result)
            cuadruplos.generate_quad_mem("PRINT", None, None, mem)

    # Puntos neuralgicos del if
    # To do: probarlos con un ejemplo, necesitamos la tabla de variables

    def np_if(self, tree):
        exp_type = pilaT.pop()
        if exp_type != "bool":
            print("Type mismatch")
            exit()
        else:
            result = pilaO.pop()
            mem = pilaMem.pop()
            cuadruplos.generate_quad("GOTOF", result, None, "blank")
            # to do: este cuadruplo de memoria tambien tiene que ir con blank?
            cuadruplos.generate_quad_mem("GOTOF", result, None, "blank")
            pSaltos.append(cuadruplos.quad_pointer - 1)

    def np_if_2(self, tree):
        end = pSaltos.pop()
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    def np_if_3(self, tree):
        cuadruplos.generate_quad("GOTO", None, None, "blank")
        falso = pSaltos.pop()
        cuadruplos.fill_quad(falso, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(falso, cuadruplos.quad_pointer)

    # Puntos neuralgicos para un while

    def np_while_1(self, tree):
        # Migaja de pan
        # En cuanto encuentras el while
        pSaltos.append(cuadruplos.quad_pointer)

    def np_while_2(self, tree):
        # Revisar que el tipo sea booleano
        exp_type = pilaT.pop()
        if exp_type != "bool":
            print("Type mismatch")
            exit()
        else:
            result = pilaO.pop()
            mem = pilaMem.pop()
            cuadruplos.generate_quad("GOTOF", result, None, "blank")
            cuadruplos.generate_quad_mem("GOTOF", result, None, "blank")
            pSaltos.append(cuadruplos.quad_pointer - 1)

    def np_while_3(self, tree):
        # Hacer un goto de regreso a la condicion del while
        # Llenar el gotoF vacio
        end = pSaltos.pop()
        regreso = pSaltos.pop()
        cuadruplos.generate_quad("GOTO", None, None, regreso)
        cuadruplos.generate_quad_mem("GOTO", None, None, regreso)
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    # Puntos neuralgicos funciones

    def np_funciones_1(self, tree):
        # Insert Function name into the DirFunc table (and its type, if any), verify semantics.
        tipo_funcion = tree.children[0].children[0].value
        nombre_funcion = tree.children[1].value
        func = FunctionClass(nombre_funcion, tipo_funcion)
        tabla_funciones.addFunc(func)
        pilaFunciones.append(nombre_funcion)
        tabla_funciones.printTable()
        # parche guadalupano maravilloso
        if tipo_funcion != "vacia":
            # asignar variable global
            mem = memoria["global"][tipo_funcion]
            memoria["global"][tipo_funcion] += 1
            var = VariableClass(nameVar=nombre_funcion,
                                typeVar=tipo_funcion, addressVar=mem)
            tabla_variables.addVar(var)

        # to do: verificar semanticas

    def mecanica2(self, tree):
        # 2 - Insert every parameter into the current (local) VarTable.
        if tree.children:
            # esto solo funciona con un parametro
            tipo = tree.children[0].children[0].value
            id_param = tree.children[1].value
            mem = memoria["local"][tipo]
            memoria["local"][tipo] += 1
            tabla_funciones.procDirectory[pilaFunciones[-1]
                                          ].addParam(tipo, id_param, mem)
            tabla_funciones.procDirectory[pilaFunciones[-1]].addTipo(tipo)
            tabla_funciones.printTable()

    def mecanica3(self, tree):
        if tree.children:
            # otro parametro
            # to do: agregar address
            tipo = tree.children[0].children[0].value
            id_param = tree.children[1].value
            mem = memoria["local"][tipo]
            memoria["local"][tipo] += 1
            tabla_funciones.procDirectory[pilaFunciones[-1]
                                          ].addParam(tipo, id_param, mem)
            tabla_funciones.procDirectory[pilaFunciones[-1]].addTipo(tipo)
            tabla_funciones.printTable()

    def np_mecanica_5(self, tree):
        print("mecanica5")
        o = pilaO.pop()
        t = pilaT.pop()
        mem = pilaMem.pop()
        # to do: como conecta esto con el parche guadalupano??
        # meter funcion actual
        cuadruplos.generate_quad("RETURN", pilaFunciones[-1], None, o)
        tabla_variables.printTable()
        mem_func = tabla_variables.tablaVar[pilaFunciones[-1]].addressVar
        # direccion de la variable global
        cuadruplos.generate_quad_mem("RETURN", mem_func, None, mem)
        # to do: el return en ejecucion asigna mv[m] a la variable global llamada como la funcion actual
        # hacer pop de llamada?

    def cambiar_quad_pointer(self, tree):
        tabla_funciones.procDirectory[pilaFunciones[-1]
                                      ].quad_inicial = cuadruplos.quad_pointer

    def fin_mecanica(self, tree):
        # varias cosas
        # release
        cuadruplos.generate_quad("ENDFunc", None, None, None)
        cuadruplos.generate_quad_mem("ENDFunc", None, None, None)
        # insert the number of temps

    # puntos neuralgicos para llamadas a funciones

    def np_llamada_funcion_1(self, tree):
        # verify that the function exists
        if tabla_funciones.findFunction(tree.children[0]):
            pilaLlamadas.append(tree.children[0].value)
        else:
            print("Error, esa funcion no existe")
            exit()

    def np_llamada_funcion_2(self, tree):
        # Generar cuadruplo ERA, nombreFuncion
        # Cuando se llama a una funcion
        cuadruplos.generate_quad("ERA", pilaLlamadas[-1], None, None)
        cuadruplos.generate_quad_mem("ERA", pilaLlamadas[-1], None, None)
        pilaK.append(0)

    def np_llamada_funcion_3(self, tree):
        # Argument= PilaO.Pop() ArgumentType= PTypes.Pop().
        # Verify ArgumentType against current Parameter (#k) in ParameterTable.
        # Generate action PARAMETER, Argument, Argument#k
        argument = pilaO[-1]
        argumentType = pilaT[-1]
        arg_mem = pilaMem[-1]
        if argumentType == tabla_funciones.procDirectory[pilaLlamadas[-1]].paramTipos[pilaK[-1]]:
            print("parametro tipo compatible")
            cuadruplos.generate_quad("PARAM", argument, None, pilaK[-1])
            cuadruplos.generate_quad_mem("PARAM", arg_mem, None, pilaK[-1])
        else:
            print("El parametro no es del tipo correcto")
            exit()

    def np_llamada_funcion_4(self, tree):
        pilaK[-1] = pilaK[-1] + 1

    def np_llamada_funcion_5(self, tree):
        print(pilaK[-1])
        # antes era numparam - 1
        if pilaK[-1] == (tabla_funciones.procDirectory[pilaLlamadas[-1]].numParam):
            print("right amount of params")
        else:
            print("Faltan parametros")
            exit()

    def np_llamada_funcion_6(self, tree):
        global availNum
        # to do: falta initial-address
        qi = tabla_funciones.procDirectory[pilaLlamadas[-1]].quad_inicial
        cuadruplos.generate_quad("GOSUB", pilaLlamadas[-1], None, None)
        cuadruplos.generate_quad_mem("GOSUB", qi, None, None)
        # to do: parche guadalupano maravilloso
        func = pilaLlamadas[-1]
        tipo_func = tabla_funciones.procDirectory[func].typeFunc
        if tipo_func != "vacia":
            result = getTemp(tipo_func)
            result_mem = memoria["temp"]["num"]
            memoria["temp"]["num"] += 1
            mem_llamada = tabla_variables.tablaVar[pilaLlamadas[-1]].addressVar
            pilaO.append(result)
            pilaT.append(tipo_func)
            pilaMem.append(result_mem)
            cuadruplos.generate_quad("=", pilaLlamadas[-1], None, result)
            cuadruplos.generate_quad_mem("=", mem_llamada, None, result_mem)

    def np_fin(self, tree):
        cuadruplos.generate_quad("ENDProgram", None, None, None)
        cuadruplos.generate_quad_mem("ENDProgram", None, None, None)
        print("tabla de variables fin")
        tabla_variables.printTable()
        cuadruplos.generaArchivos()
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
        thisID = tree.children[0].value
        ls = tree.children[1].value
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
        # este cuadruplo ya no hace nada
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
        cuadruplos.generate_quad("VER", pilaO[-1], 0, currNodo.ls)
        cuadruplos.generate_quad_mem("VER", pilaMem[-1], 0, currNodo.ls)
        if currNodo.ultimoNodo == False:
            aux = pilaO.pop()
            tipo = pilaT.pop()
            mem = pilaMem.pop()

            result = temporalesNum[availNum]
            availNum = availNum+1
            result_mem = memoria["temp"]["num"]
            memoria["temp"]["num"] += 1

            cuadruplos.generate_quad("*", aux, currNodo.val, result)
            cuadruplos.generate_quad_mem("*", mem, currNodo.val, result_mem)
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
            memoria["temp"]["num"] += 1

            cuadruplos.generate_quad("+", aux1, aux2, result)
            cuadruplos.generate_quad_mem("*", mem, currNodo.val, result_mem)
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
        memoria["temp"]["pointer"] += 1

        cuadruplos.generate_quad("+", aux, 0, result)
        cuadruplos.generate_quad_mem("+", mem, 0, result_mem)
        # TO DO cambiar esto al pointer de result
        # esto tiene que pasar antes de asig quad
        pilaO.append(result)
        pilaT.append("pointer")
        pilaMem.append(result_mem)
        pOper.pop()  # quita el fake bottom

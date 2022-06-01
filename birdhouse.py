# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Compilador

# Clase Variable para la creación de variables y sus atributos
from lark import Visitor
from cubo_semantico import cubo as cubo_semantico
from clases import *

id_Asignar = ""
pilaO = []  # Operandos
pOper = []  # Operadores
pilaT = []  # Tipos
pSaltos = []  # Saltos (migaja de pan)
pilaDim = []
temporales = []  # Temporales
temporalesBool = []  # Temporales booleanos
temporalesString = []  # Temporales de string
avail = 0  # Contador de temporales (empieza en t0)
availBool = 0
quad_pointer = 0  # Contador de cuadruplos
cuadruplos = []  # Lista de cuadruplos
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
    temporales.append("t" + str(i))
    temporalesBool.append("tB" + str(i))


# Funcion para generar cuadruplos
# Es posible moverla a un objeto para refactorizar
# TO-DO: generar los mismos cuadruplos pero con memoria virtual
# TO-DO: meter los cuadruplos a un archivo (txt?) en lugar de solo guardarlos aqui
def quad_ids(cuadruplos):
    f = open("cuadruplosID.txt", "w")
    for quad in cuadruplos:
        f.write(str(quad)+'\n')
    f.close()


def generate_quad(operator, left, right, result):
    global quad_pointer
    cuadruplo = {"operator": operator, "left": left,
                 "right": right, "result": result}
    cuadruplos.append(cuadruplo)
    #print(quad_pointer + 1, ' ', cuadruplo)
    print(quad_pointer + 1, ' ', operator, left, right, result)
    quad_pointer = quad_pointer + 1

# Regresar a un cuadruplo con ____ para meter la linea a la que tiene que brincar
# Por lo general, para gotos


def fill_quad(end, cont):
    cuadruplos[end]["result"] = cont


tabla_variables = VariableTable()  # Tabla de variables
tabla_funciones = ProcDirectory()  # Tabla de funciones


class PuntosNeuralgicos(Visitor):
    def huv_inicio(self, tree):
        print("Habia una vez", tree.children[1])
        generate_quad("GOTO", tree.children[1].value, None, "blank")
        pSaltos.append(quad_pointer)

    def titulo_asig(self, tree):
        pilaO.append(tree.children[0].value)
        pOper.append(tree.children[1].value)
        pilaO.append(tree.children[2].value)

    # Funcion ayudante recursiva para agregar multiples asignaciones de variables del mismo tipo
    def inlineVar(self, inlineT, type):
        if(inlineT != []):
            name = inlineT[0].children[0].value
            inlineT = inlineT[1].children
            var = VariableClass(name, type)
            if pilaFunciones[-1] == "global":
                tabla_variables.addVar(var)
            else:
                tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)
            self.inlineVar(inlineT, type)
        else:
            return

    def np_vars(self, tree):
        # print(tree)
        type = tree.children[0].children[0].value
        name = tree.children[1].children[0].value
        var = VariableClass(name, type)
        if pilaFunciones[-1] == "global":
            tabla_variables.addVar(var)
        else:
            tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)
        # Logica para tambien agregar variables que se declaran en la misma linea
        self.inlineVar(tree.children[3].children, type)

    # Agrega ID a pila de operandos
    def np_asig(self, tree):
        if (tabla_variables.checkExists(tree.children[0].value)):
            pilaO.append(tree.children[0].value)
            try:
                pOper.append(tree.children[1].value)
            except:
                pOper.append(tree.children[2].value)
        else:
            exit()

    def np_asig_quad(self, tree):
        print("asig quad")
        operator = pOper.pop()
        left_operand = pilaO.pop()
        right_operand = None
        result = pilaO.pop()
        generate_quad(operator, left_operand,
                      right_operand, result)

        #generate_quad("=", "value", None, tree.children[0].value)
    ''' 
    Guardado de constantes
    '''

    def guardar_id(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        print("menos uno")
        print(tree.children[-1])
        # verificarlo con el len de children -1
        # 0 o -1?
        miid = tree.children[0].value
        pilaO.append(miid)
        print("hizo push al arreglo? " + miid)
        # to do cambiar a global o funcion
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
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global avail
                    print("Result Type", result_type)
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
                result_type = cubo_semantico[operator][left_type][right_type]
                if result_type != "error":
                    global availBool
                    result = temporalesBool[availBool]
                    availBool = availBool+1
                    generate_quad(operator, left_operand,
                                  right_operand, result)
                    pilaO.append(result)
                    pilaT.append(result_type)
                    # revisar si uno de los operandos era un temporal
                else:
                    print("Error: error de tipos")
                    exit()

    def print_string(self, tree):
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
            generate_quad("GOTOF", result, None, "blank")
            pSaltos.append(quad_pointer - 1)

    def np_while_3(self, tree):
        # Hacer un goto de regreso a la condicion del while
        # Llenar el gotoF vacio
        end = pSaltos.pop()
        regreso = pSaltos.pop()
        generate_quad("GOTO", None, None, regreso)
        fill_quad(end, quad_pointer)

    # Puntos neuralgicos funciones

    def np_funciones_1(self, tree):
        # Insert Function name into the DirFunc table (and its type, if any), verify semantics.
        print("children mecanica")
        print(tree.children[0].children[0])
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
        # insert the number of temps

    # puntos neuralgicos para llamadas a funciones

    def np_llamada_funcion_1(self, tree):
        # verify that the function exists
        print("llamada funcion")
        if tabla_funciones.findFunction(tree.children[0]):
            print("Si existe la funcion")
            pilaLlamadas.append(tree.children[0])
        else:
            print("Error, esa funcion no existe")
            exit()

    def np_llamada_funcion_2(self, tree):
        # Generar cuadruplo ERA, nombreFuncion
        # Cuando se llama a una funcion
        generate_quad("ERA", pilaLlamadas[-1], None, None)
        pilaK.append(0)

    def np_llamada_funcion_3(self, tree):
        # Argument= PilaO.Pop() ArgumentType= PTypes.Pop().
        # Verify ArgumentType against current Parameter (#k) in ParameterTable.
        # Generate action PARAMETER, Argument, Argument#k
        print("verify argument type")
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

    def np_fin(self, tree):
        print("tabla de variables fin")
        tabla_variables.printTable()
        quad_ids(cuadruplos)

    # Arreglos
    def arreglo(self, tree):
        #vartable.add(id, type)
        tipo_arr_aux = tree.children[0].children[0].value
        '''
        print(tree.children)
        tipo = tree.children[0].children[0].value
        thisID = tree.children[1]
        var = VariableClass(thisID, tipo)
        # np 2
        var.isArray = True
        #np 3
        nodo = NodoArreglo(dim = 1, r = 1)
        var.arrNode = nodo
        if pilaFunciones[-1] == "global":
            tabla_variables.addVar(var)
            tabla_variables.printTable()
        else:
            tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)
            tabla_funciones.printTable()
        '''

    def arr(self, tree):
        global currNodo
        global headNodo
        global r
        print("arr")
        print(tree.children)
        print(tree.children[1])
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
        if pilaFunciones[-1] == "global":
            tabla_variables.addVar(var)
            tabla_variables.printTable()
        else:
            tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)
            tabla_funciones.printTable()

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
        '''
        var = currNodo.var
        if pilaFunciones[-1] == "global":
            tabla_variables.tablaVar[var].arrNode = currNodo
            currNodo.siguienteNodo = nuevoNodo
        else:
            tabla_funciones.procDirectory[pilaFunciones[-1]].varsFunc.tablaVar[var].arrNode = currNodo
            currNodo.siguienteNodo = nuevoNodo
            #tabla_funciones.printTable()
        '''

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
        '''
        #pilaO.push(id) pilaT.push(tipo)
        print("acceso arr")
        print(tree)
        print(tree.children)
        print(tree.children[0].value)
        idd = tree.children[0].value
        pilaO.append(idd)
        # to do: cambiar este tipo por el tipo del arreglo
        pilaT.append("num")
        '''
        print("es un arreglo")

    def np_acc_arr_2(self, tree):
        global currNodo
        idd = pilaO.pop()
        tipo = pilaT.pop()
        dim = 1
        pilaDim.append([idd, dim])
        if tabla_variables.tablaVar[idd].isArray == False:
            print(idd + "no es un arreglo")
            exit()
        currNodo = tabla_variables.tablaVar[idd].arrNode
        # fondo falso
        pOper.append("[")
        print("curr nodo")
        currNodo.imprimir()

    def np_acc_arr_3(self, tree):
        global currNodo
        global avail
        print("verificacion")
        generate_quad("VER", pilaO[-1], 0, currNodo.ls)
        if currNodo.ultimoNodo == False:
            aux = pilaO.pop()
            result = temporales[avail]
            avail = avail+1
            generate_quad("*", aux, currNodo.val, result)
            pilaO.append(result)
        dim = pilaDim[-1][1]
        if dim > 1:
            aux2 = pilaO.pop()
            aux1 = pilaO.pop()
            result = temporales[avail]
            avail = avail+1
            generate_quad("+", aux1, aux2, result)
            pilaO.append(result)

    def np_acc_arr_4(self, tree):
        global currNodo
        pilaDim[-1][1] = pilaDim[-1][1] + 1
        currNodo = currNodo.siguienteNodo

    def np_acc_arr_5(self, tree):
        global temporales
        global avail
        print("ultimo arr")
        aux = pilaO.pop()
        result = temporales[avail]
        avail = avail+1
        generate_quad("+", aux, 0, result)
        # TO DO cambiar esto al pointer de result
        # esto tiene que pasar antes de asig quad
        pilaO.append(result)
        pOper.pop()

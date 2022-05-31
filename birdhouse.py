# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Compilador

# Clase Variable para la creación de variables y sus atributos
from lark import Visitor
from cubo_semantico import cubo as cubo_semantico
from clases import *

id_Asignar = ""
pilaO = []  # Numeros
pOper = []  # Operadores
pilaT = []
pSaltos = []
temporales = []
avail = 0
quad_pointer = 0
cuadruplos = []
pilaFunciones = []
pilaFunciones.append("global")
pilaLlamadas = []
# parameter counter
pilaK = []
tipo_arr_aux = ""
r = 1
currNodo = NodoArreglo()
headNodo = NodoArreglo()


for i in range(0, 20):
    temporales.append("t" + str(i))


def generate_quad(operator, left, right, result):
    global quad_pointer
    cuadruplo = {"operator": operator, "left": left,
                 "right": right, "result": result}
    cuadruplos.append(cuadruplo)
    print(quad_pointer + 1, ' ', cuadruplo)
    quad_pointer = quad_pointer + 1


def fill_quad(end, cont):
    cuadruplos[end]["result"] = cont


# pilaO y poper
tabla_variables = VariableTable()
tabla_funciones = ProcDirectory()


class PuntosNeuralgicos(Visitor):
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

    def vars(self, tree):
        type = tree.children[0].children[0].value
        name = tree.children[1].children[0].value
        # Logica para tambien agregar variables que se declaran en la misma linea

        var = VariableClass(name, type)
        if pilaFunciones[-1] == "global":
            tabla_variables.addVar(var)
            # tabla_variables.printTable()
        else:
            tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)
            # tabla_funciones.printTable()

        self.inlineVar(tree.children[2].children, type)

    # Agrega ID a pila de operandos
    def np_asig(self, tree):
        if (tabla_variables.checkExists(tree.children[0].value)):
            pilaO.append(tree.children[0].value)
        else:
            exit()

    def np_asig_quad(self, tree):
        operator = "="
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

    # Puntos neuralgicos para un while
    # Falta probarlos

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

    def np_funciones_3(self, tree):
        # - Insert the type to every parameter uploaded into the VarTable.
        # At the same time into the ParameterTable (to create the Function’s signature)..
        # creo que esto ya lo hice?
        print("ni idea")

    def np_funciones_4(self, tree):
        # Insert into DirFunc the number of parameters defined.
        # **to calculate the workspace required for execution
        print("ni idea 2")

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

    ## Arreglos
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
        #np 3
        r = 1
        currNodo = NodoArreglo(dim = 1, r = 1, ls = ls, var = thisID)
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
        nuevoNodo = NodoArreglo(r = currNodo.r, var = currNodo.var, dim = dim)
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
        #tener un headNode y un currNode
        currNodo = headNodo
        dim = 1
        offset = 0
        size = currNodo.r
        #pasar r a variable global
        while currNodo != None:
            m = r / (currNodo.ls + 1)
            currNodo.val = m
            r = m
            if currNodo.ultimoNodo == True:
                currNodo.val = 0
            currNodo = currNodo.siguienteNodo
        
    # el siguiente cuadruplo es guardar una direccion virtual


    
    





        

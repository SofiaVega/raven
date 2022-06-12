# birdhouse.py
# por Nadia Garcia y Sofia Vega (2022)
# Compilador

from lark import Visitor
from cubo_semantico import cubo as cubo_semantico
from clases import *
from memoria import *
from errores import *

tabla_variables = VariableTable()  # Tabla de variables
tabla_funciones = ProcDirectory()  # Tabla de funciones
tabla_ctes = TablaConstantes()     # Tabla de constantes

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
# pilaFunciones[-1] es la función actual
pilaFunciones = []
pilaFunciones.append("global")
# pila de llamadas a funciones
# pila[-1] es la llamada actual
pilaLlamadas = []

# CAPITULOS
capitulos = {}

# OPCIONES indexadas por capitulo
opciones = {}
currOpciones = Opciones()
currOpcionStr = ""
currCap = ""

# ARREGLOS
# Contador de parametros
pilaK = []
tipo_arr_aux = ""  # Es el tipo con el que vamos a declarar un arreglo
# Necesitamos un auxiliar porque lo declaramos en 2 puntos diferentes
r = 1  # La r auxiliar para calcular las dimensiones de un arreglo
currNodo = NodoArreglo()  # Nodo auxiliar para recorrer los nodos de una matriz
headNodo = NodoArreglo()  # El primer nodo de la matriz que estamos declarando
dirCero = 13000

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


# ADD VAR
# Agrega una variable a la tabla de variables global o local
def addVar(var):
    if pilaFunciones[-1] == "global":
        tabla_variables.addVar(var)
    else:
        tabla_funciones.procDirectory[pilaFunciones[-1]].addVar(var)


# GET VAR
# Obtiene una variable a partir de su nombre y el contexto en el que estamos
# (global o una función)
def getVar(varID):
    if pilaFunciones[-1] == "global":
        var = tabla_variables.tablaVar[varID]
    else:
        try:
            var = tabla_funciones.procDirectory[pilaFunciones[-1]
                                                ].varsFunc.tablaVar[varID]
        except:
            var = tabla_variables.tablaVar[varID]
    return var


# CHECK EXISTS CONTEXTO
# Revisa si el id corresponde a una variable del contexto actual
def checkExists_contexto(val):
    if pilaFunciones[-1] == "global":
        return tabla_variables.checkExists(val)
    else:
        res = tabla_funciones.procDirectory[pilaFunciones[-1]
                                            ].varsFunc.checkExists(val)
        if res == False:
            res = tabla_variables.checkExists(val)
        return res


class PuntosNeuralgicos(Visitor):
    # HUV_INICIO
    # Punto neurálgico que genera cuádruplo {PROGRAM, , , programName} para definir el nombre del programa
    # Se llama desde programa
    def huv_inicio(self, tree):
        programName = tree.children[1].value
        cuadruplos.generate_quad(
            "PROGRAM", None, None, programName)
        cuadruplos.generate_quad_mem("PROGRAM", None, None, programName)

    # NP INDICE INICIO
    # Punto neurálgico que genera cuádruplo de {GOTO, indice, , []} incompleto para ser llenado posteriormente
    # Se llama desde programa
    def np_indice_inicio(self, tree):
        cuadruplos.generate_quad("GOTO", "indice", None, "blank")
        # to do: poner memoria en vez de valor
        cuadruplos.generate_quad_mem(
            "GOTO", "indice", None, "blank")
        pSaltos.append(cuadruplos.quad_pointer-1)

    # NP TITULO ASIG
    # Punto neurálgico que mete valores a pila de operandos, sus tipos a la pila de tipos, operador de
    # asignación a pila de operadores, guarda los valores en la tabla de constantes,
    # y mete la variable 'titulo' a la tabla de variables
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

    # NP INDICE
    # Punto neurálgico que rellena el cuádruplo {GOTO, indice, , []} con el número de cuádruple donde inicia el indice
    # Se llama desde programa
    def indice(self, tree):
        end = pSaltos.pop()
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    # NP LLAMADA CAPITULOS
    # Punto neurálgico que genera cuádruplos de GOCAP
    def llamada_capitulo(self, tree):
        cap = tree.children[0].value
        # estructura capitulos
        salto = capitulos[cap]
        # hacer un goto
        cuadruplos.generate_quad("GOCAP", cap, None, salto + 1)
        # to do: poner memoria en vez de valor
        cuadruplos.generate_quad_mem(
            "GOCAP", cap, None, salto + 1)

    # NP OPCIONES
    # Punto neurálgico que genera la estructura ayudante de Opciones
    def opciones(self, tree):
        # mandar cuádruplo
        global currOpciones
        currOpciones = Opciones()

    # NP OPCION
    # Punto neurálgico que genera la opción
    def opcion(self, tree):
        global currOpcionStr
        str = tree.children[0].value
        currOpcionStr = str

    # NP LLAMADA OPCION
    # Punto neurálgico que construye una llamada a una opción llamando a la
    # función de la clase Opciones, agregaOpcion
    def llamada_opcion(self, tree):
        global currOpcionStr
        global currOpciones

        cap = tree.children[0].value
        # estructura capitulos
        salto = capitulos[cap]
        str = currOpcionStr
        currOpciones.cap = cap
        currOpciones.agregaOpcion(str, cap, salto)

    # NP FIN OPCIONES
    # Punto neurálgico que genera el cuádruplo ELIGE
    def np_fin_opciones(self, tree):
        global currOpciones
        cuadruplos.generate_quad("ELIGE", None, None, currOpciones.cap)
        cuadruplos.generate_quad_mem("ELIGE", None, None, currOpciones.cap)
        opciones[currOpciones.cap] = currOpciones

    # NP CAPITULO
    # Punto neurálgico que indica el cuádruplo de inicio del capítulo
    def np_capitulo(self, tree):
        # estructura capítulos
        capitulos[tree.children[1].value] = cuadruplos.quad_pointer - 1
        # pSaltos.append(cuadruplos.quad_pointer-1)

    # NP END CAP
    # Punto neurálgico que genera el cuádruplo de ENDCAP
    def end_cap(self, tree):
        cuadruplos.generate_quad("ENDCAP", None, None, None)
        cuadruplos.generate_quad_mem("ENDCAP", None, None, None)

    # INLINE VAR
    # Función ayudante recursiva para agregar multiples asignaciones de variables del mismo tipo
    # a la tabla de variables
    def inlineVar(self, inlineT, type):
        if(inlineT != []):
            name = inlineT[0].children[0].value
            inlineT = inlineT[1].children
            mem = memoria["global"][type]
            memoria["global"][type] += 1
            # pasar esto a cuádruplos
            var = VariableClass(name, type, addressVar=mem)
            addVar(var)
            self.inlineVar(inlineT, type)
        else:
            return

    # NP VARS
    # Punto neurálgico que agrega variables a la tabla de variables
    def np_vars(self, tree):
        type = tree.children[0].children[0].value
        name = tree.children[1].children[0].value
        contexto = pilaFunciones[-1]
        if contexto != "global":
            contexto = "local"
        mem = memoria[contexto][type]
        memoria[contexto][type] += 1
        var = VariableClass(name, type, addressVar=mem)
        addVar(var)
        # Lógica para también agregar variables que se declaran en la misma línea
        self.inlineVar(tree.children[3].children, type)

    # NP ASIG
    # Punto neurálgico que agrega ID y su tipo a la pila de operadores y pila de tipos,
    # además de agregar el operador = a la pila de operadores
    def np_asig(self, tree):
        val = tree.children[0].value
        if (checkExists_contexto(val) == True):
            var = getVar(val)

            pilaO.append(val)
            tipo = var.typeVar
            mem = var.addressVar
            pilaT.append(tipo)
            pilaMem.append(mem)
            try:
                pOper.append(tree.children[1].value)
            except:
                pOper.append(tree.children[2].value)
        else:
            errorExisteContexto(val)

    # NP ASIG QUAD
    # Punto neurálgico que genera cuádruplos de asignación
    def np_asig_quad(self, tree):
        operator = pOper.pop()
        left_operand = pilaO.pop()
        right_operand = None
        left_mem = pilaMem.pop()
        result = pilaO.pop()
        res_mem = pilaMem.pop()
        cuadruplos.generate_quad(operator, left_operand,
                                 right_operand, result)
        cuadruplos.generate_quad_mem(operator, left_mem, None, res_mem)

        #generate_quad("=", "value", None, tree.children[0].value)

    ''' 
    GUARDADO DE CONSTANTES
    '''

    # NP GUARDAR ID
    # Punto neurálgico que guarda un id, sea un arreglo o no
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

    # NP GUADRAR NUM
    # Punto neurálgico que guarda un número como constante
    def guardar_num(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("num")
        mem = memoria["cte"]["num"]
        memoria["cte"]["num"] += 1
        tabla_ctes.addCte(miid, mem)
        pilaMem.append(mem)

    # NP GUARDAR STRING
    # Punto neurálgico que guarda un string como constante
    def guardar_string(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        pilaO.append(miid)
        pilaT.append("enunciado")
        mem = memoria["cte"]["enunciado"]
        memoria["cte"]["num"] += 1
        tabla_ctes.addCte(miid, mem)
        pilaMem.append(mem)

    # NP GUARDAR BOOL
    # Punto neurálgico que guarda un booleano como constante
    def guardar_bool(self, tree):
        # 1 PilaO.Push(id.name) and PTypes.Push(id.type)
        miid = tree.children[-1].value
        if miid == "Verdad":
            val = True
        else:
            val = False
        pilaO.append(val)
        pilaT.append("bool")
        mem = memoria["cte"]["bool"]
        memoria["cte"]["bool"] += 1
        tabla_ctes.addCte(val, mem)
        pilaMem.append(mem)

    # NP TÉRMINO MULT
    # Punto neurálgico que agrega el signo de multiplicación o de división a la pila de operadores
    def termino_mult(self, tree):
        signo = tree.children[0].value
        pOper.append(signo)

    # NP EXP SUMA
    # Punto neurálgico que agrega el signo de suma o resta a la pila de operadores
    def exp_suma(self, tree):
        signo = tree.children[0].value
        pOper.append(signo)

    # NP CUÁDRUPLO SUMA
    # Punto neurálgico que genera el cuádruplo de suma o de resta
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
                if left_type == "pointer" or right_type == "pointer":
                    result_type = "num"
                else:
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

    # NP CUADRUPLO MULT DIV
    # Punto neurálgico que genera el cuádruplo de multiplicación o división
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
                    # to do: en compilación no sabemos el valor de las variables, asi que este check es incorrecto
                    if right_operand == "0" or var.value == 0:
                        print("Error: no se puede dividir entre 0")
                        exit()
                if left_type == "pointer" or right_type == "pointer":
                    result_type = "num"
                else:
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

    # NP EXPRESION MAYOR
    # Punto neurálgico que agrega los signos de mayor qué menor qué mayor
    # o igual qué, menor o igual qué a la pila de operadores
    def expresion_mayor(self, tree):
        # poper.push <, >, etc
        signo = tree.children[0].value
        pOper.append(signo)

    # NP CUÁDRUPLO EXPRESIÓN
    # Punto neurálgico que genera los cuádruplos de expresiones de lógica booleana
    def cuadruplo_expresion(self, tree):
        if pOper:
            if (pOper[-1] == ">") or (pOper[-1] == "<") or (pOper[-1] == "!=") or (pOper[-1] == "==") or (pOper[-1] == ">=") or (pOper[-1] == "<="):
                right_operand = pilaO.pop()
                left_operand = pilaO.pop()
                right_type = pilaT.pop()
                left_type = pilaT.pop()
                right_mem = pilaMem.pop()
                left_mem = pilaMem.pop()
                operator = pOper.pop()
                if left_type == "pointer" or right_type == "pointer":
                    result_type = "bool"
                else:
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

    # NP PRINT STRING
    # Punto neurálgico que genera los cuádruplos de print
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
            mem = pilaMem.pop()
            cuadruplos.generate_quad("PRINT", None, None, result)
            cuadruplos.generate_quad_mem("PRINT", None, None, mem)
            tabla_ctes.addCte(result, mem)

    # NP PRINT EXPRESION
    # Punto neurálgico que genera el cuádruplo de
    def np_print_expresion(self, tree):
        result = pilaO.pop()
        pilaT.pop()
        mem = pilaMem.pop()
        cuadruplos.generate_quad("PRINT", None, None, result)
        cuadruplos.generate_quad_mem("PRINT", None, None, mem)

    # NP LECTURA
    # Puntos neurálgicos de lectura
    # Punto neurálgico que mete valores a sus respectivas pilas
    def np_lectura(self, tree):
        # meter el id
        val = tree.children[1].value
        # to do: si var es arreglo, hace otras cosas
        var = getVar(val)
        pilaO.append(val)
        pilaT.append(var.typeVar)
        pilaMem.append(var.addressVar)

    # NP ASIG LECTURA
    # Punto neurálgico que genera los cuádruplos para lectura de la respuesta del usuario
    def np_asig_lectura(self, tree):
        # crear cuádruplo para leer respuesta del usuario
        result = pilaO.pop()
        # revisar que exista la variable o acceso a arreglo
        tipo = pilaT.pop()
        mem = pilaMem.pop()
        cuadruplos.generate_quad("READ", None, None, result)
        cuadruplos.generate_quad_mem("READ", None, None, mem)

    # NP IF
    # Punto neurálgico que genera el cuádruplo de GOTOF para un IF
    def np_if(self, tree):
        exp_type = pilaT.pop()
        if exp_type != "bool":
            errorTiposB()
        else:
            result = pilaO.pop()
            t = pilaT.pop()
            mem = pilaMem.pop()
            cuadruplos.generate_quad("GOTOF", result, None, "blank")
            # to do: este cuadruplo de memoria tambien tiene que ir con blank?
            cuadruplos.generate_quad_mem("GOTOF", mem, None, "blank")
            pSaltos.append(cuadruplos.quad_pointer - 1)

    # NP IF 2
    # Punto neurálgico que llena los cuádruplos generados en los GOTO de un IF
    def np_if_2(self, tree):
        end = pSaltos.pop()
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    # NP IF 3
    # Punto neurálgico que genera los cuádruplos GOTO de un IF y
    # rellena los cuádruplos de GOTOF generados anteriormente
    def np_if_3(self, tree):
        cuadruplos.generate_quad("GOTO", None, None, "blank")
        cuadruplos.generate_quad_mem("GOTO", None, None, "blank")
        falso = pSaltos.pop()
        pSaltos.append(cuadruplos.quad_pointer - 1)
        cuadruplos.fill_quad(falso, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(falso, cuadruplos.quad_pointer)

    # NP WHILE 1
    # Punto neurálgico que mete el número de cuádruplo a la pila de saltos
    def np_while_1(self, tree):
        # Migaja de pan
        # En cuanto encuentras el while
        pSaltos.append(cuadruplos.quad_pointer)

    # NP WHILE 2
    # Punto neurálgico que genera los cuádruplos de GOTOF para un WHILE
    def np_while_2(self, tree):
        # Revisar que el tipo sea booleano
        exp_type = pilaT.pop()
        if exp_type != "bool":
            errorTiposB()
        else:
            result = pilaO.pop()
            t = pilaT.pop()
            mem = pilaMem.pop()
            cuadruplos.generate_quad("GOTOF", result, None, "blank")
            cuadruplos.generate_quad_mem("GOTOF", mem, None, "blank")
            pSaltos.append(cuadruplos.quad_pointer - 1)

    # NP WHILE 3
    # Punto neurálgico que genera los cuádruplos de GOTO para un WHILE
    # y rellena los cuádruplos de GOTOF generados con anterioridad
    def np_while_3(self, tree):
        # Hacer un goto de regreso a la condición del while
        # Llenar el gotoF vacío
        end = pSaltos.pop()
        regreso = pSaltos.pop()
        cuadruplos.generate_quad("GOTO", None, None, regreso)
        cuadruplos.generate_quad_mem("GOTO", None, None, regreso)
        cuadruplos.fill_quad(end, cuadruplos.quad_pointer)
        cuadruplos.fill_quad_mem(end, cuadruplos.quad_pointer)

    # Puntos neurálgicos funciones

    # NP FUNCIONES 1
    # Punto neurálgico que inserta las funciones y su tipo al Directorio de Funciones
    # Se verifica semántica
    def np_funciones_1(self, tree):
        # Insert Function name into the DirFunc table (and its type, if any), verify semantics.
        tipo_funcion = tree.children[0].children[0].value
        nombre_funcion = tree.children[1].value
        func = FunctionClass(nombre_funcion, tipo_funcion)
        tabla_funciones.addFunc(func)
        pilaFunciones.append(nombre_funcion)
        # parche guadalupano maravilloso
        if tipo_funcion != "vacia":
            # asignar variable global
            mem = memoria["global"][tipo_funcion]
            memoria["global"][tipo_funcion] += 1
            var = VariableClass(nameVar=nombre_funcion,
                                typeVar=tipo_funcion, addressVar=mem)
            tabla_variables.addVar(var)

        # to do: verificar semánticas

    # NP MECANICA 2
    # Punto neurálgico que inserta cada parámetro a una tabla de variables locales
    def mecanica2(self, tree):
        # 2 - Insert every parameter into the current (local) VarTable.
        if tree.children:
            # esto solo funciona con un parámetro
            tipo = tree.children[0].children[0].value
            id_param = tree.children[1].value
            mem = memoria["local"][tipo]
            memoria["local"][tipo] += 1
            tabla_funciones.procDirectory[pilaFunciones[-1]
                                          ].addParam(tipo, id_param, mem)
            tabla_funciones.procDirectory[pilaFunciones[-1]].addTipo(tipo)

    # NP MECANICA 3
    # Punto neurálgico que inserta parámetros después de la coma a tabla de variables locales
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

    # NP MECANICA 5
    # Punto neurálgico que genera cuádruplo de {RETURN, FUNC, , result}
    def np_mecanica_5(self, tree):
        o = pilaO.pop()
        t = pilaT.pop()
        mem = pilaMem.pop()
        # to do: cómo conecta esto con el parche guadalupano??
        # meter funcion actual
        cuadruplos.generate_quad("RETURN", pilaFunciones[-1], None, o)
        mem_func = tabla_variables.tablaVar[pilaFunciones[-1]].addressVar
        # direccion de la variable global
        cuadruplos.generate_quad_mem("RETURN", mem_func, None, mem)
        # to do: el return en ejecución asigna mv[m] a la variable global llamada como la función actual
        # hacer pop de llamada?

    # NP CAMBIAR QUAD POINTER
    # Punto neurálgico que rellena el cuádruplo inicial de una función en la tabla de Funciones,
    # aka Directorio de Procedimientos

    def cambiar_quad_pointer(self, tree):
        tabla_funciones.procDirectory[pilaFunciones[-1]
                                      ].quad_inicial = cuadruplos.quad_pointer

    # NP FIN_MECANICA
    # Punto neurálgico que genera el cuádruplo de ENDFUNC, libera la memoria y
    # hace un recuento de temporales utilizados
    def fin_mecanica(self, tree):
        # varias cosas
        # release
        cuadruplos.generate_quad("ENDFunc", None, None, None)
        cuadruplos.generate_quad_mem("ENDFunc", None, None, None)
        pilaFunciones.pop()
        # insert the number of temps

    # PUNTOS NEURÁLGICOS PARA LLAMADAS DE FUNCIONES
    # NP LLAMADA FUNCIÓN 1
    # Punto neurálgico que verifica que la función exista
    def np_llamada_funcion_1(self, tree):
        # verify that the function exists
        nombre_func = tree.children[0].value
        if tabla_funciones.findFunction(nombre_func):
            pilaLlamadas.append(nombre_func)
        else:
            errorFuncionNoExiste(nombre_func)

    # NP LLAMADA FUNCIÓN 2
    # Punto neurálgico que genera el cuádruplo ERA cada que se llama una función
    def np_llamada_funcion_2(self, tree):
        # Generar cuádruplo ERA, nombreFuncion
        # Cuando se llama a una funcion
        cuadruplos.generate_quad("ERA", pilaLlamadas[-1], None, None)
        cuadruplos.generate_quad_mem("ERA", pilaLlamadas[-1], None, None)
        pilaK.append(0)

    # NP LLAMADA FUNCION 3
    # Punto neurálgico que genera el cuádruplo {PARAM, argumento, , numParam}
    # Verifica que correspondan los tipos declarados de los invocados
    def np_llamada_funcion_3(self, tree):
        # Argument= PilaO. Pop() ArgumentType= PTypes.Pop().
        # Verify ArgumentType against current Parameter (#k) in ParameterTable.
        # Generate action PARAMETER, Argument, Argument#k
        argument = pilaO.pop()
        argumentType = pilaT.pop()
        arg_mem = pilaMem.pop()
        if argumentType == tabla_funciones.procDirectory[pilaLlamadas[-1]].paramTipos[pilaK[-1]]:
            cuadruplos.generate_quad("PARAM", argument, None, pilaK[-1])
            cuadruplos.generate_quad_mem("PARAM", arg_mem, None, pilaK[-1])
        else:
            errorTiposNoCoinciden(argument, argumentType)

    # NP LLAMADA FUNCION 4
    # Punto neurálgico que incrementa el contador de número de parámetros de la función
    def np_llamada_funcion_4(self, tree):
        pilaK[-1] = pilaK[-1] + 1

    # NP LLAMADA FUNCION 5
    # Punto neurálgico que revisa si el número de parámetros invocados coincide
    # coincide con el número de parámetros declarados
    def np_llamada_funcion_5(self, tree):
        # antes era numparam - 1
        if pilaK[-1] == (tabla_funciones.procDirectory[pilaLlamadas[-1]].numParam):
            print("right amount of params")
        else:
            print("Faltan parametros")
            exit()

    # NP LLAMADA FUNCION 6
    # Punto neurálgico que genera los cuádruplos de GOSUB
    # además de generar el cuádruplo de asignación para la variable
    # con el nombre de la función cuando el tipo de la función es
    # diferente de vacío
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

    # NP FIN
    # Punto neurálgico que genera el cuádruplo {ENDPROGRAM, , , }
    # además de llamar a las funciones que generarán los archivos
    # de la lista de cuádruplos y la tabla de constantes
    def np_fin(self, tree):
        cuadruplos.generate_quad("ENDProgram", None, None, None)
        cuadruplos.generate_quad_mem("ENDProgram", None, None, None)
        cuadruplos.generaArchivos()
        tabla_ctes.toTxt()

    # Arreglos
    # NP ARREGLO
    # Punto neurálgico que mete a una variable auxiliar el tipo de arreglo
    def arreglo(self, tree):
        #vartable.add(id, type)
        global tipo_arr_aux
        tipo_arr_aux = tree.children[0].children[0].value

    # NP ARR
    # Punto neurálgico que genera la variable del arreglo y construye los nodos
    # para las dimensiones del arreglo
    def arr(self, tree):
        global currNodo
        global headNodo
        global r
        global tipo_arr_aux
        tipo = tipo_arr_aux
        thisID = tree.children[0].value
        ls = int(tree.children[1].value)
        contexto = pilaFunciones[-1]
        if contexto != "global":
            contexto = "local"
        mem = memoria[contexto][tipo]
        memoria[contexto][tipo] += ls
        var = VariableClass(thisID, tipo, addressVar=mem)
        # np 2
        var.isArray = True
        # np 3
        r = 1
        mem_ls = memoria["cte"]["num"]
        memoria["cte"]["num"] += 1
        currNodo = NodoArreglo(dim=1, r=1, ls=ls, var=thisID, dirLS=mem_ls)
        var.arrNode = currNodo
        headNodo = var.arrNode
        mem_pointer = memoria["cte"]["num"]
        memoria["cte"]["num"] += 1
        tabla_ctes.addCte(mem, mem_pointer)
        addVar(var)

    # NP ARR 5
    # Punto neurálgico que genera el cálculo de las R's en la dimensión actual
    def np_arr_5(self, tree):
        global currNodo
        currNodo.calcR()

    # NP AR 6
    # Punto neurálgico que se extiende a la siguiente dimensión de un arreglo,
    # generando el nuevo nodo a seguir trabajando
    def np_arr_6(self, tree):
        # to do: ver si la referencia al objeto te permite funcionar como una linked list
        global currNodo
        dim = currNodo.dim + 1
        nuevoNodo = NodoArreglo(r=currNodo.r, var=currNodo.var, dim=dim)
        currNodo.siguienteNodo = nuevoNodo
        currNodo = nuevoNodo

    # NP ARR 7
    # Punto neurálgico que indica la última dimensión y genera los cálculos pertinentes
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

    # NP ACC ARR 2
    # Punto neurálgico que guarda una dirección virtual
    def np_acc_arr_2(self, tree):
        global currNodo
        idd = pilaO.pop()
        tipo = pilaT.pop()
        mem = pilaMem.pop()
        dim = 1
        pilaDim.append([idd, dim])
        var = getVar(idd)
        if var.isArray == False:
            errorVarNoArr(idd)
        currNodo = var.arrNode
        # fondo falso
        pOper.append("[")
        print("curr nodo")
        currNodo.imprimir()

    # NP ACC ARR 3
    # Punto neurálgico que genera los cuádruplos de verificación de límite superior para los arreglos
    # además de los cálculos de indexación
    def np_acc_arr_3(self, tree):
        global currNodo
        global availNum
        print("verificacion")
        # to do: guardar 0 y ls como constantes
        cuadruplos.generate_quad("VER", pilaO[-1], dirCero, currNodo.ls)
        cuadruplos.generate_quad_mem("VER", pilaMem[-1], dirCero, currNodo.ls)
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

    # NP ACC ARR 4
    # Punto neurálgico que cambia el nodo a trabajar, es decir, nos pasamos a la siguiente dimensión
    def np_acc_arr_4(self, tree):
        global currNodo
        pilaDim[-1][1] = pilaDim[-1][1] + 1
        currNodo = currNodo.siguienteNodo

    # NP ACC ARR 5
    # Punto neurálgico que termina de realizar las operaciones de indexación y
    # y genera los cuádruplos para las operaciones de memoria en ejecución
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
        var = getVar(currNodo.var)
        add = var.addressVar
        dir = tabla_ctes.getDir(add)
        cuadruplos.generate_quad("+", aux, currNodo.var, result)
        cuadruplos.generate_quad_mem("+", mem, dir, result_mem)

        # TO DO cambiar esto al pointer de result
        # esto tiene que pasar antes de asig quad
        pilaO.append(result)
        pilaT.append("pointer")
        pilaMem.append(result_mem)
        pOper.pop()  # quita el fake bottom

from birdhouse import *
from memoria import memoriaVirtual as mv
import ast

#pasar tablas de variables constantes y funciones

cuadruplos = []
ip = 0
pilaCalls = []
#to do: rename, es la pila donde te quedaste cuando haces una llamada
# a funcion
lineaQuede = []
fotos = []
foto = []
policia = 0

def tomarFoto():
    global foto
    global fotos
    print("foto memoria local")
    foto = mv[7000 : 12999]
    fotos.append(foto)


def restaurarFoto():
    global foto
    global fotos
    foto = fotos.pop()
    mv[7000 : 12999] = foto

def varsToMV():
    print("tabla variables")
    
    for key in tabla_variables.tablaVar:
        print("hola")
        print(key)
        mv[tabla_variables.tablaVar[key].addressVar] = tabla_variables.tablaVar[key].valueVar

def openQuads():
    f = open("cuadruplosMem.txt", "r")
    quads = f.readlines()
    for quad in quads:
        print(quad)
        cuadruplo = ast.literal_eval(quad)
        cuadruplos.append(cuadruplo)
    f.close()

def readCtes():
    f = open("tablaCtes.txt", "r")
    ctes = f.readlines()
    for c in ctes:
        print(c)
        a, b = c.split(maxsplit=1)
        s = b.rstrip()
        mv[int(a)] = s



def ejecutar():
    global ip
    global policia
    operator = cuadruplos[ip]['operator']
    left_op = cuadruplos[ip]['left']
    right_op = cuadruplos[ip]['right']
    result = cuadruplos[ip]['result']
    while operator != "ENDProgram":
        print(ip)
        print(cuadruplos[ip])

        operator = cuadruplos[ip]['operator']
        left_op = cuadruplos[ip]['left']
        right_op = cuadruplos[ip]['right']
        result = cuadruplos[ip]['result']

        if operator == "GOTO":
            print("GOTO")
            # to do: 
            ip = int(result)
            #ip += 1
        elif operator == "GOTOF":
            print("GOTOF")
            print(cuadruplos[ip])
            print(type(mv[int(left_op)]))
            print(mv[int(left_op)])
            if(mv[int(left_op)] == True):
                print("true")
                ip += 1
            else:
                print("falso")
                # to do: tomar en cuenta que los cuadruplos empiezan en 0 o en 1
                ip = int(result)
                print(ip)
        elif operator == "GOTOV":
            if(left_op):
                ip += 1
            else:
                ip = int(result)
        elif operator == "GOSUB":
            lineaQuede.append(ip + 1)
            print("antes de foto")
            #printMV()
            tomarFoto()
            print(left_op)
            ip = int(left_op)
            # to do: como regresamos a donde nos quedamos
            #pila ?
            #action(cuadruplos[int(left_op)])
            #action(cuadruplos[++ip])
        elif operator == "ERA":
            # Generar los espacios de memoria
            #action()
            #to do: reservar espacio de memoria
            pilaCalls.append(left_op)
            ip += 1
        elif operator == "PARAM":
            print("param")
            # Indicates that the argument sent must be copied into parámater#-- in Run-Time
            key = tabla_funciones.procDirectory[pilaCalls[-1]].keysParam[result]
            addv = tabla_funciones.procDirectory[pilaCalls[-1]].varsFunc.tablaVar[key].addressVar
            mv[addv] = mv[left_op]
            ip += 1
        elif operator == "=":
            print("=")
            print(cuadruplos[ip])
            # checar si es pointer
            #printMV()
            mv[int(result)] = mv[int(left_op)]
            ip += 1
        elif operator == '+':
            print("+")
            print(cuadruplos[ip])
            #checar tipo con direcciones de memoria
            mv[result] = int(mv[left_op]) + int(mv[right_op])
            #printMV()
            ip += 1
        elif operator == "-":
            print("-")
            print(cuadruplos[ip])
            printMV()
            mv[result] = int(mv[int(left_op)]) - int(mv[int(right_op)])
            ip += 1
        elif operator == "/":
            print("/")
            # to do: division por 0?
            mv[result] = mv[left_op] / mv[right_op]
            ip += 1
        elif operator == "*":
            print("*")
            #to do: puede ser int o float
            print(cuadruplos[ip])
            #printMV()
            mv[result] = int(mv[left_op]) * int(mv[right_op])
            ip += 1
        elif operator == ">":
            print(">")
            print(cuadruplos[ip])
            print(mv[left_op])
            print(mv[right_op])
            printMV()
            mv[result] = int(mv[left_op]) > int(mv[right_op])
            printMV()
            ip += 1
        elif operator == "<":
            print("<")
            mv[result] = mv[left_op] < mv[right_op]
            ip += 1
        elif operator == "<=":
            print("<=")
            mv[result] = mv[left_op] <= mv[right_op]
            ip += 1
        elif operator == ">=":
            print(">=")
            mv[result] = mv[left_op] >= mv[right_op]
            ip += 1
        elif operator == "==":
            print("==")
            print(mv[left_op])
            print(mv[right_op])
            mv[result] = int(mv[left_op]) == int(mv[right_op])
            print(mv[result])
            ip += 1
        elif operator == "!=":
            print("!=")
            mv[result] = mv[left_op] != mv[right_op]
            ip += 1
        elif operator == "PRINT":
            print("PRINT")
            print(cuadruplos[ip])
            print(mv[result])
            ip += 1
        elif operator == "ENDFunc":
            print("End function")
            restaurarFoto()
            print("despues de foto")
            #printMV()
            ip = lineaQuede.pop()
        elif operator == "RETURN":
            print("Return")
            # parche guadalupano maravilloso
            # return, dir var global func, none, val return
            print(cuadruplos[ip])
            mv[left_op] = mv[result]
            restaurarFoto()
            print("despues de foto")
            #printMV()
            ip = lineaQuede.pop()

        elif operator == "VER":
            print("Verificacion arreglos")
            # ver, x, li, ls
            if (left_op <  right_op) or (left_op >= result):
                print("Fuera de limites de arreglo " + left_op)
                exit()
            ip += 1
        policia += 1
        if(policia >= 40):
            print("alto! ya se ciclo")
            exit()

def printMV():
    cont = 0
    print("imprimiendo mv")
    for i in mv:
        if i != None:
            print(str(cont) + " " + str(i))
        cont += 1

def maquinaVirtual():
    print("-------- RAVEN TIME -------")
    readCtes()
    varsToMV()
    printMV()
    openQuads()
    try:
        openQuads()
    except:
        print("Quadruple file has not been generated yet")
    ejecutar()
    printMV()


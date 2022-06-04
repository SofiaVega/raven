from birdhouse import *
from memoria import memoriaVirtual as mv
import ast

#pasar tablas de variables constantes y funciones

cuadruplos = []
ip = 0
pilaCalls = []

def varsToMV():
    print("tabla variables")
    
    for key in tabla_variables.tablaVar:
        print("hola")
        mv[tabla_variables.tablaVar[key].addressVar] = tabla_variables.tablaVar[key].valueVar

def openQuads():
    f = open("cuadruplosMem.txt", "r")
    quads = f.readlines()
    for quad in quads:
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
    operator = cuadruplos[ip]['operator']
    left_op = cuadruplos[ip]['left']
    right_op = cuadruplos[ip]['right']
    result = cuadruplos[ip]['result']
    while operator != "ENDProgram":
        print(ip)

        operator = cuadruplos[ip]['operator']
        left_op = cuadruplos[ip]['left']
        right_op = cuadruplos[ip]['right']
        result = cuadruplos[ip]['result']

        if operator == "GOTO":
            print("GOTO")
            # to do: 
            #ip = int(result)
            ip += 1
        elif operator == "GOTOF":
            if(left_op):
                ip += 1
            else:
                ip = int(result)
        elif operator == "GOTOV":
            if(left_op):
                ip += 1
            else:
                ip = int(result)
        elif operator == "GOSUB":
            ip = int[left_op]
            # to do: como regresamos a donde nos quedamos
            #pila ?
            #action(cuadruplos[int(left_op)])
            #action(cuadruplos[++ip])
        elif operator == "ERA":
            # Generar los espacios de memoria
            #action()
            #to do: reservar espacio de memoria
            ip += 1
        elif operator == "PARAM":
            print("param")
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
            mv[result] = mv[left_op] - mv[right_op]
            #printMV()
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
            #printMV()
            mv[result] = int(mv[left_op]) > int(mv[right_op])
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
        elif operator == "PRINT":
            print("PRINT")
            print(mv[result])
            ip += 1
        elif operator == "ENDFunc":
            print("End function")
            ip += 1
        elif operator == "VER":
            print("Verificacion arreglos")
            # ver, x, li, ls
            if (left_op <  right_op) or (left_op >= result):
                print("Fuera de limites de arreglo " + left_op)
                exit()
            ip += 1

def printMV():
    cont = 0
    print("imprimiendo mv")
    for i in mv:
        if i != None:
            print(str(cont) + " " + str(i))
        cont += 1

def maquinaVirtual():
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


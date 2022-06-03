import birdhouse
from memoria import memoriaVirtual as mv
import ast

cuadruplos = []
ip = 0


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
        a, b = c.split(maxsplit=1)
        mv[int(a)] = b

def actionQuads():
    for i in cuadruplos:
        action(i)

def action(quad):
    operator = quad['operator']
    left_op = quad['left']
    right_op = quad['right']
    result = quad['result']

    if operator == "GOTO":
        print("GOTO")
        action(cuadruplos[result])
    elif operator == "GOTOF":
        if(left_op):
            action(cuadruplos[++ip])
        else:
            action(cuadruplos[int(result)])
    elif operator == "GOTOV":
        if(left_op):
            action(cuadruplos[++ip])
        else:
            action(cuadruplos[int(result)])
    elif operator == "GOSUB":
        action(cuadruplos[int(left_op)])
    elif operator == "ERA":
        # Generar los espacios de memoria
        action()
    elif operator == "PARAM":
        print("param")
    elif operator == "=":
        print("=")
        # checar si es pointer
        mv[int(result)] = mv[int(left_op)]
    elif operator == '+':
        print("+")
        mv[result] = mv[left_op] + mv[right_op]
    elif operator == "-":
        print("+")
        mv[result] = mv[left_op] - mv[right_op]
    elif operator == "/":
        print("/")
        # to do: division por 0?
        mv[result] = mv[left_op] / mv[right_op]
    elif operator == "*":
        print("*")
        #to do: puede ser int o float
        mv[result] = int(mv[left_op]) * int(mv[right_op])
    elif operator == ">":
        print(">")
        mv[result] = mv[left_op] > mv[right_op]
    elif operator == "<":
        print("<")
        mv[result] = mv[left_op] < mv[right_op]
    elif operator == "<=":
        print("<=")
        mv[result] = mv[left_op] <= mv[right_op]
    elif operator == ">=":
        print(">=")
        mv[result] = mv[left_op] >= mv[right_op]
    elif operator == "PRINT":
        print("PRINT")
        print(mv[result])
    elif operator == "ENDFunc":
        print("End function")
    elif operator == "VER":
        print("Verificacion arreglos")
        # ver, x, li, ls
        if (left_op <  right_op) or (left_op >= result):
            print("Fuera de limites de arreglo " + left_op)
            exit()

def printMV():
    cont = 0
    print("imprimiendo mv")
    for i in mv:
        if i != None:
            print(str(cont) + " " + str(i))
        cont += 1

def maquinaVirtual():
    readCtes()
    printMV()
    openQuads()
    try:
        openQuads()
    except:
        print("Quadruple file has not been generated yet")
    actionQuads()
    printMV()

maquinaVirtual()



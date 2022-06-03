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

def actionQuads():
    for i in cuadruplos:
        action(i)

def action(quad):
    operator = quad['operator']
    left_op = quad['left']
    right_op = quad['right']
    result = quad['result']
    print("operator " + operator)

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
        print(quad)
        mv[int(result)] = mv[int(left_op)]
        print(mv[int(left_op)])
    elif operator == '+':
        print("+")
        print(quad)
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
        mv[result] = mv[left_op] * mv[right_op]
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


def maquinaVirtual():
    openQuads()
    try:
        openQuads()
    except:
        print("Quadruple file has not been generated yet")
    actionQuads()

maquinaVirtual()

cont = 0
for i in mv:
    if i != None:
        print(cont + " " + i)
    ++cont

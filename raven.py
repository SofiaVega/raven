import birdhouse
import ast

cuadruplos = []
ip = 0
'''
Var globales
    num         1000
    enunciado   3000
    bool        5000

Var locales
    num         7000
    enunciado   9000
    bool        11000

Ctes
    num         13000
    enunciado   15000
    bool        17000

'''


def openQuads():
    f = open("cuadruplosID.txt", "r")
    quads = f.readlines()
    for quad in quads:
        cuadruplo = ast.literal_eval(quad)
        cuadruplos.append(cuadruplo)
    f.close()
    action(cuadruplos[ip])


def action(quad):
    operator = quad['operator']
    left_op = quad['left']
    right_op = quad['right']
    result = quad['result']

    if operator == "GOTO":
        print("GOTO")
        action(cuadruplos[int(result)])
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
    elif operator == "+":
        print("+")
    elif operator == "/":
        print("/")
    elif operator == "*":
        print("*")
    elif operator == ">":
        print(">")
    elif operator == "<":
        print("<")
    elif operator == "<=":
        print("<=")
    elif operator == ">=":
        print(">=")


availNumG = 1000
availEnunciadoG = 3000
availBoolG = 5000

availNumL = 7000
availEnunciadoL = 9000
availBoolL = 11000

availNumCTE = 13000
availEnunciadoCTE = 15000
availBoolCTE = 17000


def maquinaVirtual():
    openQuads()
    try:
        openQuads()
    except:
        print("Quadruple file has not been generated yet")

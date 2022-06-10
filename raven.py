from birdhouse import *
from memoria import memoriaVirtual as mv
import ast
from simple_term_menu import TerminalMenu

#pasar tablas de variables constantes y funciones

cuadruplos = []
ip = 0
pilaCalls = []
#to do: rename, es la pila donde te quedaste cuando haces una llamada
# a funcion
lineaQuede = []
fotos = []
policia = 0

def tomarFoto():
    global fotos
    global mv
    foto = mv[7000 : 12999]
    #printSubMV(foto)
    fotos.append(foto)

def printSubMV(smv):
    cont = 7000
    print("imprimiendo sub mv")
    for i in smv:
        if i != None:
            print(str(cont) + " " + str(i))
        cont += 1

def restaurarFoto():
    global fotos
    global mv
    mv[7000 : 12999] = fotos.pop()

def varsToMV():
    mv[13000] = 0
    
    for key in tabla_variables.tablaVar:
        #print(tabla_variables.tablaVar[key].addressVar)
        mv[int(tabla_variables.tablaVar[key].addressVar)] = tabla_variables.tablaVar[key].valueVar
    

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

        operator = cuadruplos[ip]['operator']
        left_op = cuadruplos[ip]['left']
        right_op = cuadruplos[ip]['right']
        result = cuadruplos[ip]['result']


        if operator == "GOTO":
            ip = int(result)
        elif operator == "ELIGE":
            cap = result
            strs = opciones[cap].strs
            terminal_menu = TerminalMenu(strs)
            choice_index = terminal_menu.show()
            lineaQuede.append(ip + 1)
            ip = opciones[cap].saltos[choice_index] + 1
            # muestra las opciones segun el capitulo
            # que esta en result
            # espera la respuesta del usuario
            # y hace un salto al salto que este en opciones[cap]
        elif operator == "GOCAP":
            lineaQuede.append(ip + 1)
            ip = int(result)
        elif operator == "ENDCAP":
            ip = lineaQuede.pop()
        elif operator == "PROGRAM":
            ip += 1
        elif operator == "GOTOF":
            if(mv[int(left_op)] == True):
                ip += 1
            else:
                # to do: tomar en cuenta que los cuadruplos empiezan en 0 o en 1
                ip = int(result)
        elif operator == "GOTOV":
            if(left_op):
                ip += 1
            else:
                ip = int(result)
        elif operator == "GOSUB":
            lineaQuede.append(ip + 1)
            #printMV()
            #tomarFoto()
            ip = int(left_op)
            # to do: como regresamos a donde nos quedamos
            #pila ?
            #action(cuadruplos[int(left_op)])
            #action(cuadruplos[++ip])
        elif operator == "ERA":
            # Generar los espacios de memoria
            #action()
            #to do: reservar espacio de memoria
            tomarFoto()
            pilaCalls.append(left_op)
            ip += 1
        elif operator == "PARAM":
            # Indicates that the argument sent must be copied into parámater#-- in Run-Time
            key = tabla_funciones.procDirectory[pilaCalls[-1]].keysParam[result]
            addv = tabla_funciones.procDirectory[pilaCalls[-1]].varsFunc.tablaVar[key].addressVar
            mv[addv] = mv[left_op]
            ip += 1
        elif operator == "=":
            # checar si es pointer de 25000 en adelante
            if result >= 25000:
                result = mv[int(result)]
            if left_op >= 25000:
                left_op = mv[int(left_op)]
            mv[int(result)] = mv[int(left_op)]
            ip += 1
        elif operator == '+':
            #printMV()
            #checar tipo con direcciones de memoria
            if right_op >= 25000:
                right_op = mv[int(right_op)]
            if left_op >= 25000:
                left_op = mv[int(left_op)]
            mv[result] = int(mv[left_op]) + int(mv[right_op])
            #printMV()
            ip += 1
        elif operator == "-":
            #printMV()
            if(left_op >= 25000):
                left_op = mv[left_op]
            if(right_op >= 25000):
                right_op = mv[right_op]
            mv[result] = int(mv[int(left_op)]) - int(mv[int(right_op)])
            ip += 1
        elif operator == "/":
            if(left_op >= 25000):
                left_op = mv[left_op]
            if(right_op >= 25000):
                right_op = mv[right_op]
            # to do: division por 0?
            mv[result] = mv[left_op] / mv[right_op]
            ip += 1
        elif operator == "*":
            #to do: puede ser int o float
            #printMV()
            if(left_op >= 25000):
                left_op = mv[left_op]
            if(right_op >= 25000):
                right_op = mv[right_op]
            mv[result] = int(mv[left_op]) * int(mv[right_op])
            ip += 1
        elif operator == ">":
            #printMV()
            mv[result] = int(mv[left_op]) > int(mv[right_op])
            #printMV()
            ip += 1
        elif operator == "<":
            mv[result] = int(mv[left_op]) < int(mv[right_op])
            ip += 1
        elif operator == "<=":
            mv[result] = int(mv[left_op]) <= int(mv[right_op])
            ip += 1
        elif operator == ">=":
            mv[result] = mv[left_op] >= mv[right_op]
            ip += 1
        elif operator == "==":
            if(left_op >= 25000):
                left_op = mv[left_op]
            if(right_op >= 25000):
                right_op = mv[right_op]
            try:
                mv[result] = int(mv[left_op]) == int(mv[right_op])
            except:
                mv[result] = (mv[left_op]) == (mv[right_op])
            ip += 1
        elif operator == "!=":
            mv[result] = mv[left_op] != mv[right_op]
            ip += 1
        elif operator == "PRINT":
            #printMV()
            if result >= 25000:
                result = mv[result]
            print(mv[result])
            ip += 1
        elif operator == "ENDFunc":
            restaurarFoto()
            #printMV()
            ip = lineaQuede.pop()
        elif operator == "RETURN":
            # parche guadalupano maravilloso
            # return, dir var global func, none, val return
            #printMV()
            aux = mv[result]
            restaurarFoto()
            mv[left_op] = aux
            #printMV()
            ip = lineaQuede.pop()

        elif operator == "VER":
            # ver, x, li, ls
            #printMV()
            if (int(mv[left_op]) <  int(mv[right_op])) or (int(mv[left_op]) >= int(result)):
                print("Fuera de limites de arreglo " + str(left_op))
                exit()
            ip += 1
        elif operator == "READ":
            mv[result] = input()
            ip += 1
        elif operator == "otro":
            print("otro")
            ip += 1
        
        #policia += 1
        if(policia >= 100):
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
    openQuads()
    try:
        openQuads()
    except:
        print("Quadruple file has not been generated yet")
    print("----- Inicia ejecucion ------")
    ejecutar()
    print("----- Termina ejecucion ------")
    #printMV()


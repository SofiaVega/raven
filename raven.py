from birdhouse import *
from memoria import memoriaVirtual as mv
import ast
from simple_term_menu import TerminalMenu

# pasar tablas de variables constantes y funciones

cuadruplos = []
ip = 0
pilaCalls = []
lineaQuede = []
fotos = []
policia = 0


def tomarFoto():
    global fotos
    global mv
    foto = mv[7000: 12999]
    fotos.append(foto)


def printSubMV(smv):
    cont = 7000
    for i in smv:
        if i != None:
            print(str(cont) + " " + str(i))
        cont += 1


def restaurarFoto():
    global fotos
    global mv
    mv[7000: 12999] = fotos.pop()


def varsToMV():
    mv[13000] = 0

    for key in tabla_variables.tablaVar:
        mv[int(tabla_variables.tablaVar[key].addressVar)
           ] = tabla_variables.tablaVar[key].valueVar


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
            # muestra las opciones segun el capítulo
            # que está en result
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
                ip = int(result)
        elif operator == "GOTOV":
            if(left_op):
                ip += 1
            else:
                ip = int(result)
        elif operator == "GOSUB":
            lineaQuede.append(ip + 1)
            ip = int(left_op)
        elif operator == "ERA":
            # Generar los espacios de memoria
            tomarFoto()
            pilaCalls.append(left_op)
            ip += 1
        elif operator == "PARAM":
            # Indica que el argumento enviado deben ser copiados como parámetros en ejecución
            key = tabla_funciones.procDirectory[pilaCalls[-1]
                                                ].keysParam[result]
            addv = tabla_funciones.procDirectory[pilaCalls[-1]
                                                 ].varsFunc.tablaVar[key].addressVar
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
            # checar tipo con direcciones de memoria
            if right_op >= 25000:
                right_op = mv[int(right_op)]
            if left_op >= 25000:
                left_op = mv[int(left_op)]
            mv[result] = int(mv[left_op]) + int(mv[right_op])
            ip += 1
        elif operator == "-":
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
            mv[result] = mv[left_op] / mv[right_op]
            ip += 1
        elif operator == "*":
            if(left_op >= 25000):
                left_op = mv[left_op]
            if(right_op >= 25000):
                right_op = mv[right_op]
            mv[result] = int(mv[left_op]) * int(mv[right_op])
            ip += 1
        elif operator == ">":
            mv[result] = int(mv[left_op]) > int(mv[right_op])
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
            if result >= 25000:
                result = mv[result]
            print(mv[result])
            ip += 1
        elif operator == "PRINT_TITLE":
            if result >= 25000:
                result = mv[result]
            print('╔═╗┌─┐┌─┐┬┌┬┐┬ ┬┬  ┌─┐\n' +
                  mv[result] + '\n' +
                  '╚═╝┴ ┴┴  ┴ ┴ └─┘┴─┘└─┘')
            ip += 1
        elif operator == "PRINT_BOOK_TITLE":
            if result >= 25000:
                result = mv[result]
            print('''      _.--._  _.--._
,-=.-:;:;:;\':;:;:;-._ 
\\\:;:;:;:;:;\:;:;:;:;:;\ 
 \\\:;:;:;:;:;\:;:;:;:;:;\ 
  \\\:;:;:;:;:;\:;:;:;:;:;\ 
   \\\:;:;:;:;:;\:;::;:;:;:\ 
    \\\;:;::;:;:;\:;:;:;::;:\ 
     \\\;;:;:_:--:''' + mv[result] + '''
      \\\_.-      :      ---._\ 
       \__..--------.;.----.._=> \n \n''')
            ip += 1
        elif operator == "ENDFunc":
            restaurarFoto()
            ip = lineaQuede.pop()
        elif operator == "RETURN":
            # parche guadalupano maravilloso
            # return, dir var global func, none, val return
            aux = mv[result]
            restaurarFoto()
            mv[left_op] = aux
            ip = lineaQuede.pop()

        elif operator == "VER":
            # ver, x, li, ls
            if (int(mv[left_op]) < int(mv[right_op])) or (int(mv[left_op]) >= int(result)):
                errorEjFueraLimites(left_op)
            ip += 1
        elif operator == "READ":
            mv[result] = input()
            ip += 1
        elif operator == "otro":
            ip += 1
        if(policia >= 100):
            print("alto! ya se ciclo")
            exit()
    print(''' ___          ___        
|__  |       |__  | |\ | 
|___ |___    |    | | \| 
                         ''')


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
    openQuads()
    try:
        openQuads()
    except:
        print("ERROR DE COMPILACIÓN: Archivo de cuádruplos no ha sido generado.")
    ejecutar()

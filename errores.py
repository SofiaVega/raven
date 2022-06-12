'''
ERRORES POSIBLES
- 1. Error de tipos
- 2. Variable no declarada
- 3. Redeclaracion de variable
- 4. Variable no existe
- 5. Función no existe
- 6. Redeclaracion de funcion
- 7. Discrepancia de tipos
- 8. Diferente número de parámetros
- 9. División entre 0 previo a ejecución
- 10.Variable no es arreglo
'''


# Error de Tipos (Caso Boolean)
# Aparece cuando se espera un valor booleano y se recibe
# algún otro tipo diferente
def errorTiposB():
    print("ERROR: Error de tipos. Se espera el tipo bool.")
    exit()


# Error de Tipos
# Aparece cuando se quiere hacer una operación con dos tipos
# de datos no compatibles.
def errorTipos(operador, left_type, right_type):
    print("ERROR: Error de tipos. \nEl operador ", operador,
          " no soporta operaciones con la combinación de tipos ", left_type, " y ", right_type)
    exit()


# Existencia en contexto
# Aparece cuando una variable no existe dentro del contexto actual
def errorExisteContexto(val):
    print("ERROR: La variable ", val, " no existe.")
    exit()


# Función no existe
# Aparece cuando se trata de invocar una función que no existe.
def errorFuncionNoExiste(funcion):
    print("Error. La función ", funcion, " no existe.")
    exit()


# Variable no existe
# Aparece cuando se trata de utilizar una variable que no fue
# declarada previamente
def errorVariableNoExiste(var):
    print("ERROR: La variable ", var, " no existe.")


# Error de Tipos (Discrepancia en llamada - declaración)
# Aparece cuando los tipos de los parámetros enviados en la
# invocación de una función no coinciden con los tipos de los
# parámetros de la declaración de la función.
def errorTiposNoCoinciden(param, paramType):
    print("ERROR: El parámetro ", param, " de tipo ", paramType,
          " no coincide con la declaración de la función.")
    exit()


# Error Discrepancia en número de parámetros
# Aparece cuando el número de parámetros enviados no coincide con
# el número de parámetros de la declaración de la función.
def errorDifNumParams(invocados, declarados):
    print("ERROR: Número incorrecto de parámetros. \n Se han invocado ", invocados,
          " parámetros cuando ", declarados, " parámetros fueron declarados para la función.")
    exit()


# Error de división entre 0
# Aparece cuando en compilación se detecta que el lado derecho de
# la operación división es un 0.
def errorDivCero():
    print("ERROR: Imposible dividir entre 0.")
    exit()


# Error de redeclaración de función.
# Aparece cuando se intenta declarar una función ya registrada en
# el directorio de procedimientos
def errorReFunc(key):
    print('ERROR: Redeclaración de la función' + key)


# Error de redeclaración de variable.
# Aparece cuando se intenta declarar una variable ya registrada en
# la tabla de variables de su contexto actual
def errorReVar(key):
    print('ERROR: Redeclación de la variable ', key)


# Error de acceso a variable que no es arreglo
# Aparece cuando se trata de utilizar una variable como arreglo cuando
# no fue declarada como tal
def errorVarNoArr(id):
    print("ERROR: La variable ", id, " no es un arreglo.")
    exit()


# ERRORES DE EJECUCION
def errorEjFueraLimites(left_op):
    print("ERROR: Fuera de limites de arreglo " + str(left_op))
    exit()


def errorCiclado():
    print("ERROR: me ciclé :(")
    exit()

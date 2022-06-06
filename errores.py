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
'''


def errorTipos(operador, left_type, right_type):
    print("ERROR: Error de tipos. \nEl operador ", operador,
          " no soporta operaciones con la combinación de tipos ", left_type, " y ", right_type)
    exit()


def errorExisteContexto(val):
    print("ERROR: La variable ", val, " no existe.")
    exit()


def errorFuncionNoExiste(funcion):
    print("Error. La función ", funcion, " no existe.")
    exit()


def errorTiposNoCoinciden(param, paramType):
    print("ERROR: El parámetro ", param, " de tipo ", paramType,
          " no coincide con la declaración de la función.")
    exit()


def errorDifNumParams(invocados, declarados):
    print("ERROR: Número incorrecto de parámetros. \n Se han invocado ", invocados,
          " parámetros cuando ", declarados, " parámetros fueron declarados para la función.")
    exit()

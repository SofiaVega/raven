'''
ERRORES POSIBLES
- 1. Error de tipos
- 2. Variable no declarada
- 3. Redeclaracion de variable
- 4. Variable no existe
- 5. Funcion no existe
- 6. Redeclaracion de funcion
'''


def errorTipos(operador, left_type, right_type):
    print("ERROR: Error de tipos. \nEl operador ", operador,
          " no soporta operaciones con la combinación de tipos ", left_type, " y ", right_type)
    exit()


def errorExisteContexto(val):
    print("ERROR: La variable ", val, " no existe.")

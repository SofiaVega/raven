from lark import Lark
from lark import Visitor
from birdhouse import *
from raven import *

testcases = ['testcase_oper_arreglos.txt',
             'testcase_fact_linear.txt',
             'testcase_funciones_fact.txt',
             'testcase_fib_iter.txt',
             'testcase_find.txt',
             'testcase_opciones_2.txt',
             'testcase_cyoa.txt']

parser = Lark(open("grammar", 'r').read())


def compileAndExecute(option):
    input = open("testcases/" + option, 'r').read()
    result = parser.parse(input)
    PuntosNeuralgicos().visit_topdown(result)
    maquinaVirtual()


def main():
    print("Bienvenid@ al entorno de prueba de Raven.")
    print("Seleccione el caso de prueba que desea utilizar para la evaluación de este lenguaje, su compilador y su máquina virtual.")
    terminal_menu = TerminalMenu(testcases)
    choice_index = terminal_menu.show()

    print("\n---------- RESULTADOS CASO DE PRUEBA " +
          testcases[choice_index] + " ----------\n")
    compileAndExecute(testcases[choice_index])


if __name__ == "__main__":
    main()

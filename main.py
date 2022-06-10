from lark import Lark
from lark import Visitor
from birdhouse import *
from raven import *

#testcase_oper_arreglos.txt
#testcase_fact_linear.txt
#testcase_funciones_fact.txt
#testcase_fib_iter.txt
#testcase_find.txt

parser = Lark(open("grammar", 'r').read())
#input = open("testcases/testcase_oper_arreglos.txt", 'r').read()
#input = open("testcases/testcase_fact_linear.txt", 'r').read()
#input = open("testcases/testcase_funciones_fact.txt", 'r').read()
#input = open("testcases/testcase_fib_iter.txt", 'r').read()
input = open("testcases/testcase_opciones_2.txt", 'r').read()

# print("------ Good Input --------")

result = parser.parse(input)
PuntosNeuralgicos().visit_topdown(result)
maquinaVirtual()
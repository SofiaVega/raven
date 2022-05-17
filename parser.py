from lark import Lark
from lark import Visitor
from birdhouse import *


parser = Lark(open("grammar", 'r').read())
goodInput = open("testcase_aritmetica.txt", 'r').read()
badInput = open("testcase_good.txt", 'r').read()

print("------ Good Input --------")

result = parser.parse(goodInput)
print(result.pretty())
for x in result.iter_subtrees_topdown():
    print(x.data)
print("------ Input Dificil --------")
#result = parser.parse(badInput)
# print(result.pretty())

PuntosNeuralgicos().visit_topdown(result)
print("pila o")
print(pilaO)
print("pila oper")
print(pOper)

from lark import Lark


parser = Lark(open("grammar", 'r').read())
goodInput = open("testcase_facil.txt", 'r').read()
badInput = open("testcase_good.txt", 'r').read()

print("------ Good Input --------")

result = parser.parse(goodInput)
print(result)
print("------ Input Dificil --------")
result = parser.parse(badInput)
print(result)
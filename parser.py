from lark import Lark


parser = Lark(open("grammar", 'r').read())
#goodInput = open("testcase_good.txt", 'r').read()
#badInput = open("testcase_bad.txt", 'r').read()

#print("------ Good Input --------")

#result = duck_parser.parse(goodInput)
#print(result)
#print("------ Bad Input --------")
#result = duck_parser.parse(badInput)
#print(result)
from tkinter import Variable
import birdhouse

var1 = birdhouse.VariableClass("var1", "int", 3, "local", "10001")
var2 = birdhouse.VariableClass(
    "var2", "string", "vuela vuela", "local", "10002")

tablaVariables = birdhouse.VariableTable()

tablaVariables.addVar(var1)
tablaVariables.addVar(var2)
tablaVariables.printTable()

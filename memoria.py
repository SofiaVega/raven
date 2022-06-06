'''
Var globales
    num         1000
    enunciado   3000
    bool        5000

Var locales
    num         7000
    enunciado   9000
    bool        11000

Ctes
    num         13000
    enunciado   15000
    bool        17000

Temporales
    num         19000
    enunciado   21000
    bool        23000
    pointers    25000

'''
availNumG = 1000
availEnunciadoG = 3000
availBoolG = 5000

availNumL = 7000
availEnunciadoL = 9000
availBoolL = 11000

availNumCTE = 13000
availEnunciadoCTE = 15000
availBoolCTE = 17000

availNumTemp = 19000
availEnunciadoTemp = 21000
availBoolTemp = 23000
availPointerTemp = 25000

memoria = {
    "global": {
        "num": 1000,
        "enunciado": 3000,
        "bool": 5000
    },
    "local": {
        "num": 7000,
        "enunciado": 9000,
        "bool": 11000
    },
    "cte": {
        "num": 13001,
        "enunciado": 15000,
        "bool": 17000
    },
    "temp": {
        "num": 19000,
        "enunciado": 21000,
        "bool": 23000,
        "pointer": 25000
    }
}

memoriaVirtual = [None] * 27000
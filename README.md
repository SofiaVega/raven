# raven

Un lenguaje de programacion para escribir ficción interactiva

Link a la [propuesta](https://docs.google.com/document/d/1PtagpOnKwr7J5G9_Y12FzRvn-EZwffHPhILCqVtUy80/edit?usp=sharing)

Link a la [documentación completa](https://docs.google.com/document/d/e/2PACX-1vScXdR2G7cQUrTUtJ-DdUrzyvcwnrTI5Y7j8IpCtRcujNlQf58dRSq7kKJ0C-STV2HbdEgMZzEYD_3y/pub)

## PARA CORRER EL ENTORNO DE PRUEBAS DE RAVEN 
Descarga el repositorio y asegúrate de instalar los requerimientos de este programa con el siguiente comando
`pip install -r requirements.txt`

Para después correr `python3 main.py`

¡Listo! Ya estarás usando Raven. 

---
# Manual de usuario
Raven es un lenguaje de programación sencillo y españolizado para escribir ficción interactiva. Está dividido en componentes llamados capítulos para segmentar y reorganizar el código según el flujo de la historia interactiva.

Todo programa se inicia con la palabra clave **habiaUnaVez** y el **nombre de tu archivo**
```habiaUnaVez raven```

### Título
Seguido de la **declaración del título** de tu historia

```titulo = "La historia de Raven"```

### Variables
Seguida de la **declaración de variables**
```
[tipoVar] [ID]
[tipoVar] [ID] = [valor]
```

### Tipos de Datos
En Raven tienes tres tipos de datos, `num, enunciado o bool`

## Capítulos
Después, declaras **capítulos** de la siguiente forma, siempre con su título.
Un capítulo se declara así:

``` 
capitulo uno () {
	titulo = "Capitulo uno"
}
```


Y se llaman de la siguiente manera:

`>> uno()`


Puedes llamar un __capítulo desde otro capítulo__, o desde el **índice**. El índice es el programa principal, desde donde se llaman los capítulos de manera secuencial.

```
capitulo uno(){
	titulo = "Capitulo uno"
	>> dos()
}

capitulo dos(){
	titulo = "Capitulo dos"
}

indice(){
	>> uno()
}
```

## Inputs y outputs
Para imprimir, escribe “->” antes de lo que vas a imprimir

`-> "Hola mundo!"`


Para recibir respuesta del usuario, escribe "&lt-" (lo opuesto)

`num respuesta`
`<- respuesta`


## Funciones
Una **función** se declara con la palabra **mecánica** seguida del **tipo que regresa**, y después el nombre de la mecánica. Los tienes que declarar antes de los capítulos.
```
mecanica vacia imprimir(){
	-> "Hola mundo!"
}
```

## opciones
Raven cuenta con una estructura de datos algo interesante que te ayudará bastante en tu camino de desarrollo de ficción interactiva llamada OPCIONES.

Una estructura de opciones se declara de la siguiente manera.

```
opciones : [[TEXTO], >> [CAPITULO] ; [TEXTO], >> [CAPITULO]]

opciones : ["capitulo dos", >> dos() ; "capitulo tres", >> tres()]
```

Te ayudará a que tu usuario navegue la historia tomando sus propias decisiones.

***

## EJEMPLO

Te dejamos un programa ejemplo. ¡Mucho éxito creando historias con Raven!

```
habiaUnaVez Raven
titulo = "Raven"
num b = 5
num x = 2, y = 3, a = 5
bool z = Verdad

capitulo cuatro_dos () {
    titulo = "capitulo tres"
    -> "y se murio"
}

capitulo cuatro_uno () {
    titulo = "capitulo tres"
    -> "pero aprendio y voló"
}

capitulo tres () {
    titulo = "capitulo tres"
    -> "que no sabia volar"
    opciones : ["aprender", >> cuatro_uno() ; "no aprender", >> cuatro_dos()]
}
capitulo dos () {
    titulo = "capitulo dos"
    -> "un cuervo"
    >> tres()
}
capitulo uno () {
    titulo = "capitulo uno"
    -> "habia una vez"
    opciones : ["capitulo dos", >> dos() ; "capitulo tres", >> tres()]
}
indice() {
    >> uno()
}
```

*** 

__PARA MÁS INFORMACIÓN DE ESTE LENGUAJE__
No dudes en contactar a [@SofiaVega](https://github.com/SofiaVega) o [@ncgo](https://github.com/ncgo)



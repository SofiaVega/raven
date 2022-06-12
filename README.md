# raven

Un lenguaje de programacion para escribir ficción interactiva

Link a la [propuesta](https://docs.google.com/document/d/1PtagpOnKwr7J5G9_Y12FzRvn-EZwffHPhILCqVtUy80/edit?usp=sharing)

---
# Manual de usuario
Raven es un lenguaje de programación sencillo y españolizado para escribir ficción interactiva. Está dividido en componentes llamados capítulos para segmentar y reorganizar el código según el flujo de la historia interactiva.

Todo programa se inicia con la palabra clave habiaUnaVez y el nombre de tu archivo
`habiaUnaVez raven`


Seguido de la declaración del título de tu historia
`titulo = "La historia de Raven"`


Seguida de la declaración de variables
`[tipoVar] [ID]`
`[tipoVar] [ID] = [valor]`


En Raven tienes tres tipos de datos, `num, enunciado o bool`

Después, declaras capítulos de la siguiente forma, siempre con su título.
Un capítulo se declara así:

`capitulo uno () {
	titulo = "Capitulo uno"

}`


Y se llaman de la siguiente manera:
`>> uno()`


Puedes llamar un capítulo desde otro capítulo, o desde el índice. El índice es el programa principal, desde donde se llaman los capítulos de manera secuencial.

`capitulo uno(){
	titulo = "Capitulo uno"
	>> dos()
}

indice(){
	>> uno()
}`

## Inputs y outputs
Para imprimir, escribe “->” antes de lo que vas a imprimir

`-> "Hola mundo!"`


Para recibir respuesta del usuario, escribe "<-" (lo opuesto)

`num respuesta`
`<- respuesta`


## Funciones
Una función se declara con la palabra mecánica seguida del tipo que regresa, y después el título. Los tienes que declarar antes de los capïtulos.
`mecanica vacia imprimir(){
	-> "Hola mundo!"
}`



Te dejamos un programa ejemplo. ¡Mucho éxito creando historias con Raven!


`habiaUnaVez Raven
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
}`






# Actividad en Clase: Redes Neuronales
```txt
███╗   ███╗ █████╗ ██████╗ ██╗ ██████╗ 
████╗ ████║██╔══██╗██╔══██╗██║██╔═══██╗
██╔████╔██║███████║██████╔╝██║██║   ██║
██║╚██╔╝██║██╔══██║██╔══██╗██║██║   ██║
██║ ╚═╝ ██║██║  ██║██║  ██║██║╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝
```
Modelar una red neuronal que pueda jugar al 5 en linea sin gravedad en un tablero de 20*20
* Definir el tipo de red neuronal y describir cada una de sus partes.
* Definir los patrones a utilizar.
* Definir función de activación es necesaria para este problema.
* Definir el número máximo de entradas.
* ¿Qué valores a la salida de la red se podrían esperar?
* ¿Cuales son los valores máximos que puede tener el bias?

# Definir el tipo de red neuronal y describir cada una de sus partes.
    Deberia ser una red neuronal de tipo sigmoide, en la cual es 0 es no poner la ❌/⭕ en dicha casilla y el uno seria colocar en dicha casilla.
 
Las entradas del sistema serian sencillas, es la capa de las casillas ocupadas y las de las casillas disponibles, esto se puede hacer por (X,Y), lo que no permitiria tener algo asi, (1,1,Libre) o (1,1,❌), pero aqui tenemos un pequeño problema el cuales, es ocupada pero por que esta ocupada. Osea un ❌ o un ⭕, dependiendo de eso sabemos si se puede colocar o no, eso nos da nuestra siguiente variable debido a que si en alguno de los siguientes casos se presentara 4 ❌ en cualquiera de los ángulos, la debe ser alta de 0 a 1 debido a que estamos a punto de ganar., sin embargo si fueran 4 ⭕, el valor de entre 0 y 1 deberia ser alto debido ya que debemos colocar una ❌ para evitar perder.

|   |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 1 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 2 |    |⭕ | ⭕ |⭕  |⭕ | ❌ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 3 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 4 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 5 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 6 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 7 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 8 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 9 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|10 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|11 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|12 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|13 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|14 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|15 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|16 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|17 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|18 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|19 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|20 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

Asi evitariamos que el ⭕ gane. Debido a que el 1 estaría más alto en esas posiciones.

Tambien debemos considerar la "racha" de ⭕o ❌, ocupadas en el tablero, osea si tienemos una racha de 3 y una racha de 4 no vamos a dar prioridad a la de valor más alto. 

considerar las direccion que lleva la racha. Debido a que si con un solo movimiento se puede modificar o anular la jugada tomar dicho movimiento según el patrón de la partida.

Cuidar o tener en cuenta que puede existir multiples patrones osea seguir una linealidad o cuidar ambas partes de la jugada.

|   |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 1 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 2 |    |⭕ | ⭕ |⭕  |⭕ | ❌ |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 3 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 4 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 5 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 6 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 7 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 8 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
| 9 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|10 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|11 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|12 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|13 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|14 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|15 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|16 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|17 |    |    |    |    |    |    |    |    |    |    |    |    | ⭕|  ⭕|  ⭕|  |    |    |    |    |
|18 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|19 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|20 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

Tener en cuenta que vamos a dar mas prioridad a la jugada de la fila 2 que a la de la fila 17 debido a que, el numero de "racha" o el patrón es mayor respecto de otro.

# Definir los patrones a utilizar.
El patrón sería buscar cual tiene un valor más acercado a 1 y que tome ese debido a el nivel o posibilidad de ganar o de perder. Este tiene una variable muyyyy importarnte la cual es, los "doble filo", vamos a tomar doble filo como la posibilidad de que aun que se bloquee la figura tengamos otra posibilidad de ganar.
|   |  1 |  2 |  3 |
|---|----|----|----|
| 1 | ❌|  ⭕|  ⭕|
| 2 |   |  ❌ |   |
| 3 |  ❌ |   |   |

Si vemos en este caso los ❌ tiene asegurado el gane, debido a que el siguiente movimeineto delos ⭕, no importa por que donde coloque la pieza para bloquear va a perder.
|   |  1 |  2 |  3 |
|---|----|----|----|
| 1 | ❌|  ⭕|  ⭕|
| 2 |  ⭕ |  ❌ |   |
| 3 |  ❌ |   |   |

|   |  1 |  2 |  3 |
|---|----|----|----|
| 1 | ❌|  ⭕|  ⭕|
| 2 |   |  ❌ |   |
| 3 |  ❌ |   |  ⭕ |

Debemos tener esto en mente debido a que debemos forzar llegar a una posición asi, lo que nos daria el gane en automático y evitar que nos pongan en dicha situación debido a que siginificaria la derrota.

# Definir función de activación es necesaria para este problema.
La función de activación vendría derivada de el calculo de las posiciones de la jugada, debido a que si debe activarse cuando la probabilidad de gane es más alta o cuando la probabilidad de perder sea alta. E ignorar todas las demas que tengan una probabilidad de muyyy baja de exito. 

# Definir el número máximo de entradas.
* La casilla esta ocupada
* ¿Quien ocupa la casilla?
* ¿Hay casillas al rededor ocupadas?
* ¿Quien ocupa la casilla vecina?
* ¿Hay casillas vecinas en linea?
* ¿De cuanto es la linea?


# ¿Qué valores a la salida de la red se podrían esperar?
* Valores de 0-1 tomando en cuenta que las casillas que mas se acercan a 0 es de no colocar nada y los valores de 1 la probabilidad de ganar o perder.
* Si el valor es 1 en perder, dar prioridad a quitar dicha situación.
* La "racha" es a favor o en contra.

# ¿Cuales son los valores máximos que puede tener el bias?
Los patrones de juego.
La posibilidad de perder.
La posibilidad de ganar.
La posibilidad de llegar a un patron
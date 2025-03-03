# Tarea 1: Dilema de las 8 Damas
```txt
███╗   ███╗ █████╗ ██████╗ ██╗ ██████╗ 
████╗ ████║██╔══██╗██╔══██╗██║██╔═══██╗
██╔████╔██║███████║██████╔╝██║██║   ██║
██║╚██╔╝██║██╔══██║██╔══██╗██║██║   ██║
██║ ╚═╝ ██║██║  ██║██║  ██║██║╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝
```
El enigma plantea la forma de acomodar 8 damas (🔴) en un tablero de 8*8.

⬛⬜⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜⬛<br>


Hay una actidad grande de soluciones pero la única que sigue algún patrón es el moviemiendo del caballo que siempre hace un movimiento en "L".

⬛🔴⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜🔴⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛🔴⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜🔴<br>
⬛⬜🔴⬜⬛⬜⬛⬜<br>
🔴⬛⬜⬛⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛⬜🔴⬜<br>
⬜⬛⬜⬛🔴⬛⬜⬛<br>

Se llegó a esta conclusión debido a la resolución de uno de 4*4 y aumentado damas (🔴), hasta llegar a esta solución debido a que en el momento que se coloca una dama en cualquierda de las esquinas cierra el sistema impidiendo el aumento en la siguiente dama. Vamos a verlo en el siguiente ejemplo.

⬛🔴⬛⬜<br>
⬜⬛⬜🔴<br>
🔴⬜⬛⬜<br>
⬜⬛🔴⬛<br>

En el Tablero de 4x4 se ve más claro la forma de solución debido a que no se usan los espacios de las esquinas y agregar una dama en el 5*5 es donde lo complica debido a que todos vamos a hacer el siguiente movimeinto que esta mal hecho.

⬛🔴⬛⬜⬛<br>
⬜⬛⬜🔴⬜<br>
🔴⬜⬛⬜⬛<br>
⬜⬛🔴⬛⬜<br>
⬛⬜⬛⬜🔴<br>

Al colocar la última dama en la casilla inferior derecha bloqueamos las siguientes opciones en el tablero de 6x6 entonces hay que evitar las esquinas y seguir el movimiento del caballo.

⬛🔴⬛⬜⬛⬜<br>
⬜⬛⬜🔴⬜⬛<br>
⬛⬜⬛⬜⬛🔴<br>
🔴⬛⬜⬛⬜⬛<br>
⬛⬜🔴⬜⬛⬜<br>
⬜⬛⬜⬛🔴⬛<br>
Debemos mantener el patron y en seguir la secuencia de "L" de caballo.

⬛🔴⬛⬜⬛⬜⬛<br>
⬜⬛⬜🔴⬜⬛⬜<br>
⬛⬜⬛⬜⬛🔴⬛<br>
🔴⬛⬜⬛⬜⬛⬜<br>
⬛⬜🔴⬜⬛⬜⬛<br>
⬜⬛⬜⬛🔴⬛⬜<br>
⬛⬜⬛⬜⬛⬜🔴<br>

Y por ultimo llegando a la solución más óptima con un patrón.

⬛🔴⬛⬜⬛⬜⬛⬜<br>
⬜⬛⬜🔴⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛🔴⬛⬜<br>
⬜⬛⬜⬛⬜⬛⬜🔴<br>
⬛⬜🔴⬜⬛⬜⬛⬜<br>
🔴⬛⬜⬛⬜⬛⬜⬛<br>
⬛⬜⬛⬜⬛⬜🔴⬜<br>
⬜⬛⬜⬛🔴⬛⬜⬛<br>
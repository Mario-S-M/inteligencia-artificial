# Evaluación Redes Neuronales Mediapipe
**Nombre:** Mario Eduardo Sánchez Mejía

Modelar una red neuronal que pueda identificar emociones a través de los valores obtenidos de los landmarks que genera mediapipe.
1. Definir el tipo de red neuronal y describir cada una de sus partes.
2. Definir los patrones a utilizar.
3. Definir que función de activación es necesaria para este problema.
4. Definir el numero méximo de entradas.
5. ¿Que valores a la salida de la red se podrían esperar?
6. ¿Cuales son los valores máximos que puede tener el bias?

---

## 1. Tipo de red neuronal y descripción de sus partes

Decidí usar una Red Neuronal Convolucional porque he visto que se usa mucho para cosas como imágenes, y aunque los landmarks no son exactamente una imagen, son como puntos en el espacio que tienen un orden, así que creo que puede funcionar. La CNN tiene varias partes:

* **Capa de entrada:** Aquí entran los datos de los landmarks. MediaPipe da 478 puntos con coordenadas x, y, z, entonces pensé en organizarlos como una "imagen" de 478 filas y 3 columnas (x, y, z), o algo así.
* **Capas convolucionales:** Estas capas son como filtros que buscan patrones. Creo que pondría 2 capas convolucionales:
    1. **Primera capa:** Usa filtros para encontrar cosas básicas como distancias entre puntos.
    2. **Segunda capa:** Usa filtros para patrones más complicados, como formas de la cara.
    3. **Activaciones:** Creo que usan ReLU en las capas del medio y Softmax.

---

## 2. Patrones a utilizar
Los patrones son los datos que le doy a la red. Como uso los landmarks de MediaPipe, serían:
* Las coordenadas x, y, z de los puntos.
* Pensé que tal vez podría calcular cosas como la distancia entre los ojos mediante las distancias euclidianas.
* Cada dato tiene que venir con una etiqueta que diga qué emoción es, como felicidad, enojo, estres, etc. Eso lo sacaría de un dataset o grabando caras. 

---

## 3. Funciones de activación
* **ReLU:** La uso en las capas convolucionales y densas porque es simple (si el número es negativo, lo hace 0, y si es positivo, lo deja igual).
* **Softmax:** Esta va en la salida porque quiero que me dé probabilidades de las posibles emociones. Como que "normaliza" los resultados para que sumen 1 y pueda decir cuál emoción es la más probable.

---

## 4. Numero máximo de entradas
Los landmarks de MediaPipe son 478, y cada uno tiene 3 valores (x, y, z). Entonces, hago la cuenta: 478×3=1434. Ese sería el número máximo de entradas si se usarán todos los puntos que nos da mediapipe, pero si tomaramos solo algunos puntos importantes y de destaque asi como sus distancias no seria necesario usar los 478.

---

## 5. Valores esperados de salida
| # Muestreo  | Felicidad   | Enojo       | Tristeza |
|-------------|-------------|-------------|----------|
| 1           | 0.1         | 0.6         | 0.3      |
| 2           | 0.2         | 0.5         | 0.4      |
| 3           | 0.4         | 0.3         | 0.3      |

En la salida quiero clasificar 3 emociones, así que tengo 3 neuronas. Aquí sería la cantidad e neuronas va a ser la cantidad de emociones que yo quiero detectar. Los valores dados entre 0 y 1 representan que tanto porcentaje de dicha emoción se tiene, en la muestra 1 tenemos los valores de 
* **Felicidad:** 0.1
* **Enojo:** 0.6
* **Tristeza:** 0.3

Lo que nos indica lo sigueinte la probabilidad de que enojo sea mayor es del 60% por lo tanto la emoción que se esta mostrando puede ser enojo. Y la suma de estas no debe exceder el 1, debido a nuestro SoftMax.

---

## 6. Valores máximos del bias
No se cual pudiera ser el valor máximo del bias.
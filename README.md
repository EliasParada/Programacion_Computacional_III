# _**Entrenando una IA con Tensorflow - Conversores**_

*Integrantes* | *Código*
------------ | -------------
Carlos Manuel Ábrego Martínez|USIS044220
William Alexander Amaya García|USIS032120
José Daniel Mejía Jovel|USIS010420
Elías Mauricio Parada Lozano|USIS030320

## Archivo completo y dataser
#### Archivo de colab: [AI_Conversors.ipynb](AI_Conversors.ipynb)
#### Dataset para entrenar: [entrenamiento.csv](entrenamiento.csv)

## Instrucciones
> Realizar 5 tipos de conversores distintos (longitud, masa, almacenamiento, tiempo y area) y una AI que calcule n meses acumulados

## Pasos
- Primero creamos un documento que se separa de la siguiente manera:

*Tipo* | *Valor 1* | *Valor 2* | *Valor 3* | *Valor 4* | *Valor 5* | *Valor 6*
-|-|-|-|-|-|-
Longitud | Centímetros | Metros | Kilómetros | Millas | Yardas | Pies
Masa | Gramos | Kilogramos | Toneladas | Stones | Libras | Onzas
Almacenamiento | Bytes | Kilobytes | Megabytes | Gigabytes | Terabytes | Petabytes
Tiempo | Segundos | Minutos | Horas | Días | Semanas | Meses
Area | Metros Cuadrados | Kilómetros Cuadrados | Hectareas | Millas Cuadradas | Yardas Cuadradas | Pies Cuadrados
Meses Acumulados | Meses | Acumulación 

- Ahora se importan las librerias, y seguidamente se importa el documento y se crean las listas que contendran los tipos, lo que se hace es hacer 6 listas, 5 para los conversores y una para los meses acumulados

```Python
import tensorflow as tf
import pandas as pd

inputs = pd.read_csv("/content/entrenamiento.csv", sep=";")

length = inputs[inputs.Types == "Length"]
mass = inputs[inputs.Types == "Mass"]
storage = inputs[inputs.Types == "Storage"]
time = inputs[inputs.Types == "Time"]
area = inputs[inputs.Types == "Area"]
accMonth = inputs[inputs.Types == "Accum"]
```
- Ahora se crean las variables correspondientes a cada unidad, donde repetimos la misma formula, cambiando la lista de origen de las columnas y los nombres de las variable

```Python
centi, meter, kilometer, mile, yard, foot = length['Value_A'], length['Value_B'], length['Value_C'], length['Value_D'], length['Value_E'], length['Value_F']
```

- Luego de esto se crean los modelos, se compilan y entrenan.
   - Algo importante a resaltar fue el echo de que se pidio 1 AI por conversor, pero no logramos realizar esto, pues la mayoria de intentos que relalizamos no funcionaban o incluian reentrenar la ai cada ve que convirtiera, así que optamos por una AI por conversion, de esta forma tomando cada posible permutación, aunque la desventaja de este metodo fue que con 6 unidades por 5 terminamos con 150 AI's, sin contar las permutacones entre unidades iguales, para las cuales se creo un unico modelo que se reutiliza cada vez que esto ocurre, y otra AI para los meses acumulados.

```Python
#Crear el modelo
modelEqual = tf.keras.Sequential()
modelEqual.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#Compilar el modelo
modelEqual.compile(optimizer=tf.keras.optimizers.Adam(2), loss='mean_squared_error')

#Entrenar el modelo
modelEqual.fit(centi, centi, epochs=50, verbose=0)
```
  - En el caso anterior se presento el modelo para las unidades iguales, y por eso una cantidad de epocas tan bajas, y se agrega verbose para evitar que se imprima el entrenamiento

- Una vez terminado esto se crea un array, de 3 dimenciones, con el siguiente formato (El siguiente código es unicamente demostrativo)

```Python
[Acumulacion, modeloAcumulacion]
[Longitud,
  [Centimetros,
  ModeloCentimetroAMetro,
  ModeloCentimetroAKilometro,
  ...,
  ],
  [Metros, ...], ...]
[Masa,...]
]
```

- El proposito es que la primer posición represente el tipo de conversor, la segunda es la unidad de ingreso y la tercera es la unidad de salida, que contiene los modelos para esto, de este modo si queremos centimetros a metros (array[TipoConversion][UnidadEntrada][ModeoUnidadSalida]) seria algo como array[1][1][2] (Esto se entiende mejor observando el código)

- Una vez terminamos este paso, el menu unicamente ira pidiendo los datos, las pocisiones 0 se aprovecharon para colocar las etiquetas, y la primer posicion en vista de su uso nulo fue utilizada para el calculo de meses acumulados, de esta manera no hay espacios desperdiciados y no afectará, puesto que esta conversion es la unica que no pide datos más halla de los meses, así que se pueden manejar sus parametros de una manera que el usuario no se confunda.

- Para finalizar, el valor se calculara pidiendo la posición del array que contiene el modelo necesario, y se llamara a la propiuedad predict, a la cual le ingresaremos la cantidad que el ususario desee.

- Para los meses es similar, solo que en este caso no se necesita hacer uso del array, pero puesto que ya se asigno lo utilizamos, y llamamos a predict con el numero de meses.

## Algunos ejemplos de los conversores
> Acontinuación se mostraran algunos de los ejemplos realizados.

 *Tipo de Conversor* | *Conversor con Tensorflow* | *Conversor de Google*
-|-|-
Longitud, Metors a Yardas|![150 metros son 162.6355 yardas](MeterYard.png) | ![150 metros son 164.042 yardas](GoogleMeterYard.png)
Masa, Gramos a Stones|![15700.0 Gramos son 2.4723 Stones](GramStone.png) | ![15700.0 Gramos son 2.4723268 Stones](GoogleGramStone.png)
Almacenamiento, Gigabyte a Megabyte|![15700.0 Gramos son 2.4723 Stones](MbKb.png) | ![15700.0 Gramos son 2.4723268 Stones](GoogleMbKb.png)
Tiempo, Horas a Semanas|![15700.0 Gramos son 2.4723 Stones](HoraSemana.png) | ![15700.0 Gramos son 2.4723268 Stones](GoogleHoraSemana.png)
Area, Hectareas a Pies Cuadrados|![15700.0 Gramos son 2.4723 Stones](HectareaKilometroCua.png) | ![15700.0 Gramos son 2.4723268 Stones](GoogleHectareaKilometroCua.png)
Meses Acumulados | ![8 meses acumulados son 39.9839](Meses.png) | ![8 meses acumulados son 36](Meses.jpeg)

## Datos finales

- Algunas veces la AI tiene errores, especialmente al usarla por primera vez, en caso de sentir que erra mucho seleccionar epochs=500 en cualquier entrenamiento, luego de eso se puede presionar ctr+d, lo que seleccionara al siguiente pratón de caracteres identicos a este, y repetir hasta seleccionar todas las epocas, una vez echo esto presionar la flecha derecha, y den adelante trabajar como si fuese una sola linea, cambiando el dato (sin presionar click, solo con el teclado), para modificar multiples líneas, agregar tantas epocas como se desee.

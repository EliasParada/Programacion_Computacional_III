#Crear una inteligencia artificial que calcule el numero mayor de una lista de numeros
#Importar tensorflow
import tensorflow as tf
#impiortar pandas
import pandas as pd
#importar numpy
import numpy as np

#Importar el dataset
dataset = pd.read_csv('tp.csv')
#print(dataset)

#Crear una lista de los valores de la columna para las entradas
X = dataset.iloc[:,0:4].values
#Crear una lista de los valores de la columna para las salidas
y = dataset.iloc[:,4:8].values

#Crear el modelo
model = tf.keras.Sequential()
#Crear una capa de entrada
model.add(tf.keras.layers.Dense(units=4, input_dim=4, activation='relu'))
#Crear una capa de salida
model.add(tf.keras.layers.Dense(units=4, activation='sigmoid'))

#Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['binary_accuracy'])

#Entrenar el modelo
model.fit(X, y, epochs=1000)

#Evaluar el modelo
model.evaluate(X, y)

#Crear una lista de prueba
test = np.array([[1,2,3,4]])
#Predecir el resultado
pred = model.predict(test)
print(pred)
#Imprimr el argumento mas alto
print(np.argmax(pred))
#Imprimir el resultado mas alto
print(np.argmax(pred, axis=1))
#Imprimir los argumentos mas altos
print(np.argsort(pred)[0:,2:])
#Imprimir el numero de la lista en el la posicion del argumento mas alto
print(test[0,np.argsort(pred)[0:,3:]])


#Predecir
predictions = model.predict(X)
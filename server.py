import tensorflow as tf
import pandas as pd

from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer

#Server
class basicServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Server initialiced in 8002 port'.encode())

    def do_POST(self):
        print('POST')
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)
        data = float(data)

        predict = model.predict([data])
        print('La predicción fue:', predict)
        predict = str(predict[0][0])

        message = str(data) + ' C° son ' + predict + ' F°.'
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(message.encode())
    
    def init(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write('Iniciar'.encode())

#Subir el dataset
dataset = pd.read_csv("dataset.csv", sep=";")

#Crear los inputs y ouputs
cel = dataset["Celcius"]
fahren = dataset["Fahrenheits"]

#Crear el modelo
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#Compilar
model.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

#Entrenar
train = model.fit(cel, fahren, epochs=500, verbose=0)

#Predecir
print('Datos de prueba:')
print('22 C° son 71.6 F°')
print('45 C° son 113 F°')
print('180 C° son 356 F°')
print('La AI predijo:')
f = model.predict([22])
print('22 C° son ',f[0][0],'F°')
f = model.predict([45])
print('45 C° son ',f[0][0],'F°')
f = model.predict([180])
print('180 C° son ',f[0][0],'F°')

print('Initialized server')
server = HTTPServer(('localhost', 3004), basicServer)
server.serve_forever()
from urllib import parse
import numpy as np
import urllib.request
import json

from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import cookies
import matplotlib.pyplot as plt
import tensorflow as tf

# Importar los cruds
import crudProducts
import crudUsers
import crudProviders
import crudBills
import crudCategories
import crudCarts
import crudFeatures

product = crudProducts.crud()
user = crudUsers.crud()
provider = crudProviders.crud()
bill = crudBills.crud()
category = crudCategories.crud()
cart = crudCarts.crud()
feature = crudFeatures.crud()

# CARGAR EL MODELO
model = tf.keras.models.load_model('fsmodel.h5')

# CREAMOS LA LISTA DE LAS ETIQUETAS
tags = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#LISTA DE EXTENCIONES DE ARCHIVOS PERMITIDOS
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#######CREAMOS UNA CLASE QUE MANEJARA EL SERVIDOR HTTP#######
class localServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        #######MANEJAR EL ACCESO PARA LOS PATH ACCESIBLES POR EL USUARIO#######
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        # Si el path es una imagen
        elif self.path.split('.')[-1] in ALLOWED_EXTENSIONS:
            print(self.path)
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/index.html':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/products':
            self.path = '/products.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        #######MANEJAR EL ACCESO PARA LOS PATH ACCESIBLES UNICAMENTE PARA USUARIOS#######
        elif self.path == '/admin.html':
            self.path = '/admin.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/adminproduct.html':
            self.path = '/adminproduct.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/adminusers.html':
            self.path = '/adminusers.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        #######MANEJAR LAS PETICIONES DEL INICIO EN LAS PAGINAS#######
        elif self.path == '/show_products':
            response = crud.admin_products({'action':'read'})
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            # Convertir prt_createdate y prt_expirationdate a formato fecha
            for product in response[0]:
                product['prt_createdate'] = product['prt_createdate'].strftime('%d/%m/%Y')
                product['prt_expirationdate'] = product['prt_expirationdate'].strftime('%d/%m/%Y')
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_categories':
            response = crud.admin_category({'action':'read'})
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_providers':
            response = crud.admin_provider({'action':'read'})
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        else:
            self.path = '/404.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = body.decode()
        data = parse.unquote(data)
        print(data)

        if self.path == '/admin_category':
            data = json.loads(data)
            response = crud.admin_category(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        if self.path == '/admin_provider':
            data = json.loads(data)
            response = crud.admin_provider(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        if self.path == '/admin_products':
            data = json.loads(data)
            response = crud.admin_products(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        if self.path == '/testai':
            print(data)
            matriz = np.fromstring(data, np.float32, sep=',')
            matriz = matriz.reshape(28,28)
            matriz = np.array(matriz)
            matriz = matriz.reshape(1,28,28)
            print(matriz, matriz.shape)

            prediccion = model.predict(matriz,batch_size=1)
            prediccion = str(np.argmax(prediccion))
            prediccion = tags[int(prediccion)]
            print(prediccion)

            plt.figure()
            plt.imshow(matriz[0])
            plt.colorbar()
            plt.grid(False)
            plt.show()

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(prediccion.encode())

        #conseguir la imagen
        #Generar nombre
        # url = body['url'].split('=')
        # print(url)
        # name = body['name']
        # print(name)
        #guardar la imagen
        # urllib.request.urlretrieve(url, image_name)
        #redireccionar
        # self.send_response(301)
        # # self.send_header('Location', '/')
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello, world!')

# Iniciar el servidor
print("\033[1;37;42m Iniciando el servidor \033[0;m")
server = HTTPServer(('localhost', 3000), localServer)
print("\033[1;37;42m Servidor iniciado en el puerto 3000 \033[0;m")
server.serve_forever()

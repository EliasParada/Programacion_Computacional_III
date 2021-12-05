from urllib import parse
import numpy as np
import os
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

crudProducts = crudProducts.crud()
crudUsers = crudUsers.crud()
crudProviders = crudProviders.crud()
crudBills = crudBills.crud()
crudCategories = crudCategories.crud()
crudCarts = crudCarts.crud()
crudFeatures = crudFeatures.crud()

# CARGAR EL MODELO
model = tf.keras.models.load_model("fsmodel.h5")

# CREAMOS LA LISTA DE LAS ETIQUETAS
tags = ['Manzanas', 'Galletas', '', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#LISTA DE EXTENCIONES DE ARCHIVOS PERMITIDOS
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'js', 'html'])
#######CREAMOS UNA CLASE QUE MANEJARA EL SERVIDOR HTTP#######
class localServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path.split('.')[-1])
        #######MANEJAR EL ACCESO PARA LOS PATH ACCESIBLES POR EL USUARIO#######
        if self.path == '/' or self.path == '/index' or self.path == '/account':
            self.path += '.html'
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
            response = crudProducts.show_limits(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            for product in response[0]:
                product['prt_createdate'] = product['prt_createdate'].strftime('%d/%m/%Y')
                product['prt_expirationdate'] = product['prt_expirationdate'].strftime('%d/%m/%Y')
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_categories':
            response = crudCategories.search_limit(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_providers':
            response = crudProviders.search_limit(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_users':
            response = crudUsers.show_limit(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            for date in response[0]:
                date['ux_DBirth'] = date['ux_DBirth'].strftime('%d/%m/%Y')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_features':
            response = crudFeatures.search_limit(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        # Si el path es una de las extensiones permitidas
        elif self.path.split('.')[-1] in ALLOWED_EXTENSIONS:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.path = '/404.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = body.decode()
        data = parse.unquote(data)

        if self.path == '/admin_category':
            data = json.loads(data)
            response = crudCategories.admin_categories(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/admin_provider':
            data = json.loads(data)
            response = crudProviders.admin_provider(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/admin_products':
            data = json.loads(data)
            response = crudProducts.admin_products(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/admin_users':
            data = json.loads(data)
            response = crudUsers.admin_users(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response[0], '\033[0;m')
            if data['action'] == 'create' or data['action'] == 'update':
                if response != False:
                    rgb = data['photo']
                    img = np.array([])
                    img = np.fromstring(rgb, np.uint8, sep=',')
                    img = img.reshape((400, 400, 3))

                    if data['action'] == 'create':
                        plt.imsave(f'img/users/profile{response[1]}.jpg', img)
                        response = response[0]

                    elif data['action'] == 'update' and data['imgUpdate'] == True:
                        plt.imsave(f'img/users/profile{data["id"]}.jpg', img)

            elif data['action'] == 'delete':
                if response != False:
                    os.remove(f'img/users/profile{data["id"]}.jpg')
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/search_users':
            data = json.loads(data)
            response = crudUsers.search_users(data['search'], data['init'],data['limit'])
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/testurl':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response='Yes')).encode('utf-8'))

        elif self.path == '/admin_features':
            data = json.loads(data)
            response = crudFeatures.admin_permissions(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
            
        elif self.path == '/testai':
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

            # plt.figure()
            # plt.imshow(matriz[0])
            # plt.colorbar()
            # plt.grid(False)
            # plt.show()

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(prediccion.encode())

# Iniciar el servidor
print("\033[1;37;42m Iniciando el servidor \033[0;m")
server = HTTPServer(('localhost', 3000), localServer)
print("\033[1;37;42m Servidor iniciado en el puerto 3000 \033[0;m")
server.serve_forever()

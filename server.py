from urllib import parse
import numpy as np
import os
import urllib.request
import json

from http.server import SimpleHTTPRequestHandler, HTTPServer
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
# import sessionsManager

idUsers = crudUsers
idProduct = crudProducts
crudProducts = crudProducts.crud()
crudUsers = crudUsers.crud()
crudProviders = crudProviders.crud()
crudBills = crudBills.crud()
crudCategories = crudCategories.crud()
crudCarts = crudCarts.crud()
crudFeatures = crudFeatures.crud()
# sessionsManager = sessionsManager.manager()
# CARGAR EL MODELO
model = tf.keras.models.load_model("fs_model.h5")

# CREAMOS LA LISTA DE LAS ETIQUETAS
labels = [
    ['Manzana', 1, 1],
    ['Shampoo', 7, 2],
    ['Insecticida', 9, 8],
    ['Atún', 8, 5],
    ['Galleta', 10, 7],
    ['Helado', 3, 4],
    ['Pepino', 1, 1],
    ['Pescado', 4, 6]
]
userId = False
nick = False
admin = False
logged = False
password = False
cart = False

#LISTA DE EXTENCIONES DE ARCHIVOS PERMITIDOS
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'js', 'html'])
#######CREAMOS UNA CLASE QUE MANEJARA EL SERVIDOR HTTP#######
class localServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        global userId
        global admin
        global nick
        global logged
        global password
        global cart

        self.credentials = crudUsers.loggin({'nick': nick, 'pass': password})
        print(len(self.credentials[0]), self.credentials[0])
        if len(self.credentials[0]) == 1:
            print('\033[0;30;47m Se ha iniciado sesión por \033[0;34;47m', self.credentials[0][0]['ux_nick'], '\033[0;m')
            userId = self.credentials[0][0]['ux_id']
            nick = self.credentials[0][0]['ux_nick']
            password = self.credentials[0][0]['ux_pass']
            crat = crudCarts.get_cart(userId)
            cart = crat[0][0]['car_id']
            if self.credentials[0][0]['pms_ux'] == 1:
                admin = True
            else:
                admin = False
            logged = True
        else:
            userId = False
            nick = False
            admin = False
            logged = False

        print(logged, userId, nick, admin)
        ################ ACCESO COMPLETO A TODOS LOS VISITANTES ################
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/index.html':
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/index':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        ################ ACCESO COMPLETO SOLO A LOS USUARIOS ################
        elif self.path == '/account' or self.path == '/cart':
            if logged == True:
                self.path += '.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/account.html' or self.path == '/cart.html':
            if logged == True:
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        ################ ACCESO SOLO PARA LOS NO LOGEADOS ################
        elif self.path == '/login' or self.path == '/register':
            if logged == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path += '.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/login.html' or self.path == '/register.html':
            if logged == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                return SimpleHTTPRequestHandler.do_GET(self)
        ################ ACCESO SOLO PARA LOS ADMINISTRADORES ################
        elif self.path == '/admin':
            if logged == True:
                if admin == True:
                    self.path += '.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                else:
                    self.path = '/index.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/admin.html':
            if logged == True:
                if admin == True:
                    return SimpleHTTPRequestHandler.do_GET(self)
                else:
                    self.path = '/index.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        ################ PETICIONES GET ################
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
        elif self.path == '/access':
            response = logged, admin
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_user':
            response = crudUsers.show_user(userId)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            for date in response[0]:
                date['ux_DBirth'] = date['ux_DBirth'].strftime('%d/%m/%Y')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_bills':
            response = crudBills.search_limit(0)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            for date in response[0]:
                date['fac_date'] = date['fac_date'].strftime('%d/%m/%Y')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        elif self.path == '/show_carts':
            response = crudCarts.search_limit(userId)
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

        global userId
        global admin
        global nick
        global logged
        global password

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
            if data['action'] == 'create' or data['action'] == 'update':
                if response != False:
                    rgb = data['photo']
                    img = np.array([])
                    img = np.fromstring(rgb, np.uint8, sep=',')
                    img = img.reshape((200, 200, 3))

                    if data['action'] == 'create':
                        id = idProduct.conn.generate_id('products')
                        plt.imsave(f'img/products/product{int(id) - 1}.jpg', img)
                        response = response[0]

                    elif data['action'] == 'update' and data['newPhoto'] == True:
                        plt.imsave(f'img/products/product{data["id"]}.jpg', img)

            elif data['action'] == 'delete':
                if response != False:
                    os.remove(f'img/products/product{data["id"]}.jpg')

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
                    img = img.reshape((600, 600, 3))

                    if data['action'] == 'create':
                        id = idUsers.conn.generate_id('users')
                        # carrito = crudCarts.admin_carts({'action': 'create','user': id})

                        plt.imsave(f'img/users/profile{int(id) - 1}.jpg', img)
                        response = response[0]

                    elif data['action'] == 'update' and data['newPhoto'] == True:
                        plt.imsave(f'img/users/profile{data["id"]}.jpg', img)
                        cart = crudCarts.admin_carts({'action': 'create','user': data['id']})

            elif data['action'] == 'delete':
                if response != False:
                    os.remove(f'img/users/profile{data["id"]}.jpg')
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/bill':
            data = json.loads(data)
            if data['user'] == 'None':
                data['user'] = userId
            response = crudBills.admin_bill(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/cart':
            data = json.loads(data)
            data['id'] = userId
            response = crudCarts.admin_carts(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
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

        elif self.path == '/admin_features':
            data = json.loads(data)
            response = crudFeatures.admin_permissions(data)
            print('\033[0;30;47m Se llamo a la ruta \033[0;34;47m', self.path, '\033[0;30;47m se respondio:\033[2;34;47m', response, '\033[0;m')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/loggin':
            data = json.loads(data)
            self.credentials = crudUsers.loggin(data)
            print(len(self.credentials[0]), self.credentials[0])
            if len(self.credentials[0]) == 1:
                print('\033[0;30;47m Se ha iniciado sesión por \033[0;34;47m', self.credentials[0][0]['ux_nick'], '\033[0;m')
                userId = self.credentials[0][0]['ux_id']
                nick = self.credentials[0][0]['ux_nick']
                password = self.credentials[0][0]['ux_pass']
                if self.credentials[0][0]['pms_ux'] == 1:
                    admin = True
                else:
                    admin = False
                logged = True
            else:
                userId = False
                nick = False
                password = False
                admin = False
                logged = False
            response = logged, admin
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/logout':
            userId = False
            nick = False
            admin = False
            logged = False
            password = False
            response = logged, admin
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/pagination':
            data = json.loads(data)
            if data['table'] == 'users':
                response = crudUsers.search_to()

            
        elif self.path == '/predict':
            data = json.loads(data)
            matriz = np.fromstring(data['photo'], np.float32, sep=',')
            matriz = matriz.astype(np.int32)
            matriz = matriz / 255
            matriz = matriz.reshape(48, 48, 1)

            plt.imshow(matriz, cmap='gray')
            plt.show()

            prd = model.predict(np.expand_dims(np.array(matriz, dtype=np.float32), 0))
            print(prd)

            # Mostrar la imagen en un subplot y la grafica en otro
            plt.subplot(1, 2, 1)
            plt.imshow(matriz, cmap='gray')
            plt.subplot(1, 2, 2)
            plt.bar('Fruta', prd[0][0])
            plt.bar('Shampoo', prd[0][1])
            plt.bar('Insecticida', prd[0][2])
            plt.bar('Atún', prd[0][3])
            plt.bar('Galleta', prd[0][4])
            plt.bar('Helado', prd[0][5])
            plt.bar('Pepino', prd[0][6])
            plt.bar('Pescado', prd[0][7])
            plt.show()
            
            prd = int(np.argmax(prd))
            print(prd)
            print(labels[prd])
            response = [{'label': (labels[prd][0]), 'probability': prd, 'category': labels[prd][1], 'provider': labels[prd][2]}, {'status':'ok', 'msg':'Predicción realizada'}]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

# Iniciar el servidor
print("\033[1;37;42m Iniciando el servidor \033[0;m")
server = HTTPServer(('localhost', 3000), localServer)
print("\033[1;37;42m Servidor iniciado en el puerto 3000 \033[0;m")
server.serve_forever()

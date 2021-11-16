from urllib import parse
import numpy as np
import mysql.connector
import urllib.request
import json

from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import cookies
import matplotlib.pyplot as plt
import tensorflow as tf

# CARGAR EL MODELO
model = tf.keras.models.load_model('fsmodel.h5')

# CREAMOS LA LISTA DE LAS ETIQUETAS
tags = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#######CREAMOS UNA CLASE PARA DMINISTRAR LAS SESIONES DE LA APLICACION CON COOKIES#######
class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            return None

    def set_session(self, session_id, session):
        self.sessions[session_id] = session

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session_id(self, session):
        for session_id in self.sessions:
            if self.sessions[session_id] == session:
                return session_id
        return None

#######CREAMOS UNA CLASE QUE MANEJE LAS SENTENCIAS SQL#######
class CRUD:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", port="3307", passwd="", database="fast_store")
        if self.conn.is_connected():
            print("\033[4;1;37;42m Conectado a la base de datos \033[0;m")
        else:
            print("\033[4;1;37;41m No se pudo conectar a la base de datos \033[0;m")
    ######## FUNCION PAR A EJECUTAR SENTENCIAS SQL ########
    def sql_run(self, sql, data):
        try:
            print("\033[4;1;37;42m Ejecutando sentencia SQL \033[0;m")
            print(sql)
            print(data)
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            return {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return {'status':'error', 'msg':f'Error al ejecutar la sentencia SQL: {msg}'}

    def sql_get(self, sql, data):
        try:
            print('\033[4;1;37;42m Ejecutando sentencia SQL \033[0;m')
            print('\033[4;1;37;42m Sentencia: ' + sql + '\033[0;m')
            print('\033[4;1;37;42m Datos: ' + str(data) + '\033[0;m')
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result, {'status':'ok', 'msg':f'Sentencia ejecutada correctamente'}
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return {'status':'error', 'msg':f'Error al ejecutar la sentencia SQL: {msg}'}

    def generate_id(self, table):
        if table == 'users':
            sql = "SELECT MAX(ux_id) AS id FROM ux_users"
        elif table == 'products':
            sql = "SELECT MAX(prt_id) AS id FROM prt_producto"
        elif table == 'categories':
            sql = "SELECT MAX(cat_id) AS id FROM cat_categoria"
        result = self.sql_get(sql, None)
        print('\033[4;1;37;42m Generando ID, ID actual: \033[0;m', result[0][0]['id'])
        if result[1]['status'] == 'ok':
            if result[0][0]['id'] is None:
                return 1
            else:
                return result[0][0]['id'] + 1
        else:
            return False

    ######## FUNCION PARA ADMINISTRAR LA TABLA USUARIOS ########
    def admin_users(self, data):
        if data['action'] == 'read':
            sql = "SELECT ux_users.ux_id, ux_users.ux_dui, ux_users.ux_name, ux_users.ux_tag, ux_users.ux_phone, ux_users.ux_mail, ux_users.ux_pass, ux_users.ux_DBirth, ux_users.ux_urlphoto, ux_users.pms_ux FROM ux_users INNER JOIN pms_permissions ON ux_users.pms_ux = pms_permissions.pms_id"
            return self.sql_get(sql, None)
        elif data['action'] == 'create':
            sql = "INSERT INTO ux_users (ux_dui, ux_name, ux_tag, ux_phone, ux_mail, ux_pass, ux_DBirth, ux_urlphoto, pms_ux) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            return self.sql_run(sql, (data['dui'], data['name'], data['tag'], data['phone'], data['mail'], data['pass'], data['dbirth'], data['urlphoto'], data['permiss']))
        elif data['action'] == 'update':
            sql = "UPDATE ux_users SET ux_dui = %s, ux_name = %s, ux_tag = %s, ux_phone = %s, ux_mail = %s, ux_pass = %s, ux_DBirth = %s, ux_urlphoto = %s, pms_ux = %s WHERE ux_id = %s"
            return self.sql_run(sql, (data['dui'], data['name'], data['tag'], data['phone'], data['mail'], data['pass'], data['dbirth'], data['urlphoto'], data['permiss'], data['id']))
        elif data['action'] == 'delete':
            sql = "DELETE FROM ux_users WHERE ux_id = %s"
            return self.sql_run(sql, (data['id'],))
    ######## FUNCION PARA ADMINISTRAR LA TABLA PERMISOS ########
    def admin_permissions(self, data):
        if data['action'] == 'read':
            sql = "SELECT pms_permissions.pms_id, pms_permission.pms_type FROM pms_permissions"
            return self.sql_get(sql, None)
        elif data['action'] == 'create':
            sql = "INSERT INTO pms_permissions (pms_id, pms_type) VALUES (%s, %s)"
            return self.sql_run(sql, (data['id'], data['type']))
        elif data['action'] == 'update':
            sql = "UPDATE pms_permissions SET pms_id = %s, pms_type = %s WHERE pms_id = %s"
            return self.sql_run(sql, (data['id'], data['type'], data['id']))
        elif data['action'] == 'delete':
            sql = "DELETE FROM pms_permissions WHERE pms_id = %s"
            return self.sql_run(sql, (data['id'],))
    ######## FUNCION PARA ADMINISTRAR LA TABLA PRODUCTOS ########
    def admin_products(self, data):
        if data['action'] == 'read':
            sql = "SELECT prt_producto.prt_id, prt_producto.prt_name, prov_proveedor.prov_id, prov_proveedor.prov_name, prt_producto.prt_createdate, prt_producto.prt_expirationdate, cat_categoria.cat_id, cat_categoria.cat_name, prt_producto.prt_cost, prt_producto.prt_photo FROM prt_producto INNER JOIN cat_categoria ON prt_producto.cat_id = cat_categoria.cat_id INNER JOIN prov_proveedor ON prt_producto.prov_id = prov_proveedor.prov_id"
            return self.sql_get(sql, None)
        elif data['action'] == 'create':
            sql = "INSERT INTO prt_producto (prt_id, prt_name, prov_id, prt_createdate, prt_expirationdate, cat_id, prt_cost, prt_photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            current_id = self.generate_id('products')
            return self.sql_run(sql, (current_id ,data['name'], data['prov'], data['createdate'], data['expirationdate'], data['cat'], data['cost'], data['photo'] + str(current_id)))
        elif data['action'] == 'update':
            sql = "UPDATE prt_producto SET prt_name = %s, prov_id = %s, prt_createdate = %s, prt_expirationdate = %s, cat_id = %s, prt_cost = %s, prt_photo = %s WHERE prt_id = %s"
            return self.sql_run(sql, (data['name'], data['cat'], data['createdate'], data['expirationdate'], data['prov'], data['cost'], data['photo']+str(data['id']), data['id']))
        elif data['action'] == 'delete':
            sql = "DELETE FROM prt_producto WHERE prt_id = %s"
            return self.sql_run(sql, (data['id'],))
    ######## FUNCION PARA ADMINISTRAR LA TABLA CATEGORIAS ########
    def admin_category(self, data):
        if data['action'] == 'read':
            sql = "SELECT cat_categoria.cat_id, cat_name, cat_categoria.cat_description FROM cat_categoria"
            return self.sql_get(sql, None)
        elif data['action'] == 'create':
            sql = "INSERT INTO cat_categoria (cat_id, cat_name, cat_description) VALUES (%s, %s, %s)"
            return self.sql_run(sql, (self.generate_id('categories'), data['name'], data['description']))
        elif data['action'] == 'update':
            sql = "UPDATE cat_categoria SET cat_name = %s, cat_description = %s WHERE cat_id = %s"
            return self.sql_run(sql, (data['name'], data['description'], data['id']))
        elif data['action'] == 'delete':
            sql = "DELETE FROM cat_categoria WHERE cat_id = %s"
            return self.sql_run(sql, (data['id'],))
    ######## FUNCION PARA ADMINISTRAR LA TABLA PROVEEDORES ########
    def admin_provider(self, data):
        if data['action'] == 'read':
            sql = "SELECT prov_proveedor.prov_id, prov_proveedor.prov_name, prov_proveedor.prov_phone, prov_proveedor.prov_mail FROM prov_proveedor"
            return self.sql_get(sql, None)
        elif data['action'] == 'create':
            sql = "INSERT INTO prov_proveedor (prov_id, prov_name, prov_phone, prov_mail) VALUES (%s, %s, %s, %s)"
            return self.sql_run(sql, (data['id'], data['name'], data['phone'], data['mail']))
        elif data['action'] == 'update':
            sql = "UPDATE prov_proveedor SET prov_name = %s, prov_phone = %s, prov_mail = %s WHERE prov_id = %s"
            return self.sql_run(sql, (data['name'], data['phone'], data['mail'], data['id']))
        elif data['action'] == 'delete':
            sql = "DELETE FROM prov_proveedor WHERE prov_id = %s"
            return self.sql_run(sql, (data['id'],))
    
            
crud = CRUD()

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
            matriz = matriz.reshape(1,28,28,1)
            print(matriz.shape)

            plt.figure()
            plt.imshow(matriz[0,...], cmap=plt.cm.binary)
            plt.colorbar()
            plt.grid(False)
            plt.show()
            
            prediccion = model.predict(matriz,batch_size=1)
            prediccion = str(np.argmax(prediccion))
            prediccion = tags[int(prediccion)]
            print(prediccion)

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

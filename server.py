#Crear una conexion con una base de datos
import mysql.connector
# import ast
import json

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

#Crear una conexion con la base de datos

class crud:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', port='3307', user='root',password='', database='bd_academica')
        if self.conn.is_connected():
            print('¡Conexión exitosa!')
        else:
            print('No se ha podido conectar a la base de datos')
        pass

    def insertar(self, code, name, tel):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO alumnos (CodAlm, NomAlm, TelAlm) VALUES (%s, %s, %s)"
            val = (code, name, tel)
            cursor.execute(sql, val)
            self.conn.commit()
            return {'status': True, 'msg': 'Se ha insertado correctamente'}
        except Exception as e:
            print(e)
            return {'status': False, 'msg': str(e)}

crud = crud()

#Crear una clase para manejar las peticiones
class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/insert':
            #Recibir los datos
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            print(data)
            resp = crud.insertar(data['code'], data['name'], data['tel'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode('utf-8'))

print('Initialized server in 3000 server')
server = HTTPServer(('localhost', 3000), servidorBasico)
server.serve_forever()


# #Crear una clase para manejar las peticiones
# class MyHandler(SimpleHTTPRequestHandler):
#     #Crear el metodo GET
#     def do_GET(self):
#         #Recibir la peticion
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(bytes("<html><head><title>Servidor Local 3004</title></head>", "utf-8"))
#         self.wfile.write(bytes("<body><p>Servidor en el puerto 3004</p></body>", "utf-8"))
#         self.wfile.write(bytes("<img src='https://static.wixstatic.com/media/580deb_093dff4dd68d43bcb88a2b02e25d2a84~mv2.gif'></html>", "utf-8"))
        
#     #Crear el metodo POST
#     def do_POST(self):
#         #Obtener el tamano del cuerpo de la peticion
#         length = int(self.headers['Content-Length'])
#         #Obtener el cuerpo de la peticion
#         body = self.rfile.read(length).decode('utf-8')
#         print(type(body), body)
#         #Convertir el cuerpo de la peticion a un diccionario
#         body = ast.literal_eval(body)
#         print(body)
#         #Obtener el valor de los parametros código, nombres y telefono
#         code = body['code']
#         name = body['name']
#         tel = body['tel']
        
#         #Crear el cursor
#         cursor = conn.cursor()
#         #Crear la consulta para agregar a un alumno
#         print('Code is {}, name is {} and tel is {}'.format(code, name, tel))
#         cursor.execute("INSERT INTO alumnos (code, name, tel) VALUES ('{}', '{}', '{}')".format(code, name, tel))
#         #Guardar los cambios
#         conn.commit()
#         #Cerrar el cursor
#         cursor.close()
#         #Enviar la respuesta
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()
#         #enviar la respuesta
#         self.wfile.write('Send'.encode('utf-8'))

# #inicializar el servidor
# print('Inicializando el servidor...')
# servidor = HTTPServer(('localhost', 3004), MyHandler)
# #Ejecutar el servidor
# servidor.serve_forever()


# #Crear un cursor
# cursor = conn.cursor()

# #Crear una funcion para obtener el id de un usuario
# def get_user_id(username):
#     #Obtener el id del usuario
#     cursor.execute("SELECT id FROM usuarios WHERE username = '{}'".format(username))
#     return cursor.fetchone()

# user = input('Ingrese el nombre de usuario: ')
# print(get_user_id(user))

# #crear una funcion para agregar un usuario
# def add_user(id, username):
#     #Agregar un usuario
#     cursor.execute("INSERT INTO usuarios (id, username) VALUES ('{}', '{}')".format(id, username))
#     conn.commit()
#     return cursor.lastrowid

# new_id = input('Ingrese el id: ')
# new_user = input('Ingrese el nombre de usuario: ')
# add_user(new_id, new_user)

# #Crear una funcion para obtener la tabla de usuarios
# def get_all_users():
#     #Obtener todos los usuarios
#     cursor.execute("SELECT * FROM usuarios")
#     return cursor.fetchall()


# for row in get_all_users():
#     print(row)

# #Crear una funcion para eliminar un usuario
# def delete_user(id):
#     #Eliminar un usuario
#     cursor.execute("DELETE FROM usuarios WHERE id = '{}'".format(id))
#     conn.commit()
#     return cursor.rowcount

# allow_delete = input('¿Desea eliminar el usuario? (y/n): ')
# if allow_delete == 'y':
#     user_id = input('Ingrese el id del usuario: ')
#     delete_user(user_id)
#     print('Usuario eliminado')

# #Cerrar la conexion
# conn.close()
#Crear una conexion con una base de datos
import mysql.connector
import ast

from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer

#Crear una clase para manejar las peticiones
class MyHandler(BaseHTTPRequestHandler):
    #Crear el metodo GET
    def do_GET(self):
        #Recibir la peticion
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Servidor Local 3004</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>Servidor en el puerto 3004</p></body>", "utf-8"))
        self.wfile.write(bytes("<img src='https://static.wixstatic.com/media/580deb_093dff4dd68d43bcb88a2b02e25d2a84~mv2.gif'></html>", "utf-8"))
        
    #Crear el metodo POST
    def do_POST(self):
        #Obtener el tamano del cuerpo de la peticion
        length = int(self.headers['Content-Length'])
        #Obtener el cuerpo de la peticion
        body = self.rfile.read(length).decode('utf-8')
        print(type(body), body)
        #Convertir el cuerpo de la peticion a un diccionario
        body = ast.literal_eval(body)
        print(body)
        #Obtener el valor de los parametros código, nombres y telefono
        code = body['code']
        name = body['name']
        tel = body['tel']
        
        #Crear una conexion con la base de datos
        conn = mysql.connector.connect(host='localhost',
                                    port='3307',
                                    user='root',
                                    password='',
                                    database='academica')
        #Crear el cursor
        cursor = conn.cursor()
        #Crear la consulta para agregar a un alumno
        print('Code is {}, name is {} and tel is {}'.format(code, name, tel))
        cursor.execute("INSERT INTO alumnos (code, name, tel) VALUES ('{}', '{}', '{}')".format(code, name, tel))
        #Guardar los cambios
        conn.commit()
        #Cerrar el cursor
        cursor.close()
        #Cerrar la conexion
        conn.close()
        #Enviar la respuesta
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        #enviar la respuesta
        self.wfile.write('Send'.encode('utf-8'))

#inicializar el servidor
print('Inicializando el servidor...')
servidor = HTTPServer(('localhost', 3004), MyHandler)
#Ejecutar el servidor
servidor.serve_forever()


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
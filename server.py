#Crear un servidor que conecte a mongoDB
#y que permita insertar, eliminar y actualizar
#datos en la base de datos
from types import prepare_class
import pymongo
import json
import math

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

from pymongo.database import SystemJS

mongo_time_out = '1000'

mongo_uri = 'mongodb://127.0.0.1:27017/'

#crear una clase que permita conectarse a mongoDB
class mongoCRUD():
    def __init__(self):
        try:
            self.connection = pymongo.MongoClient(mongo_uri, connectTimeoutMS=int(mongo_time_out))
            self.library = self.connection['library']
            self.books = self.library['books']
            # print('\033[4;37;44m Libros \033[0;m')
            # for book in self.books.find():
            #     print(f"\033[3;4;30;47m {book['id']}|{book['title']} \033[0;m")
            print('\033[4;1;37;42m Conexion exitosa \033[0;m')
            self.add_books({})
            self.get_books()
            self.update_books(None, {})
            self.delete_books({})
        except pymongo.errors.ServerSelectionTimeoutError as timeError:
            print(f'\033[4;1;37;41m Demasiado tiempo de espera: {timeError} \033[0;m')
        except pymongo.errors.ConnectionFailure as connError:
            print(f'\033[4;1;37;41m Error de conexion: {connError} \033[0;m')

    def add_books(self, book):
        try:
            if book == {}:
                print('\033[4;1;37;41m Datos vacios \033[0;m')
                return {'status': 'ERROR', 'message': 'Datos vacios'}
            else:
                self.books.insert_one(book)
                print('\033[4;1;37;42m Libro agregado \033[0;m')
                return {'status': 'OK', 'message': 'Libro agregado'}
        except pymongo.errors.ServerSelectionTimeoutError as timeError:
            print(f'\033[4;1;37;41m Demasiado tiempo de espera: {timeError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Demasiado tiempo de espera'}
        except pymongo.errors.ConnectionFailure as connError:
            print(f'\033[4;1;37;41m Error de conexion: {connError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Error de conexion'}
        
    def delete_books(self, id):
        try:
            if id == {}:
                print('\033[4;1;37;41m Id vacio \033[0;m')
                return {'status': 'ERROR', 'message': 'Id vacio'}
            else:
                self.books.delete_one({'id': id})
                print('\033[4;1;37;42m Libro eliminado \033[0;m')
                return {'status': 'OK', 'message': 'Libro eliminado'}
        except pymongo.errors.ServerSelectionTimeoutError as timeError:
            print(f'\033[4;1;37;41m Demasiado tiempo de espera: {timeError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Demasiado tiempo de espera'}
        except pymongo.errors.ConnectionFailure as connError:
            print(f'\033[4;1;37;41m Error de conexion: {connError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Error de conexion'}

    def update_books(self, id, book):
        try:
            if id == None:
                print('\033[4;1;37;41m Id vacio \033[0;m')
                return {'status': 'ERROR', 'message': 'Id vacio'}
            else:
                self.books.update_one({'id': id}, {'$set': book})
                print('\033[4;1;37;42m Libro actualizado \033[0;m')
                return {'status': 'OK', 'message': 'Libro actualizado'}
        except pymongo.errors.ServerSelectionTimeoutError as timeError:
            print(f'\033[4;1;37;41m Demasiado tiempo de espera: {timeError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Demasiado tiempo de espera'}
        except pymongo.errors.ConnectionFailure as connError:
            print(f'\033[4;1;37;41m Error de conexion: {connError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Error de conexion'}

    def get_books(self):
        try:
            books = {}
            # print('\033[4;1;37;42m Libros \033[0;m')
            for book in self.books.find():
                books[book['id']] = book
                books[book['id']]['_id'] = str(book['_id']) 
                # print(f"\033[3;4;30;47m {book['id']}|{book['title']} \033[0;m")
            return {'status': 'OK', 'message': 'Libros', 'data': books}
        except pymongo.errors.ServerSelectionTimeoutError as timeError:
            print(f'\033[4;1;37;41m Demasiado tiempo de espera: {timeError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Demasiado tiempo de espera'}
        except pymongo.errors.ConnectionFailure as connError:
            print(f'\033[4;1;37;41m Error de conexion: {connError} \033[0;m')
            return {'status': 'ERROR', 'message': 'Error de conexion'}
    
mongo = mongoCRUD()
# mongo.test()
# mongo.add_books({'id': 'B0003', 'title': 'El señor de los anillos', 'argument': 'sinopsis', 'tags':'some', 'author': 'J.R.R. Tolkien', 'lan':'enUS', 'date': '1954'})
# mongo.delete_books('B0003')
# mongo.update_books('B0003', {'title': 'El señor de los anillos 2', 'argument': 'sinopsis', 'tags':'some', 'author': 'J.R.R. Tolkien', 'lan':'enUS', 'date': '1954'})
class localServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body = parse.unquote(body.decode('utf-8'))
        print(body)
        body = json.loads(body)
        print(self.path)

        if self.path == '/add':
            response = mongo.add_books(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/delete':
            response = mongo.delete_books(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/update':
            response = mongo.update_books(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/get':
            response = mongo.get_books()
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        elif self.path == '/found':
            response = mongo.get_books(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Not found', 'utf-8'))

#Iniciar el servidor
print('\033[4;1;37;42m Iniciando servidor \033[0;m')
httpd = HTTPServer(('localhost', 3004), localServer)
httpd.serve_forever()



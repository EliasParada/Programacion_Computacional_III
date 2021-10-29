# #Conectar mysql con python
# import pymysql

# #Conectar con la base de datos
# conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password='',
#                        db='sistema',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)

# #Crear un cursor
# cursor = conn.cursor()

# #Crear una funcion para obtener el id de un usuario
# def get_user_id(username):
#     #Obtener el id del usuario
#     cursor.execute("SELECT id FROM usuarios WHERE username = '{}'".format(username))
#     return cursor.fetchone()

# print(get_user_id('admin'))
